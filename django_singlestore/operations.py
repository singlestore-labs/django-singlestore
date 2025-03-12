import datetime
import decimal
import uuid

from django.conf import settings
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.utils import split_tzname_delta
from django.db.models import Exists, ExpressionWrapper, Lookup
from django.db.models.constants import OnConflict
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime, parse_time
from django.utils.encoding import force_str
from django.utils.regex_helper import _lazy_re_compile


class DatabaseOperations(BaseDatabaseOperations):
    # MySQL stores positive fields as UNSIGNED ints.
    integer_field_ranges = {
        **BaseDatabaseOperations.integer_field_ranges,
        "PositiveSmallIntegerField": (0, 65535),
        "PositiveIntegerField": (0, 4294967295),
        "PositiveBigIntegerField": (0, 18446744073709551615),
    }
    cast_data_types = {
        "AutoField": "BIGINT",
        "BigAutoField": "BIGINT",
        "SmallAutoField": "BIGINT",
        "CharField": "CHAR(%(max_length)s)",
        "DecimalField": "DECIMAL(%(max_digits)s, %(decimal_places)s)",
        "TextField": "CHAR",
        "IntegerField": "INT",
        "BigIntegerField": "BIGINT",
        "SmallIntegerField": "SMALLINT",
        "PositiveBigIntegerField": "UNSIGNED BIGINT",
        "PositiveIntegerField": "UNSIGNED INT",
        "PositiveSmallIntegerField": "UNSIGNED SMALLINT",
        "DurationField": "BIGINT",
    }
    cast_char_field_without_max_length = "CHAR"
    explain_prefix = "EXPLAIN"

    # EXTRACT format cannot be passed in parameters.
    _extract_format_re = _lazy_re_compile(r"[A-Z_]+")

    def date_extract_sql(self, lookup_type, sql, params):
        # https://dev.mysql.com/doc/mysql/en/date-and-time-functions.html
        if lookup_type == "week_day":
            # DAYOFWEEK() returns an integer, 1-7, Sunday=1.
            return f"DAYOFWEEK({sql})", params
        elif lookup_type == "iso_week_day":
            # WEEKDAY() returns an integer, 0-6, Monday=0.
            return f"WEEKDAY({sql}) + 1", params
        elif lookup_type == "week":
            # Override the value of default_week_format for consistency with
            # other database backends.
            # Mode 3: Monday, 1-53, with 4 or more days this year.
            return f"WEEK({sql}, 3)", params
        elif lookup_type == "iso_year":
            # Get the year part from the YEARWEEK function, which returns a
            # number as year * 100 + week.
            return f"TRUNCATE(YEARWEEK({sql}, 3), -2) / 100", params
        else:
            # EXTRACT returns 1-53 based on ISO-8601 for the week number.
            lookup_type = lookup_type.upper()
            if not self._extract_format_re.fullmatch(lookup_type):
                raise ValueError(f"Invalid loookup type: {lookup_type!r}")
            return f"EXTRACT({lookup_type} FROM {sql})", params

    def date_trunc_sql(self, lookup_type, sql, params, tzname=None):
        sql, params = self._convert_field_to_tz(sql, params, tzname)
        if tzname:
            sql = f"CONVERT_TZ({sql}, %s, 'UTC')"
            params.append(tzname)

        trunc_sql = f"DATE_TRUNC(%s, {sql})"
        params.insert(0, lookup_type)

        return trunc_sql, params

    def _prepare_tzname_delta(self, tzname):
        tzname, sign, offset = split_tzname_delta(tzname)
        return f"{sign}{offset}" if offset else tzname

    def _convert_field_to_tz(self, sql, params, tzname):
        if tzname and settings.USE_TZ and self.connection.timezone_name != tzname:
            return f"CONVERT_TZ({sql}, %s, %s)", (
                *params,
                self.connection.timezone_name,
                self._prepare_tzname_delta(tzname),
            )
        return sql, params

    def datetime_cast_date_sql(self, sql, params, tzname):
        sql, params = self._convert_field_to_tz(sql, params, tzname)
        return f"DATE({sql})", params

    def datetime_cast_time_sql(self, sql, params, tzname):
        sql, params = self._convert_field_to_tz(sql, params, tzname)
        return f"TIME({sql})", params

    def datetime_extract_sql(self, lookup_type, sql, params, tzname):
        sql, params = self._convert_field_to_tz(sql, params, tzname)
        return self.date_extract_sql(lookup_type, sql, params)

    def datetime_trunc_sql(self, lookup_type, sql, params, tzname):
        """
        Generates SQL for truncating a datetime field to a specific precision.

        lookup_type: 'year', 'month', 'day', 'hour', 'minute', 'second'.
        sql: The SQL expression for the datetime field.
        params: Parameters for the SQL expression.
        tzname: The timezone in which to perform the truncation.
        """
        if tzname:
            # Adjust the datetime field to the specified timezone
            sql = f"CONVERT_TZ({sql}, %s, 'UTC')"
            params.append(tzname)

        # Use SingleStore's DATE_TRUNC function to truncate the datetime
        trunc_sql = f"DATE_TRUNC(%s, {sql})"
        params.insert(0, lookup_type)

        return trunc_sql, params

    def time_trunc_sql(self, lookup_type, sql, params, tzname=None):
        sql, params = self._convert_field_to_tz(sql, params, tzname)
        fields = {
            "hour": "%H:00:00",
            "minute": "%H:%i:00",
            "second": "%H:%i:%s",
        }
        if lookup_type in fields:
            format_str = fields[lookup_type]
            return f"(DATE_FORMAT({sql}, %s) :> TIME)", (*params, format_str)
        else:
            return f"TIME({sql})", params

    def fetch_returned_insert_rows(self, cursor):
        """
        Given a cursor object that has just performed an INSERT...RETURNING
        statement into a table, return the tuple of returned data.
        """
        return cursor.fetchall()

    def format_for_duration_arithmetic(self, sql):
        return "INTERVAL %s MICROSECOND" % sql

    def force_no_ordering(self):
        """
        "ORDER BY NULL" prevents MySQL from implicitly ordering by grouped
        columns. If no ordering would otherwise be applied, we don't want any
        implicit sorting going on.
        """
        return [(None, ("NULL", [], False))]

    def adapt_decimalfield_value(self, value, max_digits=None, decimal_places=None):
        return value

    def last_executed_query(self, cursor, sql, params):
        # With MySQLdb, cursor objects have an (undocumented) "_executed"
        # attribute where the exact query sent to the database is saved.
        # See MySQLdb/cursors.py in the source distribution.
        # MySQLdb returns string, PyMySQL bytes.
        return force_str(getattr(cursor, "_executed", None), errors="replace")

    def no_limit_value(self):
        # 2**64 - 1, as recommended by the MySQL documentation
        return 18446744073709551615

    def quote_name(self, name):
        if name.startswith("`") and name.endswith("`"):
            return name  # Quoting once is enough.
        return "`%s`" % name

    def return_insert_columns(self, fields):
        if not fields:
            return "", ()
        columns = [
            "%s.%s"
            % (
                self.quote_name(field.model._meta.db_table),
                self.quote_name(field.column),
            )
            for field in fields
        ]
        return "RETURNING %s" % ", ".join(columns), ()

    def sql_flush(self, style, tables, *, reset_sequences=False, allow_cascade=False):
        if not tables:
            return []

        sql = ["SET FOREIGN_KEY_CHECKS = 0;"]
        if reset_sequences:
            # It's faster to TRUNCATE tables that require a sequence reset
            # since ALTER TABLE AUTO_INCREMENT is slower than TRUNCATE.
            sql.extend(
                "%s %s;"
                % (
                    style.SQL_KEYWORD("TRUNCATE"),
                    style.SQL_FIELD(self.quote_name(table_name)),
                )
                for table_name in tables
            )
        else:
            # Otherwise issue a simple DELETE since it's faster than TRUNCATE
            # and preserves sequences.
            sql.extend(
                "%s %s %s;"
                % (
                    style.SQL_KEYWORD("DELETE"),
                    style.SQL_KEYWORD("FROM"),
                    style.SQL_FIELD(self.quote_name(table_name)),
                )
                for table_name in tables
            )
        sql.append("SET FOREIGN_KEY_CHECKS = 1;")
        return sql

    def sequence_reset_by_name_sql(self, style, sequences):
        return [
            "%s %s %s %s = 1;"
            % (
                style.SQL_KEYWORD("ALTER"),
                style.SQL_KEYWORD("TABLE"),
                style.SQL_FIELD(self.quote_name(sequence_info["table"])),
                style.SQL_FIELD("AUTO_INCREMENT"),
            )
            for sequence_info in sequences
        ]

    def validate_autopk_value(self, value):
        # Zero in AUTO_INCREMENT field does not work without the
        # NO_AUTO_VALUE_ON_ZERO SQL mode.
        if value == 0 and not self.connection.features.allows_auto_pk_0:
            raise ValueError(
                "The database backend does not accept 0 as a value for AutoField."
            )
        return value

    def adapt_datetimefield_value(self, value):
        if value is None:
            return None

        # Expression values are adapted by the database.
        if hasattr(value, "resolve_expression"):
            return value

        # SingleStore doesn't support tz-aware datetimes
        if timezone.is_aware(value):
            if settings.USE_TZ:
                value = timezone.make_naive(value, self.connection.timezone)
            else:
                raise ValueError(
                    "SingleStore backend does not support timezone-aware datetimes when "
                    "USE_TZ is False."
                )
        return str(value)

    def adapt_timefield_value(self, value):
        if value is None:
            return None

        # Expression values are adapted by the database.
        if hasattr(value, "resolve_expression"):
            return value

        # SingleStore doesn't support tz-aware times
        if timezone.is_aware(value):
            raise ValueError("SingleStore backend does not support timezone-aware times.")

        return value.isoformat(timespec="microseconds")

    def max_name_length(self):
        return 64

    def pk_default_value(self):
        return "NULL"

    def bulk_insert_sql(self, fields, placeholder_rows):
        placeholder_rows_sql = (", ".join(row) for row in placeholder_rows)
        values_sql = ", ".join("(%s)" % sql for sql in placeholder_rows_sql)
        return "VALUES " + values_sql

    def combine_expression(self, connector, sub_expressions):
        if connector == "^":
            return "POW(%s)" % ",".join(sub_expressions)
        # Convert the result to a signed integer since MySQL's binary operators
        # return an unsigned integer.
        elif connector in ("&", "|", "<<", "#"):
            connector = "^" if connector == "#" else connector
            return "CONVERT(%s, SIGNED)" % connector.join(sub_expressions)
        elif connector == ">>":
            lhs, rhs = sub_expressions
            return "FLOOR(%(lhs)s / POW(2, %(rhs)s))" % {"lhs": lhs, "rhs": rhs}
        return super().combine_expression(connector, sub_expressions)

    def get_db_converters(self, expression):
        converters = super().get_db_converters(expression)
        internal_type = expression.output_field.get_internal_type()
        if internal_type == "DateTimeField":
            converters.append(self.convert_datetimefield_value)
        elif internal_type == "DateField":
            converters.append(self.convert_datefield_value)
        elif internal_type == "TimeField":
            converters.append(self.convert_timefield_value)
        elif internal_type == "BooleanField":
            converters.append(self.convert_booleanfield_value)
        elif internal_type == "UUIDField":
            converters.append(self.convert_uuidfield_value)
        return converters

    def convert_booleanfield_value(self, value, expression, connection):
        if value in (0, 1):
            value = bool(value)
        return value

    def convert_datetimefield_value(self, value, expression, connection):
        if value is not None:
            if not isinstance(value, datetime.datetime):
                value = parse_datetime(value)
            if settings.USE_TZ and not timezone.is_aware(value):
                value = timezone.make_aware(value, self.connection.timezone)
        return value

    def convert_datefield_value(self, value, expression, connection):
        if value is not None:
            if not isinstance(value, datetime.date):
                value = parse_date(value)
        return value

    def convert_timefield_value(self, value, expression, connection):
        if value is not None:
            if not isinstance(value, datetime.time):
                value = parse_time(value)
        return value

    def convert_uuidfield_value(self, value, expression, connection):
        if value is not None:
            value = uuid.UUID(value)
        return value

    def binary_placeholder_sql(self, value):
        return (
            "_binary %s" if value is not None and not hasattr(value, "as_sql") else "%s"
        )

    def subtract_temporals(self, internal_type, lhs, rhs):
        lhs_sql, lhs_params = lhs
        rhs_sql, rhs_params = rhs
        if internal_type == "TimeField":
            return (
                "((TIME_TO_SEC(%(lhs)s) * 1000000 + MICROSECOND(%(lhs)s)) -"
                " (TIME_TO_SEC(%(rhs)s) * 1000000 + MICROSECOND(%(rhs)s)))"
            ) % {"lhs": lhs_sql, "rhs": rhs_sql}, tuple(lhs_params) * 2 + tuple(
                rhs_params
            ) * 2
        params = (*rhs_params, *lhs_params)
        return "TIMESTAMPDIFF(MICROSECOND, %s, %s)" % (rhs_sql, lhs_sql), params

    def explain_query_prefix(self, format=None, **options):
        # Alias MySQL's TRADITIONAL to TEXT for consistency with other backends.
        if format and format.upper() == "TEXT":
            format = "TRADITIONAL"
        elif (
            not format and "TREE" in self.connection.features.supported_explain_formats
        ):
            # Use TREE by default (if supported) as it's more informative.
            format = "TREE"
        analyze = options.pop("analyze", False)
        prefix = super().explain_query_prefix(format, **options)
        if analyze and self.connection.features.supports_explain_analyze:
            prefix += " ANALYZE"
        if format and not analyze:
            prefix += " FORMAT=%s" % format
        return prefix

    def regex_lookup(self, lookup_type):
        match_option = "c" if lookup_type == "regex" else "i"
        return "REGEXP_INSTR(%%s, %%s, 1, 1, 0, '%s')" % match_option

    def insert_statement(self, on_conflict=None):
        if on_conflict == OnConflict.IGNORE:
            return "INSERT IGNORE INTO"
        return super().insert_statement(on_conflict=on_conflict)

    def conditional_expression_supported_in_where_clause(self, expression):
        # MySQL ignores indexes with boolean fields unless they're compared
        # directly to a boolean value.
        if isinstance(expression, (Exists, Lookup)):
            return True
        if isinstance(expression, ExpressionWrapper) and expression.conditional:
            return self.conditional_expression_supported_in_where_clause(
                expression.expression
            )
        if getattr(expression, "conditional", False):
            return False
        return super().conditional_expression_supported_in_where_clause(expression)

    def on_conflict_suffix_sql(self, fields, on_conflict, update_fields, unique_fields):
        if on_conflict == OnConflict.UPDATE:
            conflict_suffix_sql = "ON DUPLICATE KEY UPDATE %(fields)s"
            field_sql = "%(field)s = VALUES(%(field)s)"

            fields = ", ".join(
                [
                    field_sql % {"field": field}
                    for field in map(self.quote_name, update_fields)
                ]
            )
            return conflict_suffix_sql % {"fields": fields}
        return super().on_conflict_suffix_sql(
            fields,
            on_conflict,
            update_fields,
            unique_fields,
        )

    def convert_durationfield_value(self, value, expression, connection):
        # Snowflake sometimes returns Decimal which is an unsupported type for
        # timedelta microseconds component.
        if isinstance(value, decimal.Decimal):
            value = float(value)
        return super().convert_durationfield_value(value, expression, connection)

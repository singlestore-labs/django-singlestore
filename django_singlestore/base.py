from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError
from django.db.backends import utils as backend_utils
from django.db.backends.base.base import BaseDatabaseWrapper
from django.utils.asyncio import async_unsafe
from django.utils.functional import cached_property
from django.utils.regex_helper import _lazy_re_compile

try:
    import singlestoredb as s2
except ImportError as err:
    raise ImproperlyConfigured(
        "Error loading singlestoredb module.\nDid you install singlestoredb?"
    ) from err

from singlestoredb.mysql.constants import FIELD_TYPE
from singlestoredb.mysql.converters import conversions

from .client import DatabaseClient
from .creation import DatabaseCreation
from .features import DatabaseFeatures
from .introspection import DatabaseIntrospection
from .operations import DatabaseOperations
from .schema import DatabaseSchemaEditor
from .validation import DatabaseValidation

# MySQLdb returns TIME columns as timedelta -- they are more like timedelta in
# terms of actual behavior as they are signed and include days -- and Django
# expects time.
django_conversions = {
    **conversions,
    **{FIELD_TYPE.TIME: backend_utils.typecast_time},
}

# This should match the numerical portion of the version numbers (we can treat
# versions like 5.0.24 and 5.0.24a as the same).
server_version_re = _lazy_re_compile(r"(\d{1,2})\.(\d{1,2})\.(\d{1,2})")


class CursorWrapper:
    """
    A thin wrapper around MySQLdb's normal cursor class that catches particular
    exception instances and reraises them with the correct types.

    Implemented as a wrapper, rather than a subclass, so that it isn't stuck
    to the particular underlying representation returned by Connection.cursor().
    """

    codes_for_integrityerror = (
        1048,  # Column cannot be null
        1690,  # BIGINT UNSIGNED value is out of range
        3819,  # CHECK constraint is violated
        4025,  # CHECK constraint failed
    )

    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, args=None):
        try:
            # args is None means no string interpolation
            return self.cursor.execute(query, args)
        except s2.OperationalError as e:
            # Map some error codes to IntegrityError, since they seem to be
            # misclassified and Django would prefer the more logical place.
            if e.args[0] in self.codes_for_integrityerror:
                raise IntegrityError(*tuple(e.args))
            raise

    def executemany(self, query, args):
        try:
            return self.cursor.executemany(query, args)
        except s2.OperationalError as e:
            # Map some error codes to IntegrityError, since they seem to be
            # misclassified and Django would prefer the more logical place.
            if e.args[0] in self.codes_for_integrityerror:
                raise IntegrityError(*tuple(e.args))
            raise

    def __getattr__(self, attr):
        return getattr(self.cursor, attr)

    def __iter__(self):
        return iter(self.cursor)


class DatabaseWrapper(BaseDatabaseWrapper):
    vendor = "singlestore"
    # This dictionary maps Field objects to their associated MySQL column
    # types, as strings. Column-type strings can contain format strings; they'll
    # be interpolated against the values of Field.__dict__ before being output.
    # If a column type is set to None, it won't be included in the output.
    data_types = {
        "AutoField": "integer AUTO_INCREMENT",
        "BigAutoField": "bigint AUTO_INCREMENT",
        "BinaryField": "longblob",
        "BooleanField": "bool",
        "CharField": "varchar(%(max_length)s)",
        "DateField": "date",
        "DateTimeField": "datetime(6)",
        "DecimalField": "numeric(%(max_digits)s, %(decimal_places)s)",
        "DurationField": "bigint",
        "FileField": "varchar(%(max_length)s)",
        "FilePathField": "varchar(%(max_length)s)",
        "FloatField": "double precision",
        "IntegerField": "integer",
        "BigIntegerField": "bigint",
        "IPAddressField": "char(15)",
        "GenericIPAddressField": "char(39)",
        "JSONField": "json",
        "OneToOneField": "integer",
        "PositiveBigIntegerField": "bigint UNSIGNED",
        "PositiveIntegerField": "integer UNSIGNED",
        "PositiveSmallIntegerField": "smallint UNSIGNED",
        "SlugField": "varchar(%(max_length)s)",
        "SmallAutoField": "smallint AUTO_INCREMENT",
        "SmallIntegerField": "smallint",
        "TextField": "longtext",
        "TimeField": "time(6)",
        "UUIDField": "char(32)",
    }

    operators = {
        "exact": "= %s",
        "iexact": "LIKE %s",
        "contains": "LIKE BINARY %s",
        "icontains": "LIKE %s",
        "gt": "> %s",
        "gte": ">= %s",
        "lt": "< %s",
        "lte": "<= %s",
        "startswith": "LIKE BINARY %s",
        "endswith": "LIKE BINARY %s",
        "istartswith": "LIKE %s",
        "iendswith": "LIKE %s",
    }

    # The patterns below are used to generate SQL pattern lookup clauses when
    # the right-hand side of the lookup isn't a raw string (it might be an expression
    # or the result of a bilateral transformation).
    # In those cases, special characters for LIKE operators (e.g. \, *, _) should be
    # escaped on database side.
    #
    # Note: we use str.format() here for readability as '%' is used as a wildcard for
    # the LIKE operator.
    pattern_esc = r"REPLACE(REPLACE(REPLACE({}, '\\', '\\\\'), '%', '\%'), '_', '\_')"
    pattern_ops = {
        "contains": "LIKE BINARY CONCAT('%%', {}, '%%')",
        "icontains": "LIKE CONCAT('%%', {}, '%%')",
        "startswith": "LIKE BINARY CONCAT({}, '%%')",
        "istartswith": "LIKE CONCAT({}, '%%')",
        "endswith": "LIKE BINARY CONCAT('%%', {})",
        "iendswith": "LIKE CONCAT('%%', {})",
    }

    isolation_levels = {
        "read committed",
    }

    Database = s2
    SchemaEditorClass = DatabaseSchemaEditor
    # Classes instantiated in __init__().
    client_class = DatabaseClient
    creation_class = DatabaseCreation
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations
    validation_class = DatabaseValidation

    def get_database_version(self):
        return self.s2_version

    def get_connection_params(self):
        kwargs = {
            "conv": django_conversions,
        }
        settings_dict = self.settings_dict
        if settings_dict["USER"]:
            kwargs["user"] = settings_dict["USER"]
        if settings_dict["NAME"]:
            kwargs["database"] = settings_dict["NAME"]
        if settings_dict["PASSWORD"]:
            kwargs["password"] = settings_dict["PASSWORD"]
        if settings_dict["HOST"].startswith("/"):
            kwargs["unix_socket"] = settings_dict["HOST"]
        elif settings_dict["HOST"]:
            kwargs["host"] = settings_dict["HOST"]
        if settings_dict["PORT"]:
            kwargs["port"] = int(settings_dict["PORT"])
        # We need the number of potentially affected rows after an
        # "UPDATE", not the number of changed rows.
        kwargs["client_found_rows"] = True
        kwargs["parse_json"] = False
        kwargs["conn_attrs"] = {"_connector_name": "SingleStore Django Connector"}
        # Validate the transaction isolation level, if specified.
        options = settings_dict["OPTIONS"].copy()
        isolation_level = options.pop("isolation_level", "read committed")
        if isolation_level:
            isolation_level = isolation_level.lower()
            if isolation_level not in self.isolation_levels:
                raise ImproperlyConfigured(
                    "Invalid transaction isolation level '%s' specified.\n"
                    "Use one of %s, or None."
                    % (
                        isolation_level,
                        ", ".join("'%s'" % s for s in sorted(self.isolation_levels)),
                    )
                )
        self.isolation_level = isolation_level
        kwargs.update(options)
        return kwargs

    @async_unsafe
    def get_new_connection(self, conn_params):
        return s2.connect(**conn_params)

    def init_connection_state(self):
        super().init_connection_state()
        assignments = []

        # if self.isolation_level:
        #     assignments.append(
        #         "SET SESSION TRANSACTION ISOLATION LEVEL %s"
        #         % self.isolation_level.upper()
        #     )

        if assignments:
            with self.cursor() as cursor:
                cursor.execute("; ".join(assignments))

    @async_unsafe
    def create_cursor(self, name=None):
        cursor = self.connection.cursor()
        return CursorWrapper(cursor)

    def _set_autocommit(self, autocommit):
        with self.wrap_database_errors:
            self.connection.autocommit(autocommit)

    def check_constraints(self, table_names=None):
        """
        Check each table name in `table_names` for rows with invalid foreign
        key references. This method is intended to be used in conjunction with
        `disable_constraint_checking()` and `enable_constraint_checking()`, to
        determine if rows with invalid references were entered while constraint
        checks were off.
        """
        with self.cursor() as cursor:
            if table_names is None:
                table_names = self.introspection.table_names(cursor)
            for table_name in table_names:
                primary_key_column_name = self.introspection.get_primary_key_column(
                    cursor, table_name
                )
                if not primary_key_column_name:
                    continue
                relations = self.introspection.get_relations(cursor, table_name)
                for column_name, (
                    referenced_column_name,
                    referenced_table_name,
                ) in relations.items():
                    cursor.execute(
                        """
                        SELECT REFERRING.`%s`, REFERRING.`%s` FROM `%s` as REFERRING
                        LEFT JOIN `%s` as REFERRED
                        ON (REFERRING.`%s` = REFERRED.`%s`)
                        WHERE REFERRING.`%s` IS NOT NULL AND REFERRED.`%s` IS NULL
                        """
                        % (
                            primary_key_column_name,
                            column_name,
                            table_name,
                            referenced_table_name,
                            column_name,
                            referenced_column_name,
                            column_name,
                            referenced_column_name,
                        )
                    )
                    for bad_row in cursor.fetchall():
                        raise IntegrityError(
                            "The row in table '%s' with primary key '%s' has an "
                            "invalid foreign key: %s.%s contains a value '%s' that "
                            "does not have a corresponding value in %s.%s."
                            % (
                                table_name,
                                bad_row[0],
                                table_name,
                                column_name,
                                bad_row[1],
                                referenced_table_name,
                                referenced_column_name,
                            )
                        )

    def is_usable(self):
        try:
            self.connection.ping()
        except s2.Error:
            return False
        else:
            return True

    @cached_property
    def display_name(self):
        return "SingleStore"

    @cached_property
    def singlestore_server_data(self):
        with self.temporary_connection() as cursor:
            # Select some server variables and test if the time zone
            # definitions are installed. CONVERT_TZ returns NULL if 'UTC'
            # timezone isn't loaded into the mysql.time_zone table.
            cursor.execute(
                """
                SELECT @@memsql_version,
                       @@sql_mode,
                       @@default_table_type,
                       @@table_name_case_sensitivity,
                       CONVERT_TZ('2001-01-01 01:00:00', 'UTC', 'UTC') IS NOT NULL
            """
            )
            row = cursor.fetchone()
        return {
            "version": row[0],
            "sql_mode": row[1],
            "default_table_type": row[2],
            "table_name_case_sensitivity": bool(row[3]),
            "has_zoneinfo_database": bool(row[4]),
        }

    @cached_property
    def s2_server_info(self):
        return self.singlestore_server_data["version"]

    @cached_property
    def s2_version(self):
        match = server_version_re.match(self.s2_server_info)
        if not match:
            raise Exception(
                "Unable to determine MySQL version from version string %r"
                % self.s2_server_info
            )
        return tuple(int(x) for x in match.groups())

    @cached_property
    def sql_mode(self):
        sql_mode = self.singlestore_server_data["sql_mode"]
        return set(sql_mode.split(",") if sql_mode else ())

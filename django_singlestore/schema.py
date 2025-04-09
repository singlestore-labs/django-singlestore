import os

from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.models import NOT_PROVIDED, Manager


class ModelStorageManager(Manager):
    use_in_migrations = True

    def __init__(self, table_storage_type="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        if table_storage_type not in ("ROWSTORE", "REFERENCE", "ROWSTORE REFERENCE", ""):
            raise ValueError('table_storage_type must be one of: "", "ROWSTORE", "REFERENCE", "ROWSTORE REFERENCE"')
        self.table_storage_type = table_storage_type


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):

    sql_create_table = "CREATE %(table_storage_type)s TABLE %(table)s (%(definition)s) %(comment)s"
    sql_rename_table = "ALTER TABLE %(old_table)s RENAME TO %(new_table)s"
    sql_delete_table = "DROP TABLE %(table)s"

    sql_alter_column_null = "MODIFY %(column)s %(type)s NULL"
    sql_alter_column_not_null = "MODIFY %(column)s %(type)s NOT NULL"  # only for ROWSTORE REFERENCE tables
    sql_alter_column_type = "MODIFY %(column)s %(type)s%(collation)s%(comment)s"  # not for COLUMNSTORE tables
    sql_alter_column_collate = "MODIFY %(column)s %(type)s%(collation)s"  # only for ROWSTORE tables
    sql_alter_column_no_default_null = "MODIFY %(column)s %(type)s DEFAULT NULL"

    sql_delete_column = "ALTER TABLE %(table)s DROP COLUMN %(column)s"

    sql_delete_unique = "ALTER TABLE %(table)s DROP INDEX %(name)s"

    sql_delete_index = "DROP INDEX %(name)s ON %(table)s"
    sql_rename_index = "ALTER TABLE %(table)s RENAME INDEX %(old_name)s TO %(new_name)s"

    # sql_create_pk not supported by SingleStore
    # sql_create_pk = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s PRIMARY KEY (%(columns)s)"

    sql_delete_pk = "ALTER TABLE %(table)s DROP PRIMARY KEY"  # only for ROWSTORE tables

    sql_create_index = "CREATE INDEX %(name)s ON %(table)s (%(columns)s)%(extra)s"

    sql_rename_column = "ALTER TABLE %(table)s CHANGE %(old_column)s %(new_column)s"
    
    # sql_alter_table_comment doesn't work yet TODO
    sql_alter_table_comment = "ALTER TABLE %(table)s COMMENT = %(comment)s"
    
    sql_alter_column_comment = "ALTER TABLE %(table)s MODIFY COLUMN %(column)s %(type)s %(comment)s"

    @property
    def sql_delete_check(self):
        return "ALTER TABLE %(table)s DROP CHECK %(name)s"

    def quote_value(self, value):
        self.connection.ensure_connection()
        # if isinstance(value, str):
        #     value = value.replace("%", "%%")
        # MySQLdb escapes to string, PyMySQL to bytes.
        quoted = self.connection.connection.escape(
            value, self.connection.connection.encoders
        )
        if isinstance(value, str) and isinstance(quoted, bytes):
            quoted = quoted.decode()
        return quoted

    def prepare_default(self, value):
        return self.quote_value(value)

    def column_sql(self, model, field, include_default=False):
        """
        Return the column definition for a field. The field must already have
        had set_attributes_from_name() called.
        """
        # Get the column's type and use that as the basis of the SQL.
        field_db_params = field.db_parameters(connection=self.connection)
        column_db_type = field_db_params["type"]
        # Check for fields that aren't actually columns (e.g. M2M).
        if column_db_type is None:
            return None, None

        params = []
        result_sql_parts = [column_db_type]
        if collation := field_db_params.get("collation"):
            result_sql_parts.append(self._collate_sql(collation))
        if self.connection.features.supports_comments_inline and field.db_comment:
            result_sql_parts.append(self._comment_sql(field.db_comment))
        # Include a default value, if requested.
        include_default = include_default and not field.null
        if include_default:
            default_value = self.effective_default(field)
            if default_value is not None:
                column_default = "DEFAULT " + self._column_default_sql(field)
                if self.connection.features.requires_literal_defaults:
                    # Some databases can't take defaults as a parameter (Oracle).
                    # If this is the case, the individual schema backend should
                    # implement prepare_default().
                    result_sql_parts.append(column_default % self.prepare_default(default_value))
                else:
                    result_sql_parts.append(column_default)
                    params.append(default_value)
        if not field.null:
            result_sql_parts.append("NOT NULL")
        elif not self.connection.features.implied_column_null:
            result_sql_parts.append("NULL")
        if field.primary_key:
            result_sql_parts.append("PRIMARY KEY")
        # if DJANGO_SINGLESTORE_NOT_ENFORCED_UNIQUE_<APP_ANME> env variable is set, we don't enforce unique constraints
        # on tables created for this app.
        # This is needed to create test tables that must have more than one unique field which
        # is not allowed in SingleStore distributed tables.
        elif field.unique and os.getenv("DJANGO_SINGLESTORE_NOT_ENFORCED_UNIQUE_" + model._meta.app_label.upper()) is None:
            result_sql_parts.append("UNIQUE")

        return " ".join(result_sql_parts), []

    def table_sql(self, model):
        """Take a model and return its table definition."""
        # Create column SQL, add FK deferreds if needed.
        column_sqls = []
        params = []
        table_storage_type = os.getenv("DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_" + model._meta.app_label.upper(), "")

        for manager in model._meta.local_managers:
            # if storage type is specified for the model, we use it
            if isinstance(manager, ModelStorageManager):
                table_storage_type = manager.table_storage_type

        additional_keys = []
        for field in model._meta.local_fields:
            # SQL.
            definition, extra_params = self.column_sql(model, field)
            if definition is None:
                continue
            # Check constraints can go on the column SQL here.
            db_params = field.db_parameters(connection=self.connection)
            if db_params["check"]:
                definition += " " + self.sql_check_constraint % db_params
            # Autoincrement SQL (for backends with inline variant).
            col_type_suffix = field.db_type_suffix(connection=self.connection)
            if col_type_suffix:
                definition += " %s" % col_type_suffix
            params.extend(extra_params)
            # FK.
            if field.remote_field and field.db_constraint:
                to_table = field.remote_field.model._meta.db_table
                to_column = field.remote_field.model._meta.get_field(
                    field.remote_field.field_name
                ).column
                if self.sql_create_inline_fk:
                    definition += " " + self.sql_create_inline_fk % {
                        "to_table": self.quote_name(to_table),
                        "to_column": self.quote_name(to_column),
                    }
                elif self.connection.features.supports_foreign_keys:
                    self.deferred_sql.append(
                        self._create_fk_sql(
                            model, field, "_fk_%(to_table)s_%(to_column)s"
                        )
                    )
            # Add the SQL to our big list.
            column_sqls.append(
                "%s %s"
                % (
                    self.quote_name(field.column),
                    definition,
                )
            )
            # Autoincrement SQL (for backends with post table definition
            # variant).
            if field.get_internal_type() in (
                "AutoField",
                "BigAutoField",
                "SmallAutoField",
            ):
                autoinc_sql = self.connection.ops.autoinc_sql(
                    model._meta.db_table, field.column
                )
                if autoinc_sql:
                    self.deferred_sql.extend(autoinc_sql)
            if "REFERENCE" not in table_storage_type.upper():
                if field.primary_key:
                    # we must have the unique field as the shard key. Each django model has a field
                    # designated as a primary key, so it must be the shard key as well
                    additional_keys.append(f"SHARD KEY ({self.quote_name(field.column)})")
                elif field.unique and os.getenv("DJANGO_SINGLESTORE_NOT_ENFORCED_UNIQUE_" + model._meta.app_label.upper()) is not None:
                    additional_keys.append(f"UNIQUE KEY({self.quote_name(field.column)}) UNENFORCED RELY")
        for field_names in model._meta.unique_together:
            fields = [model._meta.get_field(field) for field in field_names]
            additional_keys.append(f'UNIQUE KEY({",".join(self.quote_name(f.column) for f in fields)})')
        constraints = [
            constraint.constraint_sql(model, self)
            for constraint in model._meta.constraints
        ]
        comment = f" COMMENT {self.quote_value(model._meta.db_table_comment)}" if model._meta.db_table_comment else ""
        sql = self.sql_create_table % {
            "table": self.quote_name(model._meta.db_table),
            "table_storage_type": table_storage_type,
            "definition": ", ".join(
                str(constraint)
                for constraint in (*column_sqls, *constraints, *additional_keys)
                if constraint
            ),
            "comment": comment,
        }
        if model._meta.db_tablespace:
            tablespace_sql = self.connection.ops.tablespace_sql(
                model._meta.db_tablespace
            )
            if tablespace_sql:
                sql += " " + tablespace_sql
        return sql, params

    def add_field(self, model, field):
        super().add_field(model, field)

        # Simulate the effect of a one-off default.
        # field.default may be unhashable, so a set isn't used for "in" check.
        if field.default not in (None, NOT_PROVIDED):
            effective_default = self.effective_default(field)
            self.execute(
                "UPDATE %(table)s SET %(column)s = %%s"
                % {
                    "table": self.quote_name(model._meta.db_table),
                    "column": self.quote_name(field.column),
                },
                [effective_default],
            )

    def _set_field_new_type_null_status(self, field, new_type):
        """
        Keep the null property of the old field. If it has changed, it will be
        handled separately.
        """
        if field.null:
            new_type += " NULL"
        else:
            new_type += " NOT NULL"
        return new_type

    def _rename_field_sql(self, table, old_field, new_field, new_type):
        new_type = self._set_field_new_type_null_status(old_field, new_type)
        return super()._rename_field_sql(table, old_field, new_field, new_type)

    def _comment_sql(self, comment):
        comment_sql = super()._comment_sql(comment)
        return f" COMMENT {comment_sql}"

    def _alter_column_comment_sql(self, model, new_field, new_type, new_db_comment):
        return (
            self.sql_alter_column_comment
            % {
                "table": self.quote_name(model._meta.db_table),
                "column": self.quote_name(new_field.column),
                "type": new_type,
                "comment": self._comment_sql(new_db_comment),
            },
            [],
        )

    def _alter_column_type_sql(
        self, model, old_field, new_field, new_type, old_collation, new_collation
    ):
        new_type = self._set_field_new_type_null_status(old_field, new_type)
        return super()._alter_column_type_sql(
            model, old_field, new_field, new_type, old_collation, new_collation
        )

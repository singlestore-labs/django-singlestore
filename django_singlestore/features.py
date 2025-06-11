from typing import Any
from typing import List

from django.db import ProgrammingError
from django.db.backends.base.features import BaseDatabaseFeatures
from django.utils.functional import cached_property


class DatabaseFeatures(BaseDatabaseFeatures):
    # An optional tuple indicating the minimum supported database version.
    minimum_database_version = (8, 5, 21)  # TODO: set correct version
    gis_enabled = False
    # Oracle can't group by LOB (large object) data types.
    allows_group_by_lob = True
    allows_group_by_selected_pks = False
    allows_group_by_select_index = True
    empty_fetchmany_value: List[Any] = []
    update_can_self_select = True

    # Does the backend distinguish between '' and None?
    interprets_empty_strings_as_nulls = False

    # Does the backend allow inserting duplicate NULL rows in a nullable
    # unique field? All core backends implement this correctly, but other
    # databases such as SQL Server do not.
    supports_nullable_unique_constraints = True

    # Does the backend allow inserting duplicate rows when a unique_together
    # constraint exists and some fields are nullable but not all of them?
    supports_partially_nullable_unique_constraints = True
    # Does the backend support initially deferrable unique constraints?
    supports_deferrable_unique_constraints = False

    can_use_chunked_reads = True
    can_return_columns_from_insert = False
    can_return_rows_from_bulk_insert = False
    has_bulk_insert = True
    uses_savepoints = False
    can_release_savepoints = False

    # If True, don't use integer foreign keys referring to, e.g., positive
    # integer primary keys.
    related_fields_match_type = False
    allow_sliced_subqueries_with_in = True

    has_select_for_update = True
    has_select_for_update_nowait = False
    has_select_for_update_skip_locked = False
    has_select_for_update_of = False
    has_select_for_no_key_update = False
    # Does the database's SELECT FOR UPDATE OF syntax require a column rather
    # than a table?
    select_for_update_of_column = False

    # Does the default test database allow multiple connections?
    # Usually an indication that the test database is in-memory
    test_db_allows_multiple_connections = True

    # Can an object be saved without an explicit primary key?
    supports_unspecified_pk = True

    # Can a fixture contain forward references? i.e., are
    # FK constraints checked at the end of transaction, or
    # at the end of each save operation?
    supports_forward_references = False

    # Does the backend truncate names properly when they are too long?
    truncates_names = False

    # Is there a REAL datatype in addition to floats/doubles?
    has_real_datatype = False
    supports_subqueries_in_group_by = True

    # Does the backend ignore unnecessary ORDER BY clauses in subqueries?
    ignores_unnecessary_order_by_in_subqueries = True

    # Is there a true datatype for uuid?
    has_native_uuid_field = False

    # Is there a true datatype for timedeltas?
    has_native_duration_field = False

    # Does the database driver supports same type temporal data subtraction
    # by returning the type used to store duration field?
    supports_temporal_subtraction = False

    # Does the __regex lookup support backreferencing and grouping?
    supports_regex_backreferencing = True

    # Can date/datetime lookups be performed using a string?
    supports_date_lookup_using_string = True

    # Can datetimes with timezones be used?
    supports_timezones = False

    # Does the database have a copy of the zoneinfo database?
    has_zoneinfo_database = False

    # When performing a GROUP BY, is an ORDER BY NULL required
    # to remove any ordering?
    requires_explicit_null_ordering_when_grouping = False

    # Does the backend order NULL values as largest or smallest?
    nulls_order_largest = False

    # Does the backend support NULLS FIRST and NULLS LAST in ORDER BY?
    supports_order_by_nulls_modifier = False

    # Does the backend orders NULLS FIRST by default?
    order_by_nulls_first = False

    # The database's limit on the number of query parameters.
    max_query_params = 1048576

    # Can an object have an autoincrement primary key of 0?
    allows_auto_pk_0 = True

    # Do we need to NULL a ForeignKey out, or can the constraint check be
    # deferred
    can_defer_constraint_checks = False

    # Does the backend support tablespaces? Default to False because it isn't
    # in the SQL standard.
    supports_tablespaces = False

    # Does the backend reset sequences between tests?
    supports_sequence_reset = False

    # Can the backend introspect the default value of a column?
    can_introspect_default = True

    # Confirm support for introspected foreign keys
    # Every database can do this reliably, except MySQL,
    # which can't do it for MyISAM tables
    can_introspect_foreign_keys = False

    # Can the backend introspect the column order (ASC/DESC) for indexes?
    supports_index_column_ordering = True

    # Does the backend support introspection of materialized views?
    can_introspect_materialized_views = False

    # Support for the DISTINCT ON clause
    can_distinct_on_fields = False

    # In Django prior to https://code.djangoproject.com/ticket/28263#no1
    # transaction support requires savepoints for tests and Atomic class to work
    # properly
    # TODO: enable for django 5.0
    supports_transactions = False

    # Does the backend prevent running SQL queries in broken transactions?
    atomic_transactions = False

    # Can we roll back DDL in a transaction?
    can_rollback_ddl = False

    schema_editor_uses_clientside_param_binding = False

    # Does it support operations requiring references rename in a transaction?
    supports_atomic_references_rename = True

    # Can we issue more than one ALTER COLUMN clause in an ALTER TABLE?
    supports_combined_alters = False

    # Does it support foreign keys?
    supports_foreign_keys = False

    # Can it create foreign key constraints inline when adding columns?
    can_create_inline_fk = False

    # Can an index be renamed?
    can_rename_index = False

    # Does it automatically index foreign keys?
    indexes_foreign_keys = True

    # Does it support CHECK constraints?
    supports_column_check_constraints = False
    supports_table_check_constraints = False
    # Does the backend support introspection of CHECK constraints?
    can_introspect_check_constraints = False

    # Does the backend support 'pyformat' style ("... %(name)s ...", {'name': value})
    # parameter passing? Note this can be provided by the backend even if not
    # supported by the Python driver
    supports_paramstyle_pyformat = True

    # Does the backend require literal defaults, rather than parameterized ones?
    requires_literal_defaults = True

    # Does the backend require a connection reset after each material schema change?
    connection_persists_old_columns = False

    # What kind of error does the backend throw when accessing closed cursor?
    closed_cursor_error_class = ProgrammingError

    # Suffix for backends that don't support "SELECT xxx;" queries
    # SingleStore needs this for queries like `SELECT 1 WHERE 1` which need a FROM part
    bare_select_suffix = " FROM DUAL"

    # If NULL is implied on columns without needing to be explicitly specified
    implied_column_null = False

    # Does the backend support "select for update" queries with limit (and offset)?
    supports_select_for_update_with_limit = True

    # Does the backend ignore null expressions in GREATEST and LEAST queries unless
    # every expression is null?
    greatest_least_ignores_nulls = False

    # Can the backend clone databases for parallel test execution?
    # Defaults to False to allow third-party backends to opt-in.
    can_clone_databases = False

    # Does the backend consider table names with different casing to
    # be equal?
    # ignores_table_name_case = False

    # Place FOR UPDATE right after FROM clause. Used on MSSQL.
    for_update_after_from = False

    # Combinatorial flags
    supports_select_union = True
    supports_select_intersection = True
    supports_select_difference = False
    supports_slicing_ordering_in_compound = False
    supports_parentheses_in_compound = True
    requires_compound_order_by_subquery = True

    # Does the database support SQL 2003 FILTER (WHERE ...) in aggregate
    # expressions?
    supports_aggregate_filter_clause = False

    # Does the backend support indexing a TextField?
    supports_index_on_text_field = True

    # Does the backend support window expressions (expression OVER (...))?
    supports_over_clause = False
    supports_frame_range_fixed_distance = False
    only_supports_unbounded_with_preceding_and_following = False

    # Does the backend support CAST with precision?
    supports_cast_with_precision = True

    # How many second decimals does the database return when casting a value to
    # a type with time?
    time_cast_precision = 6

    # SQL to create a table with a composite primary key for use by the Django
    # test suite.
    create_test_table_with_composite_primary_key = None

    # Does the backend support keyword parameters for cursor.callproc()?
    supports_callproc_kwargs = False

    # What formats does the backend EXPLAIN syntax support?
    supported_explain_formats = {"JSON", ""}

    # Does the backend support the default parameter in lead() and lag()?
    supports_default_in_lead_lag = True

    # Does the backend support ignoring constraint or uniqueness errors during
    # INSERT?
    supports_ignore_conflicts = True
    # Does the backend support updating rows on constraint or uniqueness errors
    # during INSERT?
    supports_update_conflicts = True
    supports_update_conflicts_with_target = True

    # Does this backend require casting the results of CASE expressions used
    # in UPDATE statements to ensure the expression has the correct type?
    requires_casted_case_in_updates = False

    # Does the backend support partial indexes (CREATE INDEX ... WHERE ...)?
    supports_partial_indexes = False
    supports_functions_in_partial_indexes = True
    # Does the backend support covering indexes (CREATE INDEX ... INCLUDE ...)?
    supports_covering_indexes = False
    # Does the backend support indexes on expressions?
    supports_expression_indexes = False
    # Does the backend treat COLLATE as an indexed expression?
    collate_as_index_expression = False

    # Does the database allow more than one constraint or index on the same
    # field(s)?
    allows_multiple_constraints_on_same_fields = True

    # Does the backend support boolean expressions in SELECT and GROUP BY
    # clauses?
    supports_boolean_expr_in_select_clause = True
    # Does the backend support comparing boolean expressions in WHERE clauses?
    # Eg: WHERE (price > 0) IS NOT NULL
    supports_comparing_boolean_expr = True

    # Does the backend support JSONField?
    supports_json_field = True
    # Can the backend introspect a JSONField?
    can_introspect_json_field = True
    # Does the backend support primitives in JSONField?
    supports_primitives_in_json_field = True
    # has_native_json_field has some cryptic meaning in django, and django
    # generates better sql for SingleStore if has_native_json_field is set to False
    has_native_json_field = False
    # Does the backend use PostgreSQL-style JSON operators like '->'?
    has_json_operators = False
    # Does the backend support __contains and __contained_by lookups for
    # a JSONField?
    # TODO: set this to True and modify HasKeyLookup.as_sql
    supports_json_field_contains = False
    # Does value__d__contains={'f': 'g'} (without a list around the dict) match
    # {'d': [{'f': 'g'}]}?
    json_key_contains_list_matching_requires_list = False
    # Does the backend support JSONObject() database function?
    has_json_object_function = True

    # Does the backend support column collations?
    supports_collation_on_charfield = True
    supports_collation_on_textfield = True
    # Does the backend support non-deterministic collations?
    supports_non_deterministic_collations = True

    # Does the backend support column and table comments?
    supports_comments = True
    # Does the backend support column comments in ADD COLUMN statements?
    supports_comments_inline = True

    # Does the backend support the logical XOR operator?
    supports_logical_xor = False

    # Set to (exception, message) if null characters in text are disallowed.
    prohibits_null_characters_in_text_exception = None

    # Does the backend support unlimited character columns?
    supports_unlimited_charfield = False

    supports_update_conflicts_with_target = False

    @cached_property
    def introspected_field_types(self):
        return {
            **super().introspected_field_types,
            "BinaryField": "TextField",
            "BooleanField": "IntegerField",
            "DurationField": "BigIntegerField",
            "GenericIPAddressField": "CharField",
        }

    # SQL template override for tests.aggregation.tests.NowUTC
    test_now_utc_template = None

    create_test_procedure_without_params_sql = """
        CREATE PROCEDURE test_procedure ()
        AS
        DECLARE V_I INT = 0;
        BEGIN
            V_I = 1;
        END;
    """
    create_test_procedure_with_int_param_sql = """
        CREATE PROCEDURE test_procedure (P_I INTEGER)
        AS
        DECLARE V_I INT = P_I;
        BEGIN
            V_I = V_I + 1;
        END;
    """
    create_test_table_with_composite_primary_key = """
        CREATE TABLE test_table_composite_pk (
            column_1 INTEGER NOT NULL,
            column_2 INTEGER NOT NULL,
            PRIMARY KEY(column_1, column_2)
        )
    """

    @cached_property
    def test_collations(self):
        charset = "utf8mb4"
        return {
            "ci": f"{charset}_general_ci",
            "cs": f"{charset}_bin",
            "non_default": f"{charset}_esperanto_ci",
            "swedish_ci": f"{charset}_swedish_ci",
        }

    test_now_utc_template = "UTC_TIMESTAMP"

    # TODO: update this list
    @cached_property
    def django_test_skips(self):
        skips = {
            "SingleStore does not enforce FOREIGN KEY constraints":
            {
                "backends.tests.FkConstraintsTests",
                "fixtures_regress.tests.TestFixtures.test_loaddata_raises_error_when_fixture_has_invalid_foreign_key",
                "model_fields.test_uuid.TestAsPrimaryKeyTransactionTests.test_unsaved_fk",
                "transactions.tests.NonAutocommitTests.test_orm_query_after_error_and_rollback",
                "inspectdb.tests.InspectDBTestCase.test_same_relations",
            },
            "SingleStore does not support FLOAT/DOUBLE primary keys on ColumnStore tables":
            {
                "serializers.test_data.SerializerDataTests",
            },
            "SingleStore does not support UNIQUE constraints on non-shard key columns in distributed tables":
            {
                "get_or_create.tests.GetOrCreateTestsWithManualPKs.test_savepoint_rollback",
            },
            "Feature 'FOR UPDATE with subselect or join involving a columnstore table' is not supported by SingleStore":
            {
                "get_or_create.tests.UpdateOrCreateTests.test_create_with_many",
                "get_or_create.tests.UpdateOrCreateTests.test_update_with_many",
                "get_or_create.tests.UpdateOrCreateTests.test_mti_update_non_local_concrete_fields",
                "get_or_create.tests.UpdateOrCreateTests.test_manual_primary_key_test",
            },
            "update_or_create uses two nested atomic blocks, and rollback is not done properly without savepoint":
            {
                "get_or_create.tests.UpdateOrCreateTests.test_integrity",
                "get_or_create.tests.UpdateOrCreateTestsWithManualPKs.test_create_with_duplicate_primary_key",
            },
            "Unique keys are not enforced on columnstore tables when they don't contain the shard key":
            {
                "get_or_create.tests.GetOrCreateThroughManyToMany.test_something",
            },
            "The query cannot be executed. SingleStore does not support this type of query: \
scalar subselect references field belonging to outer select that is more than one level up":
            {
                "lookup.tests.LookupTests.test_nested_outerref_lhs",
                "aggregation.test_filter_argument.FilteredAggregateTests.\
test_filtered_aggregate_ref_multiple_subquery_annotation",
                "queries.tests.ExcludeTests.test_subquery_exclude_outerref",
                "expressions.tests.BasicExpressionsTests.test_annotation_with_deeply_nested_outerref",
                "expressions.tests.BasicExpressionsTests.test_annotation_with_nested_outerref",
                "expressions.tests.BasicExpressionsTests.test_nested_outerref_with_function",
                "expressions.tests.BasicExpressionsTests.test_nested_subquery_outer_ref_2",
                "expressions.tests.BasicExpressionsTests.test_nested_subquery_outer_ref_with_autofield",
            },
            "Feature 'scalar subselect inside the GROUP/ORDER BY of a pushed down query' is not supported \
by SingleStore Distributed":
            {
                "aggregation.tests.AggregateTestCase.test_aggregation_exists_multivalued_outeref",
                "aggregation.tests.AggregateTestCase.test_aggregation_subquery_annotation_multivalued",
                "aggregation.tests.AggregateTestCase.test_aggregation_subquery_annotation_related_field",
                "aggregation.tests.AggregateTestCase.test_group_by_exists_annotation",
                "aggregation.tests.AggregateTestCase.test_group_by_subquery_annotation",
                "annotations.tests.NonAggregateAnnotationTestCase.\
test_annotation_subquery_and_aggregate_values_chaining",
                "aggregation_regress.tests.AggregationTests.test_annotate_with_extra",
            },
            "Feature 'Subselect in aggregate functions' is not supported by SingleStore":
            {
                "aggregation.tests.AggregateTestCase.test_values_annotation_with_expression",
                "aggregation.test_filter_argument.FilteredAggregateTests.test_filtered_aggregate_on_exists",
                "expressions_case.tests.CaseExpressionTests.test_annotate_with_in_clause",
            },
            "Feature 'Correlated subselect that can not be transformed and does not match on shard keys' \
is not supported by SingleStore Distributed":
            {
                "aggregation.tests.AggregateAnnotationPruningTests.test_referenced_composed_subquery_requires_wrapping",
                "aggregation.tests.AggregateAnnotationPruningTests.test_referenced_subquery_requires_wrapping",
                "expressions.tests.BasicExpressionsTests.test_annotation_with_outerref",
                "expressions.tests.BasicExpressionsTests.test_case_in_filter_if_boolean_output_field",
                "expressions.tests.BasicExpressionsTests.test_subquery_filter_by_aggregate",
                "db_functions.datetime.test_extract_trunc.DateFunctionTests.test_trunc_subquery_with_parameters",
            },
            "The query cannot be executed. SingleStore does not support this type of query: \
nested scalar subselects in project list":
            {
                "aggregation.tests.AggregateTestCase.test_aggregation_nested_subquery_outerref",
                "queries.test_qs_combinators.QuerySetSetOperationTests.test_union_in_subquery",
                "queries.test_qs_combinators.QuerySetSetOperationTests.test_union_in_subquery_related_outerref",
            },
            "The query cannot be executed. SingleStore does not support this type of query: \
correlated subselect in ORDER BY":
            {
                "aggregation.tests.AggregateTestCase.test_aggregation_subquery_annotation_values_collision",
                "expressions.tests.BasicExpressionsTests.test_annotations_within_subquery",
                "expressions.tests.BasicExpressionsTests.test_order_by_exists",
                "ordering.tests.OrderingTests.test_orders_nulls_first_on_filtered_subquery",
            },
            "The query cannot be executed. SingleStore does not support this type of query: \
correlated subselect inside HAVING":
            {
                "aggregation.tests.AggregateTestCase.test_filter_in_subquery_or_aggregation",
                "annotations.tests.NonAggregateAnnotationTestCase.test_annotation_filter_with_subquery",
                "aggregation_regress.tests.AggregationTests.test_having_subquery_select",
            },
            "Feature 'Correlated subselect in the project list of a columnstore query with an ORDER BY, GROUP BY,\
or DISTINCT' is not supported by SingleStore":
            {
                "annotations.tests.NonAggregateAnnotationTestCase.test_annotation_exists_aggregate_values_chaining",
            },
            "Many-to-many intermediate tables (unless REFERENCE) in SingleStore must be built without id column, \
but certain django functionality requires id column to be present":
            {
                "queries.tests.ExcludeTests.test_exclude_subquery",
                "queries.tests.ExcludeTests.test_ticket14511",
                "fixtures.tests.CircularReferenceTests.test_circular_reference_natural_key",
                "fixtures.tests.CircularReferenceTests.test_circular_reference_natural_key",
                "fixtures.tests.FixtureLoadingTests.test_dumpdata_progressbar",
                "fixtures.tests.FixtureLoadingTests.test_dumpdata_with_excludes",
                "fixtures.tests.FixtureLoadingTests.test_dumpdata_with_file_bz2_output",
                "fixtures.tests.FixtureLoadingTests.test_dumpdata_with_file_gzip_output",
                "fixtures.tests.FixtureLoadingTests.test_dumpdata_with_file_xz_output",
                "fixtures.tests.FixtureLoadingTests.test_dumpdata_with_file_zip_output",
                "fixtures.tests.FixtureLoadingTests.test_dumpdata_with_file_lzma_output",
                "fixtures.tests.FixtureLoadingTests.test_dumpdata_with_file_output",
                "fixtures.tests.FixtureLoadingTests.test_dumpdata_with_filtering_manager",
                "fixtures.tests.FixtureLoadingTests.test_dumpdata_proxy_with_concrete",
                "fixtures.tests.FixtureLoadingTests.test_loading_and_dumping",
                "fixtures.tests.FixtureLoadingTests.test_output_formats",
                "fixtures.tests.ForwardReferenceTests.test_forward_reference_fk_natural_key",
                "fixtures.tests.ForwardReferenceTests.test_forward_reference_m2m_natural_key",
                "fixtures.tests.ForwardReferenceTests.test_forward_reference_fk",
                "fixtures.tests.ForwardReferenceTests.test_forward_reference_m2m",
                "fixtures.tests.CircularReferenceTests.test_circular_reference",
                "backends.base.test_creation.TestDeserializeDbFromString.test_circular_reference_with_natural_key",
                "backends.base.test_creation.TestDeserializeDbFromString.test_self_reference",
                "backends.base.test_creation.TestDeserializeDbFromString.test_serialize_db_to_string_base_manager",
            },
            "LIMIT with UNION affects only the second part of the union":
            {
                "queries.test_qs_combinators.QuerySetSetOperationTests.test_limits",
            },
            "%%s is not processed correctly in SingleStore":  # TODO: maybe we can fix this?
            {
                "queries.tests.Queries5Tests.test_extra_select_literal_percent_s",
            },
            "Leaf Error (127.0.0.1:3308): Subquery returns more than 1 row":
            {
                "annotations.tests.NonAggregateAnnotationTestCase.test_annotation_subquery_outerref_transform",
            },
            "ALTER TABLE which changes index `PRIMARY` is not supported on a columnstore table.":
            {
                "schema.tests.SchemaTests.test_add_auto_field",
            },
            # TODO: maybe we can run these tests on reference tables?
            "The unique key named: * cannot be created because unique keys must contain all columns of the shard key":
            {
                "schema.tests.SchemaTests.test_add_field_o2o_nullable",
                "schema.tests.SchemaTests.test_alter_field_o2o_keeps_unique",
                "schema.tests.SchemaTests.test_alter_field_o2o_to_fk",
                "schema.tests.SchemaTests.test_composed_constraint_with_fk",
                "schema.tests.SchemaTests.test_referenced_field_without_constraint_rename_inside_atomic_block",
                "schema.tests.SchemaTests.test_referenced_table_without_constraint_rename_inside_atomic_block",
                "schema.tests.SchemaTests.test_rename_referenced_field",
                "schema.tests.SchemaTests.test_unique_and_reverse_m2m",
                "schema.tests.SchemaTests.test_unique_together_with_fk",
                "schema.tests.SchemaTests.test_unique_together_with_fk_with_existing_index",
                "schema.tests.SchemaTests.test_alter_field_fk_to_o2o",
                "migrations.test_operations.OperationTests." + \
                "test_alter_field_reloads_state_on_fk_with_to_field_target_changes",
                "migrations.test_operations.OperationTests.test_alter_unique_together",   # Using \
                    # AlterUniqueTogether operation  # noqa: E131
                "migrations.test_operations.OperationTests.test_create_model_with_unique_after",   # Using \
                    # AlterUniqueTogether operation  # noqa: E131
            },
            "ALTER TABLE which drops shard index * on sharded table is not supported on a columnstore table.":
            {
                "schema.tests.SchemaTests.test_add_field_remove_field",
            },
            "ALTER TABLE which modifies column * by adding or dropping AUTO_INCREMENT is not supported on a \
columnstore table":
            {
                "schema.tests.SchemaTests.test_alter_auto_field_quoted_db_column",
                "schema.tests.SchemaTests.test_alter_smallint_pk_to_smallautofield_pk",
                "schema.tests.SchemaTests.test_char_field_pk_to_auto_field",
                "migrations.test_operations.OperationTests.test_alter_field_pk_mti_fk",
                "migrations.test_operations.OperationTests.test_alter_field_pk_mti_and_fk_to_base",
                "migrations.test_operations.OperationTests.test_smallfield_bigautofield_foreignfield_growth",
                "migrations.test_operations.OperationTests.test_smallfield_autofield_foreignfield_growth",
                "migrations.test_operations.OperationTests.test_autofield__bigautofield_foreignfield_growth",
            },
            "ALTER TABLE which modifies type of column * is not supported on a columnstore table":
            {
                "schema.tests.SchemaTests.test_alter_field_type_and_db_collation",
                "migrations.test_operations.OperationTests.test_alter_fk_non_fk",
                "migrations.test_operations.OperationTests.test_alter_field_with_index",
                "migrations.test_operations.OperationTests.test_alter_field_with_func_unique_constraint",
                "migrations.test_operations.OperationTests.test_alter_field_reloads_state_on_fk_target_changes",
                "migrations.test_operations.OperationTests.test_alter_field_pk_fk_char_to_int",
                "migrations.test_operations.OperationTests.test_alter_field_pk",
                "migrations.test_operations.OperationTests.test_rename_field_reloads_state_on_fk_target_changes",
                "migrations.test_executor.ExecutorTests.test_alter_id_type_with_fk",
                "migrations.test_operations.OperationTests.test_alter_field",
            },
            "Feature 'Reference Table without a Primary Key' is not supported by SingleStore Distributed":
            {
                "schema.tests.SchemaTests.test_alter_int_pk_to_int_unique",
                "schema.tests.SchemaTests.test_alter_not_unique_field_to_primary_key",
            },
            "ALTER TABLE which modifies column * from NULL to NOT NULL is not supported on a columnstore table.":
            {
                "schema.tests.SchemaTests.test_alter_null_to_not_null_keeping_default",
                "schema.tests.SchemaTests.test_alter_null_with_default_value_deferred_constraints",
            },
            "Feature 'CHANGE which changes the name of a REFERENCE table auto_increment column' is not supported \
by SingleStore":
            {
                "schema.tests.SchemaTests.test_autofield_to_o2o",
            },
            "A primary key cannot be added to a table after creation":
            {
                "schema.tests.SchemaTests.test_indexes",
            },
            # TODO: check if we can run these tests on reference tables using custom "through"
            "Feature 'multiple UNIQUE indexes with at least one index containing multiple columns on columnstore \
table' is not supported by SingleStore":
            {
                "schema.tests.SchemaTests.test_m2m",
                "schema.tests.SchemaTests.test_m2m_create",
                "schema.tests.SchemaTests.test_m2m_create_custom",
                "schema.tests.SchemaTests.test_m2m_create_inherited",
                "schema.tests.SchemaTests.test_m2m_custom",
                "schema.tests.SchemaTests.test_m2m_inherited",
                "schema.tests.SchemaTests.test_m2m_rename_field_in_target_model",
                "schema.tests.SchemaTests.test_m2m_repoint",
                "schema.tests.SchemaTests.test_m2m_repoint_custom",
                "schema.tests.SchemaTests.test_m2m_repoint_inherited",
                "schema.tests.SchemaTests.test_remove_unique_together_does_not_remove_meta_constraints",
                "migrations.test_operations.OperationTests.test_repoint_field_m2m",
                "migrations.test_operations.OperationTests.test_rename_model_with_self_referential_m2m",
                "migrations.test_operations.OperationTests." + \
                "test_rename_model_with_m2m_models_in_different_apps_with_same_name",
                "migrations.test_operations.OperationTests.test_rename_model_with_m2m",
                "migrations.test_operations.OperationTests.test_rename_model_with_db_table_rename_m2m",
                "migrations.test_operations.OperationTests.test_rename_m2m_target_model",
                "migrations.test_operations.OperationTests.test_alter_model_table_m2m_field",
                "migrations.test_operations.OperationTests.test_alter_model_table_m2m",
                "migrations.test_operations.OperationTests.test_alter_index_together_remove_with_unique_together",
                "migrations.test_operations.OperationTests.test_rename_m2m_model_after_rename_field",
                "migrations.test_operations.OperationTests.test_rename_field_unique_together",
                "migrations.test_operations.OperationTests.test_remove_field_m2m",
                "migrations.test_executor.ExecutorTests.test_detect_soft_applied_add_field_manytomanyfield",
                "migrations.test_operations.OperationTests.test_alter_field_m2m",
                "migrations.test_operations.OperationTests.test_add_field_m2m",
            },
            "Feature 'Multiple HASH indices on the same columns' is not supported by SingleStore":
            {
                "schema.tests.SchemaTests.test_remove_db_index_doesnt_remove_custom_indexes",
                "schema.tests.SchemaTests.test_remove_field_unique_does_not_remove_meta_constraints",
                "schema.tests.SchemaTests.test_remove_index_together_does_not_remove_meta_indexes",
                "migrations.test_operations.OperationTests.test_remove_unique_together_on_pk_field",
                "migrations.test_operations.OperationTests.test_remove_unique_together_on_unique_field",
            },
            "ALTER TABLE which adds unique/primary/foreign index * is not supported on a columnstore table":
            {
                "schema.tests.SchemaTests.test_unique_name_quoting",
            },
            "SingleStore does not support order in indexes":
            {
                "schema.tests.SchemaTests.test_order_index",
                "generic_relations_regress.tests.GenericRelationTests.test_ticket_20378",
            },
            "SingleStore does not support altering of the primary key":
            {
                "schema.tests.SchemaTests.test_primary_key",
            },
            "Feature 'select within values clause' is not supported by SingleStore":
            {
                "expressions.tests.BasicExpressionsTests.test_object_create_with_f_expression_in_subquery",
            },
            "SingleStore does not support operations on INTERVAL expression":
            {
                "expressions.tests.FTimeDeltaTests.test_durationfield_multiply_divide",
            },
            "SingleStore does not support years before 1000 in DATETIME fields":
            {
                "serializers.test_json.JsonSerializerTestCase.test_pre_1000ad_date",
                "serializers.test_jsonl.JsonlSerializerTestCase.test_pre_1000ad_date",
                "serializers.test_xml.XmlSerializerTestCase.test_pre_1000ad_date",
                "serializers.test_yaml.YamlSerializerTestCase.test_pre_1000ad_date",
            },
            "Serializer doesn't serialize non-auto fields, this is django code:\
            ```def handle_m2m_field(self, obj, field):\
                if field.remote_field.through._meta.auto_created:```\
            we changed some test models to have a through model, so m2m fields are not serialized":
            {
                "serializers.test_natural.NaturalKeySerializerTests.test_json_forward_references_m2m_errors",
                "serializers.test_natural.NaturalKeySerializerTests.test_yaml_forward_references_m2m_errors",
                "serializers.test_natural.NaturalKeySerializerTests.test_jsonl_forward_references_m2m_errors",
                "serializers.test_natural.NaturalKeySerializerTests.test_python_forward_references_m2m_errors",
                "serializers.test_natural.NaturalKeySerializerTests.test_xml_forward_references_m2m_errors",
                "serializers.test_json.JsonSerializerTestCase.test_deterministic_mapping_ordering",
                "serializers.test_jsonl.JsonlSerializerTestCase.test_deterministic_mapping_ordering",
                "serializers.test_xml.XmlSerializerTestCase.test_deterministic_mapping_ordering",
                "serializers.test_yaml.YamlSerializerTestCase.test_deterministic_mapping_ordering",
                "serializers.test_json.JsonSerializerTestCase.test_serialize_no_only_pk_with_natural_keys",
                "serializers.test_jsonl.JsonlSerializerTestCase.test_serialize_no_only_pk_with_natural_keys",
                "serializers.test_xml.XmlSerializerTestCase.test_serialize_no_only_pk_with_natural_keys",
                "serializers.test_yaml.YamlSerializerTestCase.test_serialize_no_only_pk_with_natural_keys",
                "serializers.test_json.JsonSerializerTestCase.test_serialize_only_pk",
                "serializers.test_jsonl.JsonlSerializerTestCase.test_serialize_only_pk",
                "serializers.test_xml.XmlSerializerTestCase.test_serialize_only_pk",
                "serializers.test_yaml.YamlSerializerTestCase.test_serialize_only_pk",
                "serializers.test_json.JsonSerializerTestCase.test_serialize_prefetch_related_m2m",
                "serializers.test_jsonl.JsonlSerializerTestCase.test_serialize_prefetch_related_m2m",
                "serializers.test_xml.XmlSerializerTestCase.test_serialize_prefetch_related_m2m",
                "serializers.test_yaml.YamlSerializerTestCase.test_serialize_prefetch_related_m2m",
                "serializers.test_natural.NaturalKeySerializerTests.test_json_forward_references_m2ms",
                "serializers.test_natural.NaturalKeySerializerTests.test_jsonl_forward_references_m2ms",
                "serializers.test_natural.NaturalKeySerializerTests.test_python_forward_references_m2ms",
                "serializers.test_natural.NaturalKeySerializerTests.test_xml_forward_references_m2ms",
                "serializers.test_natural.NaturalKeySerializerTests.test_yaml_forward_references_m2ms",
            },
            "The primary key defined explicitly in model causing the error of missing id field":
            {
                "get_or_create.tests.GetOrCreateTransactionTests.test_get_or_create_integrityerror",
                "get_or_create.tests.GetOrCreateThroughManyToMany.test_get_get_or_create",
                "get_or_create.tests.GetOrCreateThroughManyToMany.test_create_get_or_create",
            },
            "Feature 'ALTER TABLE...AUTO_INCREMENT=X for sharded tables' is not supported by SingleStore Distributed.":
            {
                "test_runner.tests.AutoIncrementResetTest.test_autoincrement_reset1",
                "test_runner.tests.AutoIncrementResetTest.test_autoincrement_reset2",
            },
            "SingleStore does not support datetime with timezones":
            {
                "admin_views.tests.AdminViewBasicTest.test_date_hierarchy_local_date_differ_from_utc",
                "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests." + \
                    "test_trunc_timezone_applied_before_truncation",  # noqa: E131
                "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_func_with_timezone",
                "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests." + \
                    "test_trunc_ambiguous_and_invalid_times",  # noqa: E131
                "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_none",
                "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests." + \
                    "test_extract_iso_year_func_boundaries",  # noqa: E131
                "db_functions.datetime.test_extract_trunc.DateFunctionTests.test_extract_iso_year_func_boundaries",
                "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests." + \
                    "test_extract_func_with_timezone",   # noqa: E131
            },
            "SingleStore doest not support the SHA224 hashing algorithm":
            {
                "db_functions.text.test_sha224.SHA224Tests.test_transform",
                "db_functions.text.test_sha224.SHA224Tests.test_basic",
            },
            "SingleStore CHAR() function does not support non-ASCII code points for CHR":
            {
                "db_functions.text.test_chr.ChrTests.test_non_ascii",
            },
            "SingleStore does not support datetime values before the year 1000":
            {
                "db_functions.datetime.test_extract_trunc.DateFunctionTests.test_trunc_week_before_1000",
                "db_functions.datetime.test_extract_trunc.DateFunctionTests.test_trunc_func",
            },
            "SingleStore does not support the COLLATE clause in the ORDER BY statement":
            {
                "db_functions.comparison.test_collate.CollateTests.test_collate_order_by_cs",
                "db_functions.comparison.test_collate.CollateTests.test_language_collation_order_by",
            },
            "SingleStore backend does not support iterators as arguments to executemany()":
            {
                "backends.tests.BackendTestCase.test_cursor_executemany_with_iterator",
                "backends.tests.BackendTestCase.test_cursor_executemany_with_pyformat_iterator",
            },
            "SingleStore does not support altering a Table comments":
            {
                "migrations.test_operations.OperationTests.test_remove_constraint",
            },
        }
        return skips

    @cached_property
    def django_test_expected_failures(self):
        fails = {
            # For test_regex_backreferencing to pass, SET GLOBAL regexp_format=advanced must be set
            "lookup.tests.LookupTests.test_regex_backreferencing",
            # AssertionError: 3 != 1 : 3 queries executed, 1 expected
            # Captured queries were: 1. BEGIN  2. Actual query  3. COMMIT
            # Instead of 1 and 3 we can have 5 and 7 or other numbers which differ by 2
            # Doesn't look like something is not working, maybe check later
            "order_with_respect_to.tests.OrderWithRespectToBaseTests.test_database_routing",
            "queries.test_bulk_update.BulkUpdateTests.test_database_routing",
            "queries.test_bulk_update.BulkUpdateNoteTests.test_simple",
            "queries.test_bulk_update.BulkUpdateNoteTests.test_multiple_fields",
            "queries.test_bulk_update.BulkUpdateNoteTests.test_foreign_keys_do_not_lookup",
            "queries.test_bulk_update.BulkUpdateNoteTests.test_batch_size",
            "model_inheritance.tests.ModelInheritanceDataTests.test_update_query_counts",
            "update_only_fields.tests.UpdateOnlyFieldsTests.test_num_queries_inheritance",
            "update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_fk_defer",
            "update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_inheritance",
            "update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_inheritance_defer",
            "contenttypes_tests.test_order_with_respect_to.OrderWithRespectToGFKTests.test_database_routing",
            "bulk_create.tests.BulkCreateTests.test_efficiency",
            "bulk_create.tests.BulkCreateTests.test_explicit_batch_size_respects_max_batch_size",
            "bulk_create.tests.BulkCreateTests.test_non_auto_increment_pk_efficiency",
            "generic_relations.tests.GenericRelationsTests.test_add_bulk_false",
            "basic.tests.ModelInstanceCreationTests.test_save_parent_primary_with_default",
            "bulk_create.tests.BulkCreateTests.test_explicit_batch_size_efficiency",
            "admin_views.tests.UserAdminTest.test_user_permission_performance",
            "admin_views.tests.GroupAdminTest.test_group_permission_performance",
            "auth_tests.test_management.CreatePermissionsMultipleDatabasesTests." + \
            "test_set_permissions_fk_to_using_parameter",
            "many_to_one_null.tests.ManyToOneNullTests.test_set_clear_non_bulk",
            "delete.tests.DeletionTests.test_cannot_defer_constraint_checks",
            "delete.tests.DeletionTests.test_large_delete",
            "delete.tests.DeletionTests.test_large_delete_related",
            "delete.tests.DeletionTests.test_only_referenced_fields_selected",
            "delete.tests.DeletionTests.test_proxied_model_duplicate_queries",
            "delete.tests.DeletionTests.test_bulk",
            "delete.tests.FastDeleteTests.test_fast_delete_aggregation",
            "delete.tests.FastDeleteTests.test_fast_delete_all",
            "delete.tests.FastDeleteTests.test_fast_delete_combined_relationships",
            "delete.tests.FastDeleteTests.test_fast_delete_empty_no_update_can_self_select",
            "delete.tests.FastDeleteTests.test_fast_delete_fk",
            "delete.tests.FastDeleteTests.test_fast_delete_full_match",
            "delete.tests.FastDeleteTests.test_fast_delete_inheritance",
            "delete.tests.FastDeleteTests.test_fast_delete_joined_qs",
            "delete.tests.FastDeleteTests.test_fast_delete_large_batch",
            "delete.tests.FastDeleteTests.test_fast_delete_m2m",
            "delete.tests.FastDeleteTests.test_fast_delete_qs",
            "delete.tests.FastDeleteTests.test_fast_delete_revm2m",
            # JSON_MATCH_ANY has different syntax so HasKeyLookup as_sql must be modified
            "queries.test_bulk_update.BulkUpdateTests.test_json_field",
            # other database for write is not respected during update TODO
            "queries.test_bulk_update.BulkUpdateTests.test_database_routing_batch_atomicity",
            # changing table comments is not supported
            "schema.tests.SchemaTests.test_db_comment_table",
            # delete from m2m through tables requires id TODO maybe override?
            "delete_regress.tests.DeleteCascadeTests.test_fk_to_m2m_through",
            # unsupported query is generated: DELETE FROM `delete_regress_login` WHERE
            # (`delete_regress_login`.`orgunit_id` IS NOT NULL AND COUNT(`delete_regress_login`.`description`) = 1
            # AND `delete_regress_login`.`id` = 1000026) -> ERROR 1111 (HY000): Invalid use of group function
            "delete_regress.tests.Ticket19102Tests.test_ticket_19102_annotate",
            # we issue two queries instead of one, and 2 additional queries: BEGIN and COMMIT
            "many_to_many.tests.ManyToManyTests.test_fast_add_ignore_conflicts",
            # TODO: PLAT-7420 after singlestoredb-python update these two should be fixed
            "expressions.tests.ExpressionsTests.test_patterns_escape",
            "expressions.tests.ExpressionsTests.test_insensitive_patterns_escape",
            # test performs lookup <json_fieldd> IN [json_1, ..., json_n]. For it to work, the user must explicitly
            # transform array elements to json field type. TODO: check if we can do this in the connector
            "model_fields.test_jsonfield.TestQuerying.test_key_in",
            # salted_hmac producing different results than expected
            "utils_tests.test_crypto.TestUtilsCryptoMisc.test_salted_hmac",
            # Auto increment fields must have BIGINT data type . default is BigAutoField
            "introspection.tests.IntrospectionTests.test_get_table_description_types",
            "introspection.tests.IntrospectionTests.test_smallautofield",
        }

        return fails

    @cached_property
    def ignores_table_name_case(self):
        return not self.connection.singlestore_server_data["table_name_case_sensitivity"]

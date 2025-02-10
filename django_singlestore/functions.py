from django.db.models.functions.comparison import JSONObject, TextField
from django.db.models.functions import Random, Cast
# from django.db.models.fields.json import HasKeyLookup


def random(self, compiler, connection, **extra_context):
    return self.as_sql(compiler, connection, template="RAND()", **extra_context)


def cast(self, compiler, connection, **extra_context):
    return self.as_sql(
        compiler,
        connection,
        template="(%(expressions)s) :> %(db_type)s",
        **extra_context,
    )


def json_object(self, compiler, connection, **extra_context):
    copy = self.copy()
    copy.set_source_expressions(
        [
            Cast(expression, TextField()) if index % 2 == 0 else expression
            for index, expression in enumerate(copy.get_source_expressions())
        ]
    )
    return super(JSONObject, copy).as_sql(
        compiler,
        connection,
        function="JSON_BUILD_OBJECT",
        **extra_context,
    )


# def json_key_lookup(self, compiler, connection):
#     return self.as_sql(
#         compiler, connection, template="JSON_MATCH_ANY(%s.%%s)"
#     )


def register_functions():
    Random.as_singlestore = random
    Cast.as_singlestore = cast
    JSONObject.as_singlestore = json_object
    # HasKeyLookup.as_singlestore = json_key_lookup

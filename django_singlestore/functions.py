from django.db.models.fields import TextField
from django.db.models.fields.json import HasKeyLookup, KeyTransform

from django.db.models.functions import Random, Cast, JSONObject, Repeat, RPad, Length


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


def json_extract(self, compiler, connection):
    lhs, params, key_transforms = self.preprocess_lhs(compiler, connection)

    all_params = []
    for key in key_transforms:
        lhs = f"JSON_EXTRACT_JSON({lhs}, %s)"
        all_params.append(key)

    return lhs, list(params) + all_params


def json_key_lookup(self, compiler, connection):
    return self.as_sql(
        compiler, connection, template="JSON_MATCH_ANY_EXISTS(%s, %%s)"
    )
    
def repeat(self, compiler, connection, **extra_context):
    expression, number = self.source_expressions
    length = None if number is None else Length(expression) * number
    rpad = RPad(expression, length, expression)
    return rpad.as_sql(compiler, connection, **extra_context)


def register_functions():
    Random.as_singlestore = random
    Cast.as_singlestore = cast
    JSONObject.as_singlestore = json_object
    HasKeyLookup.as_singlestore = json_key_lookup
    KeyTransform.as_singlestore = json_extract
    Repeat.as_singlestore = repeat

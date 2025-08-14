from django.db.models.expressions import Func
from django.db.models.fields import TextField
from django.db.models.fields.json import HasKeyLookup
from django.db.models.fields.json import JSONExact
from django.db.models.fields.json import JSONField
from django.db.models.fields.json import JSONIContains
from django.db.models.fields.json import KeyTextTransform
from django.db.models.fields.json import KeyTransform
from django.db.models.functions import Cast
from django.db.models.functions import JSONObject
from django.db.models.functions import Random
from django.db.models.functions import Repeat
from django.db.models.functions import RPad
from django.db.models.functions.datetime import Now
from django.db.models.functions.text import Chr
from django.db.models.functions.text import ConcatPair
from django.db.models.functions.text import Length
from django.db.models.functions.text import SHA256
from django.db.models.functions.text import SHA384
from django.db.models.functions.text import SHA512
from django.db.models.lookups import Transform


def random(self, compiler, connection, **extra_context):
    return self.as_sql(compiler, connection, template="RAND()", **extra_context)


def cast(self, compiler, connection, **extra_context):
    template = "(%(expressions)s) :> %(db_type)s"

    if getattr(self.output_field, "db_collation", None) is not None:
        template += f" COLLATE {self.output_field.db_collation}"

    return self.as_sql(
        compiler,
        connection,
        template=template,
        **extra_context,
    )


def repeat(self, compiler, connection, **extra_context):
    expression, number = self.source_expressions
    length = None if number is None else Length(expression) * number
    rpad = RPad(expression, length, expression)
    return rpad.as_sql(compiler, connection, **extra_context)


def json_object(self, compiler, connection, **extra_context):
    copy = self.copy()
    copy.set_source_expressions(
        [
            Cast(expression, TextField()) if index % 2 == 0 else expression
            for index, expression in enumerate(copy.get_source_expressions())
        ],
    )
    return super(JSONObject, copy).as_sql(
        compiler,
        connection,
        function="JSON_BUILD_OBJECT",
        **extra_context,
    )


def json_key_extract(self, compiler, connection):
    lhs, params, key_transforms = self.preprocess_lhs(compiler, connection)

    all_params = []
    for key in key_transforms:
        lhs = f"JSON_EXTRACT_JSON({lhs}, %s)"
        all_params.append(key)

    return lhs, list(params) + all_params


def json_key_lookup(self, compiler, connection, template=None):
    """
    We construct the SQL query to check if a JSON key exists in the JSON object.
    In SingleStore, we use the JSON_MATCH_ANY_EXISTS function:
    JSON_MATCH_ANY_EXISTS(json_object, key_1, key_2, ..., key_n)
    """
    # Process JSON path from the left-hand side.
    lhs_key_params = []
    if isinstance(self.lhs, KeyTransform):
        lhs, lhs_params, lhs_key_transforms = self.lhs.preprocess_lhs(
            compiler, connection,
        )
        for key in lhs_key_transforms:
            lhs_key_params.append(key)
    else:
        lhs, lhs_params = self.process_lhs(compiler, connection)

    # Process JSON path from the right-hand side.
    rhs = self.rhs
    rhs_key_params = []
    if not isinstance(rhs, (list, tuple)):
        rhs = [rhs]
    for key in rhs:
        if isinstance(key, KeyTransform):
            *_, rhs_key_transforms = key.preprocess_lhs(compiler, connection)
        else:
            rhs_key_transforms = [key]
        for k in rhs_key_transforms:
            rhs_key_params.append(k)

    if not self.logical_operator:
        sql = f"JSON_MATCH_ANY_EXISTS({lhs}, {','.join(['%s'] * (len(lhs_key_params) + len(rhs_key_params)))})"
        return sql, list(lhs_params) + list(lhs_key_params) + list(rhs_key_params)

    sql = f"JSON_MATCH_ANY_EXISTS({lhs}, {','.join(['%s'] * (len(lhs_key_params) + 1))})"
    sql = f"({self.logical_operator.join([sql] * len(rhs_key_params))})"
    all_params = list(lhs_params)
    for k in rhs_key_params:
        all_params.extend(lhs_key_params)
        all_params.append(k)
    return sql, all_params


class JSONExactSingleStore(JSONExact):
    def process_rhs(self, compiler, connection):
        rhs, rhs_params = super().process_rhs(compiler, connection)

        return f"({rhs}) :> JSON", rhs_params

    def as_singlestore(self, compiler, connection, **extra_context):
        return self.as_sql(compiler, connection, **extra_context)


class KeyTransformExactSingleStore(JSONExactSingleStore):
    def as_singlestore(self, compiler, connection, **extra_context):
        return self.as_sql(compiler, connection, **extra_context)


class JSONCaseInsensitiveMixinSingleStore:
    """
    Mixin to allow case-insensitive comparison of JSON values on SingleStore.
    SingleStore handles strings used in JSON context using the utf8mb4_bin collation.
    Because utf8mb4_bin is a binary collation, comparison of JSON values is
    case-sensitive.
    """
    def process_lhs(self, compiler, connection):
        lhs, lhs_params = super().process_lhs(compiler, connection)
        return f"LOWER(JSON_EXTRACT_STRING({lhs}))", lhs_params

    def process_rhs(self, compiler, connection):
        rhs, rhs_params = super().process_rhs(compiler, connection)
        return f"LOWER({rhs}) :> LONGTEXT", rhs_params


class JSONIContainsSingleStore(JSONCaseInsensitiveMixinSingleStore, JSONIContains):
    def as_singlestore(self, compiler, connection, **extra_context):
        return self.as_sql(compiler, connection, **extra_context)


def json_key_text_transform(self, compiler, connection):
    lhs, params, key_transforms = self.preprocess_lhs(compiler, connection)

    all_params = []
    for key in key_transforms:
        lhs = f"JSON_EXTRACT_JSON({lhs}, %s)"
        all_params.append(key)

    return f"JSON_EXTRACT_STRING({lhs})", list(params) + all_params


class SHASingleStore(Transform):
    def as_singlestore(self, compiler, connection, **extra_context):
        return self.as_sql(
            compiler,
            connection,
            template="SHA2(%%(expressions)s, %s)" % self.function[3:],
            **extra_context,
        )


class LengthSingleStore(Transform):
    def as_singlestore(self, compiler, connection, **extra_context):
        return Transform.as_sql(
            self, compiler, connection, function="CHARACTER_LENGTH", **extra_context,
        )


class NowSingleStore(Now):
    def as_singlestore(self, compiler, connection, **extra_context):
        return self.as_sql(
            compiler, connection, template="CURRENT_TIMESTAMP(6)", **extra_context,
        )


class ChrSingleStore(Transform):
    def as_singlestore(self, compiler, connection, **extra_context):
        return Transform.as_sql(self, compiler, connection, function="CHAR", **extra_context)


class ConcatPairSingleStore(Func):
    def as_singlestore(self, compiler, connection, **extra_context):
        # Use CONCAT_WS with an empty separator so that NULLs are ignored.
        return Func.as_sql(
            self,
            compiler,
            connection,
            function="CONCAT_WS",
            template="%(function)s('', %(expressions)s)",
            **extra_context,
        )


def register_functions():
    Random.as_singlestore = random
    Cast.as_singlestore = cast
    Repeat.as_singlestore = repeat

    JSONObject.as_singlestore = json_object
    HasKeyLookup.as_singlestore = json_key_lookup
    KeyTransform.as_singlestore = json_key_extract
    KeyTextTransform.as_singlestore = json_key_text_transform
    SHA256.as_singlestore = SHASingleStore.as_singlestore
    SHA512.as_singlestore = SHASingleStore.as_singlestore
    SHA384.as_singlestore = SHASingleStore.as_singlestore
    Length.as_singlestore = LengthSingleStore.as_singlestore
    Now.as_singlestore = NowSingleStore.as_singlestore
    Chr.as_singlestore = ChrSingleStore.as_singlestore
    ConcatPair.as_singlestore = ConcatPairSingleStore.as_singlestore

    KeyTransform.register_lookup(KeyTransformExactSingleStore)

    JSONField.register_lookup(JSONExactSingleStore)
    JSONField.register_lookup(JSONIContainsSingleStore)

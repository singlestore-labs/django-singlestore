from django.db.backends.base.validation import BaseDatabaseValidation


class DatabaseValidation(BaseDatabaseValidation):
    def check(self, **kwargs):
        issues = super().check(**kwargs)
        issues.extend(self._check_sql_mode(**kwargs))
        return issues

    def _check_sql_mode(self, **kwargs):
        # STRICT_ALL_TABLES is always enabled in SingleStore
        return []

    def check_field_type(self, field, field_type):
        errors = []

        return errors

"""
This script transforms a Django model with a ManyToManyField into an intermediary model
with a ManyToManyField that uses a through model. It also generates the SQL query
for creating the intermediary table.

NOTE: This script assumes the original code is well-formed and follows Django's conventions.
NOTE: The script does not handle all edge cases and is meant to create a skeleton for the actual code.

To use this script, modify the `original_code` variable with your Django model code and run the script.
"""
import re


def generate_intermediary_code(original_code):
    # Extract class name and many-to-many field definition
    class_match = re.search(r'class (\w+)\((?:models\.Model|[\w\.]+)\):', original_code)
    m2m_match = re.search(r'(\w+)\s*=\s*models\.ManyToManyField\(\s*"?(self|\w+)"?\s*(.*)\)', original_code)

    if not class_match or not m2m_match:
        return "Invalid original code format"

    class_name = class_match.group(1)
    field_name = m2m_match.group(1)
    related_model = m2m_match.group(2)
    additional_args = m2m_match.group(3).strip()

    # Handle self-referencing models
    if related_model == "self":
        related_model = class_name
        intermediary_model_name = f"{class_name}Friend"
        from_field_name = f"from_{class_name.lower()}"
        to_field_name = f"to_{class_name.lower()}"
    else:
        intermediary_model_name = f"{class_name}{related_model}"
        from_field_name = class_name.lower()
        to_field_name = related_model.lower()

    # Properly format the new code with a ManyToManyField that uses through
    additional_args_str = f", {additional_args}" if additional_args else ""
    through_str = f'through="{intermediary_model_name}"'
    new_code = re.sub(
        r'(\s*' + field_name + r'\s*=\s*models\.ManyToManyField\([^\)]*\))',
        rf'\n    {field_name} = models.ManyToManyField("{related_model}"{additional_args_str}, {through_str})',
        original_code,
    ).replace(",,", ",").replace(", ,", ",")  # This will clean up any double commas

    intermediary_code = f"""

class {intermediary_model_name}(models.Model):
    {from_field_name} = models.ForeignKey({class_name}, on_delete=models.CASCADE)
    {to_field_name} = models.ForeignKey({related_model}, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('{from_field_name}', '{to_field_name}'),)
        db_table = "{class_name.lower()}_{related_model.lower()}"
"""

    # Generate the SQL query for creating the intermediary table
    sql_query = f"""
CREATE TABLE `{class_name.lower()}_{related_model.lower()}` (
  `{from_field_name}_id` BIGINT NOT NULL,
  `{to_field_name}_id` BIGINT NOT NULL,
  SHARD KEY (`{from_field_name}_id`),
  UNIQUE KEY (`{from_field_name}_id`, `{to_field_name}_id`),
  KEY (`{from_field_name}_id`),
  KEY (`{to_field_name}_id`)
);
"""

    return new_code + intermediary_code + "\nSQL Query:\n" + sql_query


original_code = """
class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, related_name="books")
    publisher = models.ForeignKey(
        Publisher,
        models.CASCADE,
        related_name="books",
        db_column="publisher_id_column",
    )
    updated = models.DateTimeField(auto_now=True)
"""

new_code = generate_intermediary_code(original_code)
print(new_code)

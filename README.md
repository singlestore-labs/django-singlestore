# SingleStore backend for Django

**Attention**: The code in this repository is intended for experimental use only and is not yet fully tested, documented, or supported by SingleStore. Visit the [SingleStore Forums](https://www.singlestore.com/forum/) to ask questions about this repository.

The current version of `django-singlestore` is being tested with Django 4.2.

## Installation

Install from source: `pip install git+https://github.com/singlestore-labs/django-singlestore`.

## Usage

To use your SingleStore database your Django app, configure the settings as described below:

```
DATABASES = {
    "default": {
        "ENGINE": "django_singlestore",
        "HOST": "<your database server address>",
        "PORT": 3306,
        "USER": "<your database user>",
        "PASSWORD": "<your database user's password>",
        "NAME": "<database name>",
    },
}

# SingleStore does not support datetime with timezones
USE_TZ = False

# Auto increment fields must have BIGINT data type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

Django provides a [tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/) to get started.

## Features and Limitations

There is a number of limitations when using SingleStore with Django, notably the lack of Foreign Keys on the database level. In addition, a unique key on distributed table must be a superset of the shard key. To learn more about the indexes in SingleStore, visit the [docs](https://docs.singlestore.com/cloud/create-a-database/understanding-keys-and-indexes-in-singlestore/) or [troubleshooting guide](https://docs.singlestore.com/cloud/reference/troubleshooting-reference/query-errors/why-do-i-get-errors-about-unique-keys/).

SingleStore supports 4 different storage types for tables: COLUMNSTORE (default on most servers), ROWSTORE, REFERENCE, ROWSTORE REFERENCE.

#### Major limitations
- SingleStore does not enforce FOREIGN KEY constraints. The application must ensure referential integrity itself.
- SingleStore does not support UNIQUE constraints on non-shard key columns in distributed tables. In particular, this means many-to-many intermediate tables (unless REFERENCE) in SingleStore must be built without id column, as they must have a unique constraint on `(column_from, column_to)`.

To overcome the limitation on UNIQUE constraint, `django-singlestore` provides the following mechanisms.
1. Use custom table storage type in django models. There are two ways to configure it:
- Per application. Set `DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_<APP_NAME>` to one of the values: `"ROWSTORE"`, `"REFERENCE"`, `"ROWSTORE REFERENCE"`. For default django apps (where we can't modify models definitions easily) we set
    ```bash
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN="ROWSTORE REFERENCE"
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH="ROWSTORE REFERENCE"
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_CONTENTTYPES="ROWSTORE REFERENCE"
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_SITES="ROWSTORE REFERENCE"
    ```
- Per model. Example:
    ```python
    from django_singlestore.schema import ModelStorageManager

    class Food(models.Model):
        name = models.CharField(max_length=20, unique=True)

        objects = ModelStorageManager(table_storage_type="REFERENCE")

        def __str__(self):
            return self.name
    ```
2. Do not materialize `unique` constraints defined in a model if environment variable `DJANGO_SINGLESTORE_NOT_ENFORCED_UNIQUE` is set. This variable is intended to be used in testing only, as it obfuscates the lack of the unique constraint in the database from an application developer.

To overcome the limitation on unique constraints for many-to-many relationships, the following mechanism can be used: explicitly define an intermediary model (`through`) and use a custom DDL query to create it. Example:
```python
class Paragraph(models.Model):
text = models.TextField()
page = models.ManyToManyField("Page", through="ParagraphPage")


class ParagraphPage(models.Model):
    paragraph = models.ForeignKey(Paragraph)
    page = models.ForeignKey("Page")

    class Meta:
        unique_together = (('paragraph', 'page'),)
        db_table = "queries_paragraph_page"
```

Table DDL:
```sql
CREATE TABLE `queries_paragraph_page` (
  `paragraph_id` BIGINT NOT NULL,
  `page_id` BIGINT NOT NULL,
  SHARD KEY (`paragraph_id`),
  UNIQUE KEY (`paragraph_id`, `page_id`),
  KEY (`paragraph_id`),
  KEY (`page_id`)
);
```
Note that the `through` table does not have a primary key column, so some django features may not work.

#### Minor limitations
- ALTER TABLE which modifies type of column is not supported on a columnstore table. A new column must be created, populated with data, and then dropped.
- Certain query shapes are not supported, see the `django_test_skips` in `features.py` for the full list of the issues encountered in django tests.
- SingleStore does not support FLOAT/DOUBLE primary keys on ColumnStore tables.
- ALTER TABLE which changes index `PRIMARY` is not supported on a columnstore table.
- ALTER TABLE which drops shard index on sharded table is not supported on a columnstore table.
- ALTER TABLE which modifies column by adding or dropping AUTO_INCREMENT is not supported on a columnstore table.
- Feature 'Reference Table without a Primary Key' is not supported by SingleStore Distributed.
- ALTER TABLE which modifies column from NULL to NOT NULL is not supported on a columnstore table.
- A primary key cannot be added to a table after creation.
- Feature 'multiple UNIQUE indexes with at least one index containing multiple columns on columnstore table' is not supported by SingleStore.
- Feature 'Multiple HASH indices on the same columns' is not supported by SingleStore.
- ALTER TABLE which adds unique/primary/foreign index is not supported on a columnstore table.
- SingleStore does not support altering of the primary key.
- Changing table comments is not supported.

## Resources

* [Sign up](https://www.singlestore.com/cloud-trial/) for the SingleStore Free Shared Tier
* [Documentation](https://docs.singlestore.com)
* [Twitter](https://twitter.com/SingleStoreDevs)
* [SingleStore Forums](https://www.singlestore.com/forum)

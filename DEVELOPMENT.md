
## Running tests

1. Clone django sources, let's call its location `DJANGO_HOME`.
2. Install dependencies
    ```
    cd $DJANGO_HOME/tests
    python -m pip install -e ..
    python -m pip install -r requirements/py3.txt
    python -m pip install <PATH_TO>/django-singlestore
    ```
3. Place the file `singlestore_settings.py` in `$DJANGO_HOME/tests` and configure connection credentials:

    ```
    # A settings file is just a Python module with module-level variables.
    DJANGO_SETTINGS_MODULE = 'singlestore_settings'

    DATABASES = {
        "default": {
            "ENGINE": "django_singlestore",
            "HOST": "127.0.0.1",
            "PORT": 3306,
            "USER": "root",
            "PASSWORD": "p",
            "NAME": "django_db",
        },
        "other": {
            "ENGINE": "django_singlestore",
            "HOST": "127.0.0.1",
            "PORT": 3306,
            "USER": "root",
            "PASSWORD": "p",
            "NAME": "django_db_other",
        },
    }

    USE_TZ = False

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
    ```

4. Set the environemnt variables to create the needed tables:
    ```
    export PYTHONPATH=$DJANGO_HOME:$DJANGO_HOME/tests:$PYTHONPATH

    # export DJANGO_SINGLESTORE_NOT_ENFORCED_UNIQUE=1

    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN="ROWSTORE REFERENCE"
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH="ROWSTORE REFERENCE"
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_CONTENTTYPES="ROWSTORE REFERENCE"
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_SITES="ROWSTORE REFERENCE"

    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN_INLINES="ROWSTORE REFERENCE"
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH_TESTS="REFERENCE"
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_LOOKUP="REFERENCE"
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_INTROSPECTION="ROWSTORE REFERENCE"
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_VALIDATION="ROWSTORE REFERENCE"
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_CONSTRAINTS="ROWSTORE REFERENCE"
    export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_BULK_CREATE="ROWSTORE REFERENCE"
    ```

5. Run all tests:
    ```
    ./runtests.py --settings=singlestore_settings --noinput -v 3
    ```

### Initial results

```
FAILED: 1181
OK: 502
```

After turning off transactions:
FAILED: 300
OK: 1046
SKIPPED: 537


### Notes
TODO: move this to README
- the size of the list for `bulk_update` must be not greater than 900 if default `thread_stack` engine variable is used 
- Explicit `ORDER BY` is needed to retrieve results in deterministic order, no implicit order by id in SingleStore
- Alter field has a number of constraints - TODO: describe them in detail

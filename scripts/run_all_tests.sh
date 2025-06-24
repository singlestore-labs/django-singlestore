# NOTE: this script is outdated, so it needs to updated before running
export DJANGO_HOME=`pwd`

export PYTHONPATH=$DJANGO_HOME:$DJANGO_HOME/tests:$DJANGO_HOME/tests/singlestore_settings:$PYTHONPATH

# uncomment this to run tests without unique constraints on the data base level
# export NOT_ENFORCED_UNIQUE=1

# these are default django apps, we use ROWSTORE REFERENCE tabkes for them
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN="ROWSTORE REFERENCE"
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH="ROWSTORE REFERENCE"
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_CONTENTTYPES="ROWSTORE REFERENCE"
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_SITES="ROWSTORE REFERENCE"

# the block below is here to quickly run all tests; eventually it should be removed
# and replaced with a more fine-grained approach
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN_INLINES="ROWSTORE REFERENCE"
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH_TESTS="REFERENCE"
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_INTROSPECTION="ROWSTORE REFERENCE"
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_VALIDATION="ROWSTORE REFERENCE"
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_CONSTRAINTS="ROWSTORE REFERENCE"
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_BULK_CREATE="ROWSTORE REFERENCE"

# 12 many-to-many fields, just use reference tables to save time
export TABLE_STORAGE_TYPE_PREFETCH_RELATED="ROWSTORE REFERENCE"

# abstract models - specifying through is tricky
export TABLE_STORAGE_TYPE_MANY_TO_MANY="ROWSTORE REFERENCE"

prepare_settings() {
    for dir in $(find tests -maxdepth 1 -type d | awk -F '/' '{print $2}'); do
        # echo $dir
        sed -e "s|TEST_MODULE|$dir|g" tests/singlestore_settings_TMPL > tests/singlestore_settings/singlestore_settings_$dir.py
    done
}
prepare_settings
python run_tests_parallel.py

export DJANGO_HOME=`pwd`

export PYTHONPATH=$DJANGO_HOME:$DJANGO_HOME/tests:$DJANGO_HOME/tests/singlestore_settings:$PYTHONPATH

# these are the default django apps, we use ROWSTORE REFERENCE tables for them
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN="ROWSTORE REFERENCE"
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH="ROWSTORE REFERENCE"
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_CONTENTTYPES="ROWSTORE REFERENCE"
export  DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_SITES="ROWSTORE REFERENCE"

# 12 many-to-many fields, just use reference tables to save time
export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_PREFETCH_RELATED="ROWSTORE REFERENCE"

# a lot of many-to-many fields to self
export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_M2M_RECURSIVE="ROWSTORE REFERENCE"

# lot of many to many fields
export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN_VIEWS="ROWSTORE REFERENCE"

# lot of unique keys and many to many fields
export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_FOREIGN_OBJECT="ROWSTORE REFERENCE"

# lot of unique keys
export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH_TESTS="ROWSTORE REFERENCE"

# abstract models - specifying through is tricky 
export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_MANY_TO_MANY="ROWSTORE REFERENCE"

# a number of models with unique keys, 13 many-to-many fields
export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_FIXTURES_REGRESS="ROWSTORE REFERENCE"

# a model with 3 many-to-many fields caused issues
export DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_DELETE="ROWSTORE REFERENCE"


# queries app has a lot of models with OneToOne relationships
export DJANGO_SINGLESTORE_NOT_ENFORCED_UNIQUE_QUERIES=1


# # specify the path to the test to run
# MODULE_TO_TEST=""
# ./tests/runtests.py --settings=singlestore_settings --noinput -v 3 $MODULE_TO_TEST --keepdb

# Release flow

This document describes how to cut a new release of `django-singlestore`.

## Versioning

A connector for Django `MAJOR.MINOR.PATCH` should have a package version of `MAJOR.MINOR.*` (for example, Django 4.2.x maps to `django-singlestore` 4.2.x). Releases for that Django version are cut from the stable branch `stable/singlestore-django-MAJOR.MINOR.x` (for example, `stable/singlestore-django-4.2.x`).

## Steps

### 1. Update the package version

Set `__version__` in `django_singlestore/__init__.py` to the new release version:

```python
__version__ = "MAJOR.MINOR.PATCH"
```

### 2. Update dependencies

Update `install_requires` in `setup.cfg` as needed for the target Django release (for example, `django>=4.2`).

### 3. Commit on the stable branch

Make these changes on the appropriate stable branch:

```
stable/singlestore-django-MAJOR.MINOR.x
```

For example, releases for Django 4.2 use `stable/singlestore-django-4.2.x`.

### 4. Push a release tag

Push a tag with the desired version on that branch, prefixed with `v`:

```
vMAJOR.MINOR.PATCH
```

For example:

```bash
git tag v4.2.0
git push origin v4.2.0
```

### 5. Let CI publish the release

Pushing a `v*` tag triggers the [Release django-singlestore](.github/workflows/publish.yml) GitHub Action, which:

1. Runs the full test suite.
2. Builds the package.
3. Publishes to PyPI.
4. Creates a draft GitHub Release for the tag.

### 6. Verify the release on PyPI

Manually confirm that the expected version is available on PyPI:

https://pypi.org/project/django-singlestore/

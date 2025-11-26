import re


def check_version_ge(connection, min_version):
    """
    Check if SingleStore version is greater than or equal to the minimum version.

    Args:
        connection: Django database connection
        min_version: String version like "8.7", "8.9.0", "9.0"

    Returns:
        bool: True if current version >= min_version, False otherwise
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT @@memsql_version")
            version_string = cursor.fetchone()[0]

        # Extract version number from string like "8.5.32" or "memsql-8.7.10"
        match = re.search(r'(\d+)\.(\d+)(?:\.(\d+))?', version_string)
        if not match:
            return False

        current_major = int(match.group(1))
        current_minor = int(match.group(2))
        current_patch = int(match.group(3) or 0)

        # Parse minimum version
        min_parts = min_version.split('.')
        min_major = int(min_parts[0])
        min_minor = int(min_parts[1]) if len(min_parts) > 1 else 0
        min_patch = int(min_parts[2]) if len(min_parts) > 2 else 0

        # Compare versions
        current = (current_major, current_minor, current_patch)
        minimum = (min_major, min_minor, min_patch)
        print("here")
        print(current, minimum)

        return current >= minimum

    except Exception:
        # If we can't determine version, assume it's old
        return False

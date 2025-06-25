import sys
import subprocess

def setup_group(group_id):
    print(f"Setting up for group {group_id}")
    sql_file = "testrepo/tests/_utils/setup.sql"
    mysql_cmd = [
        "mysql",
        "-h", "127.0.0.1",
        "-P", "3307",
        "-u", "root",
        "-proot",
        "-e", f"source {sql_file}"
    ]
    try:
        subprocess.run(mysql_cmd, check=True)
        print("SQL setup script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute SQL setup script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup_group.py <group_id>")
        sys.exit(1)

    group_id = int(sys.argv[1])
    setup_group(group_id)

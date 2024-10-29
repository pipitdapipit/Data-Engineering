import os
import time
import subprocess
from collections import defaultdict

def find_dependencies(file_sql):
    """Finds the dependencies of an SQL file."""
    dependencies = defaultdict(list)
    with open(file_sql, 'r') as f:
        for line in f:
            if line.startswith('-- depends on:'):
                dependency = line.split(':')[1].strip()
                dependencies.append(dependency)
    return dependencies

def run_sql_file(file_sql):
    """Runs an SQL file using subprocess."""
    subprocess.run(['sqlcmd', '-S', 'your_server', '-U', 'your_username', '-P', 'your_password', '-i', file_sql])
    time.sleep(2)  # Simulate execution

def execute_sql_files(file_sql, dependencies):
    """Executes SQL files in the correct order using DFS."""
    visited = set()
    stack = []

    def dfs(file_sql):
        if file_sql not in visited:
            visited.add(file_sql)
            for dep in dependencies[file_sql]:
                dfs(dep)
            stack.append(file_sql)

    for fileSQL in file_sql:
        dfs(file_sql)

    while stack:
        sql_file = stack.pop()
        print(f"Running: {file_sql}")
        run_sql_file(file_sql)

def main():
    fileSQL = []
    dependencies = {}

    for root, files in os.walk('sql'):
        for file in files:
            if file.endswith('.sql'):
                file_sql = os.path.join(root, file)
                fileSQL.append(file_sql)
                dependencies[file_sql] = find_dependencies(file_sql)

    execute_sql_files(fileSQL, dependencies)

if __name__ == '__main__':
    main()

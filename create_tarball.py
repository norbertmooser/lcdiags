import os
import tarfile
from datetime import datetime

# Directory containing .py files
directory = '.'

# List of .py files in the directory
py_files = [filename for filename in os.listdir(directory) if filename.endswith('.py')]

# Current time
current_time = datetime.now().strftime("%y%m%d%H%M")

# Name of the tarball
tarball_name = f"{current_time}_lcdiags.tar.gz"

# Create tarball
with tarfile.open(tarball_name, 'w:gz') as tar:
    for py_file in py_files:
        file_path = os.path.join(directory, py_file)
        tar.add(file_path, arcname=os.path.basename(file_path))

print(f"Tarball '{tarball_name}' created successfully with {len(py_files)} .py files.")

import os

from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        if os.path.commonpath([working_directory_abs, target_file]) != working_directory_abs:
            raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file):
            raise Exception(f'File not found or is not a regular file: "{file_path}"')
        with open(target_file, 'r') as f:
            content = f.read(MAX_CHARS)  # Read up to MAX_CHARS characters
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += (f'[...File "{file_path}" truncated at {MAX_CHARS} characters]')
        return content
    except Exception as e:
        return f"Error: {e}"
import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        if not os.path.isdir(directory):
            raise Exception(f'"{directory}" is not a directory')
        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
        if os.path.commonpath([working_directory_abs, target_dir]) != working_directory_abs:
            raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory')
        return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f"Error: {e}"


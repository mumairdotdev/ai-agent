import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            raise Exception(f'Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(abs_file_path):
            raise Exception(f'"{file_path}" does not exist or is not a regular file')
        if not abs_file_path.endswith(".py"):
            raise Exception(f'"{file_path}" is not a Python file')
        command = ["python", abs_file_path]
        if args:
            command.extend(args)
        complete_process = subprocess.run(
            command, 
            cwd=abs_working_dir, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        output_string = ""
        if complete_process.returncode != 0:
            output_string += f"Process exited with code {complete_process.returncode}"
        if not complete_process.stdout and not complete_process.stderr:
            output_string += f"\nNo output produced"
        output_string += f"\nSTDOUT: {complete_process.stdout}" if complete_process.stdout else "\nNo output produced"
        output_string += f"\nSTDERR: {complete_process.stderr}" if complete_process.stderr else "\nNo output produced"
        return output_string
    except Exception as e:
        return f"Error: {e}"
    
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes or run a Python file in a specified working directory and returns the output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}
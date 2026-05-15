import os
import re
import subprocess


def list_files(path, extensions=None):
    result = []

    SKIP = ['node_modules', '.git', '__pycache__', '.venv', 'dist', 'build']
    
    for dirpath, dirnames, filenames in os.walk(path):
        
        dirnames[:] = [d for d in dirnames if d not in SKIP] 

        for filename in filenames:
            if extensions is None or any(filename.endswith(ext) for ext in extensions):
                full_path = os.path.join(dirpath, filename)
                result.append(full_path)

    return result


def read_file(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return "ERROR : No file found"
    except UnicodeDecodeError:
        return "ERROR : Binary file, skipping"


    numbered = ''
    for i, line in enumerate(lines, start=1):
        if i >= 500:
            numbered += '...truncating at 500 lines'
            break
        numbered += f'{i}: {line}'

    return numbered

def search_pattern(pattern, path, extensions=None):
    files = list_files(path, extensions)
    results = []

    for file in files:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            continue
        
        for i, line in enumerate(lines, start=1):
            try:
                if re.search(pattern, line):
                    results.append({'file':file, 'line': i, 'content':line.strip()})
            except re.error:
                return 'ERROR L invalid regex pattern'

    if len(results) == 0:
        return 'No matches found'
    else: 
        return results

def run_file(file_path):
    if not file_path.endswith('.py'):
        return 'ERROR: Only Python files supported'
    
    if not os.path.exists(file_path):
        return 'ERROR : File not found'
    
    try:
        result = subprocess.run(['python3', file_path], capture_output=True, text=True, timeout=10)

        return {
            'stdout':result.stdout,
            'stderr':result.stderr,
            'exit_code':result.returncode
        }
    except subprocess.TimeoutExpired:
        return 'ERROR : Execution time out'
    
def run_tests(file_path):
    if not os.path.exists(file_path):
        return 'ERROR : Path not found'
    
    try:
        result = subprocess.run(["pytest", file_path, "--tb=short", "-q"], capture_output=True, text=True, timeout=30)
        return result.stdout + result.stderr
    except FileNotFoundError:
        test_files = list_files(file_path, extensions=['.py'])
        test_files = [f for f in test_files if os.path.basename(f).startswith('test_')]

        if test_files:
            outputs = []
            for f in test_files:
                try:
                    result = subprocess.run(['python3', f], capture_output=True, text=True, timeout=30)
                    outputs.append(result.stdout + result.stderr)
                except subprocess.TimeoutExpired:
                    return 'ERROR : Tests timed out'
                
            return '\n'.join(outputs)
        else:
            return 'No test framework detected'


def dispatch_tool(name, inputs):
    if name == "list_files":
        return list_files(**inputs)
    elif name == "read_file":
        return read_file(**inputs)
    elif name == "search_pattern":
        return search_pattern(**inputs)
    elif name == "run_file":
        return run_file(**inputs)
    elif name == "run_tests":
        return run_tests(**inputs)
    else:
        return f"Error: unknown tool '{name}'"

        
TOOLS = [
    {
        "name": "list_files",
        "description": "Lists all files in a directory recursively. Use this first to understand the repo structure before reading any files.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The directory path to list files from"
                },
                "extensions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of file extensions to filter by e.g. ['.py', '.js']. If omitted returns all files."
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "read_file",
        "description": "Reads a file and returns its contents with line numbers. Use to inspect specific files after identifying them with list_files.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The full path to the file to read"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "search_pattern",
        "description": "Searches for a regex pattern across all files in a directory. Use to find specific functions, variables, or suspicious patterns across the whole codebase.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Regex pattern to search for"
                },
                "path": {
                    "type": "string",
                    "description": "Directory to search in"
                },
                "extensions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional file extension filter"
                }
            },
            "required": ["pattern", "path"]
        }
    },
    {
        "name": "run_file",
        "description": "Executes a Python file and returns stdout, stderr, and exit code. Use to verify if code actually runs without errors.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "run_tests",
        "description": "Runs the test suite for a project using pytest. Use to check if existing tests pass before and after reviewing changes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the project root to run tests from"
                }
            },
            "required": ["file_path"]
        }
    }
]
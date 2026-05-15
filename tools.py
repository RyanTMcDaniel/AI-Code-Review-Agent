import os


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


        
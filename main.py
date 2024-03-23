import os
import sys

def merge_text_files(directory, extension):
    # Initialize variables to store total number of lines and merged content
    total_lines = 0
    merged_content = []

    excluded_dirs = ['__pycache__', 'env', 'env1', '.env', 'build', 'dist', 'node_modules', 'venv', '.git']

    file_map = []
    # Iterate through each directory and subdirectory
    for root, dirs, files in os.walk(directory, topdown=True):
        if root != directory:
            level = root[len(directory) + len(os.path.sep):].count(os.path.sep)
            if level >= 2:
                continue  # Skip directories more than two levels down

        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        # Get list of files with specified extension in the current directory
        for file_name in files:
            if file_name.endswith(extension):
                file_path = os.path.join(root, file_name)
                # Read the content of the file
                with open(file_path, 'r', encoding='utf') as file:
                    content = file.readlines()
                    file_map.append([file_path, len(content)])

                # Add file name and number of lines to merged content
                merged_content.append(f"# {file_path} {len(content)}\n\n")
                # Increment total number of lines
                total_lines += len(content)
                # Add content of the file to merged content
                merged_content.extend(content)
                # Add an extra empty line between files
                merged_content.append('\n')

    # Create the merged file
    with open('merged_file.txt', 'w') as merged_file:
        # Write total number of files
        merged_file.write(f"# Total number of lines: {total_lines}\n")
        # Write file name and number of lines for each file

        file_map.sort(key=lambda x: x[1], reverse=True)
        for line in file_map:
            merged_file.write(f"# {line[0]}: {line[1]}\n")
        # Write an empty line after file metadata
        merged_file.write('\n')

        # Write merged content
        merged_file.writelines(merged_content)

    print("Merged file created: merged_file.txt")
if __name__ == "__main__":
    # Check if correct number of command line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python merge_text_files.py <directory> <extension>")
        sys.exit(1)

    directory = sys.argv[1]
    extension = sys.argv[2]

    # Check if specified directory exists
    if not os.path.isdir(directory):
        print("Directory not found.")
        sys.exit(1)

    merge_text_files(directory, extension)

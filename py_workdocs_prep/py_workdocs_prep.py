import os

directories_to_delete_if_found = [
    '.git',
    'venv*',
    'node_modules'
]

# Print every file with its size recursing through dirs
def recurse_dir(root_dir):
    root_dir = os.path.abspath(root_dir)
    for item in os.listdir(root_dir):
        item_full_path = os.path.join(root_dir, item)

        if os.path.isdir(item_full_path):
            recurse_dir(item_full_path)
        else:
            print("%s - %s bytes" % (item_full_path, os.stat(item_full_path).st_size))

if __name__ == "__main__":
    #recurse_dir("")
    print('Starting')
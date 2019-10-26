import os

directories_to_delete_if_found = [
    '.git',
    'venv*',
    'node_modules'
]


def recurse_dir(root_dir):
    '''
    Note: Initial pattern from https://www.devdungeon.com/content/walk-directory-python was adopted in the final product.
    '''
    root_dir = os.path.abspath(root_dir)
    for item in os.listdir(root_dir):
        item_full_path = os.path.join(root_dir, item)

        if os.path.isdir(item_full_path):
            recurse_dir(item_full_path)
        else:
            print("%s - %s bytes" % (item_full_path, os.stat(item_full_path).st_size))


def start(start=os.getcwd()):
    print('Starting in "{}"'.format(start))
    recurse_dir(root_dir=start)

if __name__ == "__main__":
    start(start=os.getcwd())

# EOF

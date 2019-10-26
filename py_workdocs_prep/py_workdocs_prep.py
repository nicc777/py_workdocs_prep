import os

directories_to_delete_if_found = [
    '.git',
    'venv*',
    'node_modules'
]

ignore_names_exact = [
    'Microsoft User Data',
    'Outlook files',
    'Thumbs.db',
    'Thumbnails',
]

warnings = list()

data = dict()
data['all_original_files'] = list()
data['all_original_dirs_only'] = list()
data['processing'] = dict()

def recurse_dir(root_dir):
    '''
    Note: Initial pattern from https://www.devdungeon.com/content/walk-directory-python was adopted in the final product.
    '''
    root_dir = os.path.abspath(root_dir)
    for item in os.listdir(root_dir):
        item_full_path = os.path.join(root_dir, item)
        if item in ignore_names_exact:
            warnings.append('Ignoring based on configuration: "{}"'.format(item_full_path))
        else:
            if os.path.isdir(item_full_path):
                data['all_original_dirs_only'].append(item_full_path)
                recurse_dir(item_full_path)
            else:
                data['all_original_files'].append(item_full_path)
                #print("%s - %s bytes" % (item_full_path, os.stat(item_full_path).st_size))


def dump_warnings():
    if len(warnings) > 0:
        print('\nWARNINGS\n--------\n\n')
        for w in warnings:
            print('warning> {}'.format(w))
    else:
        print('No warnings')


def start(start=os.getcwd()):
    print('Starting in "{}"'.format(start))
    recurse_dir(root_dir=start)
    dump_warnings()


if __name__ == "__main__":
    start(start=os.getcwd())

# EOF

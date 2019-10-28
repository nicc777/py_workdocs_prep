import os
import re
import shutil

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
data['processing']['directories_deleted'] = list()
data['processing']['files_deleted'] = list()


def is_directory_to_be_deleted(current_directory_name: str, directories_to_delete_if_found: list=directories_to_delete_if_found)->bool:
    for term in directories_to_delete_if_found:
        if re.search(term, current_directory_name, re.IGNORECASE) is not None:
            try:
                shutil.rmtree(current_directory_name)
                data['processing']['directories_deleted'].append(current_directory_name)
            except:
                warnings.append('Error while deleting directory "{}"'.format(current_directory_name))
            return True
    return False


def is_file_starting_or_ending_with_tilde(current_file_with_full_path: str)->bool:
    file = current_file_with_full_path.split(os.sep)[-1]
    if re.search('^~', file) is not None or re.search('~$', file) is not None:
        try:
            os.unlink(current_file_with_full_path)
            data['processing']['files_deleted'].append(current_file_with_full_path)
        except:
            warnings.append('Error while deleting file "{}"'.format(current_file_with_full_path))
        return True
    return False


def recurse_dir(root_dir, directories_to_delete_if_found: list=directories_to_delete_if_found):
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
                if is_directory_to_be_deleted(item_full_path, directories_to_delete_if_found=directories_to_delete_if_found) is False:
                    data['all_original_dirs_only'].append(item_full_path)
                    recurse_dir(item_full_path, directories_to_delete_if_found=directories_to_delete_if_found)
            else:
                keep_file = 0
                if is_file_starting_or_ending_with_tilde(current_file_with_full_path=item_full_path) is False:
                    keep_file += 1
                if keep_file > 0:
                    data['all_original_files'].append(item_full_path)


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

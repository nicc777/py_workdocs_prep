import os
import re
import shutil
from datetime import datetime

VALID_NAME_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890-_.'

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
data['processing']['renamed_files'] = list()
data['processing']['renamed_directories'] = list()


def is_directory_to_be_deleted(current_directory_name: str, directories_to_delete_if_found: list=directories_to_delete_if_found)->bool:
    last_part = current_directory_name.split(os.sep)[-1]
    must_delete = False
    for term in directories_to_delete_if_found:
        if re.search(term, current_directory_name, re.IGNORECASE) is not None:
            must_delete = True
    if re.search('.tmp$', current_directory_name):
        must_delete = True
    if re.search('^\\.', last_part) is not None or re.search('\\.$', last_part):
        must_delete = True
    if must_delete is True:
        try:
            shutil.rmtree(current_directory_name)
            data['processing']['directories_deleted'].append(current_directory_name)
        except:
            warnings.append('Error while deleting directory "{}"'.format(current_directory_name))
        return True
    return False


def is_file_starting_or_ending_with_tilde(current_file_with_full_path: str)->bool:
    file_name = current_file_with_full_path.split(os.sep)[-1]
    #last_part = current_file_with_full_path.split(os.sep)[-1]  # Refactored furing issue #6 - can be deleted (duplicate of file_name)
    must_delete = False
    if re.search('^~', file_name) is not None or re.search('~$', file_name) is not None:
        must_delete = True
    if re.search('.tmp$', current_file_with_full_path):
        must_delete = True
    if re.search('^\\.', file_name) is not None or re.search('\\.$', file_name):
        must_delete = True
    if must_delete is True:
        try:
            os.unlink(current_file_with_full_path)
            data['processing']['files_deleted'].append(current_file_with_full_path)
        except:
            warnings.append('Error while deleting file "{}"'.format(current_file_with_full_path))
        return True
    return False


def file_rename(current_file_with_full_path: str)->str:
    file_name = current_file_with_full_path.split(os.sep)[-1]
    path_name = ''
    if os.sep == '/':
        path_name = '/'.join(current_file_with_full_path.split(os.sep)[:-1]) 
    else:
        path_name = '\\'.join(current_file_with_full_path.split(os.sep)[:-1]) 
    final_file_name = ''
    for char in file_name:
        if char not in VALID_NAME_CHARS:
            final_file_name = '{}{}'.format(final_file_name, '_')
        else:
            final_file_name = '{}{}'.format(final_file_name, char)
    target_file = '{}{}{}'.format(path_name, os.sep, final_file_name)
    if file_name != final_file_name:
        pattern = re.compile('__*')
        final_file_name = pattern.sub('_', final_file_name)
        target_file = '{}{}{}'.format(path_name, os.sep, final_file_name)
        try:
            shutil.move(current_file_with_full_path, target_file)
            data['processing']['renamed_files'].append(
                (
                    current_file_with_full_path,
                    target_file,
                )
            )
        except:
            warnings.append('Error while moving file "{}"'.format(current_file_with_full_path))
    return target_file


def directory_rename(current_directory_name: str)->str:
    dir_name = current_directory_name.split(os.sep)[-1]
    path_name = ''
    if os.sep == '/':
        path_name = '/'.join(current_directory_name.split(os.sep)[:-1]) 
    else:
        path_name = '\\'.join(current_directory_name.split(os.sep)[:-1]) 
    final_dir_name = ''

    for char in dir_name:
        if char not in VALID_NAME_CHARS:
            final_dir_name = '{}{}'.format(final_dir_name, '_')
        else:
            final_dir_name = '{}{}'.format(final_dir_name, char)
    target_dir = '{}{}{}'.format(path_name, os.sep, final_dir_name)
    if dir_name != final_dir_name:
        pattern = re.compile('__*')
        final_dir_name = pattern.sub('_', final_dir_name)
        target_dir = '{}{}{}'.format(path_name, os.sep, final_dir_name)
        try:
            shutil.move(current_directory_name, target_dir)
            data['processing']['renamed_directories'].append(
                (
                    current_directory_name,
                    target_dir,
                )
            )
        except:
            warnings.append('Error while moving directory "{}"'.format(current_directory_name))
    return target_dir


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
                    item_full_path = directory_rename(current_directory_name=item_full_path)
                    data['all_original_dirs_only'].append(item_full_path)
                    recurse_dir(item_full_path, directories_to_delete_if_found=directories_to_delete_if_found)
            else:
                keep_file = 0
                if is_file_starting_or_ending_with_tilde(current_file_with_full_path=item_full_path) is False:
                    keep_file += 1
                if keep_file > 0:
                    final_file_name_and_full_path = file_rename(current_file_with_full_path=item_full_path)
                    data['all_original_files'].append(final_file_name_and_full_path)
                else:
                    warnings.append('File "{}" was marked to be deleted'.format(item_full_path))


def report_producer():
    report_file_name = '{}{}py_workdocs_prep.log'.format(
        os.getcwd(),
        os.sep
    )
    with open(report_file_name, 'a') as out_file:
        out_file.write('----------------------------------------\n')
        out_file.write('NEW RUN: pwd={}\n'.format(os.getcwd()))
        out_file.write('TIMESTAMP (UTC): {}\n'.format(datetime.utcnow().isoformat()))
        out_file.write('----------------------------------------\n')
        out_file.writelines('\n\n')
        out_file.writelines('Final File List:\n')
        out_file.writelines('---------------\n\n')
        for item in data['all_original_files']:
            out_file.write(
                'final file [{}]: {}\n'.format(
                    '{}'.format(len(item)).rjust(6),
                    item
                )
            )
        out_file.writelines('\n\n')
        out_file.writelines('Deleted Files:\n')
        out_file.writelines('-------------\n\n')
        for item in data['processing']['files_deleted']:
            out_file.write('deleted file: {}'.format(item))
        out_file.writelines('\n\n')
        out_file.writelines('Deleted Directories:\n')
        out_file.writelines('-------------------\n\n')
        for item in data['processing']['directories_deleted']:
            out_file.write('deleted directory: {}\n'.format(item))
        out_file.writelines('\n\n')
        out_file.writelines('Renamed Files:\n')
        out_file.writelines('-------------\n\n')
        for item in data['processing']['renamed_files']:
            out_file.write('renamed file: {}\n'.format(item))
        out_file.writelines('\n\n')
        out_file.writelines('Renamed Directories:\n')
        out_file.writelines('-------------------\n\n')
        for item in data['processing']['renamed_directories']:
            out_file.write('renamed directory: {}\n'.format(item))
        out_file.writelines('\n\n')
        out_file.writelines('WARNINGS:\n')
        out_file.writelines('--------\n\n')
        if len(warnings) > 0:
            for item in warnings:
                out_file.write('warning: {}\n'.format(item))
        else:
            out_file.write('warning: none\n')
        out_file.write('\n------------- DONE -------------------\n\n\n')
    print('Written log to "{}"'.format(report_file_name))


def start(start=os.getcwd()):
    print('Starting in "{}"'.format(start))
    recurse_dir(root_dir=start)
    report_producer()


if __name__ == "__main__":
    start(start=os.getcwd())

# EOF

'''Essentially a test for th recurse_dir() function under controlled conditions.

Basic steps:

1. Setup a Test start directory relative to where this script is executed from
2. Prepare dummy directories and files
3. Run the recurse_dir() function
4. Test result
5. Cleanup dummy directories and files
'''

import unittest
import random
import os
import shutil
from py_workdocs_prep.py_workdocs_prep import recurse_dir, data, warnings


PWD = os.getcwd()
directories_to_delete_if_found = [
    'venv*',
    'node_modules'
]


def create_file_text_contents():
    content = ''
    content_length = random.randint(5,25)
    while len(content) < content_length:
        content = '{}*'.format(content)
    return content


def create_dir(parent_dir: str, new_directory: str):
    os.makedirs(
        os.path.join(parent_dir, new_directory)
    )


def create_file(directory: str, file_name: str, content: str):
    with open('{}{}{}'.format(directory, os.sep, file_name), 'w') as f:
        f.write(content)


def create_test_data(pwd: str, test_data: list):
    print('pwd={}'.format(pwd))
    for item in test_data:
        if 'DIR' in item['Type']:
            create_dir(pwd, item['Name'])
            if isinstance(item['Contents'], list):
                if len(item['Contents']) > 0:
                    create_test_data(pwd='{}{}{}'.format(pwd, os.sep, item['Name']), test_data=item['Contents'])
        else:
            create_file(directory=pwd, file_name=item['Name'], content=item['Contents'])


'''Test data
.
├── Test1
│   ├── ~test1.txt      <- delete
│   ├── test1.txt
│   ├── test2.txt
│   |── test3.txt
│   └── vEnv            <- delete
│       |── ~test1.txt  <- ignore
│       |── test1.txt   <- ignore
│       └── test2.txt   <- ignore
│   
├── Test2
│   ├── Test2 1
│   │   |── test1.txt
│   │   └── test2.txt
│   ├── venv_1          <- delete
│   │   |── test1.txt   <- ignore
│   │   └── test2.txt   <- ignore
│   ├── test1.txt
│   ├── test 4.txt.tmp  <- delete
│   ├── test 4.txt.     <- delete
│   ├── .test 4.txt     <- delete
│   ├── test 3 +.txt    <- rename to test 3 _.txt
│   ├── tes++t 3 +.txt  <- rename to tes_t 3 _.txt
│   ├── test2.txt~      <- delete
│   └── test2.txt
│   
├── .Test3              <- delete
│   ├── test1.txt       <- ignore
│   └── test2.txt       <- ignore
│   
├── Test4 +             <- rename to "Test4 _"
│   ├── test1.txt       
│   └── test2.txt       
│   ├── Test ++  3      <- rename to "Test _  3"
│   │   |── test+1.txt  <- rename to "test_1.txt"
│   │   └── test++2.txt <- rename to "test_2.txt"
'''
test_data = [
    {
        'Name': 'UnitTestData',
        'Type': 'DIR',
        'Contents': [
            {
                'Name': 'Test1',
                'Type': 'DIR',
                'Contents': [
                    {
                        'Name': '~test1.txt',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'test1.txt',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'test2.txt',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'test3.txt',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'vEnv',
                        'Type': 'DIR',
                        'Contents': [
                            {
                                'Name': '~test1.txt',
                                'Type': 'FILE',
                                'Contents': create_file_text_contents()
                            },
                            {
                                'Name': 'test1.txt',
                                'Type': 'FILE',
                                'Contents': create_file_text_contents()
                            },
                            {
                                'Name': 'test2.txt',
                                'Type': 'FILE',
                                'Contents': create_file_text_contents()
                            },
                        ]
                    },
                ]
            },
            {
                'Name': 'Test2',
                'Type': 'DIR',
                'Contents': [
                    {
                        'Name': 'Test2 1',
                        'Type': 'DIR',
                        'Contents': [
                            {
                                'Name': 'test1.txt',
                                'Type': 'FILE',
                                'Contents': create_file_text_contents()
                            },
                            {
                                'Name': 'test2.txt',
                                'Type': 'FILE',
                                'Contents': create_file_text_contents()
                            },
                        ]
                    },
                    {
                        'Name': 'venv_1',
                        'Type': 'DIR',
                        'Contents': [
                            {
                                'Name': 'test1.txt',
                                'Type': 'FILE',
                                'Contents': create_file_text_contents()
                            },
                            {
                                'Name': 'test2.txt',
                                'Type': 'FILE',
                                'Contents': create_file_text_contents()
                            },
                        ]
                    },
                    {
                        'Name': 'test1.txt',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'test 4.txt.tmp',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'test 4.txt.',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': '.test 4.txt',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'test 3 +.txt',     # Must be changed to 'test 3 _.txt'
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'tes++t 3 +.txt',    # Must be changed to 'tes_t 3 _.txt'
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'test2.txt~',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'test2.txt',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                ]
            },
            {
                'Name': '.Test3',
                'Type': 'DIR',
                'Contents': [
                    {
                        'Name': 'test1.txt',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'test2.txt',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                ]
            },
            {
                'Name': 'Test4 +',
                'Type': 'DIR',
                'Contents': [
                    {
                        'Name': 'test1.txt',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'test2.txt',
                        'Type': 'FILE',
                        'Contents': create_file_text_contents()
                    },
                    {
                        'Name': 'Test ++  3',
                        'Type': 'DIR',
                        'Contents': [
                            {
                                'Name': 'test+1.txt',
                                'Type': 'FILE',
                                'Contents': create_file_text_contents()
                            },
                            {
                                'Name': ' test++2.txt',
                                'Type': 'FILE',
                                'Contents': create_file_text_contents()
                            },
                        ]
                    },
                ]
            },
        ]
    },
]


class TestBasicWalkDir(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_test_data(pwd=PWD, test_data=test_data)

    @classmethod
    def tearDownClass(cls):
        pwd = '{}{}{}'.format(PWD, os.sep, test_data[0]['Name'])
        try:
            shutil.rmtree(pwd)
        except:
            print('Error while deleting directory "{}"'.format(pwd))

    def setUp(self):
        self.pwd = '{}{}{}'.format(PWD, os.sep, test_data[0]['Name'])
        print('test data location: {}'.format(self.pwd))

    def test_recurse_dir(self):
        recurse_dir(root_dir=self.pwd, directories_to_delete_if_found=directories_to_delete_if_found)
        self.assertEqual(5, len(data['all_original_dirs_only']))
        self.assertEqual(14, len(data['all_original_files']))
        self.assertEqual(3, len(data['processing']['directories_deleted']))
        for directory in data['all_original_dirs_only']:
            self.assertTrue(os.path.exists(directory), 'directory={}'.format(directory))
            self.assertTrue(os.path.isdir(directory), 'directory={}'.format(directory))
        for item in data['all_original_files']:
            self.assertTrue(os.path.exists(item))
            if '.txt' in item:
                self.assertTrue(os.path.isfile(item), 'item={}'.format(item))
            else:
                self.assertTrue(os.path.isdir(item), 'item={}'.format(item))
        self.assertEqual(2, len(data['processing']['renamed_directories']), 'Invalid number of renamed directories.') 
        self.assertEqual(4, len(data['processing']['renamed_files']), 'Invalid number of renamed files.') 
        venv_directory_deleted_seen = 0
        dot_directory_deleted = 0
        for item in data['processing']['directories_deleted']:
            if 'venv' in item.lower():
                venv_directory_deleted_seen += 1
            if '.' in item:
                dot_directory_deleted += 1
        self.assertEqual(2, venv_directory_deleted_seen)
        self.assertEqual(1, dot_directory_deleted)
        tilde_files_deleted = 0
        for item in data['processing']['files_deleted']:
            if '~' in item:
                tilde_files_deleted += 1
        self.assertEqual(2, tilde_files_deleted, 'It appears not all tilde files were deleted')

# EOF

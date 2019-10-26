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
from py_workdocs_prep.py_workdocs_prep import recurse_dir, data


PWD = os.getcwd()


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
│   ├── test1.txt
│   ├── test2.txt
│   └── test3.txt
│   
├── Test1
│   ├── Test2 1
│   │   |── test1.txt
│   │   └── test2.txt
│   ├── test1.txt
│   └── test2.txt
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
        recurse_dir(root_dir=self.pwd)
        self.assertEqual(3, len(data['all_original_dirs_only']))
        self.assertEqual(7, len(data['all_original_files']))
        for directory in data['all_original_dirs_only']:
            self.assertTrue(os.path.exists(directory), 'directory={}'.format(directory))
            self.assertTrue(os.path.isdir(directory), 'directory={}'.format(directory))
        for item in data['all_original_files']:
            self.assertTrue(os.path.exists(item))
            if '.txt' in item:
                self.assertTrue(os.path.isfile(item), 'item={}'.format(item))
            else:
                self.assertTrue(os.path.isdir(item), 'item={}'.format(item))

# EOF

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py_workdocs_prep',  
    version='0.5.1',
    download_url = 'https://github.com/nicc777/py_workdocs_prep/releases/download/release-0.5.1/py_workdocs_prep-0.5.1.tar.gz',
    description='AWS Workdocs Preparation Utility',  
    long_description=long_description,  
    long_description_content_type='text/markdown',  
    url='https://github.com/nicc777/py_workdocs_prep',  
    author='Nico Coetzee',  
    author_email='nicc777@gmail.com',  
    classifiers=[  
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Topic :: System :: Archiving',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='aws workdocs',  
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  
    python_requires='>=3.6, <4',
    install_requires=[],  
    extras_require={  
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={  
        'console_scripts': [
            'wdp=py_workdocs_prep.py_workdocs_prep:start',
        ],
    },
    project_urls={  
        'Bug Reports': 'https://github.com/nicc777/py_workdocs_prep/issues',
        'Source': 'https://github.com/nicc777/py_workdocs_prep',
    },
)

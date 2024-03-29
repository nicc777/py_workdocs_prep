# py_workdocs_prep

A bulk directory and file renaming utility to prepare files for migration to [AWS WorkDocs](https://aws.amazon.com/workdocs/)

If you run the script, it will start to traverse the current directory and will do one of the following with each file and directory:

* Keep as is
* Rename
* Delete

All actions taken will be written out to STDOUT after all operations is completed

**WARNING** The actions will make changes to your directories and/or files. It is *HIGHLY RECOMMENDED* you first do a full backup of your data.

This project was a result of me migrating from Dropbox to AWS Workdocs and finding a lot issues due to the names of files and/or directories that were invalid in AWS Workdocs.

For details of this potential problem, refer to the [AWS Workdocs Administration Guide](https://docs.aws.amazon.com/workdocs/latest/adminguide/prepare.html)

Here is the most important limitations as of 2019-10-26:

* Amazon WorkDocs Drive displays only files with a full directory path of 260 characters or fewer
* Invalid characters in names:
  * Trailing spaces
  * Periods at the beginning or end–For example: `.file`, `.file.ppt`, `.`, `..`, or `file.`
  * Tildes at the beginning or end–For example: `file.doc~`, `~file.doc`, or `~$file.doc`
  * File names ending in .tmp–For example: `file.tmp`
  * File names exactly matching these case-sensitive terms: `Microsoft User Data`, `Outlook files`, `Thumbs.db`, or `Thumbnails`
  * File names containing any of these characters – `*` (asterisk), `/` (forward slash), `\` (back slash), `:` (colon), `<` (less than), `>` (greater than), `?` (question mark), `|` (vertical bar/pipe), `"` (double quotes), or \202E (character code 202E)

## Quick Start

The following examples assume a MS Windows system, as the intend is to prepare a directory for AWS WorkDocs, which typically only has clients for Windows (unless you are on mobile).

### From PyPi

Prerequisites:

* Python 3.7+

The example below will show how to get started very quickly using the most current version. The example will demonstrate a dry-run operation that will allow you to inspect the log file and review changes before committing.

Assuming you are on the Windows command line:

```shell
> pip install py-workdocs-prep
> cd <the directory you whish to prepare for migration>
> wdp --dry-run
```

A log file called `py_workdocs_prep.log` will be generated. If it already exist, new entries will be appended.

**NOTE** It is highly recommended that you inspect the log file and understand how the application will change your files - and delete certain directories and files. Also take special note of any warnings, especially those about the total path length that may be too long (search for the string `TOTAL LENGTH EXCEEDED THRESHOLD`). [Read here](https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file?redirectedfrom=MSDN#maximum-path-length-limitation) why this is important.

To commit all changes, but first backup all files and directories, you can run the following (assuming the application is already installed):

```shell
> wdp -b
```

#### Command Line Arguments

| Option             | Description                                                                                                                           | Example           |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `-b` or `--backup` | Create a backup of all current files and directories. A `tar.gz` file will be created.                                                | `> wdp -b`        |
| `--dry-run`        | The application will not perform any file or directory modifications, but only log what would be done.                                | `> wdp --dry-run` |
| `--delete-dirs`    | Define a comma separated list of directories to be deleted. Don't include any spaces, but rather use proper Python regex expressions. | `> wdp --delete-dirs="test1,ven*,node_mod*"`

### From Source

Prerequisites:

* Python 3.7+
* git

Assuming your target directory is something like `D:\Dropbox`, and you want to backup first, you can run the following commands:

```bash
> git clone https://github.com/nicc777/py_workdocs_prep.git
> cd py_workdocs_prep
> python setup.py sdist
> pip install dist\*
> d:
> cd Dropbox
> wdp -b
```

## Strategy

I had a very large number of files (600,000+) and it turned out a lot of them violated the mentioned restrictions. I had to make a plan...

Here is how the script works:

### Long path names

The Default Windows starting folder is `W:\My Documents\` and it contains 16 characters. 

Therefore, any other directory and/or file name combined in my Dropbox root folder had to come in under 244 characters.

I decided that after the transformation, I would just print WARNINGS for each item with the number of characters over. I would then make a decision later on to either rename some part of the directory and/or file name or sometimes completely reorganize the directory structure. This would remain a manual operation.

### Getting rid of redundant files

As I used Dropbox as a "working" documents directory I ended up with a large number `.git`, `venv` and `node_modules` directories (to name a view examples). So the obvious first step for me was to delete all these directories. (`DONE`)

Files that will also be deleted include files starting or ending with the tilde (`~`) character. (`PENDING`)

Files ending in `.tmp` will also be deleted. (`PENDING`)

### Directory and file renaming strategy

Any directory names and files containing any of the listed invalid characters (including any whitespace) will be renamed, replacing the violating characters with an underscore (`_`) character. Repeating underscore characters will be replaced with just a single underscore character.

## Processing Methodology

In terms of processing, the following order of processing will be followed:

1. First, all directories will be traversed and file names will be checked:
   1. If it is identified as a file to be deleted, write out a delete command
   2. Process illegal characters and issue a rename command if required
2. Now traverse all directories and identify all directories to be renamed
   1. After the list is determined: order the list in terms of length (from longest to least)
   2. Loop through the list and commit rename commands
3. Now, assuming we have a list of final directory and file names, determine which items are over the total length limit and print warnings for these

## Acknowledgements

Thanks to [NanoDano](https://www.devdungeon.com/users/nanodano) for the [examples](https://www.devdungeon.com/content/walk-directory-python) I used to walk through the directories.

## Geek Food

### Manual Testing

To inspect the project and prepare for migrating to AWS Workdocs...

Clone the project and `cd` into the project directory

```python
>>> from py_workdocs_prep.py_workdocs_prep import start
>>> start()
```
### Memory Profiling

You can try the following:

```bash
> pip install -U memory_profiler
```

Then:

```python
>>> from py_workdocs_prep.py_workdocs_prep import start
>>> from memory_profiler import memory_usage
>>> memory_usage((start, ('D:\\Dropbox',))) 
Starting in "D:\Dropbox"
[15.54296875, 15.54296875, 15.54296875,..., 178.421875]
```

This means the script started scanning the directory `D:\Dropbox` and the application grew from a starting 15.5 MiB to 178.4 MiB (early testing).

My machine has plenty of RAM, so this was acceptable for me.

References:

* [memory_profiler](https://pypi.org/project/memory-profiler/)
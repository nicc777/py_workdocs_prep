# py_workdocs_prep

A bulk directory and file renaming utility to prepare files for migration to [AWS WorkDocs](https://aws.amazon.com/workdocs/)

If you run the script, it will start to traverse the current directory a produce a file full of MS Windows Powershell commands that will perform either one of the following actions on an item:

* Keep as is
* Rename
* Delete

The Powershell file will be save in the current working directory as `aws_workdocs_prep.ps1` - if the file exists, it will first be deleted!

I did this so that you can manually review the actions before committing to any changes.

**WARNING** The actions from the resulting Powershell script, when run, will make changes to your directories and/or files. It is *HIGHLY RECOMMENDED* you first do a full backup of your data.

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
  * File names containing any of these characters–* (asterisk), / (forward slash), \ (back slash), : (colon), < (less than), > (greater than), ? (question mark), | (vertical bar/pipe), " (double quotes), or \202E (character code 202E)

## Strategy

I had a very large number of files (600,000+) and it turned out a lot of them violated the mentioned restrictions. I had to make a plan...

Here is how the script works:

### Long path names

The Default Windows starting folder is `W:\My Documents\` and it contains 16 characters. 

Therefore, any other directory and/or file name combined in my Dropbox root folder had to come in under 244 characters.

I decided that after the transformation, I would just print WARNINGS for each item with the number of characters over. I would then make a decision later on to either rename some part of the directory and/or file name or sometimes completely reorganize the directory structure. This would remain a manual operation.

### Getting rid of redundant files

As I used Dropbox as a "working" documents directory I ended up with a large number `.git`, `venv` and `node_modules` directories (to name a view examples). So the obvious first step for me was to delete all these directories.

Files that will also be deleted include files starting or ending with the tilde (`~`) character.

Files ending in `.tmp` will also be deleted.

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
# -*- coding: utf-8 -*-
import logging
import os
import pathlib
import re


def list_directory(folder=pathlib.Path.cwd(),
                   recurse=False,
                   extension='',
                   wildcard='',
                   print_log=False,
                   out_folder=pathlib.Path.cwd()):
    '''
    List all files in a root folder.root

    Parameters
    ----------
    folder: pathlib.Path or str
        Root folder path to be listed. Defaults to current working directory

    recurse: boolean
        Does the function recursively list all subfolder? Defaults to False

    extension: str
        File extension to look for. Defaults to '' (ie all files are listed)

    wildcard: str
        String that has to be in the selected file. Defaults to ''.

    print_log: boolean
        Does the function print its output to command line? Defaults to False

    out_folder: pathlib.Path or str
        Output folder for the file list text file. No text file created
        if empty. Defaults to current workind directory.

    Returns
    -------
    file_list: list
        list of all relevant files

    '''
    logging.info('START - File listing extraction')
    # Check folders
    root = pathlib.Path(folder)
    if not root.exists():
        raise AttributeError(f'{root} is not a valid folder.')
    if out_folder in [None, '', ' ']:
        out_folder = None
    else:
        out_folder = pathlib.Path(out_folder)
        if not out_folder.exists():
            raise AttributeError(f'{out_folder} is not a valid folder.')
    # Check and format extension and wildcard
    if extension != '':
        extension = re.sub('.*\s', '', extension)
    # Check recurse and print_log param
    if not isinstance(recurse, bool):
        raise AttributeError('recurse parameter is not a valid boolean.')
    if not isinstance(print_log, bool):
        raise AttributeError('print_log parameter is not a valid boolean.')
    # Get file list
    file_list = []
    for ra, dirs, files in os.walk(root, topdown=False):
        for name in files:
            # filter wildcard
            if wildcard in name and extension in name:
                if recurse == False:
                    if pathlib.Path(ra) == root:
                        path = pathlib.Path(ra, name)
                        file_list.append(path)
                elif recurse == True:
                    path = pathlib.Path(ra, name)
                    file_list.append(path)
    # Prepare output string
    ext_string, wild_string = '', ''
    if len(extension) > 0:
        ext_string = f' restricted to {extension} files'
    if len(wildcard) > 0:
        wild_string = f' with filename containing {wildcard}'
    header = f'LIST ALL FILES for folder {root}{ext_string}{wild_string}'
    # Output to cmd
    if print_log:
        print(header)
        print(40*'-')
        for item in file_list:
            print(str(item))
    # Output to text
    if out_folder:
        f = open(pathlib.Path(out_folder, 'File_listing.txt'), 'w')
        f.write(header)
        f.write(40*'-'+ '\n\n')
        for item in file_list:
            f.write(str(item)+'\n')
    logging.info('END - File listing extraction')
    return file_list


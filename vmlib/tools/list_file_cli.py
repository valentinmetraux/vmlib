import pathlib
import click
import vmlib as vm


@click.command()
def main():
    '''
    Lists all files in a folder.
    Prompts user to input root folder, output folder,
    inspect or not subfolders, limit search to a file extension,
    limit search to file names containing user-specific string.

    '''

    folder = click.prompt('Folder to inspect',
                          default='',
                          show_default=False,
                          type=str
                          )
    out = click.prompt('Output folder (no output if empty)',
                       default='',
                       show_default=False,
                       type=str
                       )
    recurse = click.prompt('Inspect subfolders (y/n)',
                           default='n',
                           show_default=False,
                           type=str
                           )
    ext = click.prompt('Limit to the extension (can be empty)',
                       default='',
                       show_default=False,
                       type=str
                       )
    wildcard = click.prompt('Limit to filename containing (can be empty)',
                            default='',
                            show_default=False,
                            type=str
                            )
    print_log = click.prompt('Display result?',
                             default='y',
                             show_default=False,
                             type=str
                             )
    # Precompile parameters
    if recurse == 'y':
        rec = True
    else:
        rec = False
    if print_log == 'y':
        log = True
    else:
        log = False
    # Execute
    print('\n')
    vm.dir.list_directory(folder, rec,
                          ext, wildcard, log, out)


if __name__ == '__main__':
    main()

import vmlib as vm

folder = r'C:\Users\Valentin\Desktop\QC'
recurse = False
extension = '. pptx'
wildcard = 'DailyQC'
print_log = True
out_folder = '' #r'C:\Users\Valentin\Desktop'


vm.dir.list_directory(folder, recurse,
                      extension, wildcard, print_log, out_folder)

import pathlib
import vmlib as vm

# Get all sgy files
root = pathlib.Path(r'C:\Users\Valentin\Desktop\Geneva_14-15')
files = list(root.glob('*.SEGY'))  # Check for other sgy/SGY/segy/SEGY

# Loop on files
for file in files:
    print(f'Exporting {file.stem}')
    segy = vm.io.segy.import_navmerge(file, data=False)
    segy.export_text_header(output='folder')
    segy.export_bin_header(output='folder')
    segy.export_trace_header(output='folder')

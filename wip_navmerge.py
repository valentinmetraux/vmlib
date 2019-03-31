import pathlib
import vmlib as vm

# Get all sgy files
root = pathlib.Path(r'C:\Users\Valentin\Desktop\SEIS_QC\Nav-merge')
files = list(root.glob('*.SEGY'))  # Check for other sgy/SGY/segy/SEGY
if len(files) > 1:
    output = 'folder'
else:
    output = 'root'

# Loop on files
for file in files:
    vm.utils.print.headings(f'{file.stem}', length=50, symbol='#')
    # Load and initialize file
    vm.utils.print.info('File loading', 1)
    navmerge = vm.io.segy.import_navmerge(filename=file, data=True,
                                          rcv_header='CROSSLINE_3D',
                                          src_between_rcv=True,
                                          epsg='2056')
    # Export headers
    vm.utils.print.info('Export headers', 1)
    navmerge.export_text_header(output=output)
    navmerge.export_bin_header(output=output)
    navmerge.export_trace_header(output=output)
    # Export SPS & GIS & TXT
    vm.utils.print.info('Export SPS and GIS files', 1)
    # Export plots
    vm.utils.print.info('Export plots', 1)
    navmerge.generate_plots(output=output, src=True, rcv=True, cdp=True,
                            midpoints=True)
    # Export shots & CDP
    vm.utils.print.info('Export gathers', 1)
    # Export report
    vm.utils.print.info('Export report', 1)

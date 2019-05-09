import pathlib
import vmlib as vm

# PARAMETERS
params = {'root': pathlib.Path(r'C:\Users\Valentin\Desktop\SEIS_QC\Nav-merge'),
          'extension': '*.SEGY',
          'output_type': 'root',
          'epsg': '2056',
          'load_traces': True,
          'rcv_header': 'CROSSLINE_3D',
          'src_header': 'ShotPoint',
          'src_geom': True,
          'plot_src': True,
          'plot_rcv': True,
          'plot_cdp': True,
          'plot_midpoints': True,
          'export_headers': True,
          'export_report': True,
          'short_offset_lim': 250,  # m
          'short_offset_cut': 300,  # ms
          }


vm.utils.print.headings(f'Nav merge QC')
# Get all relevant files
files = list(params['root'].glob(params['extension']))
# Adapt output type to number of inspected files:
if len(files) > 1:
    params['output_type'] = 'folder'
# Loop on files
for file in files:
    vm.utils.print.info(f'{file.stem}')
    # Load and initialize file
    vm.utils.print.info('File loading', 2)
    navmerge = vm.io.segy.import_navmerge(filename=file,
                                          data=params['load_traces'],
                                          rcv_header=params['rcv_header'],
                                          src_header=params['src_header'],
                                          src_between_rcv=params['src_geom'],
                                          epsg=params['epsg'])
    # Export headers
    if params['export_headers']:
        vm.utils.print.info('Export headers', 2)
        navmerge.export_text_header(output=params['output_type'])
        navmerge.export_bin_header(output=params['output_type'])
        navmerge.export_trace_header(output=params['output_type'])

    # Export SPS & GIS & TXT
    vm.utils.print.info('Export SPS and GIS files', 2)

    # Create plots
    vm.utils.print.info('Export plots', 2)
    navmerge.generate_plots(params)


    # ADD PLOT OPTION FOR WIGGLES

    # Export summary report in root folder
    vm.utils.print.info('Export report', 2)



    # Report Title
    # Line summary (n src, n_rcv, n_trace, etc)
    # Headers (text, bin)
    # Plots
    # Shot gathers

    # Add T0 integrity check (monotrace with shortest offset for each shot)

    # Delete
    del navmerge

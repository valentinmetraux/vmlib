import pathlib
import vmlib as vm

# Get all sgy files
root = pathlib.Path(r'C:\Users\Valentin\Desktop\Lignano')
files = list(root.glob('*.sgy'))  # Check for other sgy/SGY/segy/SEGY

# Loop on files
for file in files:
    # Load
    segy = vm.io.segy.import_section(root.joinpath(file), data=True)
    # Get and format text header from template
    #header = vm.seismic.rx_sect_qc.get_info_from_text_header(segy,
    #                                                         template='SIG')

    '''
    # Compare text and bin headers
    for k in segy.bin_header.keys():
        print(f'{k}')

    print(segy.bin_header['JobID'])



    comparison = vm.seismic.rx_sect_qc.compare_text_bin_header(header,
                                                               segy.bin_header)
    # Analyze trace headers

    # Compare trace headers with text/bin

    '''


    '''
    # Get interCDP (18SIG specific)
    name = str(file.stem).split('-')[1].split('_')[0]
    if 'Q' in name:
        intercdp = 3
    elif name[0] == '1':
        intercdp = 2.5
    else:
        intercdp = 6
    '''
    intercdp = 2.5
    # QC Plots
    vm.seismic.rx_sect_plot.cdp_spacing(section=segy,
                                        output='folder')
    vm.seismic.rx_sect_plot.basemap(section=segy,
                                    output='folder')
    vm.seismic.rx_sect_plot.distances(section=segy, inter_cdp=intercdp,
                                      output='folder')
    # Plot section (with fold)


    # Export report and summary files


    '''

    # Plot section
    vm.seismic.rx_sect_plot.section(section=segy,
                                    timerange=[0,1500],
                                    tracerange=[],
                                    fold=False,
                                    cm='gray',
                                    hillshade=False,
                                    type='twt',
                                    hscale=5000,
                                    vscale=5000,
                                    output='folder')
    '''

import vmlib as vm


def basemap(file, output='root', src=True, rcv=True, cdp=True, midpoints=True):
    # Resolve output filename
    filename = file.stats['filename']
    if output == 'root':
        out = filename.parent
    else:
        out = filename.parent.joinpath('Maps')
        out.mkdir(parents=True, exist_ok=True)
    # Save file
    outfile = out.joinpath(f'{filename.stem}_navmerge.jpg')
    # Plot
    vm.plot.seis.basemap_line(file, outfile, src, rcv, cdp, midpoints)
    vm.utils.print.info('Basemap created', 2)
    return None


def elevation(file, output='root'):
    # Resolve output filename
    filename = file.stats['filename']
    if output == 'root':
        out = filename.parent
    else:
        out = filename.parent.joinpath('Elevations')
        out.mkdir(parents=True, exist_ok=True)
    # Save file
    outfile = out.joinpath(f'{filename.stem}_elevation.jpg')
    # Plot
    vm.plot.seis.elevation(file, outfile)
    vm.utils.print.info('Elevation created', 2)
    return None


def offset_cdp_fold(file, output='root'):
    # Resolve output filename
    filename = file.stats['filename']
    if output == 'root':
        out = filename.parent
    else:
        out = filename.parent.joinpath('Fold')
        out.mkdir(parents=True, exist_ok=True)
    # Save file
    outfile = out.joinpath(f'{filename.stem}_cdp_offset_fold.jpg')
    # Plot
    vm.plot.seis.offset_cdp_fold(file, outfile)
    vm.utils.print.info('CDP-Offset-Fold chart created', 2)
    return None


def amplitude_offset(file, output='root'):
    # Resolve output filename
    filename = file.stats['filename']
    if output == 'root':
        out = filename.parent
    else:
        out = filename.parent.joinpath('Amplitude')
        out.mkdir(parents=True, exist_ok=True)
    # Save file
    outfile = out.joinpath(f'{filename.stem}_amplitude_offset.jpg')
    # Plot
    vm.plot.seis.amplitude_offset(file, outfile)
    vm.utils.print.info('Amplitude-Offset chart created', 2)
    return None


def stacking(file, output='root'):
    # Resolve output filename
    filename = file.stats['filename']
    if output == 'root':
        out = filename.parent
    else:
        out = filename.parent.joinpath('Geometry')
        out.mkdir(parents=True, exist_ok=True)
    # Save file
    outfile = out.joinpath(f'{filename.stem}_shooting_geometry.jpg')
    # Plot
    vm.plot.seis.stacking(file, outfile)
    vm.utils.print.info('Stacking chart created', 2)
    return None


def fold(file, output='root'):
    # Resolve output filename
    filename = file.stats['filename']
    if output == 'root':
        out = filename.parent
    else:
        out = filename.parent.joinpath('Fold')
        out.mkdir(parents=True, exist_ok=True)
    # Save file
    outfile = out.joinpath(f'{filename.stem}_fold.jpg')
    # Plot
    vm.plot.seis.fold(file, outfile)
    vm.utils.print.info('Fold chart created', 2)
    return None


def cdp_spacing(file, output='root'):
    # Resolve output filename
    filename = file.stats['filename']
    if output == 'root':
        out = filename.parent
    else:
        out = filename.parent.joinpath('Spacing')
        out.mkdir(parents=True, exist_ok=True)
    # Save file
    outfile = out.joinpath(f'{filename.stem}_dcp_spacing.jpg')
    # Plot
    vm.plot.seis.cdp_spacing(file, outfile)
    vm.utils.print.info('CDP spacing chart created', 2)
    return None

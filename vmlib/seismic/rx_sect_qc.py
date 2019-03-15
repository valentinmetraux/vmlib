# -*- coding: utf-8 -*-
import re


# Load templates
def _text_header(template='Geo2X'):
    entries = {}
    if template.lower() == 'geo2x':
        entries['client'] = ['C01', 'CLIENT:']
        entries['area'] = ['C01', 'AREA:']
        entries['date'] = ['C01', 'SEG-Y DATE:']
        entries['survey'] = ['C02', 'SURVEY:']
        entries['line'] = ['C02', 'LINE :']
        entries['source'] = ['C07', 'SOURCE TYPE:']
        entries['sample_rate'] = ['C08', 'SAMPLE RATE:']
        entries['record_length'] = ['C08', 'RECORDING LENGTH:']
        entries['nominal fold'] = 'Blank'
        entries['shot_interval'] = ['C10', 'SOURCE POINT INTERVAL:']
        entries['rcv_interval'] = ['C10', 'RECEIVER POINT INTERVAL:']
        entries['datum'] = ['C11', 'SEISMIC DATUM:']
        entries['repl_velocity'] = ['C11', 'REPL. VEL:']
        entries['data_type'] = ['C17', 'DATA TYPE:']
        entries['data_sample_format'] = ['C05', 'SAMPLE FORMAT:']
        entries['byte_alloc'] = ['C31', 'C38']
        entries['processing_flow'] = ['C23', 'C26']
        entries['crs'] = 'C15'
        entries['segy_rev'] = 'C39'
        entries['closure'] = 'C40'
    if template.lower() == 'sig':
        entries['client'] = ['C01', 'CLIENT:']
        entries['area'] = ['C01', 'AREA:']
        entries['date'] = ['C01', 'SEG-Y DATE:']
        entries['survey'] = ['C02', 'SURVEY:']
        entries['line'] = ['C02', 'LINE :']
        entries['source'] = ['C06', 'SOURCE TYPE:']
        entries['sample_rate'] = ['C07', 'SAMPLE RATE:']
        entries['record_length'] = ['C07', 'RECORDING LENGTH:']
        entries['nominal fold'] = ['C07', 'NOMINAL FOLD:']
        entries['shot_interval'] = ['C08', 'SOURCE POINT INTERVAL:']
        entries['rcv_interval'] = ['C09', 'RECEIVER POINT INTERVAL:']
        entries['datum'] = ['C14', 'SEISMIC DATUM:']
        entries['repl_velocity'] = ['C14', 'REPL. VEL:']
        entries['data_type'] = ['C15', 'DATA TYPE:']
        entries['data_sample_format'] = ['C39', 'FORMAT:']
        entries['byte_alloc'] = ['C29', 'C36']
        entries['processing_flow'] = ['C22', 'C25']
        entries['crs'] = 'C13'
        entries['segy_rev'] = 'Blank'
        entries['closure'] = 'C40'
    return entries


def _get_inline_item(header, entries, label):
    try:
        # Labels that are within the same entry
        key = entries[label][0]
        value = entries[label][1]
        labels = [entries[k][1] for k, v in entries.items() if v[0] == key]
        # Get label index
        ix = labels.index(value)
        # Get header entry and split on label
        entry = header[key].split(labels[ix])[1]
        # if not last index, strip with next ix
        if ix < len(labels) - 1:
            entry = entry.split(labels[ix + 1])[0]
        return entry.strip()
    except:
        return 'To check'


def _get_whole_line(header, entries, label):
    try:
        entry = header[entries[label]]
        return entry.strip()
    except:
        return 'To check'


def _compile_lines(header, entries, label):
    # Compile line list
    start = int(entries[label][0][1::])
    end = int(entries[label][1][1::])
    keys = [f'C{x}' for x in range(start, end+1)]
    # Get lines and compile
    lines = [header[k].strip() for k in keys]
    return '\n'.join(lines)


def get_info_from_text_header(section, template='Geo2X'):
    # Get text header and basic informations
    header = section.text_header
    t_head = {}
    # Get template
    entries = _text_header(template)
    # Get items
    t_head['client'] = _get_inline_item(header, entries, 'client')
    t_head['area'] = _get_inline_item(header, entries, 'area')
    t_head['date'] = _get_inline_item(header, entries, 'date')
    t_head['survey'] = _get_inline_item(header, entries, 'survey')
    t_head['line'] = _get_inline_item(header, entries, 'line')
    t_head['source'] = _get_inline_item(header, entries, 'source')
    t_head['sample_rate'] = _get_inline_item(header, entries, 'sample_rate')
    t_head['record_length'] = _get_inline_item(header, entries,
                                               'record_length')
    t_head['src_spacing'] = _get_inline_item(header, entries, 'shot_interval')
    t_head['rcv_spacing'] = _get_inline_item(header, entries, 'rcv_interval')
    t_head['datum'] = _get_inline_item(header, entries, 'datum')
    t_head['repl_velocity'] = _get_inline_item(header, entries,
                                               'repl_velocity')
    t_head['data_type'] = _get_inline_item(header, entries, 'data_type')
    t_head['data_sample_format'] = _get_inline_item(header,
                                                    entries,
                                                    'data_sample_format')
    t_head['byte_alloc'] = _compile_lines(header, entries, 'byte_alloc')
    t_head['processing_flow'] = _compile_lines(header, entries,
                                               'processing_flow')
    t_head['crs'] = _get_whole_line(header, entries, 'crs')
    if entries['segy_rev'].lower() != 'blank':
        t_head['segy_rev'] = _get_whole_line(header, entries, 'segy_rev')
    t_head['closure'] = _get_whole_line(header, entries, 'closure')
    # Clean parameters
    if t_head['sample_rate'] != 'To check':
        t_head['sample_rate_unit'] = re.sub("[^a-zA-Z]", '',
                                            t_head['sample_rate']).lower()
        t_head['sample_rate'] = float(re.sub("[^0-9]", '',
                                             t_head['sample_rate']))
    if t_head['record_length'] != 'To check':
        t_head['record_length_unit'] = re.sub("[^a-zA-Z]",
                                              '',
                                              t_head['record_length']).lower()
        t_head['record_length'] = float(re.sub("[^0-9]", '',
                                               t_head['record_length']))
    if t_head['src_spacing'] != 'To check':
        t_head['src_spacing_unit'] = re.sub("[^a-zA-Z]", '',
                                            t_head['src_spacing']).lower()
        t_head['src_spacing'] = float(re.sub("[^0-9]", '',
                                             t_head['src_spacing']))
    if t_head['rcv_spacing'] != 'To check':
        t_head['rcv_spacing_unit'] = re.sub("[^a-zA-Z]", '',
                                            t_head['rcv_spacing']).lower()
        t_head['rcv_spacing'] = float(re.sub("[^0-9]", '',
                                             t_head['rcv_spacing']))
    if t_head['datum'] != 'To check':
        t_head['datum_unit'] = re.sub("[^a-zA-Z]", '', t_head['datum']).lower()
        t_head['datum'] = float(re.sub("[^0-9]", '', t_head['datum']))
    if t_head['repl_velocity'] != 'To check':
        t_head['repl_velocity'] = float(re.sub("[^0-9]", '',
                                        t_head['repl_velocity']))
    if t_head['crs'] != 'To check':
        t_head['epsg'] = t_head['crs'].split('epsg:')[1]
        t_head['epsg'] = int(re.sub("[^0-9]", '', t_head['epsg']))
    if t_head['data_sample_format'] != 'To check':
        t_head['data_sample_format'] = re.sub('[^A-Za-z0-9\s]+', '',
                                              t_head['data_sample_format'])
    return t_head


def compare_text_bin_header(text_header, bin_header):
    # Compare line numbers
    print(text_header['line'])
    print(bin_header['LineNumber'])
    comparison = {'line_check': 'ok'}


    # How to get access to bin headers?

    # Compare line number

    # Compare sample interval

    # Compare n_sample per trace

    # Compare data sample format code



    return comparison

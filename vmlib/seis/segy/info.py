import re
import geopandas as gpd
import pandas as pd
import shapely as sp
import segyio


def build(segy):
    info = {}
    # Get basic statistics
    info['n_traces'] = segy.tracecount
    info['sample_rate'] = segyio.tools.dt(segy)/1000.
    info['n_samples'] = segy.samples.size
    info['trace_length'] = info['sample_rate'] * (info['n_samples'] - 1)
    info['twt'] = segy.samples
    # Get headers
    info['bin'] = segy.bin
    info['text'], info['crs'] = _parse_text_header(segy)
    info['trace'] = _parse_trace_header(segy, info)
    return info


def _parse_text_header(segy):
    raw_header = segyio.tools.wrap(segy.text[0])
    # Split on header keys
    cut_header = re.split(r'C\d{1,2}\s', raw_header)[1::]
    # Remove end of line return
    text_header = [x.replace('\n', ' ') for x in cut_header]
    text_header[-1] = text_header[-1][:-2]
    # Format in dict
    clean_header = {}
    crs = None
    i = 1
    for item in text_header:
        key = 'C' + str(i).rjust(2, '0')
        i += 1
        clean_header[key] = item
        # Get epsg
        if any(re.findall(r'epsg|EPSG', item, re.IGNORECASE)):
            crs = re.split(r'\D', item.upper().split('EPSG')[1])
            crs = max([int(x) for x in crs if len(x) > 0])
    return clean_header, crs


def _parse_trace_header(segy, info):
    # Get all header keys
    headers = segyio.tracefield.keys
    # Initialize dataframe with trace id as index and headers as columns
    df = pd.DataFrame(index=range(1, info['n_traces'] + 1),
                      columns=headers.keys())
    # Fill dataframe with all header values
    for k, v in headers.items():
        df[k] = segy.attributes(v)[:]
    # Fill the geometry
    x = df['CDP_X'] / (-df['SourceGroupScalar'])
    y = df['CDP_Y'] / (-df['SourceGroupScalar'])
    df['geometry'] = [sp.geometry.Point(xy) for xy in zip(x, y)]
    # Test crs and if valid, convert to geodataframe
    try:
        gdf = gpd.GeoDataFrame(df, geometry=df['geometry'])
        gdf.crs = {'init': f"epsg:{info['crs']}"}
        return gdf
    except:
        return df


def export_csv():
    pass


def export_shp():
    pass


def export_xls():
    pass

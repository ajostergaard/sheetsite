import os
from sheetsite.site import Site
from sheetsite.source import read_source
from sheetsite.destination import write_destination
import shutil

def apply_chain(site, path):

    if not(os.path.exists(path)):
        os.makedirs(path)

    source = site['source']
    destination = site['destination']

    wb = read_source(source)

    ss = Site(wb, os.path.join(path, 'geocache.sqlite'))
    if 'flags' in site:
        ss.configure(site['flags'])
    raw_file = os.path.join(path, 'raw.json')
    output_file = os.path.join(path, 'public.json')
    prev_raw_file = os.path.join(path, 'prev_raw.json')
    private_output_file = os.path.join(path, 'private.json')
    if os.path.exists(raw_file):
        shutil.copyfile(raw_file, prev_raw_file)

    ss.save_local(raw_file, enhance=False)
    ss.save_local(output_file)
    if not os.path.exists(prev_raw_file):
        shutil.copyfile(raw_file, prev_raw_file)
    ss.save_local(private_output_file, private_sheets=True)

    state = {
        'path': path,
        'output_file': output_file,
        'workbook': ss.public_workbook()
    }
    write_destination(destination, state)

    return {
        'prev_raw_file': prev_raw_file,
        'raw_file': raw_file
    }
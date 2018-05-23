import datetime
import os
import shutil
import subprocess


def create_dbdump():
    date_str = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    time_str = str(datetime.datetime.now().strftime('%H-%M-%S'))
    out_dir = 'dump_' + date_str + '__' + time_str
    out_name = date_str + '__' + time_str
    os.mkdir(out_dir)
    for collection in ['audiotube', 'videotube']:
        process_call_str = 'mongodump --out {0} ' \
                           '--collection users --db {1}'.format(out_dir, collection)
        status = subprocess.check_call(process_call_str, shell=True)
    filename = shutil.make_archive(out_name, 'zip', out_dir)
    return os.path.abspath(filename), os.path.abspath(out_dir)

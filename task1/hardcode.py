#!/usr/bin/env python
import time
import psutil
import subprocess
import re
import json
import argparse

from os import path


# Arguments for terminal ussage:
parser = argparse.ArgumentParser(description=format(
            'This program provides an opportunity to collect data about'
            'the selected process (cpu, rss, vms). '
            'The data is stored in the root of the program in data.json.'
            'Arguments can be passed or defaults will be used instead'
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--interpreter',
    default='python',
    type=str,
    help='interpeter of launching subprocces'
)
parser.add_argument('-p', '--path_to_process',
    default='./sleep_process.py',
    type=str,
    help='realtive or absolute path for subprocess'
)
parser.add_argument('-t', '--time_interval',
    default='1',
    type=int,
    help='data collecting time interval (sec.)'
)
args = parser.parse_args()
config = vars(args)
print(config)


# # User imput defaults:
PROC_INTERPRETER = config['interpreter']
PROC_PATH = config['path_to_process']
COLLECT_INTEVAL = config['time_interval']


def main():
    """
    Gets info (cpu/rss/vms) about selected process and pass it to data storage
    in json format.
    DATA_STORAGE path can be changed below.
    """

    DATA_STORAGE = './data.json'

    # Run subprocess:
    proc = subprocess.Popen([str(PROC_INTERPRETER), str(PROC_PATH)], shell=False)
    proc_watcher_pid = proc.pid
    print('Current sleep_proccess PID is ' + f'{proc.pid}')

    try:
        while True:
            # Init time record:
            record_time_UTC = time.gmtime()
            time_string = time.strftime('%m/%d/%Y %H:%M:%S', record_time_UTC)
            time_day = time.strftime('%m/%d/%Y', record_time_UTC)
            time_clock = time.strftime('%H:%M:%S', record_time_UTC)

            #  Collecting data about selected process:
            psu = psutil.Process(proc_watcher_pid)
            psu_cpu = psu.cpu_percent(interval=0.1)
            psu_rss = psu.memory_info().rss
            psu_vms = psu.memory_info().vms

            data = {
                'day': time_day,
                'time': time_clock,
                'cpu': psu_cpu,
                'rss': psu_rss,
                'vms': psu_rss
                }
            print('--> Collected data: ' + str(data))

            # Check if data.json exists, create if not.
            # Write data append to data.json:
            data_file = DATA_STORAGE
            listObj = []

            warning = False
            if path.isfile(data_file) is False:
                warning = True
                print('WARNING: data.json Not Found!')
            else:
                if path.getsize(data_file) == 0:
                    print('WARNING: data.json is empty. Initiating new record.')
                    pass
                else:
                    with open(data_file, 'r') as df:
                        # Handle wrong wormating in data.json:
                        try:
                            listObj = json.loads(df.read())
                        except Exception as json_e:
                            print('ERROR: ' + str(json_e))
                            print('WARNING: Wrong data format in data.json. It will be overwriten!')
                            raise Exception(json_e)

            listObj.append(data)

            # overwriting data.json:
            with open(data_file, 'w') as json_file:
                json.dump(listObj, json_file,
                                indent=4,
                                separators=(',',': '))
            if warning:
                print('WARNING: New data.json was created!')

            time.sleep(int(COLLECT_INTEVAL))

    except (Exception, KeyboardInterrupt) as e:
        print('ERROR: ' + str(e))

        subprocess.call(['kill', '-9', '%d' % proc.pid])
        print(f'{proc.pid}' + ' sleep_process.py ' + 'terminated')


if __name__ == "__main__":
    main()

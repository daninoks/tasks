#!/usr/bin/env python
import argparse
import os
import shutil
import time




# Arguments for terminal ussage:
parser = argparse.ArgumentParser(description='Arguments can be passed or defaults will be used instead',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-s', '--source_dir',
    default='./source_dir',
    type=str,
    help='realtive or absolute path for source directory'
)
parser.add_argument('-r', '--replica_dir',
    default='./replica_dir',
    type=str,
    help='realtive or absolute path for replica directory'
)
parser.add_argument('-t', '--time_interval',
    default='10',
    type=int,
    help='Synchronization interval.(sec.)'
)
parser.add_argument('-l', '--logs_dir',
    default='./logs',
    type=str,
    help='Insert path for creation/copying/removal logs'
)
args = parser.parse_args()
config = vars(args)
print(config)


SOURCE_DIR = config['source_dir']
REPLICA_DIR = config['replica_dir']
TIME_INTERVAL = config['time_interval']
LOGS_DIR = config['logs_dir']


print(f'# Current Source directory is {SOURCE_DIR}')
print(f'# Current Source Replica directory is {REPLICA_DIR}')
print(f'# Choosen Synchronization time interval is {TIME_INTERVAL}')
print(f'# Synchronization logs will be stored at {LOGS_DIR}')

def main():
    ERROR_MSG = ''
    try:
        while True:
            # Init time record:
            record_time_UTC = time.gmtime()
            time_string = time.strftime('%m/%d/%Y %H:%M:%S', record_time_UTC)
            time_day = time.strftime('%m/%d/%Y', record_time_UTC)
            time_clock = time.strftime('%H:%M:%S', record_time_UTC)

            copied = []
            created = []
            removed = []

            sd_content = os.listdir(SOURCE_DIR)
            rd_content = os.listdir(REPLICA_DIR)

            #  Create REPLICA_DIR if not exist:
            if not os.path.exists(REPLICA_DIR):
                os.mkdir(REPLICA_DIR)
                print(f'---> REPLICA_DIR just created! path: {REPLICA_DIR}')

            # Copy files:
            for sd_item in sd_content:
                if sd_item not in rd_content:
                    created.append(sd_item)

                try:
                    shutil.copy(f'{SOURCE_DIR}/{sd_item}', REPLICA_DIR)
                    print(f'---> {sd_item} copied to {SOURCE_DIR}/{sd_item} successfully')
                    copied.append(sd_item)

                # If source and destination are same:
                except shutil.SameFileError:
                    e = 'EROROR: Source and destination represents the same file.'
                    ERROR_MSG += f'{e}\n'
                    print(e)
                    raise Exception(e)
                # If there is any permission issue:
                except PermissionError:
                    e = 'ERROR: Permission denied.'
                    ERROR_MSG += f'{e}\n'
                    print(e)
                    raise Exception(e)
                # For other errors
                except Exception as e:
                    ERROR_MSG += f'{e}\n'
                    print('ERROR: ' + str(e))
                    raise Exception(e)

            print(rd_content)
            # Remove deleted files:
            for rd_item in rd_content:
                if rd_item not in sd_content:
                    try:
                        os.remove(f'{REPLICA_DIR}/{rd_item}')
                        print(f'---> {rd_item} removed from {REPLICA_DIR}/{rd_item} successfully.')
                        removed.append(rd_item)

                    # If there is any permission issue:
                    except PermissionError:
                        e = 'ERROR: Permission denied.'
                        ERROR_MSG += f'{e}\n'
                        print(e)
                        raise Exception(e)
                    # For other errors:
                    except Exception as e:
                        ERROR_MSG += f'{e}\n'
                        print('ERROR: ' + str(e))
                        raise Exception(e)

            if ERROR_MSG:
                data = format(
                    f'--- {time_string}\n' \
                    f'Synchronization {SOURCE_DIR} to {REPLICA_DIR} finished with followind ERROR(s):\n' \
                    f'{ERROR_MSG}' \
                )
            else:
                data = format(
                    f'--- {time_string}\n' \
                    f'Synchronization {SOURCE_DIR} to {REPLICA_DIR} completed:\n' \
                    f'--copied:  {copied}\n' \
                    f'--created: {created}\n' \
                    f'--removed: {removed}\n' \
                )
            print(data)

            try:
                #  Create LOGS_DIR if not exist:
                if not os.path.exists(LOGS_DIR):
                    os.mkdir(LOGS_DIR)
                    print(f'---> LOGS_DIR just created! path: {LOGS_DIR}')

                with open(f'{LOGS_DIR}/sync.log', "a") as file_object:
                    # Append at the end of file:
                    file_object.write(data)
            # If there is any permission issue:
            except PermissionError:
                e = 'ERROR: Permission denied.'
                print(e)
                raise Exception(e)

            time.sleep(TIME_INTERVAL)

    except Exception as err:
        print('ERROR: ' + str(err))
    except KeyboardInterrupt as err:
        print(' Stoped: get KeyboardInterrupt signal')



if __name__ == "__main__":
    main()

import subprocess
import re
from datetime import datetime,timedelta
import argparse
import os
import sys
import configuration
import reporter
import xls


def start():

    parser = argparse.ArgumentParser()
    parser.add_argument("--date_start", dest = 'date_start', type = str,
                        help="Format: yyyy.mm.dd. Start date of period.", default = 'None')
    parser.add_argument("--date_end", dest='date_end', type=str,
                        help="Format: yyyy.mm.dd. end date of period", default = 'None')

    args = parser.parse_args()

    date_start_str = args.date_start
    date_end_str = args.date_end
    date_start_is_valid  = check_date(date_start_str)
    date_end_is_valid = check_date(date_end_str)
    if date_start_is_valid & date_end_is_valid == False:
        print("Please, use specific format for date: yyyy.mm.dd")
        exit()


    credential = configuration.init_config()
    print('Enter Project Name:')
    project_key = input()
    date_start = date_start_str.replace('.','-')
    date_end = date_end_str.replace('.', '-')

    worklog_info_list = reporter.get_report(project_key, credential, date_start, date_end)
    excell_filename = xls.write_report(worklog_info_list, f"{date_start_str}-{date_end_str}")

    # After report creating, open it
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', excell_filename))
    elif os.name == 'nt':  # For Windows
        os.startfile(excell_filename)
    elif os.name == 'posix':  # For Linux, Mac, etc.
        subprocess.call(('xdg-open', excell_filename))

def check_date(date: str):
    if re.search(r'\d{4}.\d{2}.\d{2}', date): return True
    else: return False

if __name__ == "__main__":
    start()

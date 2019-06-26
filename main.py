import subprocess
import re
import os
import sys
import configuration
import reporter
import xls
from datetime import timedelta

def start():
    credential = configuration.init_config()
    print('Enter Project Name:')
    project_key = input()
    print('Enter date start (yyyy-mm-dd):')
    date_start_str = input()
    print('Enter date end (yyyy-mm-dd):')
    date_end_str = input()

    date_start_is_valid  = check_date(date_start_str)
    date_end_is_valid = check_date(date_end_str)
    if date_end_str == '':
        end_date_is_auto = True
        date_end_is_valid = False


    if date_start_is_valid == False or (date_end_is_valid == False and date_end_str !='') :
        print("Please, use specific format for date: yyyy-mm-dd")
        input()
        os.exit()
    date_start = reporter.convert_date(date_start_str)
    if date_end_is_valid:
        date_end = reporter.convert_date(date_end_str)
    elif end_date_is_auto:
        date_end = date_start + timedelta(days=5)
        date_end_str = str(date_end.date())
    else:
        print("Something goes wrong, please try again")
        input()
    worklog_info_list = reporter.get_report(project_key, credential, date_start_str, date_end_str, date_start, date_end)
    excell_filename = xls.write_report(worklog_info_list, f"{date_start_str}-{date_end_str}")

    # After report creating, open it
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', excell_filename))
    elif os.name == 'nt':  # For Windows
        os.startfile(excell_filename)
    elif os.name == 'posix':  # For Linux, Mac, etc.
        subprocess.call(('xdg-open', excell_filename))

def check_date(date: str):
    if re.search(r'\d{4}-\d{2}-\d{2}', date): return True
    else: return False

if __name__ == "__main__":
    start()

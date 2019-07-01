"""Jira Work Logger. Author timoha199490@gmail.com"""
import os
import sys
import re
import subprocess
from datetime import timedelta
import reporter
import configuration
import xls


def start():
    """Main method"""
    configuration.init_config()
    print('Enter Project Name:')
    project_key = input()
    print('Enter date start (yyyy-mm-dd):')
    date_start_str = input()
    print('Enter date end (yyyy-mm-dd). You can skip it, date will be +1 weak:')
    date_end_str = input()

    date_start_is_valid = check_date(date_start_str)
    date_end_is_valid = check_date(date_end_str)
    if date_end_str == '':
        end_date_is_auto = True
        date_end_is_valid = False

    if date_start_is_valid is False or (date_end_is_valid  is False and date_end_str != ''):
        print("Please, use specific format for date: yyyy-mm-dd")
        input()
        exit()
    date_start = reporter.convert_date(date_start_str)
    if date_end_is_valid:
        date_end = reporter.convert_date(date_end_str)
    elif end_date_is_auto:
        date_end = date_start + timedelta(days=6)
        date_end_str = str(date_end.date())
    else:
        print("Something goes wrong, please try again")
        input()
    work_log_info_list = reporter.get_report(project_key, date_start_str, date_end_str, date_start, date_end)
    excel_filename = xls.write_report(work_log_info_list, f"{date_start_str}-{date_end_str}")

    if sys.platform.startswith('darwin'):
        subprocess.call(('open', excel_filename))
    elif os.name == 'nt':
        os.startfile(excel_filename)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', excel_filename))


def check_date(date: str):
    """Checking param date(str) with regex"""
    if re.search(r'\d{4}-\d{2}-\d{2}', date):
        return True
    return False

if __name__ == "__main__":
    start()

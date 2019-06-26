from jira import JIRA
import subprocess
import re
from datetime import datetime,timedelta
import os
import sys
import openpyxl
import argparse
import configuration
import reporter


def write_report(worklog_info_list: list, work_date_str: str):
    wb = openpyxl.Workbook()
    worksheet = wb['Sheet']

    # Create header in report
    worksheet['A1'] = 'ProjectName'
    worksheet['B1'] = 'IssueKey'
    worksheet['C1'] = 'Summary'
    worksheet['D1'] = 'Assignee'
    worksheet['E1'] = 'IssueType'
    worksheet['F1'] = 'Status'
    worksheet['G1'] = 'Description'
    worksheet['H1'] = 'LogWorkDate'
    worksheet['I1'] = 'LogWorkTime'
    worksheet['J1'] = 'TimeSpent'

    column_num = 2
    # Write report data
    for worklog_info_item in worklog_info_list:
        i = str(column_num)
        worksheet['A' + i] = worklog_info_item.ProjectName
        worksheet['B' + i] = worklog_info_item.IssueKey
        worksheet['C' + i] = worklog_info_item.Summary
        worksheet['D' + i] = worklog_info_item.Assignee
        worksheet['E' + i] = worklog_info_item.IssueType
        worksheet['F' + i] = worklog_info_item.Status
        worksheet['G' + i] = worklog_info_item.Description
        worksheet['H' + i] = worklog_info_item.LogWorkDate
        worksheet['I' + i] = worklog_info_item.LogWorkTime
        worksheet['J' + i] = worklog_info_item.TimeSpent
        column_num += 1
    excell_filename = work_date_str + '_report.xlsx'
    wb.save(excell_filename)
    print('Report is ready!')

    return excell_filename
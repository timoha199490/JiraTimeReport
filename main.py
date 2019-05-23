from jira import JIRA
import subprocess
import re
from datetime import datetime,timedelta
import os
import sys
import openpyxl
import configparser



def start():
    class WorklogInfo:
        ProjectName = ''
        IssueKey = ''
        Summary = ''
        Assignee = ''
        IssueType = ''
        Status = ''
        Description = ''
        TimeSpent = ''
        LogWorkDate = ''
        LogWorkTime = ''

    if os.path.isfile('./config.ini'):
        config = configparser.ConfigParser()
        config.sections()
        config.read('config.ini')
        login = config['DEFAULT']['Login']
        api_key = config['DEFAULT']['ApiKey']
        server = config['DEFAULT']['Server']
    else:
        print('Enter jira login(format - user@domain.com):')
        login = input()
        print('Enter Jira API key(instruction here https://confluence.atlassian.com/cloud/api-tokens-938839638.html):')
        api_key = input()
        print('Enter jira URI:')
        server = input()

        config = configparser.ConfigParser()
        config['DEFAULT'] = {'Login': login,
                             'ApiKey': api_key,
                             'Server': server}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    result = True
    while result:
        print('Enter date (format YYYY-mm-dd):')
        date = input()
        work_date_raw = re.search(r'(\d{4}-\d{2}-\d{2})', date)
        if work_date_raw is not None:
            work_date = datetime.strptime(work_date_raw.group(0), '%Y-%m-%d')
            work_week_day = work_date.isocalendar()[2]
            week_start = work_date + timedelta(days=-work_date.isocalendar()[2] + 1)
            result = False

    print('Enter Project Name:')
    project_key = input()

    jira_options = {'server': server}
    jira = JIRA(options=jira_options, basic_auth=(login, api_key))



    jql_str = 'project = ' + project_key + ' AND  worklogDate >= ' + work_date_raw.group(0) + ' ORDER BY created DESC'

    issues_list = jira.search_issues(jql_str)
    worklog_info_list = []

    work_weak = work_date.isocalendar()[1]

    for issue_item in issues_list:
        issue = jira.issue(issue_item.key)
        issue_worklogs = issue.fields.worklog.worklogs

        for worklog in issue_worklogs:
            worklog_date_str = re.search(r'(\d{4}-\d{2}-\d{2})', worklog.started)
            worklog_date = datetime.strptime(worklog_date_str.group(0), '%Y-%m-%d')
            if worklog_date.isocalendar()[1] == work_weak:
                log_work_date = re.search(r'\d{4}-\d{2}-\d{2}', worklog.started)
                log_work_time = re.search(r'\d{2}:\d{2}:\d{2}', worklog.started)

                worklog_info = WorklogInfo()
                worklog_info.IssueKey = str('=HYPERLINK("' + server + '/browse/' + issue.key + '","' + issue.key + '")')
                worklog_info.TimeSpent = (str(int(worklog.timeSpentSeconds) / 3600))
                worklog_info.Assignee = str(worklog.updateAuthor.displayName)
                worklog_info.ProjectName = str(issue.fields.project.name)
                worklog_info.Summary = str(issue.fields.summary)
                worklog_info.IssueType = str(issue.fields.issuetype.name)
                worklog_info.LogWorkDate = str(log_work_date.group(0))
                worklog_info.LogWorkTime = str(log_work_time.group(0))
                worklog_info.Description = str(issue.fields.description).strip()
                worklog_info.Status = str(issue.fields.status.name)
                worklog_info_list.append(worklog_info)


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

    j = 2
    # Write report data
    for worklog_info_item in worklog_info_list:
        i = str(j)
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
        j += 1
    excell_filename = work_date_raw.group(0) + '_report.xlsx'
    wb.save(excell_filename)
    print('Report is ready!')

    # After report creating, open it
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', excell_filename))
    elif os.name == 'nt':  # For Windows
        os.startfile(excell_filename)
    elif os.name == 'posix':  # For Linux, Mac, etc.
        subprocess.call(('xdg-open', excell_filename))
    input()

if __name__ == "__main__":
    start()

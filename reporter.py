from jira import JIRA
import subprocess
import re
from datetime import datetime,timedelta
import os
import sys
import openpyxl
import argparse
from configuration import Credential
from worcklogdata import WorklogInfo

def get_report(project_key: str, credential: Credential, work_date_start_str, work_date_end_str, work_date_start, work_date_end):

    jira_options = {'server': credential.ServerUrl}
    jira = JIRA(options=jira_options, basic_auth=(credential.Login, credential.ApiKey))
    jql_str = f"project = {project_key} AND worklogDate >= {work_date_start_str} AND worklogDate <= {work_date_end_str} ORDER BY created DESC"
    issues_list = jira.search_issues(jql_str)
    worklog_info_list = []


    for issue_item in issues_list:
        issue = jira.issue(issue_item.key)
        issue_worklogs = issue.fields.worklog.worklogs

        for worklog in issue_worklogs:


            log_work_date_str = re.search(r'\d{4}-\d{2}-\d{2}', worklog.started)
            log_work_time = re.search(r'\d{2}:\d{2}:\d{2}', worklog.started)
            log_work_date = datetime.strptime(log_work_date_str.group(0), '%Y-%m-%d')


            if log_work_date >= work_date_start and log_work_date <= work_date_end:
                worklog_info = WorklogInfo()
                worklog_info.IssueKey = str('=HYPERLINK("' + credential.ServerUrl + '/browse/' + issue.key + '","' + issue.key + '")')
                worklog_info.TimeSpent = (str(int(worklog.timeSpentSeconds) / 3600))
                worklog_info.Assignee = str(worklog.updateAuthor.displayName)
                worklog_info.ProjectName = str(issue.fields.project.name)
                worklog_info.Summary = str(issue.fields.summary)
                worklog_info.IssueType = str(issue.fields.issuetype.name)
                worklog_info.LogWorkDate = str(log_work_date_str.group(0))
                worklog_info.LogWorkTime = str(log_work_time.group(0))
                worklog_info.Description = str(issue.fields.description).strip()
                worklog_info.Status = str(issue.fields.status.name)
                worklog_info_list.append(worklog_info)

    return worklog_info_list
def convert_date(date: str):
    return datetime.strptime(date, '%Y-%m-%d')
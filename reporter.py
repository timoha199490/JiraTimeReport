from datetime import datetime
import re
from jira import JIRA
from configuration import init_config


class WorkLogInfo:
    project_name: str
    issue_key: str
    summary: str
    assignee: str
    issue_type: str
    status: str
    description: str
    time_spent: str
    log_work_date: str
    log_work_time: str


def get_report(project_key, work_date_start_str,
               work_date_end_str, work_date_start, work_date_end):
    credential = init_config()
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
                worklog_info = WorkLogInfo()
                worklog_info.issue_key = str('=HYPERLINK("' + credential.ServerUrl +
                                            '/browse/' + issue.key + '","' + issue.key + '")')
                worklog_info.time_spent = (str(int(worklog.timeSpentSeconds) / 3600))
                worklog_info.assignee = str(worklog.updateAuthor.displayName)
                worklog_info.project_name = str(issue.fields.project.name)
                worklog_info.summary = str(issue.fields.summary)
                worklog_info.issue_type = str(issue.fields.issuetype.name)
                worklog_info.log_work_date = str(log_work_date_str.group(0))
                worklog_info.log_work_time = str(log_work_time.group(0))
                worklog_info.description = str(issue.fields.description).strip()
                worklog_info.status = str(issue.fields.status.name)
                worklog_info_list.append(worklog_info)
    return worklog_info_list


def convert_date(date: str):
    return datetime.strptime(date, '%Y-%m-%d')

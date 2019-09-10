"""Connect to jira and get report. Author timoha@gmail.com"""
from datetime import datetime
import re
from jira import JIRA
from configuration import init_config


class WorkLogInfo:
    """Structure for saving work log"""
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

    def __init__(self):
        """Constructor"""
        pass


def get_report(project_key, work_date_start_str,
               work_date_end_str, work_date_start, work_date_end):
    undefined = object()

    """Get report from jira project via jira client. Using JQL filter"""
    credential = init_config()
    jira_options = {'server': credential.server_url}
    jira = JIRA(options=jira_options, basic_auth=(credential.login, credential.api_key))
    jql_str = f"project = {project_key} AND worklogDate >= {work_date_start_str} AND worklogDate <= {work_date_end_str} ORDER BY created DESC"
    issues_list = jira.search_issues(jql_str)
    worklog_info_list = []

    for issue_item in issues_list:
        issue = jira.issue(issue_item.key)
        issue_work_logs = issue.fields.worklog.worklogs

        for work_log in issue_work_logs:
            log_work_date_str = re.search(r'\d{4}-\d{2}-\d{2}', work_log.started)
            log_work_time = re.search(r'\d{2}:\d{2}:\d{2}', work_log.started)
            log_work_date = datetime.strptime(log_work_date_str.group(0), '%Y-%m-%d')

            if log_work_date >= work_date_start and log_work_date <= work_date_end:
                work_log_info = WorkLogInfo()
                work_log_info.issue_key = str(f'=HYPERLINK("{credential.server_url}/browse/{issue.key}","{issue.key}")')
                work_log_info.time_spent = (str(int(work_log.timeSpentSeconds) / 3600))
                work_log_info.assignee = str(work_log.updateAuthor.displayName)
                work_log_info.project_name = str(issue.fields.project.name)
                work_log_info.summary = str(issue.fields.summary)
                work_log_info.issue_type = str(issue.fields.issuetype.name)
                work_log_info.log_work_date = str(log_work_date_str.group(0))
                work_log_info.log_work_time = str(log_work_time.group(0))
                work_log_comment = getattr(work_log, "comment", undefined)
                if work_log_comment is not undefined:
                    work_log_info.description = work_log_comment
                else:
                    work_log_info.description = str(issue.fields.summary)
                work_log_info.status = str(issue.fields.status.name)
                worklog_info_list.append(work_log_info)
    return worklog_info_list


def convert_date(date: str):
    """Convert date from string to specific format"""
    return datetime.strptime(date, '%Y-%m-%d')

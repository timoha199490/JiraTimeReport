import openpyxl


def write_report(worklog_info_list: list, work_date_str: str):
    workbook = openpyxl.Workbook()
    worksheet = workbook['Sheet']

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
        worksheet['A' + i] = worklog_info_item.project_name
        worksheet['B' + i] = worklog_info_item.issue_key
        worksheet['C' + i] = worklog_info_item.summary
        worksheet['D' + i] = worklog_info_item.assignee
        worksheet['E' + i] = worklog_info_item.issue_type
        worksheet['F' + i] = worklog_info_item.status
        worksheet['G' + i] = worklog_info_item.description
        worksheet['H' + i] = worklog_info_item.log_work_date
        worksheet['I' + i] = worklog_info_item.log_work_time
        worksheet['J' + i] = worklog_info_item.time_spent
        column_num += 1
    excell_filename = work_date_str + '_report.xlsx'
    workbook.save(excell_filename)
    print('Report is ready!')

    return excell_filename

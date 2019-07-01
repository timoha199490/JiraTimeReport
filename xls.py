"""Working with excel file. Author timoha199490@gmail.com"""
import openpyxl


def write_report(worklog_info_list: list, work_date_str: str):
    """Writing report data to excel file"""
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
    for work_log_info_item in worklog_info_list:
        i = str(column_num)
        worksheet['A' + i] = work_log_info_item.project_name
        worksheet['B' + i] = work_log_info_item.issue_key
        worksheet['C' + i] = work_log_info_item.summary
        worksheet['D' + i] = work_log_info_item.assignee
        worksheet['E' + i] = work_log_info_item.issue_type
        worksheet['F' + i] = work_log_info_item.status
        worksheet['G' + i] = work_log_info_item.description
        worksheet['H' + i] = work_log_info_item.log_work_date
        worksheet['I' + i] = work_log_info_item.log_work_time
        worksheet['J' + i] = work_log_info_item.time_spent
        column_num += 1
    excel_filename = work_date_str + '_report.xlsx'
    workbook.save(excel_filename)
    print('Report is ready!')

    return excel_filename

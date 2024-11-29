employee_path_stem = "employees"
position_path_stem = "positions"
timesheet_path_stem = "timesheet"

csv_schemas = {
    employee_path_stem: ("employee_full_name", "position_nm"),
    position_path_stem: ("position_nm", "hh_billing_rate"),
    timesheet_path_stem: ("task_cd", "employee_full_name", "task_start_dttm", "task_end_dttm"),
}

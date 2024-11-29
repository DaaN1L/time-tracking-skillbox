csv_schemas = {
    "employees": ("employee_full_name", "position_nm"),
    "positions": ("position_nm", "hh_billing_rate"),
    "timesheet": ("task_cd", "employee_full_name", "task_start_dttm", "task_end_dttm"),
}
employee_path_stem = "employees"
position_path_stem = "positions"

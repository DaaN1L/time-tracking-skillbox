from pathlib import Path

from ..utils import read_csv, pprint
from ..exceptions import InvalidInFilename
from ..engine import engine
from ..crud import (
    insert_employee,
    insert_position,
    insert_timesheet,
    insert_task,
    get_employee_names,
    get_employee_timesheet,
    del_employee_timesheet,
    get_top_n_long_tasks,
    get_top_n_employees_worked_the_most,
    get_top_n_cost_tasks,
)
from ...constants import (
    csv_schemas,
    employee_path_stem,
    position_path_stem
)


def insert_from_csv(
        path: str
):
    path_resolved = Path(path).resolve()
    filename = path_resolved.stem
    if filename not in csv_schemas.keys():
        raise InvalidInFilename
    data = read_csv(path_resolved, header=csv_schemas[filename])

    with engine.connect() as conn:
        conn.begin()
        if filename == position_path_stem:
            insert_position(conn, data)
        elif filename == employee_path_stem:
            insert_employee(conn, data)
        else:
            unique_task_codes = {d["task_cd"] for d in data}
            task_data = [{"task_cd": cd} for cd in unique_task_codes]
            insert_task(conn, task_data)
            insert_timesheet(conn, data)
        conn.commit()


def print_employee_names():
    with engine.connect() as conn:
        pprint(get_employee_names(conn), show_index=True)


def print_employee_timesheet(employee_full_name: str):
    with engine.connect() as conn:
        pprint(get_employee_timesheet(conn, employee_full_name), show_index=True)


def delete_employee_timesheet(employee_full_name: str):
    with engine.connect() as conn:
        conn.begin()
        del_employee_timesheet(conn, employee_full_name)
        conn.commit()


def print_top_n_cost_tasks(n: int):
    with engine.connect() as conn:
        pprint(get_top_n_cost_tasks(conn, n), show_index=True)


def print_top_n_long_tasks(n: int):
    with engine.connect() as conn:
        pprint(get_top_n_long_tasks(conn, n), show_index=True)


def print_top_n_employees_worked_the_most(n: int):
    with engine.connect() as conn:
        pprint(get_top_n_employees_worked_the_most(conn, n), show_index=True)

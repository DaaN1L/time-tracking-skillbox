from typing import Any

import sqlalchemy
from sqlalchemy import (
    delete,
    insert,
    select,
    bindparam,
    text,
    desc
)
from sqlalchemy.engine import Connection, CursorResult
from sqlalchemy.sql.elements import OperatorExpression
from sqlalchemy import func as f


from .models import (
    Position,
    Task,
    Employee,
    Timesheet,
)


def _insert(
        conn: Connection,
        data: list[dict[Any]],
        model,
        subq: dict[str] | None = None,
        verbose: bool = True,
        ignore: bool = True,
) -> int:
    stmt = insert(model)
    if ignore:
        stmt = stmt.prefix_with("IGNORE")
    if subq:
        stmt = stmt.values(**subq)
    result = conn.execute(stmt, data)
    inserted_cnt: int = result.rowcount  # noqa
    if verbose:
        print(f"Table: {model.__tablename__}")
        print(f"Imported: {inserted_cnt} rows")

        incorrect_cnt = len(data) - inserted_cnt
        if incorrect_cnt:
            print(f"Incorrect: {incorrect_cnt} rows")
    return inserted_cnt


def _delete(
        conn: Connection,
        model,
        where_expr: OperatorExpression | list[OperatorExpression] | None = None,
        verbose: bool = True,
) -> int:
    if where_expr is None:
        where_expr = []
    if not isinstance(where_expr, list):
        where_expr = [where_expr]

    stmt = delete(model)
    for expr in where_expr:
        stmt = stmt.where(expr)

    result = conn.execute(stmt)
    deleted_cnt: int = result.rowcount  # noqa
    if verbose:
        print(f"Table: {model.__tablename__}")
        print(f"Deleted: {deleted_cnt} rows")
    return deleted_cnt


def insert_employee(
        conn: Connection,
        data: list[dict[str]],
) -> int:
    position_id_subq = (
        select(Position.position_id)
        .where(Position.position_nm == bindparam("position_nm"))
        .scalar_subquery()
    )
    return _insert(
        conn,
        data,
        Employee,
        {"position_id": position_id_subq},
    )


def insert_position(
        conn: Connection,
        data: list[dict[str]],
) -> int:
    return _insert(conn, data, Position)


def insert_task(
        conn: Connection,
        data: list[dict[str]],
) -> int:
    return _insert(conn, data, Task)


def insert_timesheet(
        conn: Connection,
        data: list[dict[str]],
) -> int:
    task_id_subq = (
        select(Task.task_id)
        .where(Task.task_cd == bindparam("task_cd"))
        .scalar_subquery()
    )
    employee_id_subq = (
        select(Employee.employee_id)
        .where(Employee.employee_full_name == bindparam("employee_full_name"))
        .scalar_subquery()
    )
    return _insert(
        conn,
        data,
        Timesheet,
        {"task_id": task_id_subq, "employee_id": employee_id_subq},
    )


def get_employee_names(conn) -> CursorResult:
    return conn.execute(select(Employee.employee_full_name))


def get_employee_timesheet(conn: Connection, employee_full_name: str):
    stmt = (
        select(
            Employee.employee_full_name,
            Task.task_cd,
            Timesheet.task_start_dttm,
            Timesheet.task_end_dttm
        )
        .where(Employee.employee_full_name == employee_full_name)
        .select_from(Employee)
        .join(Timesheet)
        .join(Task)
    )
    return conn.execute(stmt)


def del_employee_timesheet(conn: Connection, employee_full_name: str) -> int:
    where_expr = [
        Employee.employee_id == Timesheet.employee_id,
        Employee.employee_full_name == employee_full_name
    ]
    return _delete(conn, Timesheet, where_expr)


def get_top_n_long_tasks(conn: Connection, n: int) -> CursorResult:
    stmt = (
        select(
            Task.task_cd,
            f.sum(f.TIMESTAMPDIFF(
                text("HOUR"),
                Timesheet.task_start_dttm,
                Timesheet.task_end_dttm
            )).label("spent_hours")
        )
        .join(Task)
        .group_by(Task.task_cd)
        .order_by(desc("spent_hours"))
        .limit(n)
    )
    return conn.execute(stmt)


def get_top_n_employees_worked_the_most(conn: Connection, n: int) -> CursorResult:
    stmt = (
        select(
            Employee.employee_full_name,
            f.sum(f.TIMESTAMPDIFF(
                text("HOUR"),
                Timesheet.task_start_dttm,
                Timesheet.task_end_dttm
            )).label("spent_hours")
        )
        .join(Employee)
        .group_by(Employee.employee_id)
        .order_by(desc("spent_hours"))
        .limit(n)
    )
    return conn.execute(stmt)


def get_top_n_cost_tasks(conn: Connection, n: int) -> CursorResult:
    # Потрачено денег на задачу в разбивке по позициям
    money_spent_cte = (
        select(Timesheet.task_id,
               (f.sum(f.TIMESTAMPDIFF(text("HOUR"),
                                      Timesheet.task_start_dttm,
                                      Timesheet.task_end_dttm)) * Position.hh_billing_rate).label("money_spent"))
        .select_from(Timesheet)
        .join(Employee)
        .join(Position)
        .group_by(Timesheet.task_id, Position.position_id)
    ).cte()

    stmt = (
        select(Task.task_cd,
               f.sum(money_spent_cte.c.money_spent).label("total_money_spent"))
        .join_from(money_spent_cte, Task,
                   Task.task_id == money_spent_cte.c.task_id)
        .group_by(Task.task_cd)
        .order_by(desc("total_money_spent"))
        .limit(n)
    )
    return conn.execute(stmt)

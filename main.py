import click

from src.database.queries import *


@click.group()
def cli():
    ...


@cli.command(name="import")
@click.argument("path")
def import_(path: str):
    insert_from_csv(path)


@cli.command()
@click.argument("employee_name")
def get(employee_name: str):
    print_employee_timesheet(employee_name)


@cli.command()
@click.argument("employee_name")
def remove(employee_name: str):
    delete_employee_timesheet(employee_name)


# report subgroup
# ——————————————————————————
@cli.group()
def report():
    ...


@report.command(name="top5longTasks")
def top_5_long_tasks():
    print_top_n_long_tasks(5)


@report.command(name="top5costTasks")
def top_5_cost_tasks():
    print_top_n_cost_tasks(5)


@report.command(name="top5employees")
def top_5_employees():
    print_top_n_employees_worked_the_most(5)


# list subgroup
# ——————————————————————————
@cli.group(name="list")
def list_():
    ...


@list_.command(name="employee")
def list_employee():
    print_employee_names()


if __name__ == '__main__':
    cli()

import datetime as dt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Position(Base):
    __tablename__ = "position"

    position_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    position_nm: Mapped[str] = mapped_column(unique=True)
    hh_billing_rate: Mapped[int]

    employees: Mapped[list["Employee"]] = relationship(back_populates="position")


class Employee(Base):
    __tablename__ = "employee"

    employee_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_full_name: Mapped[str] = mapped_column(unique=True)
    position_id: Mapped[int] = mapped_column(ForeignKey("position.position_id"))

    position: Mapped[Position] = relationship(back_populates="employees")
    task_work: Mapped[list["Timesheet"]] = relationship(back_populates="employee")


class Task(Base):
    __tablename__ = "task"

    task_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_cd: Mapped[str] = mapped_column(unique=True)

    timesheets: Mapped[list["Timesheet"]] = relationship(back_populates="task")


class Timesheet(Base):
    __tablename__ = "timesheet"

    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.employee_id"), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.task_id"), primary_key=True)
    task_start_dttm: Mapped[dt.datetime] = mapped_column(primary_key=True)
    task_end_dttm: Mapped[dt.datetime]

    employee: Mapped[Employee] = relationship(back_populates="task_work")
    task: Mapped[Task] = relationship(back_populates="timesheets")

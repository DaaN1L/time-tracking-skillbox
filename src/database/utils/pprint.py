from tabulate import tabulate
from sqlalchemy.engine import CursorResult


def pprint(result: CursorResult, show_index: bool = False) -> None:
    print(tabulate(
        result.all(),
        result.keys(),  # noqa
        showindex=show_index,
        tablefmt="psql",
    ))

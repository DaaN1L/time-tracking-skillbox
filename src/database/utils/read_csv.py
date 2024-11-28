from pathlib import Path
import csv


def read_csv(
        path: str | Path,
        header: tuple[str, ...],
        delimiter=","
) -> list[dict[str]]:
    if isinstance(path, str):
        path = Path(path).resolve()
    with open(path, "r") as fin:
        csv_reader = csv.DictReader(fin, fieldnames=header, delimiter=delimiter)
        result = [row for row in csv_reader]
        return result  # noqa

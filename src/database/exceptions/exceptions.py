class InvalidInFilename(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "The filename must be one of: " \
                       "positions.csv, employees.csv, timesheet.csv"

    def __str__(self):
        return self.message

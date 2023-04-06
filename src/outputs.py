import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (BASE_DIR, DATETIME_FORMAT, DEFAULT_OUTPUT, FILE_OUTPUT,
                       PRETTY_TABLE_OUTPUT, RESULTS_DIR)

FILE_SAVE = 'Файл с результатами был сохранён: {}'


def default_output(results, *args):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args, *args):
    results_dir = BASE_DIR / RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        csv.writer(
          f, dialect=csv.excel
        ).writerows(
          results
        )
    logging.info(FILE_SAVE.format(file_path))


OUTPUT_FUNCTIONS = {
    PRETTY_TABLE_OUTPUT: pretty_output,
    FILE_OUTPUT: file_output,
    DEFAULT_OUTPUT: default_output
}


def control_output(results, cli_args):
    OUTPUT_FUNCTIONS.get(
        cli_args.output,
        OUTPUT_FUNCTIONS[DEFAULT_OUTPUT]
        )(results, cli_args)

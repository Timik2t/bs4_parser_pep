import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import DATETIME_FORMAT, BASE_DIR


FILE_SAVE = 'Файл с результатами был сохранён: {}'


def control_output(results, cli_args):
    output_functions = {
        'pretty': pretty_output,
        'file': file_output,
        'default': default_output
    }
    output = cli_args.output
    output_function = output_functions.get(output, output_functions['default'])
    output_function(results, cli_args)


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
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, dialect=csv.excel)
        writer.writerows(results)
    logging.info(FILE_SAVE.format(file_path))

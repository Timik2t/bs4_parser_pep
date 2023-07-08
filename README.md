# Парсер документации python и PEP

## Описание

Парсер информации из **<https://docs.python.org/3/>** и **<https://peps.python.org/>**

## Технологии

Python 3.9

beautifulsoup4 4.9

prettytable 2.1

requests-cache 1.0

## Подготовка и запуск проекта

1. Склонируйте репозиторий на локальную машину:

    ```bash
    git clone git@github.com:Timik2t/bs4_parser_pep.git
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    ```

    Активация окружения
    ```bash
    # Windows
    source venv/Scripts/activate
    ```
    ```bash
    # Linux
    source venv/bin/activate
    ```
3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

5. Смените директорию на src/

    ```bash
    cd src/
    ```

6. Запустите файл main.py выбрав необходимый парсер и аргументы(приведены ниже)

    ```bash
    python main.py [вариант парсера] [аргументы]
    ```
## Выбор парсера
##№ Встроенные парсеры

- whats-new
Парсер выводящий спсок изменений в python.

    ```bash
    python main.py whats-new
    ```

- latest_versions
Парсер выводящий список версий python и ссылки на их документацию.

    ```bash
    python main.py latest-versions
    ```

- download
Парсер скачивающий архив с документацией python в pdf формате.

    ```bash
    python main.py download
    ```

- pep
Парсер выводящий список статусов документов PEP, количество документов в каждом статусе и общее количество.

    ```bash
    python main.py pep [аргументы]
    ```

### Аргументы

Есть возможность указывать аргументы для изменения работы программы:

- -h, --help
Общая информация о командах.

    ```bash
    python main.py -h
    ```

- -c, --clear-cache
Очистка кеша перед выполнением парсинга.

    ```bash
    python main.py [вариант парсера] -c
    ```

- -o {pretty,file}, --output {pretty,file}
Дополнительные способы вывода данных
pretty - выводит данные в таблице
file - сохраняет информацию в формате csv в папке results/
    
    ```bash
    python main.py [вариант парсера] -o file
    ```

- При выводе информации в файл (-o file) он сохраняется в папке src/results/
- Скачанная документация Python сохраняется в папке src/downloads/
- Логи работы парсера расположены в папке src/logs/

### Автор
[Исхаков Тимур](https://github.com/Timik2t "GitHub аккаунт")

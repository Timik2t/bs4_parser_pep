# Парсер документации python и PEP

## Описание

Парсер информации из **<https://docs.python.org/3/>** и **<https://peps.python.org/>**

## Технологии

beautifulsoup4

prettytable

requests-cache

## Подготовка и запуск проекта

### Склонировать репозиторий на локальную машину:

```
git clone git@github.com:Timik2t/bs4_parser_pep.git
```

В корневой папке проекта нужно создать виртуальное окружение и установить зависимости.

```
python -m venv venv
```
и
```
pip install -r requirements.txt
```

### смените директорию на папку src/

```
cd src/
```

### запустите файл main.py выбрав необходимый парсер и аргументы(приведены ниже)

```
python main.py [вариант парсера] [аргументы]
```

### Встроенные парсеры

- whats-new
Парсер выводящий спсок изменений в python.

```
python main.py whats-new
```

- latest_versions
Парсер выводящий список версий python и ссылки на их документацию.

```
python main.py latest-versions
```

- download
Парсер скачивающий архив с документацией python в pdf формате.

```
python main.py download
```

- pep
Парсер выводящий список статусов документов PEP, количество документов в каждом статусе и общее количество.

```
python main.py pep [аргументы]
```

### Аргументы

Есть возможность указывать аргументы для изменения работы программы:

- -h, --help
Общая информация о командах.

```
python main.py -h
```

- -c, --clear-cache
Очистка кеша перед выполнением парсинга.

```
python main.py [вариант парсера] -c
```

- -o {pretty,file}, --output {pretty,file}
Дополнительные способы вывода данных
pretty - выводит данные в таблице
file - сохраняет информацию в формате csv в папке results/

```
python main.py [вариант парсера] -o file
```

import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOADS_URL, EXPECTED_STATUS, MAIN_DOC_URL,
                       PEP_LOG, PEP_URL, WHATS_NEW_URL)
from exceptions import DownloadLinkNotFound, VersionsNotFound
from outputs import control_output
from utils import find_tag, get_response, get_soup

VERSION_NOT_FOUND = 'Не найден список c версиями Python'
DOWNLOAD_LINK_NOT_FOUND = 'Не найдена ссылка на архив с документацией'
ARCHIVE_SAVED_MESSAGE = 'Архив был загружен и сохранён: {}'
PARSER_STARTED = 'Парсер запущен!'
CMD_ARGS = 'Аргументы командной строки: {}'
PARSER_ENDED = 'Парсер завершил работу.'
SOUP_ERROR = 'Ошибка создания soup по адресу: {}'
ERROR = 'Ошибка: {}'


def whats_new(session):
    results = []
    logs = []
    for python_version in tqdm(
            get_soup(session, WHATS_NEW_URL).select(
                '#what-s-new-in-python div.toctree-wrapper li.toctree-l1 a')):
        version_link = urljoin(WHATS_NEW_URL, python_version['href'])
        soup = get_soup(session, version_link)
        if soup is None:
            logs.append(SOUP_ERROR.format(version_link))
            continue
        results.append((version_link, find_tag(soup, 'h1').text,
                        find_tag(soup, 'dl').text.replace('\n', ' ')))
    if len(logs) > 0:
        logging.warning("\n".join(logs))
    return [('Ссылка на статью', 'Заголовок', 'Редактор, Автор'), *results]


def latest_versions(session):
    for ul in find_tag(get_soup(session, MAIN_DOC_URL), 'div', {
            'class': 'sphinxsidebarwrapper'
    }).find_all('ul'):
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise VersionsNotFound(VERSION_NOT_FOUND)
    results = []
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((a_tag['href'], version, status))
    return [('Ссылка на документацию', 'Версия', 'Статус'), *results]


def download(session):
    soup = get_soup(session, DOWNLOADS_URL)
    pdf_a4_tag = soup.select_one(
        'div[role="main"] table.docutils a[href$="pdf-a4.zip"]')
    if not pdf_a4_tag:
        raise DownloadLinkNotFound(DOWNLOAD_LINK_NOT_FOUND)
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(DOWNLOADS_URL, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(ARCHIVE_SAVED_MESSAGE.format(archive_path))


def pep(session):

    def process_pep_status(pep_row):
        pep_link = urljoin(PEP_URL, pep_row.a['href'])
        response = get_response(session, pep_link)
        soup = BeautifulSoup(response.text, 'lxml')
        if soup is None:
            logs.append(SOUP_ERROR.format(response))
        main_card_dl_tag = find_tag(
            find_tag(soup, 'section', {'id': 'pep-content'}), 'dl',
            {'class': 'rfc2822 field-list simple'})
        for tag in main_card_dl_tag:
            if tag.name != 'dt' or tag.text != 'Status:':
                continue
            card_status = tag.next_sibling.next_sibling.string
            count_status_in_card[card_status] += 1
            if len(pep_row.td.text) != 1:
                table_status = pep_row.td.text[1:]
                if card_status[0] != table_status:
                    logs.append(
                        PEP_LOG.format(
                            link=pep_link,
                            card_status=card_status,
                            expected_statuses=EXPECTED_STATUS[table_status]))

    logs = []
    pep_rows = find_tag(get_soup(session, PEP_URL), 'section', {
        'id': 'numerical-index'
    }).find_all('tr')
    count_status_in_card = defaultdict(int)
    for pep_row in tqdm(pep_rows[1:], desc='Парсинг PEP'):
        process_pep_status(pep_row)
    if logs:
        [logging.info(log) for log in logs]
    return [('Статус', 'Количество'), *count_status_in_card.items(),
            ('Всего', sum(count_status_in_card.values()))]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    try:
        configure_logging()
        logging.info(PARSER_STARTED)
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info(CMD_ARGS.format(args))
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
        logging.info(PARSER_ENDED)
    except Exception as error:
        logging.exception(ERROR.format(error))


if __name__ == '__main__':
    main()

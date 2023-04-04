from bs4 import BeautifulSoup

from exceptions import ParserFindTagException

TAG_NOT_FOUND_ERROR = 'Не найден тег {tag} {attrs}'
REQUEST_ERROR = 'Возникла ошибка при загрузке страницы {url}'


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except ConnectionError as error:
        raise ConnectionError(REQUEST_ERROR.format(url=url)) from error


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(
            TAG_NOT_FOUND_ERROR.format(tag=tag, attrs=attrs)
        )
    return searched_tag


def get_soup(session, url):
    return BeautifulSoup(session.get(url).text, features='lxml')

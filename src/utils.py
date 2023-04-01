from requests import RequestException

from exceptions import ParserFindTagException

TAG_NOT_FOUND_ERROR = 'Не найден тег {tag} {attrs}'
REQUEST_ERROR = 'Возникла ошибка при загрузке страницы {url}'


def get_response(session, url, encoding=None):
    encoding = 'utf-8' if encoding is None else encoding
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as error:
        raise RequestException(REQUEST_ERROR.format(url=url)) from error


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(
            TAG_NOT_FOUND_ERROR.format(tag=tag, attrs=attrs)
        )
    return searched_tag

class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class VersionsNotFound(Exception):
    """Вызывается, когда парсер не может найти список c версиями Python"""
    pass


class DownloadLinkNotFound(Exception):
    """Парсер не может найти ссылку на архив с документацией"""
    pass

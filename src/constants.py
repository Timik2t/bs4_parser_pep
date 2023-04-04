from pathlib import Path
from urllib.parse import urljoin

# URLs
MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, 'whatsnew/')
DOWNLOADS_URL = urljoin(MAIN_DOC_URL, 'download.html')

# File and directory names
BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / 'downloads'
RESULTS_DIR = 'results'
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
LOG_FILENAME = 'logs.log'

# Date and time formats
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
DT_LOG_FORMAT = '%d.%m.%Y %H:%M:%S'

# Expected PEP statuses
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

# Logging settings
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
LOG_MAX_BYTES = 10 ** 6
LOG_BACKUP_COUNT = 5

# Other constants
PEP_LOG = (
    '\nНесовпадающие статусы:\n'
    '{link}\n'
    'Статус в карточке: {card_status}\n'
    'Ожидаемые статусы: {expected_statuses}'
)

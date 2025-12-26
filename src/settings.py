import os
import locale
from dotenv import load_dotenv


load_dotenv()

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

APP_NAME = os.environ['APP_NAME']
DATA_SOURCE_NAME = os.environ['DATA_SOURCE_NAME']

SELIC_API_URL = os.environ['SELIC_API_URL']
IPCA_API_URL = os.environ['IPCA_API_URL']

DEFAULT_SELIC_RATE = os.environ['DEFAULT_SELIC_RATE']
DEFAULT_SELIC_MAX_RATE = os.environ['DEFAULT_SELIC_MAX_RATE']
DEFAULT_IPCA_RATE = os.environ['DEFAULT_IPCA_RATE']
DEFAULT_IPCA_MAX_RATE = os.environ['DEFAULT_IPCA_MAX_RATE']

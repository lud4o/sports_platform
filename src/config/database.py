import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    'default': {
        'url': os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/sports_platform'),
        'echo': os.getenv('SQL_ECHO', 'false').lower() == 'true'
    },
    'test': {
        'url': os.getenv('TEST_DATABASE_URL', 'postgresql://user:password@localhost:5432/sports_platform_test'),
        'echo': True
    }
}
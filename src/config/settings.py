import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    
    # Database settings
    DATABASE_CONFIGS = {
        'default': {
            'url': os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/sports_platform'),
            'echo': os.getenv('SQL_ECHO', 'false').lower() == 'true'
        },
        'test': {
            'url': os.getenv('TEST_DATABASE_URL', 'postgresql://user:password@localhost:5432/sports_platform_test'),
            'echo': True
        }
    }
    
    # Application settings
    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    
    @classmethod
    def get_database_config(cls, environment: str = 'default') -> Dict[str, Any]:
        """Get database configuration for specified environment"""
        return cls.DATABASE_CONFIGS.get(environment, cls.DATABASE_CONFIGS['default'])
    
    @classmethod
    def get_database_url(cls, environment: str = 'default') -> str:
        """Get database URL for specified environment"""
        return cls.get_database_config(environment)['url']
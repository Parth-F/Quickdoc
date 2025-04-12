import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = False
    TESTING = False
    CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', 'chroma')
    DATA_PATH = os.getenv('DATA_PATH', 'data')
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', '5000'))
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True 

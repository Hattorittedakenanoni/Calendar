import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """アプリケーション設定"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # DATABASE_URL を取得
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Render は postgres:// を使うことがあるので postgresql:// に変換
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url
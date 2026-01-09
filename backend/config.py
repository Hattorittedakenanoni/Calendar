import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """アプリケーション設定"""
    # PostgreSQL接続URL（.envから読み込み）
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # 接続URLが設定されていない場合のエラーチェック
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL environment variable is not set")
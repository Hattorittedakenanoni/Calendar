from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """ユーザーテーブル"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    # リレーション
    companies = db.relationship('Company', backref='user', lazy=True)
    schedules = db.relationship('Schedule', backref='user', lazy=True)
    proposed_dates = db.relationship('ProposedDate', backref='user', lazy=True)

class Company(db.Model):
    """企業テーブル（就活状況）"""
    __tablename__ = 'companies'
    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    via = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=True)
    level = db.Column(db.String(255), nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    goodpoint = db.Column(db.String(1000), nullable=True)
    badpoint = db.Column(db.String(1000), nullable=True)
    memo = db.Column(db.String(1000), nullable=True)

    # リレーション
    schedules = db.relationship('Schedule', backref='company', lazy=True)
    proposed_dates = db.relationship('ProposedDate', backref='company', lazy=True)

class Schedule(db.Model):
    """スケジュールテーブル（カレンダー表示用などの一般的な予定）"""
    __tablename__ = 'schedules'
    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_type = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=True)
    schedule_name = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    memo = db.Column(db.String(1000), nullable=True)

class ProposedDate(db.Model):
    """面接候補日テーブル（調整中の日程ストック用）"""
    __tablename__ = 'proposed_dates'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=True)
    date_text = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
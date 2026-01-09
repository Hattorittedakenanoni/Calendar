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


class Company(db.Model):
    """企業テーブル（就活状況）"""
    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    via = db.Column(db.String(255), nullable=True)  # 経由
    status = db.Column(db.String(255), nullable=True)  # 選考ステータス
    level = db.Column(db.String(255), nullable=True)  # 志望度
    start_time = db.Column(db.DateTime, nullable=True)  # 次回選考 開始日時
    end_time = db.Column(db.DateTime, nullable=True)  # 次回選考 終了日時
    goodpoint = db.Column(db.String(1000), nullable=True)  # 良いと思う点
    badpoint = db.Column(db.String(1000), nullable=True)  # 懸念点
    memo = db.Column(db.String(1000), nullable=True)

    # リレーション
    schedules = db.relationship('Schedule', backref='company', lazy=True)
    proposed_dates = db.relationship('ProposedDate', backref='company', lazy=True)

    class Schedule(db.Model):
    """スケジュールテーブル"""
    __tablename__ = 'schedules'

    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_type = db.Column(db.String(255), nullable=False)  # 種別
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=True)  # NULLable に変更
    schedule_name = db.Column(db.String(255), nullable=False)  # 予定名
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    memo = db.Column(db.String(1000), nullable=True)


class ProposedDate(db.Model):
    """面接候補日テーブル"""
    __tablename__ = 'proposed_dates'

    date_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)  # 予定名
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
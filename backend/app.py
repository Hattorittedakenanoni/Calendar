# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, User, Company, Schedule, ProposedDate
from datetime import datetime

app = Flask(__name__)
# 日本語の文字化け防止とJSON整形設定
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config.from_object(Config)

# CORS設定：全てのオリジンからのアクセスを許可し、ヘッダーも受け入れます
CORS(app, resources={r"/api/*": {"origins": "*"}})

db.init_app(app)

TEMP_USER_ID = 1

# ===========================================
# 面接候補日 (ProposedDate) 用のAPI
# ===========================================

@app.route('/api/proposals', methods=['GET'])
def get_proposals():
    """保存されている全ての面接候補日を取得"""
    proposals = ProposedDate.query.filter_by(user_id=TEMP_USER_ID).all()
    result = []
    for p in proposals:
        result.append({
            'id': p.id,
            'company_id': p.company_id,
            'date_text': p.date_text, # "2026/01/26 10:00" などの形式を想定
            'created_at': p.created_at.isoformat() if p.created_at else None
        })
    return jsonify(result), 200

@app.route('/api/proposals', methods=['POST'])
def create_proposal():
    """新しい面接候補日を保存"""
    data = request.get_json()
    if not data.get('date_text'):
        return jsonify({'error': '日付データがありません'}), 400
    
    new_proposal = ProposedDate(
        user_id=TEMP_USER_ID,
        company_id=data.get('company_id'), # どの企業用か（空でも可）
        date_text=data.get('date_text')
    )
    db.session.add(new_proposal)
    db.session.commit()
    return jsonify({'message': '候補日を保存しました', 'id': new_proposal.id}), 201

@app.route('/api/proposals/<int:prop_id>', methods=['DELETE'])
def delete_proposal(prop_id):
    """候補日を削除"""
    prop = ProposedDate.query.filter_by(id=prop_id, user_id=TEMP_USER_ID).first()
    if not prop:
        return jsonify({'error': 'データが見つかりません'}), 404
    db.session.delete(prop)
    db.session.commit()
    return jsonify({'message': '削除しました'}), 200

# ===========================================
# 既存の企業管理API (一部修正・維持)
# ===========================================

@app.route('/api/companies', methods=['GET'])
def get_companies():
    companies = Company.query.filter_by(user_id=TEMP_USER_ID).all()
    result = []
    for c in companies:
        result.append({
            'company_id': c.company_id,
            'company_name': c.company_name,
            'via': c.via,
            'status': c.status,
            'level': c.level,
            'start_time': c.start_time.isoformat() if c.start_time else None,
            'end_time': c.end_time.isoformat() if c.end_time else None,
            'goodpoint': c.goodpoint,
            'badpoint': c.badpoint,
            'memo': c.memo,
        })
    return jsonify(result), 200

@app.route('/api/companies', methods=['POST'])
def create_company():
    data = request.get_json()
    if not data.get('company_name'):
        return jsonify({'error': '企業名は必須です'}), 400
    
    new_company = Company(
        user_id=TEMP_USER_ID,
        company_name=data.get('company_name'),
        via=data.get('via'),
        status=data.get('status'),
        level=data.get('level'),
        # 日時文字列が空でない場合のみパースする処理を追加
        start_time=datetime.fromisoformat(data['start_time']) if data.get('start_time') else None,
        end_time=datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
        goodpoint=data.get('goodpoint'),
        badpoint=data.get('badpoint'),
        memo=data.get('memo'),
    )
    db.session.add(new_company)
    db.session.commit()
    return jsonify({'message': '企業を追加しました', 'company_id': new_company.company_id}), 201

# --- (中略：update / delete / health はそのまま維持) ---

@app.route('/api/companies/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    company = Company.query.filter_by(company_id=company_id, user_id=TEMP_USER_ID).first()
    if not company: return jsonify({'error': '企業が見つかりません'}), 404
    db.session.delete(company)
    db.session.commit()
    return jsonify({'message': '削除しました'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # テーブル作成
        # テストユーザー作成
        existing_user = db.session.get(User, TEMP_USER_ID)
        if not existing_user:
            test_user = User(id=TEMP_USER_ID, user_name='testuser', email='test@example.com', password='password123')
            db.session.add(test_user)
            db.session.commit()
    
    app.run(debug=True, port=5000)
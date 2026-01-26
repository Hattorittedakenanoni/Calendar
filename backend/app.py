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

# CORS設定：全てのオリジンからのアクセスを許可
CORS(app, resources={r"/api/*": {"origins": "*"}})

db.init_app(app)

TEMP_USER_ID = 1


# ===========================================
# アプリ起動時にテーブル作成（トップレベルで実行）
# ===========================================
with app.app_context():
    db.create_all()
    print("テーブルを作成/確認しました")
    
    # テストユーザー作成
    existing_user = db.session.get(User, TEMP_USER_ID)
    if not existing_user:
        test_user = User(
            id=TEMP_USER_ID,
            user_name='testuser',
            email='test@example.com',
            password='password123'
        )
        db.session.add(test_user)
        db.session.commit()
        print("テストユーザーを作成しました")
    else:
        print("テストユーザーは既に存在します")


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
            'date_text': p.date_text,
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
        company_id=data.get('company_id'),
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
# 企業管理API
# ===========================================

@app.route('/api/companies', methods=['GET'])
def get_companies():
    """企業一覧を取得"""
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
    """企業を追加"""
    data = request.get_json()
    if not data.get('company_name'):
        return jsonify({'error': '企業名は必須です'}), 400
    
    new_company = Company(
        user_id=TEMP_USER_ID,
        company_name=data.get('company_name'),
        via=data.get('via'),
        status=data.get('status'),
        level=data.get('level'),
        start_time=datetime.fromisoformat(data['start_time']) if data.get('start_time') else None,
        end_time=datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
        goodpoint=data.get('goodpoint'),
        badpoint=data.get('badpoint'),
        memo=data.get('memo'),
    )
    db.session.add(new_company)
    db.session.commit()
    return jsonify({'message': '企業を追加しました', 'company_id': new_company.company_id}), 201


@app.route('/api/companies/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    """企業を削除"""
    company = Company.query.filter_by(company_id=company_id, user_id=TEMP_USER_ID).first()
    if not company:
        return jsonify({'error': '企業が見つかりません'}), 404
    db.session.delete(company)
    db.session.commit()
    return jsonify({'message': '削除しました'}), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """ヘルスチェック"""
    return jsonify({'status': 'ok'}), 200


# ===========================================
# ローカル開発用
# ===========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)

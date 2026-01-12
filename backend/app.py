from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, User, Company, Schedule, ProposedDate

app = Flask(__name__)

app.config.from_object(Config)

# CORS設定（フロントエンドから�?�アクセスを許可?�?
CORS(app)

# DB初期�?
db.init_app(app)

# 仮のユーザーID?��ログイン機�?�実�?まではこれを使�??�?
TEMP_USER_ID = 1

# ===========================================
# 初期セ�?トア�?プ用
# ===========================================
@app.route('/api/init', methods=['POST'])
def init_db():
    """DB�?ーブル作�?? & �?スト用ユーザー作�??"""
    db.create_all()
    
    # �?スト用ユーザーがいなければ作�??
    if not User.query.get(TEMP_USER_ID):
        test_user = User(
            id=TEMP_USER_ID,
            user_name='testuser',
            email='test@example.com',
            password='password123'
        )
        db.session.add(test_user)
        db.session.commit()
    
    return jsonify({'message': 'Database initialized'}), 200

# ---------------
# �?機�?�を実�?
# ---------------
# ===========================================
# 企業?��就活状�??��API
# ===========================================
@app.route('/api/companies', methods=['GET'])
def get_companies():
    """企業一覧を取�?"""
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
    """企業を追�?"""
    data = request.get_json()
    
    # �?須�??目チェ�?ク
    if not data.get('company_name'):
        return jsonify({'error': '企業名�?��?須で�?'}), 400
    
    new_company = Company(
        user_id=TEMP_USER_ID,
        company_name=data.get('company_name'),
        via=data.get('via'),
        status=data.get('status'),
        level=data.get('level'),
        start_time=data.get('start_time'),  # 後でパ�?�ス処�?を追�?
        end_time=data.get('end_time'),
        goodpoint=data.get('goodpoint'),
        badpoint=data.get('badpoint'),
        memo=data.get('memo'),
    )
    
    db.session.add(new_company)
    db.session.commit()
    
    return jsonify({
        'message': '企業を追�?しました',
        'company_id': new_company.company_id
    }), 201


@app.route('/api/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    """企業詳細を取�?"""
    company = Company.query.filter_by(
        company_id=company_id,
        user_id=TEMP_USER_ID
    ).first()
    
    if not company:
        return jsonify({'error': '企業が見つかりません'}), 404
    
    return jsonify({
        'company_id': company.company_id,
        'company_name': company.company_name,
        'via': company.via,
        'status': company.status,
        'level': company.level,
        'start_time': company.start_time.isoformat() if company.start_time else None,
        'end_time': company.end_time.isoformat() if company.end_time else None,
        'goodpoint': company.goodpoint,
        'badpoint': company.badpoint,
        'memo': company.memo,
    }), 200


@app.route('/api/companies/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    """企業�?報を更新"""
    company = Company.query.filter_by(
        company_id=company_id,
        user_id=TEMP_USER_ID
    ).first()
    
    if not company:
        return jsonify({'error': '企業が見つかりません'}), 404
    
    data = request.get_json()
    
    # 更新可能なフィール�?
    if 'company_name' in data:
        company.company_name = data['company_name']
    if 'via' in data:
        company.via = data['via']
    if 'status' in data:
        company.status = data['status']
    if 'level' in data:
        company.level = data['level']
    if 'start_time' in data:
        company.start_time = data['start_time']
    if 'end_time' in data:
        company.end_time = data['end_time']
    if 'goodpoint' in data:
        company.goodpoint = data['goodpoint']
    if 'badpoint' in data:
        company.badpoint = data['badpoint']
    if 'memo' in data:
        company.memo = data['memo']
    
    db.session.commit()
    
    return jsonify({'message': '企業�?報を更新しました'}), 200


@app.route('/api/companies/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    """企業を削除"""
    company = Company.query.filter_by(
        company_id=company_id,
        user_id=TEMP_USER_ID
    ).first()
    
    if not company:
        return jsonify({'error': '企業が見つかりません'}), 404
    
    db.session.delete(company)
    db.session.commit()
    
    return jsonify({'message': '企業を削除しました'}), 200



# ===========================================
# 動作確認用
# ===========================================
@app.route('/api/health', methods=['GET'])
def health_check():
    """ヘルスチェ�?ク"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # �?ストユーザーがいなければ作�??
        # existing_user = User.query.get(TEMP_USER_ID)
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
            print('�?ストユーザーを作�?�しました')
        else:
            print('�?ストユーザーは既に存在しま�?')
    
    app.run(debug=True, port=5000)


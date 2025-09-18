import os
import pandas as pd
import sqlite3

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

is_anywhere = False

if not is_anywhere:
    # 업로드 폴더 설정
    UPLOAD_FOLDER = 'uploads'
    DATABASE_FOLDER = ''
else:
    # 파이썬 애니웨어 경로
    UPLOAD_FOLDER = '/home/samedu/mysite/uploads'
    DATABASE_FOLDER = '/home/samedu/mysite/'

ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def get_connection():
    return sqlite3.connect(DATABASE_FOLDER + 'bank_database.db')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """홈페이지 - AI 데이터 분석 서비스 소개"""
    return render_template('index.html')

@app.route('/marketing')
def marketing():
    """마케팅 분석 체험 페이지"""
    filename = request.args.get('file')
    print('마케팅 페이지 호출....', filename)
    if filename:
        df = pd.read_csv(os.path.join(UPLOAD_FOLDER, filename))
        items = df.values.tolist()
        print(items)

        return render_template('marketing.html', items=items)
    
    return render_template('marketing.html')

@app.route('/loan')
def loan():
    """대출 심사 분석 체험 페이지"""
    print('대출 페이지 호출....')
    name = request.args.get('name')
    birth = request.args.get('birth')
    
    if name and birth:
        print('name', name, ', birth', birth)
        user = finduser(name, birth)
        print('왜 안되지...', list(user[0]))
        return render_template('loan.html', user=list(user[0]))
    
    return render_template('loan.html')

# 마케팅 파일 업로드
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print('upload_file')
    if request.method == 'POST':
        # 'file'은 form input의 name 속성과 일치해야 함
        file = request.files['file']
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)  # 보안 처리된 파일명
            filename = file.filename
            print('filename : ', filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '성공'
    
    return '업로드 실패'

def finduser(name, birth):
    conn = get_connection()
    cursor = conn.cursor()
    # 이름으로 가져오기
    # cursor.execute('SELECT * FROM users WHERE name LIKE ? AND phone = ', (name,))
    cursor.execute('SELECT * FROM users WHERE name LIKE ? AND phone = ?', ('홍서연', '01099454336'))
    user = cursor.fetchall()
    print('find user : ', user)
    return user
    

# @app.route('/upload_marketing', methods=['POST'])
# def upload_marketing():
#     """마케팅 데이터 업로드 및 분석"""
#     if 'file' not in request.files:
#         return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
        
#         try:
#             # CSV 파일 읽기
#             df = pd.read_csv(filepath)
            
#             # 간단한 분석 수행 (실제로는 더 복잡한 ML 분석)
#             analysis_result = {
#                 'data_shape': df.shape,
#                 'columns': df.columns.tolist(),
#                 'summary': df.describe().to_dict(),
#                 'segmentation': {
#                     'VIP': 23,
#                     'Regular': 54, 
#                     'New': 23
#                 },
#                 'predictions': {
#                     'growth': 15,
#                     'accuracy': 87
#                 }
#             }
            
#             return jsonify({
#                 'success': True,
#                 'message': '분석이 완료되었습니다.',
#                 'data': analysis_result
#             })
            
#         except Exception as e:
#             return jsonify({'error': f'파일 분석 중 오류가 발생했습니다: {str(e)}'}), 500
#         finally:
#             # 업로드된 파일 삭제 (선택사항)
#             if os.path.exists(filepath):
#                 os.remove(filepath)
    
#     return jsonify({'error': '지원하지 않는 파일 형식입니다.'}), 400

# @app.route('/upload_loan', methods=['POST'])
# def upload_loan():
#     """대출 데이터 업로드 및 분석"""
#     if 'file' not in request.files:
#         return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
        
#         try:
#             # CSV 파일 읽기
#             df = pd.read_csv(filepath)
            
#             # 간단한 대출 리스크 분석 (실제로는 더 복잡한 ML 분석)
#             analysis_result = {
#                 'data_shape': df.shape,
#                 'columns': df.columns.tolist(),
#                 'risk_distribution': {
#                     'high_risk': 12,
#                     'medium_risk': 23,
#                     'low_risk': 65
#                 },
#                 'approval_rate': 73,
#                 'model_accuracy': 92,
#                 'risk_factors': {
#                     'credit_score': 32,
#                     'debt_ratio': 28,
#                     'employment': 24,
#                     'others': 16
#                 }
#             }
            
#             return jsonify({
#                 'success': True,
#                 'message': '대출 리스크 분석이 완료되었습니다.',
#                 'data': analysis_result
#             })
            
#         except Exception as e:
#             return jsonify({'error': f'파일 분석 중 오류가 발생했습니다: {str(e)}'}), 500
#         finally:
#             # 업로드된 파일 삭제 (선택사항)
#             if os.path.exists(filepath):
#                 os.remove(filepath)
    
#     return jsonify({'error': '지원하지 않는 파일 형식입니다.'}), 400

@app.route('/analyze_individual', methods=['POST'])
def analyze_individual():
    """개별 대출 신청자 분석"""
    data = request.get_json()
    
    try:
        age = int(data.get('age', 0))
        income = int(data.get('income', 0))
        credit_score = int(data.get('creditScore', 0))
        loan_amount = int(data.get('loanAmount', 0))
        
        # 간단한 리스크 점수 계산
        risk_score = calculate_risk_score(age, income, credit_score, loan_amount)
        is_approved = risk_score < 60
        
        return jsonify({
            'success': True,
            'risk_score': risk_score,
            'approval': is_approved,
            'recommendation': '승인 권장' if is_approved else '승인 거절',
            'factors': {
                'credit_score_impact': abs(credit_score - 700) / 10,
                'debt_ratio_impact': (loan_amount / income) * 100,
                'age_factor': 'normal' if 25 <= age <= 65 else 'risk'
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'분석 중 오류가 발생했습니다: {str(e)}'}), 500

def calculate_risk_score(age, income, credit_score, loan_amount):
    """간단한 리스크 점수 계산 함수"""
    risk = 50  # 기본 리스크
    
    # 신용점수 영향
    if credit_score < 600:
        risk += 30
    elif credit_score < 700:
        risk += 15
    elif credit_score > 800:
        risk -= 15
    
    # 소득 대비 대출액 비율
    if income > 0:
        ratio = (loan_amount / income) * 100
        if ratio > 500:
            risk += 25
        elif ratio > 300:
            risk += 15
        elif ratio < 100:
            risk -= 10
    
    # 나이 영향
    if age < 25 or age > 65:
        risk += 10
    
    return max(0, min(100, round(risk)))


# 테스트 데이터 다운로드
@app.route('/download_test_data')
def download_test_data():
    """테스트 데이터 CSV 파일 다운로드"""
    try:
        # 절대 경로로 파일 경로 생성
        file_path = os.path.join(app.root_path, 'download', 'bank_marketing_user.csv')
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name='bank_marketing_user.csv')
        else:
            # 상대 경로도 시도
            file_path_relative = os.path.join('download', 'bank_marketing_user.csv')
            if os.path.exists(file_path_relative):
                return send_file(file_path_relative, as_attachment=True, download_name='bank_marketing_user.csv')
            else:
                return jsonify({'error': f'테스트 데이터 파일을 찾을 수 없습니다. 경로: {file_path}'}), 404
    except Exception as e:
        return jsonify({'error': f'파일 다운로드 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/download_sample/<sample_type>')
def download_sample(sample_type):
    """샘플 데이터 다운로드"""
    # 실제로는 미리 준비된 샘플 파일을 제공
    sample_files = {
        'marketing': 'sample_marketing_data.csv',
        'sales': 'sample_sales_data.csv', 
        'customer': 'sample_customer_data.csv',
        'personal': 'sample_personal_loan.csv',
        'business': 'sample_business_loan.csv',
        'mortgage': 'sample_mortgage_loan.csv'
    }
    
    if sample_type in sample_files:
        # 샘플 파일이 있다면 전송, 없다면 임시로 JSON 응답
        return jsonify({
            'message': f'{sample_type} 샘플 데이터 다운로드',
            'filename': sample_files[sample_type]
        })
    
    return jsonify({'error': '요청한 샘플 파일을 찾을 수 없습니다.'}), 404

if __name__ == '__main__':
    # uploads 폴더가 없으면 생성
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    # 외부 접근 가능하도록 host='0.0.0.0' 설정
    app.run(debug=True, host='0.0.0.0', port=5001)
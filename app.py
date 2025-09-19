import os
import pandas as pd
import sqlite3
import joblib
import numpy as np

from sklearn.ensemble import VotingClassifier
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for

app = Flask(__name__)

# 파이썬 에니웨어의 경우 경로가 다르기때문에 플래그 사용 
is_anywhere = False

if not is_anywhere:
    # 업로드 폴더 설정
    UPLOAD_FOLDER = 'uploads'
    BASE_FOLDER = ''
else:
    # 파이썬 애니웨어 경로
    UPLOAD_FOLDER = '/home/samedu/mysite/uploads'
    BASE_FOLDER = '/home/samedu/mysite/'

ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def get_connection():
    return sqlite3.connect(BASE_FOLDER + 'bank_database.db')

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
    if filename:
        count = int(request.args.get('count'))
        df = pd.read_csv(os.path.join(UPLOAD_FOLDER, filename))
        df = predict_deposit(df, count)
        items = df.values.tolist()
        return render_template('marketing.html', items=items)
    
    return render_template('marketing.html')

def predict_deposit(df: pd.DataFrame, count):
    """예/적금 가입 가능성 예측"""
    print('predict_deposit')
    term_deposits = df.copy()
    term_deposits = term_deposits.iloc[:, 2:]
    
    #데이터 전처리
    label_index = joblib.load(os.path.join(BASE_FOLDER, 'label_index.pkl'))

    term_deposits['job'] = term_deposits['job'].map(label_index['job'])
    term_deposits['marital'] = term_deposits['marital'].map(label_index['marital'])
    term_deposits['education'] = term_deposits['education'].map(label_index['education'])
    term_deposits['contact'] = term_deposits['contact'].map(label_index['contact'])
    term_deposits['poutcome'] = term_deposits['poutcome'].map(label_index['poutcome'])
    term_deposits['month'] = term_deposits['month'].map(label_index['month'])
    term_deposits['default'] = term_deposits['default'].map(label_index['default'])
    term_deposits['loan'] = term_deposits['loan'].map(label_index['loan'])
    term_deposits['housing'] = term_deposits['housing'].map(label_index['housing'])
    
    target_name = 'deposit'
    X = term_deposits.drop(target_name, axis=1)
    
    # 모델 로드 및 예측 / 정렬
    voting_clf = joblib.load(os.path.join(BASE_FOLDER, 'votingclf_deposit.pkl'))
    df['pred'] = np.round(voting_clf.predict_proba(X)[:, 1] * 100, 2)
    df = df.sort_values(by='pred', ascending=False)
    return df[:count]
    
@app.route('/loan')
def loan():
    """대출 심사 분석 체험 페이지"""
    name = request.args.get('name')
    phone = request.args.get('phone')
    
    if name and phone:
        user = finduser(name, phone)
        if len(user) > 0:
            return render_template('loan.html', user=list(user[0]))
    
    return render_template('loan.html')

@app.route('/eval_loan', methods=['POST'])
def eval_loan():
    print('eval_loan')
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone').replace('-', '')
        print(name, phone)
        
        users = finduser(name, phone)
        print(users)
        if users:
            pred = predict_loan(users[0])
            print(pred)
        return jsonify({"result": pred[0]})
    
    return jsonify({"result": 0})

def predict_loan(user):
    """예/적금 가입 가능성 예측"""
    print('predict_loan')
    data = list(user[2:])
    term_loans = pd.DataFrame(data)
    term_loans = term_loans.T
    term_loans.columns = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'deposit']
    print(term_loans)
    
    #데이터 전처리
    label_index = joblib.load(os.path.join(BASE_FOLDER, 'label_index.pkl'))

    term_loans['job'] = term_loans['job'].map(label_index['job'])
    term_loans['marital'] = term_loans['marital'].map(label_index['marital'])
    term_loans['education'] = term_loans['education'].map(label_index['education'])
    term_loans['contact'] = term_loans['contact'].map(label_index['contact'])
    term_loans['poutcome'] = term_loans['poutcome'].map(label_index['poutcome'])
    term_loans['month'] = term_loans['month'].map(label_index['month'])
    term_loans['default'] = term_loans['default'].map(label_index['default'])
    term_loans['loan'] = term_loans['loan'].map(label_index['loan'])
    term_loans['housing'] = term_loans['housing'].map(label_index['housing'])
    # term_loans['deposit'] = term_loans['deposit'].map(label_index['deposit'])

    X = term_loans.drop('deposit', axis=1)
    
    # 모델 로드 및 예측 / 정렬
    voting_clf = joblib.load(os.path.join(BASE_FOLDER, 'votingclf_deposit.pkl'))
    prob = voting_clf.predict_proba(X)
    print('prob : ', prob)
    return np.round(prob[:, 1] * 100, 2)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """마케팅 파일 업로드 및 저장"""
    print('upload_file')
    if request.method == 'POST':
        # 'file'은 form input의 name 속성과 일치해야 함
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return 'success'
    
    return 'error'

# 데이터 베이스에서 사용자 가져오기
def finduser(name, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE name LIKE ? AND phone = ?', (name, phone))
    user = cursor.fetchall()
    return user

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

# @app.route('/download_sample/<sample_type>')
# def download_sample(sample_type):
#     """샘플 데이터 다운로드"""
#     # 실제로는 미리 준비된 샘플 파일을 제공
#     sample_files = {
#         'marketing': 'sample_marketing_data.csv',
#         'sales': 'sample_sales_data.csv', 
#         'customer': 'sample_customer_data.csv',
#         'personal': 'sample_personal_loan.csv',
#         'business': 'sample_business_loan.csv',
#         'mortgage': 'sample_mortgage_loan.csv'
#     }
    
#     if sample_type in sample_files:
#         # 샘플 파일이 있다면 전송, 없다면 임시로 JSON 응답
#         return jsonify({
#             'message': f'{sample_type} 샘플 데이터 다운로드',
#             'filename': sample_files[sample_type]
#         })
    
#     return jsonify({'error': '요청한 샘플 파일을 찾을 수 없습니다.'}), 404

if __name__ == '__main__':
    # uploads 폴더가 없으면 생성
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    # 외부 접근 가능하도록 host='0.0.0.0' 설정
    app.run(debug=True, host='0.0.0.0', port=5001)
// SimSim AI 마케팅 분석 서비스 JavaScript

// 전역 변수
let currentAnalysisType = 'marketing';

// DOM 로드 완료 후 실행
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 앱 초기화
function initializeApp() {
    console.log('SimSim AI 앱이 초기화되었습니다.');
    
    // 폼 이벤트 리스너 등록
    setupFormHandlers();
    
    // 기타 이벤트 리스너 등록
    setupEventListeners();
    
    // 마케팅 예산 계산기 초기화
    initializeMarketingCalculator();
}

// 폼 핸들러 설정
function setupFormHandlers() {
    // 마케팅 분석 폼
    const marketingForm = document.getElementById('uploadForm');
    if (marketingForm) {
        marketingForm.addEventListener('submit', handleMarketingUpload);
    }
    
    // 대출 분석 폼
    const loanForm = document.getElementById('loanUploadForm');
    if (loanForm) {
        loanForm.addEventListener('submit', handleLoanUpload);
    }
    
    // 개별 분석 폼
    const individualForm = document.getElementById('individualForm');
    if (individualForm) {
        individualForm.addEventListener('submit', handleIndividualAnalysis);
    }
}

// 마케팅 예산 계산기 초기화
function initializeMarketingCalculator() {
    const totalBudgetInput = document.getElementById('total-budget');
    const costPerPersonInput = document.getElementById('cost-per-person');
    const targetCountElement = document.getElementById('target-count');
    
    if (totalBudgetInput && costPerPersonInput && targetCountElement) {
        // 로컬스토리지에서 저장된 값 불러오기
        loadStoredValues();
        
        // 입력 이벤트 리스너 등록
        totalBudgetInput.addEventListener('input', calculateMarketingTarget);
        costPerPersonInput.addEventListener('input', calculateMarketingTarget);
        
        // 초기 계산
        calculateMarketingTarget();
    }
}

// 마케팅 목표수 계산
function calculateMarketingTarget() {
    console.log('calculateMarketingTarget....')
    const totalBudgetInput = document.getElementById('total-budget');
    const costPerPersonInput = document.getElementById('cost-per-person');
    const targetCountElement = document.getElementById('target-count');
    
    if (!totalBudgetInput || !costPerPersonInput || !targetCountElement) return;

    const totalBudget = parseFloat(totalBudgetInput.value) || 0;
    const costPerPerson = parseFloat(costPerPersonInput.value) || 0;
    
    let targetCount = 0;
    
    if (costPerPerson > 0) {
        targetCount = Math.floor(totalBudget / costPerPerson);
    }
    
    // 결과 표시
    targetCountElement.innerHTML = `${targetCount.toLocaleString()} <span>명</span>`;
    
    // 로컬스토리지에 저장
    saveToLocalStorage({
        totalBudget: totalBudget,
        costPerPerson: costPerPerson,
        targetCount: targetCount
    });
    
    console.log(`마케팅 목표수 계산: ${targetCount}명 (예산: ${totalBudget.toLocaleString()}원, 1인당: ${costPerPerson.toLocaleString()}원)`);
}

// 로컬스토리지에 저장
function saveToLocalStorage(data) {
    try {
        localStorage.setItem('marketingBudget', JSON.stringify(data));
    } catch (error) {
        console.error('로컬스토리지 저장 실패:', error);
    }
}

// 로컬스토리지에서 값 불러오기
function loadStoredValues() {
    try {
        const stored = localStorage.getItem('marketingBudget');
        if (stored) {
            const data = JSON.parse(stored);
            const totalBudgetInput = document.getElementById('total-budget');
            const costPerPersonInput = document.getElementById('cost-per-person');
            
            if (totalBudgetInput && data.totalBudget) {
                totalBudgetInput.value = data.totalBudget;
            }
            if (costPerPersonInput && data.costPerPerson) {
                costPerPersonInput.value = data.costPerPerson;
            }
        }
    } catch (error) {
        console.error('로컬스토리지 불러오기 실패:', error);
    }
}

function loadStoredata() {
    try {
        const stored = localStorage.getItem('marketingBudget');
        if (stored) {
            const data = JSON.parse(stored);
            return data
        }

        return null
    } catch (error) {
        console.error('로컬스토리지 불러오기 실패:', error);
    }
}

// 이벤트 리스너 설정
function setupEventListeners() {
    // 파일 입력 변화 감지
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('click', clickFileSelect);
        input.addEventListener('change', handleFileSelect);
    });
    
    // 네비게이션 활성화
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add('active');
        }
    });
}

function clickFileSelect(event) {
    console.log('clickFileSelect...')
    const totalBudgetInput = document.getElementById('total-budget');
    const costPerPersonInput = document.getElementById('cost-per-person');
    const targetCountElement = document.getElementById('target-count');
    
    if (!totalBudgetInput || !costPerPersonInput || !targetCountElement) return;

    const totalBudget = parseFloat(totalBudgetInput.value) || 0;
    const costPerPerson = parseFloat(costPerPersonInput.value) || 0;

    if (totalBudget == 0 || costPerPerson == 0 ) {
        event.preventDefault()
        alert('마케팅 예산과 1인당 예산을 입력하세요.')
        return
    } 
}

// 파일 선택 핸들러
// 마케팅 페이지에서 csv 파일 업로드 시 호출
async function handleFileSelect(event) {
    console.log("handleFileSelect/.....")
    const file = event.target.files[0];
    if (file) {
        const maxSize = 16 * 1024 * 1024; // 16MB
        
        if (file.size > maxSize) {
            showAlert('파일 크기가 너무 큽니다. 16MB 이하의 파일을 선택해주세요.', 'warning');
            event.target.value = '';
            return;
        }
        
        if (!file.name.toLowerCase().endsWith('.csv')) {
            showAlert('CSV 파일만 업로드 가능합니다.', 'warning');
            event.target.value = '';
            return;
        }
        
        console.log(`파일 선택됨: ${file.name} (${formatFileSize(file.size)})`);

        // FormData 객체 생성
        const formData = new FormData();
        formData.append("file", file);

        console.log('여기는 오니...')
        try {
            const response = await fetch("/upload", {
            method: "POST",
            body: formData
            });

            const result = await response.text();
            console.log('완료...')
            data = loadStoredata()
            targetCount = data.targetCount
            window.location.href = '/marketing?file=' + file.name + '&count=' + targetCount;
            // window.location.href = 'loan';
        } catch (error) {
            console.error("업로드 실패:", error);
        }
    }

}

// 마케팅 데이터 업로드 핸들러
async function handleMarketingUpload(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const analysisTypes = [];
    
    // 선택된 분석 유형 수집
    const checkboxes = document.querySelectorAll('input[name="analysis_type"]:checked');
    checkboxes.forEach(cb => analysisTypes.push(cb.value));
    
    if (analysisTypes.length === 0) {
        showAlert('최소 하나의 분석 유형을 선택해주세요.', 'warning');
        return;
    }
    
    formData.append('analysis_types', JSON.stringify(analysisTypes));
    
    try {
        showLoading('마케팅 데이터 분석');
        
        const response = await fetch('/upload_marketing', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            hideLoading();
            displayMarketingResults(result.data);
            showAlert('분석이 완료되었습니다!', 'success');
        } else {
            throw new Error(result.error || '분석 중 오류가 발생했습니다.');
        }
        
    } catch (error) {
        hideLoading();
        showAlert(error.message, 'danger');
        console.error('마케팅 분석 오류:', error);
    }
}

// 대출 데이터 업로드 핸들러
async function handleLoanUpload(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const analysisTypes = [];
    
    // 선택된 분석 유형 수집
    const checkboxes = document.querySelectorAll('input[name="analysis_type"]:checked');
    checkboxes.forEach(cb => analysisTypes.push(cb.value));
    
    if (analysisTypes.length === 0) {
        showAlert('최소 하나의 분석 유형을 선택해주세요.', 'warning');
        return;
    }
    
    formData.append('analysis_types', JSON.stringify(analysisTypes));
    
    try {
        showLoading('대출 리스크 분석', 'loan');
        
        const response = await fetch('/upload_loan', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            hideLoading('loan');
            displayLoanResults(result.data);
            showAlert('대출 분석이 완료되었습니다!', 'success');
        } else {
            throw new Error(result.error || '분석 중 오류가 발생했습니다.');
        }
        
    } catch (error) {
        hideLoading('loan');
        showAlert(error.message, 'danger');
        console.error('대출 분석 오류:', error);
    }
}

// 개별 분석 핸들러
async function handleIndividualAnalysis(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    // 입력값 검증
    if (!validateIndividualData(data)) {
        return;
    }
    
    try {
        const response = await fetch('/analyze_individual', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayIndividualResults(result, data);
            showAlert('개별 분석이 완료되었습니다!', 'success');
        } else {
            throw new Error(result.error || '분석 중 오류가 발생했습니다.');
        }
        
    } catch (error) {
        showAlert(error.message, 'danger');
        console.error('개별 분석 오류:', error);
    }
}

// 로딩 표시
function showLoading(message = '분석 중...', type = 'marketing') {
    const loadingId = type === 'loan' ? 'loanLoadingSection' : 'loadingSection';
    const progressId = type === 'loan' ? 'loanProgressBar' : 'progressBar';
    
    const loadingSection = document.getElementById(loadingId);
    if (loadingSection) {
        loadingSection.style.display = 'block';
        
        // 프로그레스 바 애니메이션
        const progressBar = document.getElementById(progressId);
        let progress = 0;
        
        const interval = setInterval(() => {
            progress += Math.random() * 10;
            if (progress > 95) progress = 95;
            
            if (progressBar) {
                progressBar.style.width = progress + '%';
            }
            
            if (progress >= 95) {
                clearInterval(interval);
            }
        }, 300);
        
        // 나중에 완료 처리를 위해 interval ID 저장
        loadingSection.dataset.intervalId = interval;
    }
}

// 로딩 숨김
function hideLoading(type = 'marketing') {
    const loadingId = type === 'loan' ? 'loanLoadingSection' : 'loadingSection';
    const progressId = type === 'loan' ? 'loanProgressBar' : 'progressBar';
    
    const loadingSection = document.getElementById(loadingId);
    if (loadingSection) {
        // 프로그레스 바를 100%로 설정
        const progressBar = document.getElementById(progressId);
        if (progressBar) {
            progressBar.style.width = '100%';
        }
        
        // 진행 중인 interval 정리
        const intervalId = loadingSection.dataset.intervalId;
        if (intervalId) {
            clearInterval(parseInt(intervalId));
        }
        
        // 잠시 후 로딩 섹션 숨김
        setTimeout(() => {
            loadingSection.style.display = 'none';
        }, 500);
    }
}

// 마케팅 결과 표시
function displayMarketingResults(data) {
    const resultSection = document.getElementById('resultSection');
    if (resultSection) {
        resultSection.style.display = 'block';
        
        // 스크롤을 결과 섹션으로 이동
        resultSection.scrollIntoView({ behavior: 'smooth' });
        
        // 실제 데이터로 결과 업데이트
        updateMarketingCharts(data);
    }
}

// 대출 결과 표시
function displayLoanResults(data) {
    const resultSection = document.getElementById('loanResultSection');
    if (resultSection) {
        resultSection.style.display = 'block';
        
        // 스크롤을 결과 섹션으로 이동
        resultSection.scrollIntoView({ behavior: 'smooth' });
        
        // 실제 데이터로 결과 업데이트
        updateLoanCharts(data);
    }
}

// 개별 결과 표시
function displayIndividualResults(result, inputData) {
    const resultSection = document.getElementById('individualResultSection');
    if (resultSection) {
        // 입력 데이터 표시
        document.getElementById('resultAge').textContent = inputData.age + '세';
        document.getElementById('resultIncome').textContent = formatNumber(inputData.income) + '만원';
        document.getElementById('resultCreditScore').textContent = inputData.creditScore + '점';
        document.getElementById('resultLoanAmount').textContent = formatNumber(inputData.loanAmount) + '만원';
        
        // 분석 결과 표시
        document.getElementById('riskScore').textContent = result.risk_score;
        
        const approvalElement = document.getElementById('approvalResult');
        if (result.approval) {
            approvalElement.textContent = '승인 권장';
            approvalElement.className = 'badge bg-success fs-4 mb-3';
        } else {
            approvalElement.textContent = '승인 거절';
            approvalElement.className = 'badge bg-danger fs-4 mb-3';
        }
        
        resultSection.style.display = 'block';
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// 마케팅 차트 업데이트
function updateMarketingCharts(data) {
    // Chart.js 또는 다른 차트 라이브러리를 사용하여 실제 차트 생성
    console.log('마케팅 차트 업데이트:', data);
}

// 대출 차트 업데이트
function updateLoanCharts(data) {
    // Chart.js 또는 다른 차트 라이브러리를 사용하여 실제 차트 생성
    console.log('대출 차트 업데이트:', data);
}

// 개별 데이터 검증
function validateIndividualData(data) {
    const { age, income, creditScore, loanAmount } = data;
    
    if (!age || age < 18 || age > 100) {
        showAlert('올바른 나이를 입력해주세요. (18-100세)', 'warning');
        return false;
    }
    
    if (!income || income <= 0) {
        showAlert('올바른 연소득을 입력해주세요.', 'warning');
        return false;
    }
    
    if (!creditScore || creditScore < 300 || creditScore > 850) {
        showAlert('올바른 신용점수를 입력해주세요. (300-850점)', 'warning');
        return false;
    }
    
    if (!loanAmount || loanAmount <= 0) {
        showAlert('올바른 대출희망액을 입력해주세요.', 'warning');
        return false;
    }
    
    return true;
}

// 알림 표시
function showAlert(message, type = 'info') {
    console.log('showAlert....')
    // Bootstrap 알림 생성
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // 5초 후 자동 제거
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// 파일 크기 포맷팅
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 숫자 포맷팅 (천 단위 콤마)
function formatNumber(num) {
    return new Intl.NumberFormat('ko-KR').format(num);
}

// 샘플 데이터 다운로드
function downloadSample(type) {
    window.location.href = `/download_sample/${type}`;
}

// 대출 샘플 데이터 다운로드
function downloadLoanSample(type) {
    window.location.href = `/download_sample/${type}`;
}

// 유틸리티 함수들
const Utils = {
    // 디바운스 함수
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // 로컬 스토리지 저장
    saveToLocalStorage: function(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (error) {
            console.error('로컬 스토리지 저장 실패:', error);
        }
    },
    
    // 로컬 스토리지 읽기
    loadFromLocalStorage: function(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (error) {
            console.error('로컬 스토리지 읽기 실패:', error);
            return null;
        }
    }
};

// 전역으로 노출할 함수들
window.downloadSample = downloadSample;
window.downloadLoanSample = downloadLoanSample;

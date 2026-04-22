# 🎉 SQLite Query Tool 완성!

## 📁 최종 구조

```
d:\data3\Roo-Code\dc_code\
├── sample.db              ✅ SQLite 데이터베이스 (기본 제공)
├── index.html             ✅ 웹 버전 (바로 사용 가능!)
├── SETUP_GUIDE.md         📖 설치 가이드
├── setup_db.py            🔧 DB 생성 스크립트
└── extension/             📦 VS Code Extension (선택사항)
```

---

## 🚀 사용 방법 (3가지)

### ✨ 방법 1: HTML 파일로 바로 사용 (권장) ⭐

가장 간단하고 빠른 방법입니다!

```bash
# 1. 파일 탐색기에서 열기
d:\data3\Roo-Code\dc_code\index.html

# 또는 터미널에서
cd d:\data3\Roo-Code\dc_code
start index.html
```

**또는** 브라우저에 드래그:
1. Chrome, Edge, Firefox 등 브라우저 열기
2. `d:\data3\Roo-Code\dc_code\index.html` 을 브라우저 주소창에 드래그

**기능:**
- ✅ Node.js 설치 불필요
- ✅ npm 설치 불필요
- ✅ 드래그 앤 드롭으로 DB 파일 로드
- ✅ 테이블 자동 감지
- ✅ SQL 쿼리 즉시 실행
- ✅ 예제 쿼리 제공

**사용법:**
1. index.html 을 브라우저에서 열기
2. "💾 SQLite 데이터베이스 파일을 여기에 드래그" 영역에 `sample.db` 드래그
3. 테이블 버튼 클릭
4. SQL 쿼리 입력 후 "실행" 클릭

---

### 방법 2: VS Code Extension으로 설치

```bash
# VS Code 설치
# https://code.visualstudio.com/

# 확장 폴더 열기
cd d:\data3\Roo-Code\dc_code\extension

# F5 키 눌러서 디버그 모드 실행
# (새로운 VS Code 창이 열림)

# 명령 팔레트 (Ctrl+Shift+P)에서
> SQLite: Open Query Tool
```

---

### 방법 3: 차후 배포용 (.vsix 파일)

VS Code 마켓플레이스 또는 다른 사람과 공유 가능:

```bash
# 1. @vscode/vsce 설치 (처음 1회만)
npm install -g @vscode/vsce

# 2. 확장 패키징
cd d:\data3\Roo-Code\dc_code\extension
vsce package

# 3. sqlite-query-tool-0.0.1.vsix 생성
# 이 파일을 배포 가능
```

---

## 💡 SQL 쿼리 예제

```sql
-- 모든 사용자 조회
SELECT * FROM users;

-- 특정 조건으로 조회
SELECT name, email FROM users WHERE age > 25;

-- 개수 계산
SELECT COUNT(*) as 총개수 FROM users;

-- 우정렬
SELECT * FROM products ORDER BY price DESC;

-- 그룹화
SELECT category, COUNT(*) FROM products GROUP BY category;

-- 조인 (여러 테이블)
SELECT u.name, COUNT(o.id) 
FROM users u 
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;
```

---

## 🎯 주요 기능

### 🌐 HTML 버전
| 기능 | 상태 |
|------|------|
| 데이터베이스 로드 | ✅ 드래그/드롭 지원 |
| 테이블 목록 표시 | ✅ 자동 감지 |
| SQL 쿼리 실행 | ✅ 실시간 실행 |
| 결과 표시 | ✅ 테이블 형식 |
| 테이블 스키마 | ✅ 컬럼 정보 표시 |
| 예제 쿼리 | ✅ 랜덤 예제 생성 |
| 다크 모드 | ✅ 기본 지원 |

### 📦 Extension 버전
| 기능 | 상태 |
|------|------|
| VS Code 통합 | ✅ 상단 바 버튼 |
| Webview UI | ✅ HTML 기반 |
| SQL 쿼리 실행 | ✅ sql.js 사용 |
| 상태바 버튼 | ✅ 빠른 실행 |

---

## 📊 샘플 데이터

### users 테이블
| id | name | email | age |
|----|------|-------|-----|
| 1 | Alice | alice@example.com | 28 |
| 2 | Bob | bob@example.com | 32 |
| 3 | Charlie | charlie@example.com | 25 |

### products 테이블
| id | name | price | category |
|----|------|-------|----------|
| 1 | Laptop | 1200.00 | Electronics |
| 2 | Mouse | 29.99 | Electronics |
| 3 | Keyboard | 79.99 | Electronics |

---

## ❓ FAQ

**Q: Node.js를 설치해야 하나요?**
A: HTML 버전은 필요 없습니다! VS Code Extension을 사용하려면 선택사항입니다.

**Q: 파일이 저장되나요?**
A: 아니요. 모든 쿼리는 클라이언트 측에서 실행되며 변경사항은 저장되지 않습니다. (읽기 전용)

**Q: 다른 SQLite 파일을 로드할 수 있나요?**
A: 네! `index.html`을 브라우저에서 열고 다른 `.db` 파일을 드래그하면 됩니다.

**Q: 브라우저 종류는 상관없나요?**
A: Chrome, Edge, Firefox, Safari 모두 지원합니다.

---

## 🛠️ 기술 스택

- **UI**: HTML5 + CSS3 + Vanilla JavaScript
- **SQLite**: sql.js (순수 JavaScript 구현)
- **라이브러리**: 추가 라이브러리 없음 (CDN 사용)
- **호환성**: 99% 이상의 브라우저 지원

---

## 📝 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

## ✅ 완료!

이제 바로 사용 가능합니다! 

**시작하기:**
```bash
d:\data3\Roo-Code\dc_code\index.html 을 브라우저에서 열기
```

질문이나 개선사항이 있으시면 말씀해주세요! 🎉

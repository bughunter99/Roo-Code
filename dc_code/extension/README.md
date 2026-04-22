# SQLite Query Tool for VS Code

VS Code에서 SQLite 데이터베이스를 쉽게 쿼리할 수 있는 확장입니다.

## 기능

- ✅ 테이블 목록 표시
- ✅ SQL 쿼리 실행
- ✅ 결과를 테이블 형식으로 표시
- ✅ 테이블 스키마 확인
- ✅ 쿼리 히스토리 (선택적)

## 설치

### 방법 1: VS Code 마켓플레이스에서 설치 (향후)
마켓플레이스에서 "SQLite Query Tool" 검색 후 설치

### 방법 2: 로컬에서 개발 모드로 실행

```bash
cd dc_code/extension
npm install
npm run esbuild
```

F5를 눌러 Extension 실행 (Debug 모드)

### 방법 3: .vsix 파일로 설치

```bash
npm install -g @vscode/vsce
cd dc_code/extension
npm run vscode:prepublish
vsce package
# sqlite-query-tool-0.0.1.vsix 생성됨
```

VS Code에서 `.vsix` 파일을 드래그앤드롭하거나 명령팔레트에서 설치

## 사용 방법

1. **VS Code 명령팔레트** (Ctrl+Shift+P / Cmd+Shift+P)에서 "SQLite: Open Query Tool" 입력
2. 또는 우측 상단 상태바의 **SQLite Query** 버튼 클릭
3. 테이블 목록에서 테이블명 클릭하면 SELECT 쿼리 자동 생성
4. SQL 쿼리 입력 후 **실행** 버튼 클릭
5. 결과가 테이블 형식으로 표시됨

## 쿼리 예제

```sql
SELECT * FROM users;
SELECT name, email FROM users WHERE age > 25;
SELECT COUNT(*) FROM products;
SELECT category, SUM(price) FROM products GROUP BY category;
```

## 지원 버전

- VS Code: v1.85.0 이상
- Node.js: v16.0.0 이상

## 개발자 정보

- 데이터베이스 라이브러리: better-sqlite3
- UI 프레임워크: Webview (HTML/CSS/JavaScript)

## 라이선스

MIT

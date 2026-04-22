# 🚀 간단한 SQLite Query Extension 설치 가이드

이 Extension은 **Node.js 없이** 순수 JavaScript로 작동하므로 npm 설치 없이 바로 사용 가능합니다!

## 신속한 설치 방법 (VS Code 디버그 모드)

### 1️⃣ Requirements
- VS Code 1.85 이상
- TypeScript 컴파일러 (선택사항)

### 2️⃣ 빠른 실행 (TypeScript 없이)

1. **VS Code에서 확장 폴더 열기**
   ```bash
   cd d:\data3\Roo-Code\dc_code\extension
   code .
   ```

2. **F5 킬 눌러 디버그 모드 시작**
   - VS Code가 자동으로 확장을 로드합니다
   - 새로운 VS Code 창이 열립니다 (Extension이 활성화됨)

3. **명령 팔레트 열기** (Ctrl+Shift+P)
   ```
   > SQLite: Open Query Tool
   ```

4. **쿼리 실행**
   - `users` 또는 `products` 테이블 버튼 클릭
   - SQL 쿼리 입력 후 "실행" 클릭

## 예제 쿼리

```sql
-- 모든 사용자 조회
SELECT * FROM users;

-- 가격이 100 이상인 상품
SELECT name, price FROM products WHERE price >= 100;

-- 총 개수 계산
SELECT COUNT(*) as 사용자수 FROM users;

-- 카테고리별 상품 수
SELECT category, COUNT(*) FROM products GROUP BY category;
```

## 기술 정보

- **DB 라이브러리**: sql.js (순수 JavaScript SQLite 구현)
- **Webview**: HTML5 + 바닐라 JavaScript
- **빌드 없음**: 모든 코드가 클라이언트에서 직접 실행

## 문제해결

### "데이터베이스 로드 실패" 오류
- sample.db 파일이 `d:\data3\Roo-Code\dc_code\` 에 있는지 확인

### "SQLite: Open Query Tool" 명령을 찾을 수 없음
- F5를 눌러 디버그 모드를 다시 시작
- 명령 팔레트에서 "Extensions: Show Recommended Extensions" 입력

## 다음 단계 (선택사항)

### .vsix 파일로 패키징하기 (배포용)
```bash
# 1. @vscode/vsce 설치
npm install -g @vscode/vsce

# 2. 확장 폴더에서
cd d:\data3\Roo-Code\dc_code\extension
vsce package

# 3. sqlite-query-tool-0.0.1.vsix 생성됨
# 이 파일을 다른 사람과 공유하거나 마켓플레이스에 제출 가능
```

### VS Code 마켓플레이스에 등록하기
1. [Visual Studio Code 마켓플레이스](https://marketplace.visualstudio.com) 접속
2. Publisher 등록
3. vsce publish 명령으로 배포

## 라이선스
MIT

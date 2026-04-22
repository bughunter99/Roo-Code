# PyRoo (Django)

왼쪽 패널에서 `Base LLM URL`, `Token`, `Model`을 입력하고,
오른쪽에서 질문/답변을 주고받는 Django 웹 앱입니다.

## 1) 설치

```bash
cd pyroo
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2) 실행

```bash
python manage.py migrate
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000` 접속

## 3) API 호출 형식

앱은 기본적으로 아래 OpenAI 호환 엔드포인트를 호출합니다.

- 입력한 Base URL이 `https://example.com` 이면
  - 최종 호출: `https://example.com/v1/chat/completions`
- 입력한 Base URL이 `https://example.com/v1` 이면
  - 최종 호출: `https://example.com/v1/chat/completions`
- 입력한 Base URL이 `.../chat/completions` 로 끝나면
  - 그대로 호출

## 4) 참고

- 토큰, 모델, URL은 브라우저 localStorage에 저장됩니다.
- 배포용에서는 `DEBUG=False`, `SECRET_KEY` 분리, CSRF 강화가 필요합니다.

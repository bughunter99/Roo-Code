import json
from typing import Any

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, "chat/index.html")


def _build_endpoint(base_url: str) -> str:
    clean = base_url.strip().rstrip("/")
    if clean.endswith("/chat/completions"):
        return clean
    if clean.endswith("/v1"):
        return f"{clean}/chat/completions"
    return f"{clean}/v1/chat/completions"


def _extract_answer(data: dict[str, Any]) -> str:
    choices = data.get("choices", [])
    if not choices:
        return "응답을 받지 못했습니다."

    first = choices[0] or {}
    message = first.get("message", {})
    content = message.get("content")

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        if parts:
            return "\n".join(parts)

    return "응답 형식을 해석하지 못했습니다."


@csrf_exempt
@require_http_methods(["POST"])
def ask(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "잘못된 JSON 형식입니다."}, status=400)

    base_url = (body.get("base_url") or "").strip()
    token = (body.get("token") or "").strip()
    model = (body.get("model") or "").strip()
    question = (body.get("question") or "").strip()

    if not base_url:
        return JsonResponse({"error": "Base LLM URL을 입력해주세요."}, status=400)
    if not token:
        return JsonResponse({"error": "토큰을 입력해주세요."}, status=400)
    if not model:
        return JsonResponse({"error": "모델명을 입력해주세요."}, status=400)
    if not question:
        return JsonResponse({"error": "질문을 입력해주세요."}, status=400)

    endpoint = _build_endpoint(base_url)

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        "temperature": 0.7,
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=60)
    except requests.RequestException as exc:
        return JsonResponse({"error": f"LLM 호출 실패: {exc}"}, status=502)

    if resp.status_code >= 400:
        detail = resp.text[:1000]
        return JsonResponse(
            {
                "error": f"LLM 서버 오류 ({resp.status_code})",
                "detail": detail,
            },
            status=502,
        )

    try:
        data = resp.json()
    except ValueError:
        return JsonResponse({"error": "LLM 응답이 JSON이 아닙니다."}, status=502)

    answer = _extract_answer(data)
    return JsonResponse({"answer": answer})

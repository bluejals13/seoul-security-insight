---
name: security
description: API Key, 비밀번호, 토큰, 환경변수(.env, st.secrets) 및 보안 민감 정보를 다루거나 Git 노출 방지 작업을 수행할 때 사용한다.
---

# Security & Credentials Guidelines

## 1. 민감 정보 관리
- **하드코딩 금지**: API key, 비밀번호, 토큰 등 인증 정보는 코드에 직접 작성(하드코딩)하지 않는다.
- **환경 변수/Secret 활용**: `.env` 파일 또는 Streamlit secrets (`.streamlit/secrets.toml`)를 사용한다.
- **Git 커밋 금지**: `.env` 파일, API Key, 인증 정보 파일이 Git에 커밋되지 않도록 `.gitignore` 설정을 철저히 유지한다.

## 2. 외부 데이터 API 요청 및 보안
- 외부 API 호출 실패나 인증 실패가 전체 대시보드 렌더링에 영향을 미치지 않도록 안전한 예외 처리를 구성한다.
- 개인정보 및 민감 데이터가 포함된 경우 비식별화 처리 및 외부 노출을 차단한다.

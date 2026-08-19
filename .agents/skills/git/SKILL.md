---
name: git
description: Git 브랜치, 커밋, PR, 배포 저장소 설정 및 버전 관리 작업을 수행할 때 사용한다.
---

# Git & Deployment Guidelines

## 1. 저장소 및 브랜치 정보
- **Repository**: `bluejals13/seoul-security-insight`
- **Main Branch**: `main`

## 2. Commit & Push 수칙
- API key, 토큰, `.env` 등 민감한 자격 증명 파일은 절대로 Git commit 및 push하지 않는다.
- 파괴적이거나 비가역적인 Git 작업 (`git push --force`, `git reset --hard`, `git clean -fd` 등)은 사전 승인 없이 실행하지 않는다.
- 명확하고 구체적인 Commit message를 작성한다.

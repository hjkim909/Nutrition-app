---

# [PRD] Project: Nutri-Agent Flow (with Claude Code & Antigravity)

**Version:** 1.1

**Lead Agent:** Claude Code (CLI Orchestrator)

**Environment:** Google Antigravity IDE

**Tech Stack:** Python (FastAPI), PostgreSQL, MCP (Model Context Protocol)

---

## 1. 프로젝트 비전 및 협업 구조

본 프로젝트는 Claude Code를 메인 개발 및 실행 에이전트로 활용하여, Antigravity 내의 다양한 데이터 도구와 서브 에이전트를 통합 관리합니다.

* **Claude Code의 역할:** 코드 베이스 관리, 서브 에이전트 스크립트 실행 및 모니터링, 외부 API(MCP 등) 연동 관리.
* **Antigravity의 역할:** 인프라 제공, 에이전트 간 병렬 처리 환경 및 데이터 시각화.

---

## 2. 업데이트된 에이전트 분업 체계 (Agentic Workflow)

Claude Code가 각 서브 에이전트의 결과물을 취합하여 최종 사용자에게 전달하는 구조입니다.

| 에이전트명 | Claude Code와의 상호작용 방식 | 핵심 태스크 |
| --- | --- | --- |
| **Inventory Agent** | 파일 시스템 및 DB 상태 보고 | 냉장고 재고 추적 및 유통기한 임계치 알림 |
| **Nutri-Strategist** | SQL 쿼리 실행 결과 전달 | BMR 기반 영양 Rebalancing 로직 연산 |
| **Recipe Chef** | 추천 레시피 JSON 스키마 제공 | 가용 재료 기반 최적 레시피 생성 |

---

## 3. 핵심 기능 상세 (Technical Specifications)

### 3.1 영양 Rebalancing 알고리즘 (Data-Driven)

데이터 분석가로서의 정교한 접근을 위해, 단순 합산이 아닌 **'영양소 편차 보정'** 로직을 적용합니다.

* **Target:** 일일 권장 섭취량 대비 최근 일간의 이동 평균() 분석.
* **Formula:** 금일 목표 섭취량()은 다음과 같이 조정됩니다.



### 3.2 Claude Code 최적화 인터페이스

* **MCP (Model Context Protocol) 활용:** Claude Code가 Google Antigravity 내부의 PostgreSQL이나 외부 영양소 DB에 직접 쿼리하여 데이터를 가져올 수 있도록 설정합니다.
* **CLI 기반 제어:** 사용자는 자연어로 명령하고, Claude Code는 서브 에이전트들을 순차적 혹은 병렬로 호출하여 결과를 도출합니다.

---

## 4. 데이터 스키마 및 인프라 (Refined)

Claude Code가 읽고 쓰기 편하도록 정형화된 구조를 유지합니다.

* **Database:** PostgreSQL (Antigravity 내장 혹은 Cloud SQL)
* **Logs:** 에이전트 간 통신 로그를 `agent_interaction.log`에 기록하여 Claude Code가 에러 발생 시 스스로 디버깅하도록 설계.

---

## 5. 수익화 모델 및 확장 계획 (Monetization)

* **Phase 1 (MVP):** 개인화 식단 추천 및 재고 관리 (Freemium).
* **Phase 2 (Growth):** 식재료 커머스(Affiliate) 및 운동 데이터 연동.
* **Phase 3 (B2B):** 임직원 건강 관리 대시보드 API 판매.

---

## 6. 개발 로드맵 (Claude Code Action Plan)

1. **Step 1:** Claude Code를 통해 Antigravity 내 프로젝트 구조 생성 및 기본 DB 스키마 마이그레이션.
2. **Step 2:** `Nutri-Strategist` 에이전트의 SQL 분석 모듈 개발 (사용자 히스토리 기반).
3. **Step 3:** Recipe 생성 에이전트와 재고 관리 에이전트 간의 JSON 통신 프로토콜 정의.
4. **Step 4:** 통합 테스트 및 유저 피드백 기반 리밸런싱 로직 고도화.

---

### **💡 개발 꿀팁 (For Data Analyst)**

Claude Code를 쓰실 때, **"Analyze the recent intake trends from the database and suggest a protein-heavy recipe using only the ingredients in the inventory"** 같은 복합 명령을 던져보세요. Claude Code가 `Nutri-Strategist`와 `Inventory Agent`를 동시에 실행하여 최적의 답을 찾아내는 과정을 Antigravity 터미널에서 실시간으로 확인하실 수 있습니다.

**이제 실제 개발에 착수하기 위해, Claude Code에게 전달할 첫 번째 '에이전트 시스템 프롬프트'나 '초기 DB 스키마 SQL'을 짜드릴까요?**
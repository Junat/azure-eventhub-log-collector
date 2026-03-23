# Azure Event Hub Log Collector

Microsoft Azure Event Hub을 활용하여 분산된 시스템의 로그를 중앙에서 수집하고 처리하는 Python 기반 로그 수집 프로그램 프로젝트입니다.

## 💡 프로젝트 개요
여러 소스(서버, 애플리케이션, 센서 등)에서 발생하는 대량의 로그 데이터를 실시간으로 수집하여 Azure Event Hub으로 전송하고, 필요에 따라 이를 소비(Consume)하여 정제하거나 스토리지로 저장하는 것을 목표로 합니다.

## 🚀 주요 기능 아이디어
1. **로그 생산자 (Producer):**
   - 로컬 로그 파일 모니터링 및 실시간 전송
   - HTTP/REST API를 통한 로그 수집 엔드포인트 제공
   - 비동기 방식(`asyncio`)을 통한 고성능 데이터 전송

2. **로그 소비자 (Consumer):**
   - Event Hub에서 데이터를 읽어와서 출력 또는 파일 저장
   - 로그 정제 및 구조화 (JSON 포맷팅)
   - (확장) 데이터베이스(PostgreSQL, MongoDB 등) 연동

3. **운영 편의성:**
   - 환경 변수(`.env`)를 통한 설정 관리 (ConnectionString, HubName 등)
   - 상세 로깅 및 오류 처리 (재시도 메커니즘)
   - Docker 기반 컨테이너화 지원

## 🛠 기술 스택
- **Language:** Python 3.10+
- **SDK:** `azure-eventhub`, `azure-eventhub-checkpointstoreblob-aio`
- **Concurrency:** `asyncio`
- **Environment:** Azure Event Hubs

## 📂 프로젝트 구조 (예시)
```text
.
├── src/
│   ├── producer/          # 로그를 Event Hub로 보내는 모듈
│   ├── consumer/          # Event Hub에서 로그를 읽는 모듈
│   └── common/            # 공통 유틸리티 및 설정
├── tests/                 # 유닛 테스트
├── .env.example           # 환경 변수 템플릿
├── requirements.txt       # 의존성 목록
└── README.md
```

## 📝 초기 할당 작업 (Roadmap)
- [ ] 프로젝트 기본 구조 세팅 (Folder, README)
- [ ] `azure-eventhub` 라이브러리를 활용한 기본 연결 테스트
- [ ] 환경 변수 관리 모듈 구현
- [ ] Async Producer 구현 (간단한 메시지 전송)
- [ ] Async Consumer 구현 (메시지 수신 확인)

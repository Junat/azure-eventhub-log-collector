# Local Event Hubs Emulator Setup Guide

클라우드 비용 걱정 없이 로컬 환경에서 Azure Event Hubs와 통신하는 로그 수집기를 개발하기 위한 에뮬레이터 설정 가이드입니다.

## 🛠 필수 준비물
- **Docker Desktop**: 설치 및 실행 중이어야 합니다.
- **Docker Compose**: 멀티 컨테이너 실행을 위해 필요합니다.

## 🚀 에뮬레이터 구성 요소
1. **Event Hubs Emulator**: 실제 Event Hubs 서비스의 핵심 기능을 로컬에서 재현합니다.
2. **Azurite**: Event Hubs의 체크포인트(Checkpoint) 저장을 위한 Azure Storage Emulator입니다.

## 📦 1. Docker Compose 설정 (`docker-compose.yml`)
프로젝트 루트에 아래 내용으로 `docker-compose.yml` 파일을 생성합니다.

```yaml
version: '3.8'

services:
  # Azure Storage Emulator (체크포인트 저장용)
  azurite:
    image: mcr.microsoft.com/azure-storage/azurite
    container_name: azurite
    ports:
      - "10000:10000"
      - "10001:10001"
      - "10002:10002"

  # Event Hubs Emulator
  eventhubs-emulator:
    image: mcr.microsoft.com/azure-messaging/eventhubs-emulator:latest
    container_name: eventhubs-emulator
    depends_on:
      - azurite
    ports:
      - "5672:5672"   # AMQP port
      - "9093:9093"   # Kafka port
    environment:
      - AZURE_EVENTHUBS_CONNECTION_STRING=Endpoint=sb://localhost;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=SAS_Key_Value;EntityPath=ehub-local
      - ACCEPT_EULA=Y
```

## 🏃 2. 에뮬레이터 실행 방법
터미널에서 프로젝트 루트 폴더로 이동한 후 아래 명령어를 실행합니다.

```bash
# 에뮬레이터 시작 (백그라운드 실행)
docker-compose up -d

# 실행 상태 확인
docker ps
```

## 🔗 3. 로컬 개발용 연결 정보
개발 중인 로그 수집기 코드에서 아래 정보를 사용하여 연결합니다.

- **Connection String**: `Endpoint=sb://localhost;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=SAS_Key_Value;EntityPath=ehub-local`
- **Event Hub Name**: `ehub-local`
- **Consumer Group**: `$Default`

## ✅ 4. 정상 작동 확인 (Checklist)
- [ ] `docker ps` 명령어로 `eventhubs-emulator`와 `azurite` 컨테이너가 `Up` 상태인지 확인
- [ ] Python 코드에서 `azure-eventhub` 라이브러리를 통해 연결 테스트 수행
- [ ] 메시지 송신 후 에뮬레이터 로그에서 수신 여부 확인 (`docker logs eventhubs-emulator`)

## ⚠️ 주의 사항
- 에뮬레이터는 **로컬 개발 및 테스트 전용**입니다.
- 실제 Azure 환경으로 이전할 때는 연결 문자열(Connection String)만 실제 Azure 포털에서 복사한 값으로 변경하면 됩니다.

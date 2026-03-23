# Azure Event Hubs 인증 및 클라우드 전환 가이드

본 가이드는 로컬 에뮬레이터에서 개발된 코드를 실제 Azure 클라우드 환경으로 전환할 때 필요한 인증 방식과 보안 베스트 프랙티스를 정리합니다.

## 🔐 인증 방식 비교

실제 운영 환경에서는 보안 수준에 따라 다음과 같은 인증 방식을 선택할 수 있습니다.

| 방식 | 보안 수준 | 특징 | 권장 상황 |
| :--- | :--- | :--- | :--- |
| **SAS (Connection String)** | 낮음 | 가장 단순함. 문자열 하나로 모든 권한 제어. | 초기 테스트, 로컬 개발 |
| **Managed Identity (추천)** | **매우 높음** | 암호/키가 필요 없음. Azure 리소스(VM 등) 자체에 권한 부여. | **Azure 서비스 내 구동 시 필수** |
| **Service Principal** | 높음 | App Registration을 통해 클라이언트 ID/Secret 사용. | Azure 외부(온프레미스) 구동 시 |

---

## 🛠 1. Vault 연동 및 인증 (회사 환경)

사용자님의 회사에서 Vault(예: Azure Key Vault)를 사용하신다면, 아래와 같이 **Managed Identity**를 사용하여 Vault에서 안전하게 정보를 가져오는 구조가 가장 일반적입니다.

### 필수 라이브러리 설치
```bash
pip install azure-identity azure-keyvault-secrets azure-eventhub
```

### Vault 연동 코드 예시
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.eventhub import EventHubProducerClient

# 1. DefaultAzureCredential 설정 (로컬 개발 환경과 Azure 환경 자동 감지)
credential = DefaultAzureCredential()

# 2. Key Vault에서 Connection String 가져오기
vault_url = "https://<your-vault-name>.vault.azure.net/"
secret_client = SecretClient(vault_url=vault_url, credential=credential)
connection_string = secret_client.get_secret("EventHubConnectionString").value

# 3. 가져온 인증 정보로 Event Hub 연결
producer = EventHubProducerClient.from_connection_string(
    conn_str=connection_string,
    eventhub_name="your-event-hub-name"
)
```

---

## 🚀 2. 에뮬레이터에서 클라우드로 전환하기

현재 작성된 코드는 에뮬레이터를 사용하고 있습니다. 실제 Azure로 전환할 때 다음 세 가지 환경 변수만 변경하면 코드는 수정 없이 작동합니다.

### .env 파일 수정 예시 (Production)
```bash
# 로컬 에뮬레이터 대신 실제 Azure 정보를 입력합니다.
EVENT_HUB_CONNECTION_STR="Endpoint=sb://<your-ns>.servicebus.windows.net/;SharedAccessKeyName=...;SharedAccessKey=..."
EVENT_HUB_NAME="<real-hub-name>"
CONSUMER_GROUP="$Default"

# 체크포인트용 실제 Azure Storage 연결 정보
AZURE_STORAGE_CONNECTION_STR="DefaultEndpointsProtocol=https;AccountName=<acc>;AccountKey=<key>;..."
```

---

## 💡 3. 보안 베스트 프랙티스 (Checklist)

1.  **Passwordless 권장**: 가능하면 Connection String(SAS) 대신 **Managed Identity**를 사용하여 Event Hub에 직접 권한(RBAC)을 부여하세요.
    *   역할: `Azure Event Hubs Data Sender` (생산자용)
    *   역할: `Azure Event Hubs Data Receiver` (소비자용)
2.  **DefaultAzureCredential 활용**: 이 라이브러리를 사용하면 로컬에서는 `az login` 정보를, 서버에서는 Managed Identity를 자동으로 사용하여 코드를 변경할 필요가 없습니다.
3.  **최소 권한 원칙**: Vault에서 비밀 정보를 읽을 때도 해당 App의 ID에 `Key Vault Secrets User` 권한만 부여하세요.
4.  **로그 보안**: 실시간 로그 수집 시 로그 내용에 비밀번호나 개인정보(PII)가 포함되지 않도록 필터링 로직을 추가하는 것이 좋습니다.

---

## 📝 내일의 할 일 (Roadmap)
- [ ] 실제 Azure 리소스(Event Hub, Key Vault) 생성 확인
- [ ] `DefaultAzureCredential`을 활용한 인증 로직 통합 테스트
- [ ] 회사 Vault에서 인증 정보를 읽어오는 공통 모듈 작성

import asyncio
import logging
import json
import datetime
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from ..common.config import Config

# 로깅 설정
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger("Producer")

async def send_log(message: dict):
    """Event Hub로 로그 메시지를 하나 보냅니다."""
    # 설정 검증
    Config.validate()

    # 클라이언트 생성
    producer = EventHubProducerClient.from_connection_string(
        conn_str=Config.EVENT_HUB_CONNECTION_STR,
        eventhub_name=Config.EVENT_HUB_NAME
    )

    async with producer:
        # 메시지 생성
        event_data_batch = await producer.create_batch()
        
        # 메시지에 현재 시간 추가
        message["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        event_data = EventData(json.dumps(message))
        event_data_batch.add(event_data)
        
        # 전송
        await producer.send_batch(event_data_batch)
        logger.info(f"로그 전송 완료: {message}")

async def main():
    """테스트용 메인 함수"""
    test_log = {"source": "test-app", "level": "INFO", "message": "Hello Azure Event Hub!"}
    await send_log(test_log)

if __name__ == "__main__":
    asyncio.run(main())

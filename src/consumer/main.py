import asyncio
import logging
from azure.eventhub.aio import EventHubConsumerClient
from ..common.config import Config

# 로깅 설정
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger("Consumer")

async def on_event(partition_context, event):
    """메시지 수신 시 처리할 콜백 함수"""
    logger.info(f"수신한 메시지: {event.body_as_str()}")
    # 체크포인트 저장 (에뮬레이터에서도 작동)
    await partition_context.update_checkpoint(event)

async def main():
    """Event Hub에서 로그를 지속적으로 수신합니다."""
    # 설정 검증
    Config.validate()

    # 클라이언트 생성
    client = EventHubConsumerClient.from_connection_string(
        conn_str=Config.EVENT_HUB_CONNECTION_STR,
        consumer_group=Config.CONSUMER_GROUP,
        eventhub_name=Config.EVENT_HUB_NAME
    )

    async with client:
        logger.info("로그 수신 대기 중...")
        # 메시지 수신 시작
        await client.receive(on_event=on_event)

if __name__ == "__main__":
    asyncio.run(main())

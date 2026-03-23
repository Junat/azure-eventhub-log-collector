import asyncio
import logging
import json
import datetime
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from ..common.config import Config
from .file_tailer import tail_file

# 로깅 설정
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger("Producer")

async def run_producer():
    """파일의 변화를 감지하여 Event Hub로 실시간 전송합니다."""
    # 설정 검증
    Config.validate()

    logger.info(f"생산자 시작: {Config.LOG_FILE_PATH} 모니터링 중...")

    # 클라이언트 생성
    client = EventHubProducerClient.from_connection_string(
        conn_str=Config.EVENT_HUB_CONNECTION_STR,
        eventhub_name=Config.EVENT_HUB_NAME
    )

    async with client:
        # 파일의 새로운 라인을 실시간으로 읽어옴
        async for line in tail_file(Config.LOG_FILE_PATH):
            if not line:
                continue
                
            try:
                # 메시지 구성
                message = {
                    "source": "macos-system-log",
                    "file": Config.LOG_FILE_PATH,
                    "content": line,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
                }

                # 배치 생성 (단일 메시지라도 배치 사용이 권장됨)
                batch = await client.create_batch()
                batch.add(EventData(json.dumps(message, ensure_ascii=False)))
                
                # 전송
                await client.send_batch(batch)
                logger.info(f"로그 전송됨: {line[:50]}...")
            
            except Exception as e:
                logger.error(f"메시지 전송 실패: {e}")
                # 재시도 전 잠깐 대기
                await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(run_producer())
    except KeyboardInterrupt:
        logger.info("생산자 종료 중...")

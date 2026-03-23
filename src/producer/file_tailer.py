import asyncio
import os
import aiofiles
import logging

logger = logging.getLogger("FileTailer")

async def tail_file(file_path: str):
    """
    지정된 파일을 실시간으로 모니터링하여 새로운 라인을 yield합니다.
    (Unix 'tail -f' 기능과 유사)
    """
    if not os.path.exists(file_path):
        logger.error(f"파일을 찾을 수 없습니다: {file_path}")
        return

    async with aiofiles.open(file_path, mode='r') as f:
        # 파일의 끝으로 이동
        await f.seek(0, os.SEEK_END)
        logger.info(f"파일 모니터링 시작: {file_path}")

        while True:
            line = await f.readline()
            if not line:
                # 새로운 내용이 없으면 잠시 대기
                await asyncio.sleep(1)
                continue
            
            # 한 라인을 yield (개행 문자 제거)
            yield line.strip()

async def example():
    """테스트용 예시 코드"""
    async for line in tail_file("/var/log/system.log"):
        print(f"New line: {line}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(example())

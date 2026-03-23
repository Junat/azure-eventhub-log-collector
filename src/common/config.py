import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    """애플리케이션 설정을 관리하는 클래스"""
    # Azure Event Hubs 설정
    EVENT_HUB_CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STR")
    EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")
    CONSUMER_GROUP = os.getenv("CONSUMER_GROUP", "$Default")

    # Azure Storage 설정 (체크포인트용)
    AZURE_STORAGE_CONNECTION_STR = os.getenv("AZURE_STORAGE_CONNECTION_STR")
    CHECKPOINT_CONTAINER_NAME = os.getenv("CHECKPOINT_CONTAINER_NAME", "checkpoint-container")

    # 로그 설정
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "/var/log/system.log")

    @classmethod
    def validate(cls):
        """필수 설정값이 있는지 검증"""
        missing = []
        if not cls.EVENT_HUB_CONNECTION_STR: missing.append("EVENT_HUB_CONNECTION_STR")
        if not cls.EVENT_HUB_NAME: missing.append("EVENT_HUB_NAME")
        
        if missing:
            raise ValueError(f"필수 환경 변수가 누락되었습니다: {', '.join(missing)}")
        return True

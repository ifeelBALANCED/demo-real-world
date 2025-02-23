import os


class EnvParser:
    @staticmethod
    def str(key: str, default: str = None) -> str:
        return os.getenv(key, default)

    @staticmethod
    def int(key: str, default: int = None) -> int:
        value = os.getenv(key, default)
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def bool(key: str, default: bool = None) -> bool:
        value = os.getenv(key, default)
        if isinstance(value, str):
            if value.lower() in ["true", "1", "yes"]:
                return True
            elif value.lower() in ["false", "0", "no"]:
                return False
        return default

    @staticmethod
    def list(key: str, default: list = None) -> list:
        value = os.getenv(key, default)
        if isinstance(value, str):
            return [item.strip() for item in value.split(",")]
        return default

    @staticmethod
    def dict(key: str, default: dict = None) -> dict:
        value = os.getenv(key, default)
        if isinstance(value, str):
            items = [item.split("=") for item in value.split(",")]
            return {key.strip(): val.strip() for key, val in items}
        return default


def convert_bytes_to_mb(file_size):
    """
    1 MB = 1000^2 bytes
    1 MiB = 1024^2 bytes
    https://stackoverflow.com/questions/2365100/converting-bytes-to-megabytes
    """
    return float(file_size / (1000**2))

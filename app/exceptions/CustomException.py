from typing import Any, Dict, Optional
from sqlalchemy.orm import Session


class CustomException(Exception):
    def __init__(
        self,
        db: Session,
        status_code: int,
        info: Any = None,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        language: Optional[str] = None
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.info = info
        self.headers = headers

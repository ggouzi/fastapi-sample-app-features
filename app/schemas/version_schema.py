from pydantic import BaseModel


class Version(BaseModel):
    id: int
    version: str
    supported: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "version": "1.0",
                    "supported": True
                }
            ]
        }
    }

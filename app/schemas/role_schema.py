from pydantic import BaseModel
from enum import Enum


class RoleStr(str, Enum):
    USER = 'user'
    ADMIN = 'admin'


class RoleBase(BaseModel):
    name: RoleStr

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Admin"
                }
            ]
        }
    }


class Role(RoleBase):
    id: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Admin"
                }
            ]
        }
    }

from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ItemCreate(BaseModel):
    name: str
    description: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "item name",
                    "description": "item description",
                }
            ]
        }
    }


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "item name",
                    "description": "item description",
                }
            ]
        }
    }
    pass


class ItemResponse(ItemCreate):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    user_id: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "item name",
                    "description": "item description",
                    "updated_at": "2023-10-15T20:40:10",
                    "created_at": "2023-10-15T20:45:08",
                    "user_id": 2
                }
            ]
        }
    }


class Item(ItemResponse):
    model_config = ConfigDict(from_attributes=True)


class ItemList(BaseModel):
    page: int
    limit: int
    total: int
    items: List[Item]

from pydantic import BaseModel


class Status(BaseModel):
    detail: str


responses = {
    201: {
        "content": {"application/json": {
            "example": {"detail": "Return a HTTP 201 on resource creation"}
        }},
        "model": Status,
        "description": "Return created"
    },
    400: {
        "content": {"application/json": {
            "example": {"detail": "Invalid role_id 3"}
        }},
        "model": Status,
        "description": "Bad request"
    },
    401: {
        "content": {"application/json": {
            "example": {"detail": "Invalid username/password"}
        }},
        "model": Status,
        "description": "Invalid credentials"
    },
    403: {
        "content": {"application/json": {
            "example": {"detail": "Foridden access"}
        }},
        "model": Status,
        "description": "Foridden access: You do not have access to edit this resource"
    },
    404: {
        "content": {"application/json": {
            "example": {"detail": "Not found"}
        }},
        "model": Status,
        "description": "Resource was not found"
    },
    409: {
        "content": {"application/json": {
            "example": {"detail": "Item with the same name is already registered"}
        }},
        "model": Status,
        "description": "Conflict"
    },
    422: {
        "content": {"application/json": {
            "example": {"detail": "Unexpected JSON payload"}
        }},
        "model": Status,
        "description": "Wrong datatype in input"
    },
    426: {
        "content": {"application/json": {
            "example": {"detail": "Version 0.X not supported"}
        }},
        "model": Status,
        "description": "Version X is not supported anymore"
    },
    500: {
        "content": {"application/json": {
            "example": {"detail": "Internal error: Failed to update User"}
        }},
        "model": Status,
        "description": "Internal error"
    }
}


def get_responses(arr):
    result = {}
    for status_code in arr:
        if status_code in responses:
            result[status_code] = responses[status_code]
    return result

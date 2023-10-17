from pydantic import BaseModel


class Status(BaseModel):
    detail: str


responses = {
    201: {
        "content": {"application/json": {
            "example": {"detail": "Resource created"}
        }},
        "model": Status,
        "description": "Return a HTTP 201 on resource creation"
    },
    400: {
        "content": {"application/json": {
            "example": {"detail": "Bad request"}
        }},
        "model": Status,
        "description": "Cannot find role_id 3"
    },
    401: {
        "content": {"application/json": {
            "example": {"detail": "Invalid credentials"}
        }},
        "model": Status,
        "description": "Invalid username/password"
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
        "description": "Item with the same name is already registered"
    },
    422: {
        "content": {"application/json": {
            "example": {"detail": "Wrong datatype in input"}
        }},
        "model": Status,
        "description": "JSON input payload is not expected"
    },
    426: {
        "content": {"application/json": {
            "example": {"detail": "Version 0.X not supported"}
        }},
        "model": Status,
        "description": "Version 0.9 is not supported anymore"
    },
    500: {
        "content": {"application/json": {
            "example": {"detail": "Internal server error"}
        }},
        "model": Status,
        "description": "Internal error: Failed to update User"
    }
}


def get_responses(arr):
    result = {}
    for status_code in arr:
        if status_code in responses:
            result[status_code] = responses[status_code]
    return result

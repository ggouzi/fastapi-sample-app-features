from pydantic import BaseModel


class AuthLogin(BaseModel):
    username: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "username",
                    "password": "password"
                }
            ]
        }
    }


class AuthToken(BaseModel):
    id: int
    access_token: str
    expires: int
    refresh_token: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "access_token": "IYIPy4728BDS8CIqQLmIqbL1kANdinIU0jH2bbOj41BzBaAWD0GDr44gL9AxJQySlrx2FXufgHQW7kjS92oiGsmBuVnAvq8XWh2KrP5Bbd2cMf8L4FmFtcfFAtgKGcrE",
                    "expires": 7200,
                    "id": 1,
                    "refresh_token": "0GRZWIUy1pPH3Y7RoLHtEOSRCRMQufOVD0Sh3RuDZnymcaSrX0eI4N6KFGYoyIDN4wRvGX5mEQ16w1M99WO8NXddEQMmXIjaA0MZzS3MQBYkZtFnhPymgNkPN0FAgv75"
                }
            ]
        }
    }


class AuthRefresh(BaseModel):
    refresh_token: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "refresh_token": "0GRZWIUy1pPH3Y7RoLHtEOSRCRMQufOVD0Sh3RuDZnymcaSrX0eI4N6KFGYoyIDN4wRvGX5mEQ16w1M99WO8NXddEQMmXIjaA0MZzS3MQBYkZtFnhPymgNkPN0FAgv75"
                }
            ]
        }
    }

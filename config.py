from pydantic import BaseSettings

class Setting(BaseSettings):
    db_password : str
    db_name : str

    class Config:
        env_file = '.env'

settings = Setting()
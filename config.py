from pydantic import BaseSettings

class Setting(BaseSettings):
    db_password : str
    db_name : str
    db_host : str
    db_port : int
    db_user : str
    class Config:
        env_file = '.env'

settings = Setting()
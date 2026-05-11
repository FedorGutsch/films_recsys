from pydantic_settings import SettingsConfigDict, BaseSettings
from enum import Enum

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8' ,extra='ignore', case_sensitive=True)

class Age_limits(Enum):
    ALL_AGES = '0+'
    KIDS_FROM_6_TO_12 = '6+'
    KIDS_FROM_12_TO_16 = '12+'
    KIDS_FROM_16_TO_18 = '16+'
    ADULTS = '18+'


settings = Settings()
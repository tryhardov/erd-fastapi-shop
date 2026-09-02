from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'FastAPI Enfants Riches Deprimes'
    debug: bool = True
    database_url: str = 'sqlite+aiosqlite:///./erd.db'
    cors_origins: list[str] = [
        'http://localhost:3000',
        'http://localhost:5173',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5173'
    ]
    static_dir: str = 'static'
    images_dir: str = 'static/images'
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
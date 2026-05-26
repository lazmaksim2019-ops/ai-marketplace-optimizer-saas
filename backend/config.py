from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str = ""
    proxy_host: str = ""
    proxy_port: int = 0
    proxy_user: str = ""
    proxy_pass: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def proxy_url(self) -> str | None:
        if self.proxy_host and self.proxy_port:
            if self.proxy_user and self.proxy_pass:
                return f"socks5://{self.proxy_user}:{self.proxy_pass}@{self.proxy_host}:{self.proxy_port}"
            return f"socks5://{self.proxy_host}:{self.proxy_port}"
        return None


settings = Settings()

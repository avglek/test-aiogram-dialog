from dataclasses import dataclass
from environs import Env


@dataclass
class TelegramBotConfig:
    token: str


@dataclass
class Config:
    tg_bot: TelegramBotConfig


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(tg_bot=TelegramBotConfig(token=env.str("BOT_TOKEN")))
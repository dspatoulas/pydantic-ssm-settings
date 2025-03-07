import logging
from typing import Any, Tuple, Type

from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    InitSettingsSource,
    PydanticBaseSettingsSource,
    SecretsSettingsSource,
    SettingsConfigDict,
)

from .source import AwsSsmSettingsSource

logger = logging.getLogger(__name__)


class SsmSettingsConfigDict(SettingsConfigDict):
    ssm_prefix: str


class BaseSettingsSsmWrapper(BaseSettings):
    """
    Wrapper to store the _ssm_prefix parameter as an instanc attribute.
    Need a direct access to the attributes dictionary to avoid raising an AttributeError:
    __pydantic_private__ exception
    """

    def __init__(self, *args, _ssm_prefix: str = None, **kwargs: Any) -> None:
        """
        Args:
            _ssm_prefix: Prefix for all ssm parameters. Must be an absolute path,
            separated by "/". NB:unlike its _env_prefix counterpart, _ssm_prefix
            is treated case sensitively regardless of the _case_sensitive
            parameter value.
        """
        self.__dict__["__ssm_prefix"] = _ssm_prefix
        super().__init__(self, *args, **kwargs)


class AwsSsmSourceConfig(BaseSettingsSsmWrapper):
    def settings_customise_sources(
        self,
        settings_cls: Type[BaseSettings],
        init_settings: InitSettingsSource,
        env_settings: EnvSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: SecretsSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        ssm_settings = AwsSsmSettingsSource(
            settings_cls=settings_cls,
            ssm_prefix=self.__dict__["__ssm_prefix"],
        )

        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            ssm_settings,
        )

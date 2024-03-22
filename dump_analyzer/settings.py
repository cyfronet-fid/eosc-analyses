# pylint: disable=too-few-public-methods

import logging
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from dump_analyzer.data_loader.schema.properties.data import (
    AFFILIATION,
    AUTHOR,
    BESTACCESSRIGHT,
    CONTAINER,
    CONTEXT,
    COUNTRY,
    EOSCIF,
    GEOLOCATION,
    INDICATOR,
    INSTANCE,
    LANGUAGE,
    PID,
    PROJECT,
    PROVENANCE,
    RELATIONS,
    SUBJECT,
)

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Configuration parameters"""

    # Logging Level
    LOG_LEVEL: str = logging.getLevelName(logging.INFO)

    # Paths for data sources
    DATASET_PATH: str = "input/dataset"
    PUBLICATION_PATH: str = "input/publication"
    SOFTWARE_PATH: str = "input/software"
    OTHER_RP_PATH: str = "input/other_rp"
    METADATA_PATH: str = "output/metadata"
    PROCESSED_METADATA_PATH: str = "output/processed_metadata"

    # Defined data types, "type" property of each data type
    SOFTWARE: str = "software"
    OTHER_RP: str = "other_rp"
    DATASET: str = "dataset"
    PUBLICATION: str = "publication"

    DUMP_YYYYMM: str = "YYYYMM"

    NESTED_FIELDS_LIST: List = [
        AFFILIATION,
        AUTHOR,
        BESTACCESSRIGHT,
        CONTAINER,
        CONTEXT,
        COUNTRY,
        EOSCIF,
        GEOLOCATION,
        INDICATOR,
        INSTANCE,
        LANGUAGE,
        PID,
        PROJECT,
        PROVENANCE,
        RELATIONS,
        SUBJECT,
    ]

    # Get config from .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    COLLECTIONS: dict = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialize_additional_configs()

    def initialize_additional_configs(self):
        self.COLLECTIONS = self.get_collections_config()

    def get_collections_config(self) -> dict:
        """Get collections config"""
        INPUT_PATH = "INPUT_PATH"
        METADATA = "METADATA"

        collections = {
            self.SOFTWARE: {
                INPUT_PATH: self.SOFTWARE_PATH,
                METADATA: os.path.join(self.METADATA_PATH, self.SOFTWARE),
            },
            self.OTHER_RP: {
                INPUT_PATH: self.OTHER_RP_PATH,
                METADATA: os.path.join(self.METADATA_PATH, self.OTHER_RP),
            },
            self.DATASET: {
                INPUT_PATH: self.DATASET_PATH,
                METADATA: os.path.join(self.METADATA_PATH, self.DATASET),
            },
            self.PUBLICATION: {
                INPUT_PATH: self.PUBLICATION_PATH,
                METADATA: os.path.join(self.METADATA_PATH, self.PUBLICATION),
            },
        }

        return collections


settings = Settings()

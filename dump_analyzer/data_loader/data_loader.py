import json
import os
import inspect
import pandas as pd
from enum import Enum
from logging import getLogger
from pydantic import BaseModel
from typing import Dict, Generator, List, Type
from tqdm import tqdm
from dump_analyzer.settings import settings

logger = getLogger(__name__)


def normalize_directory_name(directory_name: str) -> str:
    """
    Normalize directory names to match the naming convention used in settings.
    Parameters:
        directory_name (str): The original directory name.
    Returns:
        str: The normalized directory name.
    """
    normalization_map = {
        "organization": "organisation",
        "otherresearchproduct": "other_rp",
    }
    return normalization_map.get(directory_name, directory_name)


def process_file(
    file_path: str, model: Type[BaseModel]
) -> Generator[BaseModel, None, None]:
    with open(file_path, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                yield model.parse_obj(data)
            except Exception as e:
                logger.error(f"Error parsing item in {file_path=}: {e}\n{line=}")


def convert_model_to_dict(value, parent_key=None) -> dict:
    """
    Convert a value to a dictionary, handling Enums, lists, and Pydantic models.
    """
    if isinstance(value, BaseModel):
        return {
            f"{parent_key}_{k}" if parent_key else k: convert_model_to_dict(v, k)
            for k, v in value.dict().items()
        }
    elif isinstance(value, Enum):
        return value.value
    elif isinstance(value, list):
        return [convert_model_to_dict(item, parent_key) for item in value]
    else:
        return value


def process_and_save_data(path: str, model: Type[BaseModel]) -> None:

    settings_collection = os.path.basename(path.rstrip(os.sep))

    files_generator = (
        os.path.join(root, file_name)
        for root, _, files in os.walk(path)
        for file_name in files
        if file_name.endswith(".json")
    )

    total_files = sum(1 for _ in files_generator)

    files_generator = (
        os.path.join(root, file_name)
        for root, _, files in os.walk(path)
        for file_name in files
        if file_name.endswith(".json")
    )

    dataframes: Dict[str, List] = {
        field_name: []
        for field_name in model.__fields__
        if field_name in settings.NESTED_FIELDS_LIST
    }
    one_lvl_data: Dict[str, List] = {
        field_name: []
        for field_name in model.__fields__
        if field_name not in settings.NESTED_FIELDS_LIST
    }

    for file_path in tqdm(files_generator, total=total_files, desc="Processing Files"):
        for rp in process_file(file_path, model):
            rp_id_type_data = {
                "rp_id": rp.id,
                "rp_type": rp.type,
                "rp_publisher": rp.publisher,
            }
            for field_name, field_type in model.__fields__.items():
                field_data = getattr(rp, field_name, None)
                if field_name in settings.NESTED_FIELDS_LIST:
                    converted_field_data = convert_model_to_dict(field_data, parent_key=field_name)
                else:
                    converted_field_data = convert_model_to_dict(field_data)

                if field_name in settings.NESTED_FIELDS_LIST:
                    if converted_field_data:
                        if isinstance(converted_field_data, list):
                            for item in converted_field_data:
                                if isinstance(item, dict):
                                    item.update(rp_id_type_data)
                            dataframes[field_name].extend(converted_field_data)
                        elif isinstance(converted_field_data, dict):
                            converted_field_data.update(rp_id_type_data)
                            dataframes[field_name].append(converted_field_data)
                        else:
                            single_field_data = {field_name: converted_field_data}
                            single_field_data.update(rp_id_type_data)
                            dataframes[field_name].append(single_field_data)
                    else:
                        if inspect.isclass(field_type) and issubclass(field_type, BaseModel):
                            empty_data = {nested_field: None for nested_field in field_type.__fields__}
                            empty_data.update(rp_id_type_data)
                            dataframes[field_name].append(empty_data)
                        else:
                            # For fields that are not Pydantic models, just append rp_id_type_data
                            dataframes[field_name].append(rp_id_type_data)
                else:
                    if isinstance(converted_field_data, dict):
                        converted_field_data.update(rp_id_type_data)
                    one_lvl_data[field_name].append(converted_field_data)

    for field_name, data in tqdm(dataframes.items(), desc="Saving DataFrames"):
        if data:
            df = pd.DataFrame(data)
            df.to_parquet(
                os.path.join(
                    settings.COLLECTIONS[normalize_directory_name(settings_collection)]['METADATA'],
                    f"{normalize_directory_name(settings_collection)}_{field_name}.parquet",
                ),
                index=False,
            )

    one_lvl_df = pd.DataFrame(one_lvl_data)
    one_lvl_df.to_parquet(
        os.path.join(
            settings.COLLECTIONS[normalize_directory_name(settings_collection)]['METADATA'],
            f"{normalize_directory_name(settings_collection)}_one_level_data.parquet",
        ),
        index=False,
    )

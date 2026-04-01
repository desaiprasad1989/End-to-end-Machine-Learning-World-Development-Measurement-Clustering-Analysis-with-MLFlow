from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
    data_path: Path
    cleaned_data_path: Path
    schema_path: Path
    INGESTION_REPORT: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    unzip_data_dir: Path
    STATUS_FILE: str
    all_schema: dict
    number_of_columns: int
    VALIDATION_REPORT: Path


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    transformed_data_path: Path
    preprocessor_obj_file_path: Path
    transformed_data_obj_file_path: Path
    TRANSFORMATION_REPORT: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    transformed_data_path: Path 
    model_params: dict
    TRAINING_REPORT: Path

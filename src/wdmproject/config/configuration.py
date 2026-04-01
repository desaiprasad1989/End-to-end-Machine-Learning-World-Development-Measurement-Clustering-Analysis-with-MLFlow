from wdmproject.constants import *
from wdmproject.utils.common import read_yaml, create_directories
from wdmproject.entity.config_entity import(DataIngestionConfig,
                                            DataValidationConfig,
                                            DataTransformationConfig,
                                            ModelTrainerConfig)


class ConfigurationManager:
    def __init__(
        self,
        config_filepath: Path = CONFIG_FILE_PATH,
        params_filepath: Path = PARAMS_FILE_PATH,
        schema_filepath: Path = SCHEMA_FILE_PATH
    ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        create_directories([self.config.artifacts_root])
    
    #-------------------------------------------------------
    # Data Ingestion related configuration
    #-------------------------------------------------------

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
            data_path=Path(config.data_path),
            cleaned_data_path=Path(config.cleaned_data_path),
            schema_path=Path(config.schema_path),
            INGESTION_REPORT=Path(config.INGESTION_REPORT)
        )
        
        return data_ingestion_config
    
    #-------------------------------------------------------
    # Data Validation related configuration
    #-------------------------------------------------------

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema_columns = self.schema.COLUMNS
        number_of_columns = self.schema.NUMBER_OF_COLUMNS

        create_directories([config.root_dir])
        
        data_validation_config = DataValidationConfig(
            root_dir=Path(config.root_dir),
            unzip_data_dir=Path(config.unzip_data_dir),
            STATUS_FILE=Path(config.STATUS_FILE),
            all_schema=schema_columns,
            number_of_columns=number_of_columns,
            VALIDATION_REPORT=Path(config.VALIDATION_REPORT),
        )
        
        return data_validation_config
    
    #-------------------------------------------------------
    # Data Transformation related configuration
    #-------------------------------------------------------
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path),
            transformed_data_path=Path(config.transformed_data_path),
            preprocessor_obj_file_path=Path(config.preprocessor_obj_file_path),
            transformed_data_obj_file_path=Path(config.transformed_data_obj_file_path),
            TRANSFORMATION_REPORT=Path(config.TRANSFORMATION_REPORT)
        )

        return data_transformation_config
    
    #-------------------------------------------------------
    # Model Trainer related configuration
    #-------------------------------------------------------

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.model_training

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=Path(config.root_dir),
            transformed_data_path=Path(config.transformed_data_path),
            model_params=params,
            TRAINING_REPORT=Path(config.TRAINING_REPORT)
        )

        return model_trainer_config
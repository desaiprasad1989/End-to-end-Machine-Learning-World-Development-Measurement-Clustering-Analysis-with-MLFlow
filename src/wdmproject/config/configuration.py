from wdmproject.constants import *
from wdmproject.utils.common import read_yaml, create_directories
from wdmproject.entity.config_entity import(DataIngestionConfig,
                                            DataValidationConfig)


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
            INGESTION_REPORT=Path(config.INGESTION_REPORT)
        )
        
        return data_ingestion_config
    
    #-------------------------------------------------------
    # Data Ingestion related configuration
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
from wdmproject.config.configuration import ConfigurationManager
from wdmproject.components.data_validation import DataValidation
from wdmproject import logger

STAGE_NAME = "Data Validation"

class DataValidationPipeline:
    def __init__(self):
        pass


    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()
        logger.info(f"Data Validation Pipeline Completed Successfully.")



if __name__ == '__main__':
    try:
        logger.info(f">>>>> Stage :  {STAGE_NAME} Initiated.... <<<<<")
        obj =  DataValidationPipeline()
        obj.main()
        logger.info(f">>>>> Stage : {STAGE_NAME} Completed Successfully ! <<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
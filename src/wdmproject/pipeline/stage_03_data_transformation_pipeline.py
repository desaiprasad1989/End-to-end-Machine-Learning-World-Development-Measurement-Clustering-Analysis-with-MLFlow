from wdmproject.config.configuration import ConfigurationManager
from wdmproject.components.data_transformation import DataTransformation
from wdmproject import logger

STAGE_NAME = "Data Transformation"

class DataTransformationPipeline:
    def __init__(self):
        pass


    def main(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.initiate_data_transformation()
        logger.info(f"Data Transformation Pipeline Completed Successfully.")



if __name__ == '__main__':
    try:
        logger.info(f">>>>> Stage :  {STAGE_NAME} Initiated.... <<<<<")
        obj =  DataTransformationPipeline()
        obj.main()
        logger.info(f">>>>> Stage : {STAGE_NAME} Completed Successfully ! <<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
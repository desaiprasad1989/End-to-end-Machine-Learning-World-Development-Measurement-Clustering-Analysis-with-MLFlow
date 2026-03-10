from wdmproject.config.configuration import ConfigurationManager
from wdmproject.components.data_ingestion import DataIngestion
from wdmproject import logger


STAGE_NAME   = "Data Ingestion"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.initiate_data_ingestion()


if __name__ == "__main__":
    try:
        logger.info(f">>>>> Stage :  {STAGE_NAME} Initiated.... <<<<<")
        data_ingestion_pipeline = DataIngestionPipeline()
        data_ingestion_pipeline.main()
        logger.info(f">>>>> Stage : {STAGE_NAME} Completed Successfully ! <<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
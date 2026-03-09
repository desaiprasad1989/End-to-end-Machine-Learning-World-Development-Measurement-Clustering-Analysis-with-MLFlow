from wdmproject import logger
from wdmproject.pipeline.stage_01_data_ingestion_pipeline import DataIngestionPipeline
from wdmproject.pipeline.stage_02_data_validation_pipeline import DataValidationPipeline


STAGE_NAME   = "Data Ingestion Stage"
try:
    logger.info(f">>>>> Stage : {STAGE_NAME} Initiated.... <<<<<")
    data_ingestion_pipeline = DataIngestionPipeline()
    data_ingestion_pipeline.main()
    logger.info(f">>>>> Stage : {STAGE_NAME} Completed Successfully ! <<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME   = "Data Validation"
try:
    logger.info(f">>>>> Stage :  {STAGE_NAME} Initiated.... <<<<<")
    obj =  DataValidationPipeline()
    obj.main()
    logger.info(f">>>>> Stage : {STAGE_NAME} Completed Successfully ! <<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e
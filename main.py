from wdmproject import logger
from wdmproject.pipeline.stage_01_data_ingestion_pipeline import DataIngestionPipeline
from wdmproject.pipeline.stage_02_data_validation_pipeline import DataValidationPipeline
from wdmproject.pipeline.stage_03_data_transformation_pipeline import DataTransformationPipeline
from wdmproject.pipeline.stage_04_model_trainer_pipeline import ModelTrainerPipeline


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


STAGE_NAME   = "Data Transformation"
try:
    logger.info(f">>>>> Stage :  {STAGE_NAME} Initiated.... <<<<<")
    obj =  DataTransformationPipeline()
    obj.main()
    logger.info(f">>>>> Stage : {STAGE_NAME} Completed Successfully ! <<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME   = "Model Trainer"
try:
    logger.info(f">>>>> Stage :  {STAGE_NAME} Initiated.... <<<<<")
    obj =  ModelTrainerPipeline()
    obj.main()
    logger.info(f">>>>> Stage : {STAGE_NAME} Completed Successfully ! <<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e
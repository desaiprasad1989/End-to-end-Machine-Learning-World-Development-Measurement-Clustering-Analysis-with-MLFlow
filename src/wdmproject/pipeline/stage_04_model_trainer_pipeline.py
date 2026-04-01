from wdmproject.config.configuration import ConfigurationManager
from wdmproject.components.model_trainer import ModelTrainer
from wdmproject import logger


STAGE_NAME = "Model Trainer"

class ModelTrainerPipeline:
    def __init__(self):
        pass


    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.initiate_model_trainer()
        logger.info(f"Moder Trainer Pipeline Completed Successfully.")


if __name__ == '__main__':
    try:
        logger.info(f">>>>> Stage :  {STAGE_NAME} Initiated.... <<<<<")
        obj =  ModelTrainerPipeline()
        obj.main()
        logger.info(f">>>>> Stage : {STAGE_NAME} Completed Successfully ! <<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
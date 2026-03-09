import os
import urllib.request as request
import zipfile
from wdmproject.utils.common import save_json, load_json, save_bin, load_bin, get_size
from wdmproject import logger
from pathlib import Path
from wdmproject.entity.config_entity import (DataIngestionConfig)
import pandas as pd


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(f"file downloaded successfully and saved at: {filename}\n{headers}")
            logger.info(f"file size: {get_size(Path(filename))}")
        else:
            logger.info(f"file already exists of size: {get_size(Path(self.config.local_data_file))}")
            logger.info(f"file already exists at: {self.config.local_data_file}")

    def extract_zip_file(self):
        """
        zip_file_path: str 
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        logger.info(f"File extracted successfully at: {self.config.unzip_dir}")


    def initiate_data_ingestion(self):
        logger.info("Entered the data ingestion method")
        try:    
            self.download_file()
            self.extract_zip_file()
            df=pd.read_excel("artifacts/data_ingestion/World_development_mesurement.xlsx")
            logger.info(f"Read the dataset as dataframe with shape: {df.shape}")
            logger.info("Data ingestion method completed successfully.")

            return df   
        
        except Exception as e:
            logger.exception(e)
            raise e

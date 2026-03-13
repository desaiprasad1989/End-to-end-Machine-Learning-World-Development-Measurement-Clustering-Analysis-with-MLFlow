import os
import urllib.request as request
import zipfile

import importlib
import wdmproject.utils.common as common
importlib.reload(common)

from wdmproject.utils.common import save_json, get_size, standardize_column_name, is_standard_column
from wdmproject import logger
from pathlib import Path
from wdmproject.entity.config_entity import (DataIngestionConfig)
import pandas as pd
import json
import yaml
from datetime import datetime


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.ingestion_report = {}
        

    ## Download Data
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(f"file downloaded successfully and saved at: {filename}\n{headers}")
            logger.info(f"file size: {get_size(Path(filename))}")

            self.ingestion_report['dataset_download'] = {
                 "status" : "Success",
                 "file_name" : filename,
                 "file_size" : get_size(Path(filename))
            }

        else:
            logger.info(f"file already exists of size: {get_size(Path(self.config.local_data_file))}")
            logger.info(f"file already exists at: {self.config.local_data_file}")

            self.ingestion_report['dataset_download'] = {
                "status" : "Warning",
                "mesaage" : "File already exists.",
                "file_size" : get_size(self.config.local_data_file)
            }

    ## Extract Data
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
        logger.info(f"file extracted successfully at: {self.config.unzip_dir}")

        self.ingestion_report['dataset_extraction'] = {
                 "status" : "Success",
                 "message" : "File Extracted Successfully."
        }



     # Dataset Loading
    def load_data(self):
        try:
            self.data = pd.read_excel(self.config.data_path)
            #with open(self.config.STATUS_FILE, 'w') as f:
                 #  f.write(f"Data Loaded Successfully. \n")
            logger.info('Data Loaded Succesfully.')
            logger.info(f"Dataset Columns : {self.data.columns}")

            self.ingestion_report['dataset_load'] = {
                 "status" : "Success",
                 "rows" : self.data.shape[0],
                 "columns" : self.data.shape[1]
            }


        except Exception as e:
            logger.error(f"Error Loading Dataset. {e}")
            self.ingestion_report['dataset_load'] = {
                 "status" : "Failed",
                 "error_msg" : "Error Loading Dataset.",
                 "error" : str(e),
            }
            raise e


    ## Renaming columns to standard naming format

    def stadardize_dataset_columns(self):
        try:
            
            data = self.data
            rename_map = {}
            non_standard_columns = []

            for col in data.columns:
                if not is_standard_column(col):
                    clean_col = standardize_column_name(col)
                    rename_map[col] = clean_col
                    non_standard_columns.append(col)

            if rename_map:
                data.rename(columns=rename_map, inplace=True)
                logger.info(f"Standardize Columns Names: {rename_map}")

                self.ingestion_report['standardize_columns'] = {
                    "status" : "Warning",
                    "columns" : rename_map,
                }
            else:
                logger.info("All columns names are already in standard format.")
                self.ingestion_report['standardize_columns'] = {
                    "status" : "Success",
                    "message" : "All columns names are already in standard format.",
                }

            self.data = data

            return rename_map

        except Exception as e:
            logger.error(f"Column standardization error: {e}")
            raise e



    ## Save Cleaned Dataset

    def save_cleaned_dataset(self):
        try: 
            clean_data_path = self.config.cleaned_data_path
            self.data.to_excel(clean_data_path, index=False)
            logger.info(f"Cleaned dataset saved at : {clean_data_path}")
        except Exception as e:
            logger.error(f"Saving cleaned dataset failed: {e}")
            raise e
        

    ## Genearate New Schema
    def generate_schema(self):
        try:
            data = self.data

            schema = {
               "NUMBER_OF_COLUMNS": len(data.columns),
               "COLUMNS": {}
            }


            for col, dtype in data.dtypes.items():

                dtype_str = str(dtype)

                if "int" in dtype_str:
                    schema["COLUMNS"][col] = "int64"

                elif "float" in dtype_str:
                    schema["COLUMNS"][col] = "float64"

                elif "bool" in dtype_str:
                    schema["COLUMNS"][col] = "bool"
                
                elif "datetime" in dtype_str:
                    schema["COLUMNS"][col] = "datetime"
                else:
                    schema["COLUMNS"][col] = "object"
            
            schema_path = self.config.schema_path

            with open(schema_path, "w") as file:
                yaml.dump(schema, file, sort_keys=False)

            logger.info(f"Schema file updated at {schema_path}")
            self.ingestion_report['schema_generation'] = {
                "status" : "Success",
                "message" : "Schema file updated.",
                "schema" : schema
            }


        except Exception as e:
            logger.error(f"Schema generation error : {e}")

            self.ingestion_report['schema_generation'] = {
                "status" : "Error",
                "message" : "Schema generation error",
                "error" : str(e)
            }

            raise e


    ## Save Ingestion Report
    def save_ingestion_report(self):
            report_path = self.config.INGESTION_REPORT

            with open(report_path, "w") as f:

                json.dump(self.ingestion_report, f, indent=4)

            logger.info(f"Ingestion report saved at {report_path}")


    ## Inititate Data Ingestion

    def initiate_data_ingestion(self):
        try: 
            
            ## Intiating Data Ingestion stage

            self.ingestion_report["stage_metadata"] = {
                "stage_name" : "Data Ingestion",
                "stage_status" : "Running",
                "start_time" : str(datetime.now())
            }

            logger.info("Initiating Data Ingestion Stage.")

            ## Saving start_time
            start_time = datetime.now()

            ## Downloading Dataset
            self.download_file()

            ## Extracting Data
            self.extract_zip_file()

             ## Load Data
            self.load_data()

            ## Renaming columns to standard format
            self.stadardize_dataset_columns()

            ## Save Cleaned Dataset
            self.save_cleaned_dataset()

            ## Generate New Schema and save im schema.yaml
            self.generate_schema()

            ## Stage Success
            self.ingestion_report["stage_metadata"]["stage_status"] = "Success"
            self.ingestion_report["stage_metadata"]["end_time"] = str(datetime.now())

            ## Calculating Stage Duration
             
            stage_duration = (datetime.now() - start_time).total_seconds()
            self.ingestion_report["stage_metadata"]["stage_duration"] = stage_duration
            
            # Saving Ingestion Report JSON
            self.save_ingestion_report()

            logger.info("Data Ingestion Checks Completed Successfully.")

        except Exception as e:
            
            logger.error(f"Data Ingestion Error : {e}")

            end_time = datetime.now()

            self.ingestion_report["stage_metadata"]["stage_status"] = "Failed"
            self.ingestion_report["stage_metadata"]["end_time"] = str(end_time)
            self.ingestion_report["stage_metadata"]["error"] = str(e)

            self.save_ingestion_report()

            raise e

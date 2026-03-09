import os
from wdmproject import logger
import pandas as pd
from wdmproject.entity.config_entity import DataValidationConfig


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    ## Checking wheather all the columns in dataset matches with schema
    def validate_all_columns(self) -> bool:
        try:

            data = pd.read_excel(self.config.unzip_data_dir)
            
            validation_status = None
            
            ## First checking the columns in dataset with expected columns in schema
            if len(data.columns) != self.config.number_of_columns:
                validation_status = False
                with open(self.config.STATUS_FILE, 'w') as f:
                    f.write(f"Data Validation Failed: Expected {self.config.number_of_columns} columns, but found {len(data.columns)} columns.\n")
                logger.error(f"Expected {self.config.number_of_columns} columns, but found {len(data.columns)} columns.")
                return validation_status
            
            ## IF columns lenght matches move forward to check the cloumns with the dtypes

            expected_columns = set(self.config.all_schema.keys())
            actual_columns = set(data.columns)
        
            missing_columns = expected_columns - actual_columns
            extra_columns = actual_columns - expected_columns
        
            ## Checking missing columns        
            if missing_columns:

                validation_status = False
                with open(self.config.STATUS_FILE, 'w') as f:
                    f.write(f"Data Validation Failed: Missing columns: {missing_columns}\n")
                logger.error(f"Missing columns: {missing_columns}")
            else:
                validation_status = True
                with open(self.config.STATUS_FILE, 'w') as f:
                    f.write("Data Validation Passed: All expected columns are present.\n")

            if extra_columns:
                logger.warning(f"Extra columns: {extra_columns}")

            ## Validating Datatypes
            dtype_mismatch = []

            for column, expected_dtype in self.config.all_schema.items():

                if column in data.columns:

                    actual_dtype = str(data[column].dtype)

                    if actual_dtype != expected_dtype:

                        dtype_mismatch.append(
                            f"{column}: expected {expected_dtype}, got {actual_dtype}"
                        )

            
            if dtype_mismatch:
                validation_status = False
                logger.error(f"Datatype Mismatch: {dtype_mismatch}")

            ## Validation
            with open(self.config.STATUS_FILE, 'w') as f:

                if validation_status:
                    f.write('Validation Passed Successfully. \n')
                else:
                    f.write('Validation Failed Unfortunately. \n')
            
                if missing_columns:
                    f.write(f"Missing Columns : {missing_columns}\n")
                else:
                    f.write(f"No missing columns found!\n")

                if dtype_mismatch:
                    f.write(f"Datatype Mismatch: {dtype_mismatch}\n")
                else:
                    f.write(f"All the datatypes matched with the schema.\n")

        
            return validation_status 
        
        except Exception as e:
            logger.error(f"Data Validation Error: {e}")
            raise e
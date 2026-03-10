import os
from wdmproject import logger
import pandas as pd
import numpy as np
import json
from datetime import datetime
from wdmproject.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
        ## Global class variable for dataframe
        self.data = None
        self.validation_report = {}

            
    # Dataset Loading
    def load_data(self):
        try:
            self.data = pd.read_excel(self.config.unzip_data_dir)
            with open(self.config.STATUS_FILE, 'w') as f:
                    f.write(f"Data Loaded Successfully. \n")
            logger.info('Data Loaded Succesfully.')

            self.validation_report['dataset_load'] = {
                 "status" : "Success",
                 "rows" : self.data.shape[0],
                 "columns" : self.data.shape[1]
            }


        except Exception as e:
            logger.error(f"Error Loading Dataset. {e}")
            self.validation_report['dataset_load'] = {
                 "status" : "Failed",
                 "error_msg" : "Error Loading Dataset.",
                 "error" : str(e),
            }
            raise e


    ## Checking wheather all the columns in dataset matches with schema
    def validate_all_columns(self) -> bool:
        try:

            data = self.data
            
            validation_status = None
            
            ## First checking the columns in dataset with expected columns in schema
            if len(data.columns) != self.config.number_of_columns:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Data Validation Failed: Expected {self.config.number_of_columns} columns, but found {len(data.columns)} columns.\n")
                    logger. error(f"Expected {self.config.number_of_columns} columns, but found {len(data.columns)} columns.")
                
                    self.validation_report["columns_count"] = {
                        "status" : "Warning",
                        "expected" : self.config.number_of_columns,
                        "actual" : len(data.columns)
                    }
            
            else:
                
                validation_status = True
                self.validation_report["columns_count"] = {
                    "status" : "Success",
                    "expected" : self.config.number_of_columns,
                    "actual" : len(data.columns)
                }
            
                logger.info(f"Column Count Validation Passed. Expected {self.config.number_of_columns} columns, Actual {len(data.columns)} columns.")
                #return validation_status

                ## IF columns lenght matches move forward to check the cloumns with the dtypes

            expected_columns = set(self.config.all_schema.keys())
            actual_columns = set(data.columns)
        
            missing_columns = expected_columns - actual_columns
            extra_columns = actual_columns - expected_columns

               
            ## Checking missing columns        
            if missing_columns:

                validation_status = False
                with open(self.config.STATUS_FILE, 'w') as f:
                    f.write(f"Missing Columns Check Failed: Missing columns: {missing_columns}\n")
                logger.error(f"Missing columns: {missing_columns}")

                self.validation_report["missing_columns"] = {
                    "status" : "Warning",
                    "message" : "Missing Columns Check Failed",
                    "data" : list(missing_columns) 
                }
                

            else:
                validation_status = True
                with open(self.config.STATUS_FILE, 'w') as f:
                    f.write("Missing Columns Check Passed: All expected columns are present.\n")
                
                logger.info("Missing Columns Check Passed: All expected columns are present.\n")

                self.validation_report["missing_columns"] = {
                    "status" : "Success",
                    "message" : "Missing Columns Check Passed"
                }
                

            if extra_columns:
                logger.warning(f"Extra Columns Found: {extra_columns}")

                self.validation_report["extra_columns"] = {
                    "status" : "Warning",
                    "message" : "Extra Columns Found",
                    "data" : list(extra_columns) 
                }
            else:
                logger.info(f"No Extra columns: {extra_columns}")

                self.validation_report["extra_columns"] = {
                    "status" : "Success",
                    "message" : "No Extra Columns Found",
                    "data" : list(extra_columns) 
                }

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

                self.validation_report["datatype_mismatch"] = {
                    "status" : "Warning",
                    "message" : "Datatype Mismatch in Schema Check Failed",
                    "data" : dtype_mismatch 
                }
            else:
                validation_status = True
                logger.info("No Datatype Mismatch Found in Schema.")

                self.validation_report["datatype_mismatch"] = {
                    "status" : "Success",
                    "message" : "No Datatype Mismatch Found in Schema"
                }

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
            
            self.validation_report["columns_validation"] = {
                    "status" : "Failed",
                    "message" : "Data Validation Error",
                    "error" : str(e)
                }
            
            raise e

        
    
    ## Checking Missing Values
        
    def check_missing_values(self) -> bool:
        try:    
            
            data = self.data
            
            missing = data.isnull().sum()
            
            missing_cols = missing[missing > 0]

            missing_values = missing_cols.to_dict()

            if len(missing_cols) > 0 :
                logger.warning(f"Missing Values Found in : {missing_values}")

                self.validation_report["missing_values_check"] = {
                    "status" : "Warning",
                    "message" : "Missing Values Found.",
                    "columns" : missing_values
                    }

            else:
                logger.info("No Missing Values Found.")

                self.validation_report["missing_values_check"] = {
                    "status" : "Success",
                    "message" : "No Missing Values Found.",
                }

        except Exception as e:
            raise e


    ## Checking Duplicate Rows

    def check_duplicates(self):
        try:
            data = self.data

            duplicates = data.duplicated().sum()

            if duplicates > 0:
                logger.warning(f"Duplicate Rows Found in the Dataset : {duplicates}")
                self.validation_report["duplicates_check"] = {
                    "status" : "Warning",
                    "message" : "Duplicate Rows Found.",
                    "data" : duplicates
                }

            else: 
                logger.info("No Duplicate Rows Found in the Dataset")
                
                self.validation_report["duplicates_check"] = {
                    "status" : "Success",
                    "message" : "No Duplicate Rows Found.",
                }

        except Exception as e:
            raise e


    ## Checking Constant Count

    def check_constant_columns(self):
        try: 
            data = self.data

            constant_cols = [col for col in data.columns if data[col].nunique() <= 1]
            
            if constant_cols:
                logger.warning(f"Constant Columns Found : {constant_cols}")
                self.validation_report["constant_col_check"] = {
                    "status" : "Warning",
                    "message" : "Constant Columns Found.",
                    "columns" : constant_cols
                }
            else:
                logger.info("No Constant Columns Found.")
                self.validation_report["constant_col_check"] = {
                    "status" : "Success",
                    "message" : "No Constant Columns Found."
                }

        except Exception as e:
            raise e
        

     ## Validating Features distribution

    def validate_feature_distribution(self):
        try:
            data = self.data

            numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns

            features = {}
            zero_variance_cols = []

            for col in numeric_cols:

                mean = data[col].mean()
                std = data[col].std()
                min = data[col].min()
                max = data[col].max()
                skewness = data[col].skew()
                kurtosis = data[col].kurtosis()

                ## Calculating Z-Score for outliers 
                if std != 0:
                    z_scores = np.abs( (data[col] - mean) / std )
                    outliers = ( z_scores > 3 ).sum()
                    outliers_percentage = ( outliers / len(data[col])) * 100
                else: 
                    outliers_percentage = 0
                    zero_variance_cols.append(col)
                    logger.warning(f"{col} has zero variance.")

                #logger.info(f"{col} -> mean : {mean}, std : {std}")

                features[col] = {
                    "mean" : float(mean),
                    "std" : float(std),
                    "min" : float(min),
                    "max" : float(max),
                    "skewness" : float(skewness),
                    "kurtosis" : float(kurtosis),
                    "outlier_percentage" : round(float(outliers_percentage), 2)
                }


            if zero_variance_cols:
                self.validation_report["feature_distribution"] = {
                    "status" : "Warning",
                    "message" : "Some features have zero variance",
                    "zero_variance_features" : zero_variance_cols,
                    "features" : features,
                }
            else:
                self.validation_report["feature_distribution"] = {
                    "status" : "Success",
                    "message" : "Feature Distribution Validated",
                    "features" : features,
                }


            logger.info("Feature Disctribution validation completed.")

        except Exception as e:
            logger.info("Feature Disctribution validation error: {e}")
            self.validation_report["feature_distribution"] = {
                "status": "Failed",
                "error": str(e)
            }
            raise e


    # Saving Validation Report 
    def save_validation_report(self):

        report_path = self.config.VALIDATION_REPORT

        with open(report_path, "w") as f:

            json.dump(self.validation_report, f, indent=4)

        logger.info(f"Validation report saved at {report_path}")


    ## Initialising Data Validation Pipeline 

    def initiate_data_validation(self):
        try: 
            
            ## Intiating Data Validation stage

            self.validation_report["stage_metadata"] = {
                "stage_name" : "Data Validation",
                "stage_status" : "Running",
                "start_time" : str(datetime.now())
            }

            logger.info("Initiating Data Validation Stage.")

            ## Saving start_time
            start_time = datetime.now()

            ## Loading Dataset
            self.load_data()

            ## Validating all columns, datatypes, and dataframe
            self.validate_all_columns()

            ## Check Missing Values 
            self.check_missing_values()

            ## Checking Duplicates 
            self.check_duplicates()

            ## Checking Constant Columns
            self.check_constant_columns()

             ## Univariate Analysis / Validating Feature Distribution
             ## Mean, std, min, max, skewness, kurtosis, outier percentage
            self.validate_feature_distribution()

            ## Stage Success
            self.validation_report["stage_metadata"]["stage_status"] = "Success"
            self.validation_report["stage_metadata"]["end_time"] = str(datetime.now())

            ## Calculating Stage Duration
             
            stage_duration = (datetime.now() - start_time).total_seconds()
            self.validation_report["stage_metadata"]["stage_duration"] = stage_duration
            
            # Saving Validations Report JSON
            self.save_validation_report()

            logger.info("All Data Validation Checks Completed Successfully.")

        except Exception as e:
            
            logger.error(f"Validation Error : {e}")

            end_time = datetime.now()

            self.validation_report["stage_metadata"]["stage_status"] = "Failed"
            self.validation_report["stage_metadata"]["end_time"] = str(end_time)
            self.validation_report["stage_metadata"]["error"] = str(e)

            self.save_validation_report()

            raise e

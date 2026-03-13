
import os
import json
from wdmproject import logger
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, PowerTransformer
from sklearn.decomposition import PCA
import pickle, joblib

from wdmproject.entity.config_entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.data = None
        self.transformation_report = {}


    ## Load Dataset for transformation
    def load_data(self):
        try:
            self.data = pd.read_excel(self.config.data_path)
            #with open(self.config.STATUS_FILE, 'w') as f:
            #       f.write(f"Data Loaded Successfully. \n")
            logger.info('Data Loaded Succesfully.')

            self.transformation_report['dataset_load'] = {
                 "status" : "Success",
                 "rows" : self.data.shape[0],
                 "columns" : self.data.shape[1]
            }


        except Exception as e:
            logger.error(f"Error Loading Dataset. {e}")
            self.transformation_report['dataset_load'] = {
                 "status" : "Failed",
                 "error_msg" : "Error Loading Dataset.",
                 "error" : str(e),
            }
            raise e
        

    ## Droping and Saving Country Column for later use

    def separate_country_column(self):

        self.country = self.data["country"].reset_index(drop=True)
        
        self.data = self.data.drop(columns=["country", "number_of_records"]).reset_index(drop=True)

        logger.info("Country column separated.")

    
    ## Removing currency symbols and any other spaces from the data
    # Data cleaning and converting object dtype to numeric

    def convert_object_to_numeric(self):
        try:
            data = self.data

            for col in data.columns:
                if data[col].dtype == "object":

                    data[col] = (
                        data[col]
                        .astype(str)
                        .str.replace(r"[^\d.-]","",regex=True)
                    )

                    data[col] = pd.to_numeric(data[col], errors='coerce').astype('float64')

            #dt = data.info()
            logger.info(f"Object columns converted to numeric.")
    
        except Exception as e:
            logger.info(f"Object columns conversion to numeric failed : {e}")
            raise e


    ## Creating numeric Pipeline preprocessor with Imputer, power transformer and Roburst scaler 

    def create_preprocessor(self):
        try:
            data = self.data
            
            logger.info("Creating preprocessing pipeline...")
            numeric_cols = data.select_dtypes(include=["int64", "float64"]).columns.tolist()
            
            logger.info(f"Total numeric features for transformation: {len(numeric_cols)}")
            logger.info(f"Numeric features: {numeric_cols}")
            
            numeric_pipeline = Pipeline([
                ("imputer", KNNImputer(n_neighbors=5)),
                ("power_transform", PowerTransformer(method="yeo-johnson")),
                ("scaler", RobustScaler())
            ])

            logger.info("Numeric pipeline created with steps:")
            logger.info("1. KNNImputer (n_neighbors=5)")
            logger.info("2. PowerTransformer (method='yeo-johnson')")
            logger.info("3. RobustScaler")

            logger.info(f"Type of numeric_pipeline: {type(numeric_pipeline)}")
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", numeric_pipeline, numeric_cols)
                ]
            )

            logger.info("ColumnTransformer created successfully.")

            self.transformation_report["preprocessing"] = {
                "status": "Success",
                "total_numeric_features": len(numeric_cols),
                "numeric_features": numeric_cols,
                "pipeline_steps": [
                    "KNNImputer",
                    "PowerTransformer (Yeo-Johnson)",
                    "RobustScaler"
                ]
            }

            return preprocessor

        except Exception as e:
            logger.error(f"Preprocessor creation failed: {e}")

            self.transformation_report["preprocessing"] = {
                "status": "Failed",
                "error": str(e)
            }

            raise e
        

    ## Creating Full Pipeline with PCA
    def create_full_pipeline(self):
        try:
            preprocessor = self.create_preprocessor()

            logger.info("Applying PCA with 90% variance retention")

            pca = PCA(n_components=0.90, random_state=42)

            pipeline = Pipeline([
                ("preprocessor", preprocessor),
                ("pca", pca)
            ])

            logger.info("Pipeline with PCA created successfully")

            self.transformation_report["pca"] = {
                "status": "Success",
                "variance_retained": 0.90,
                "random_state": 42
            }

            return pipeline
        
        except Exception as e:

            logger.error(f"Preprocessor with PCA creation failed: {e}")

            self.transformation_report["pca"] = {
                "status": "Failed",
                "error": str(e)
            }

            raise e
        

    ## Transform Data fit data function
    def transform_data(self):
        try:
            data = self.data

            pipeline = self.create_full_pipeline()

            logger.info(f"Fitting Transformation Pipiline.")

            transformed_data = pipeline.fit_transform(data)

            logger.info("Transformation completed successfully")
           
            ## Check KNN Imputation
            missing_before = data.isnull().sum().sum()
            logger.info(f"Total missing values before imputation: {missing_before}")
            missing_after = np.isnan(transformed_data).sum()
            logger.info(f"Total missing values after transformation: {missing_after}")

            self.transformation_report["preprocessing"]["imputation"] = {
                "method": "KNNImputer",
                "neighbors": 5,
                "missing_before": int(missing_before),
                "missing_after": int(missing_after)
            }

            ## Checking Power Transformations

            skew_before = self.data.skew().to_dict()
            df_transformed = pd.DataFrame(transformed_data)
            skew_after = df_transformed.skew().to_dict()

            logger.info("Skewness before transformation calculated")
            logger.info("Skewness after transformation calculated")

            self.transformation_report["preprocessing"]["power_transformation"] = {
                "method": "Yeo-Johnson",
                "skewness_before_sample": dict(list(skew_before.items())[:5]),
                "skewness_after_sample": dict(list(skew_after.items())[:5])
            }
            
            ## Checking Scaling Effect
            logger.info("Feature scaling completed using RobustScaler")

            self.transformation_report["preprocessing"]["scaling"] = {
                "method": "RobustScaler",
                "sample_feature_stats_after_scaling": {
                    "mean": df_transformed.mean().head().to_dict(),
                    "std": df_transformed.std().head().to_dict()
                }
            }

            ## PCA
            pca = pipeline.named_steps["pca"]
            
            logger.info(f"PCA Components: {pca.n_components_}")
            logger.info(f"Explained Variance Ratio: {pca.explained_variance_ratio_}")

            self.transformation_report["pca"] = {
                "status": "Success",
                "components_generated": int(pca.n_components_),
                "variance_ratio": pca.explained_variance_ratio_.tolist(),
                "random_state": 42 
            }

            logger.info(f"Data Transformation pipeline Completed Successfully")

            return transformed_data, pipeline

        except Exception as e:
            logger.error(f"Transformation pipeline failed : {str(e)}")
            raise e     


    ## Saving transformed Dataset
    def save_transformed_data(self, transformed_data):
        try: 
            df_transformed = pd.DataFrame(transformed_data)

            df_transformed["country"] = self.country.values

            transformed_data_path = self.config.transformed_data_path
            self.data.to_excel(transformed_data_path, index=False)
            logger.info(f"Transformed dataset saved at : {transformed_data_path}")
        except Exception as e:
            logger.error(f"Saving transformed dataset failed: {e}")
            raise e
        

    ## Saving Preprocessor Object
    def save_preprocessor(self, pipeline):

        joblib.dump(
            pipeline,
            self.config.preprocessor_obj_file_path
        )

    logger.info("Preprocessor object saved")

    ## Saving Transformation Report 
    def save_transformation_report(self):

        report_path = self.config.TRANSFORMATION_REPORT

        with open(report_path, "w") as f:

            json.dump(self.transformation_report, f, indent=4)

        logger.info(f"Transformation report saved at {report_path}")


    ## Initialising Data Transformation Pipeline 

    def initiate_data_transformation(self):
        try: 
            
            ## Intiating Data Transformation stage

            self.transformation_report["stage_metadata"] = {
                "stage_name" : "Data Transformation",
                "stage_status" : "Running",
                "start_time" : str(datetime.now())
            }

            logger.info("Initiating Data Transformation Stage.")

            ## Saving start_time
            start_time = datetime.now()

            ## Loading Dataset
            self.load_data()

            ## Save country names for later use and drop it 
            self.separate_country_column()

            ## Clean currency from columns for transformation and update the datatype from object to numeric
            self.convert_object_to_numeric()      

            ## Create Preprocessor Pipeline with Knn Imputer, Power transformer and Rosbust scaling with PCA
            self.transform_data()   

            transformed_data, pipeline = self.transform_data()

            ## Save Transformed Dataset
            self.save_transformed_data(transformed_data)

            ## Save Preprocessor pickle file
            self.save_preprocessor(pipeline)

            ## Stage Success
            self.transformation_report["stage_metadata"]["stage_status"] = "Success"
            self.transformation_report["stage_metadata"]["end_time"] = str(datetime.now())

            ## Calculating Stage Duration
             
            stage_duration = (datetime.now() - start_time).total_seconds()
            self.transformation_report["stage_metadata"]["stage_duration"] = stage_duration
            
            # Saving Transformations Report JSON
            self.save_transformation_report()

            logger.info("All Data Transformation Checks Completed Successfully.")

        except Exception as e:
            
            logger.error(f"Transformation Error : {e}")

            end_time = datetime.now()

            self.transformation_report["stage_metadata"]["stage_status"] = "Failed"
            self.transformation_report["stage_metadata"]["end_time"] = str(end_time)
            self.transformation_report["stage_metadata"]["error"] = str(e)

            self.save_transformation_report()

            raise e

import os
import json
from wdmproject import logger
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, MeanShift
from sklearn.mixture import GaussianMixture
from sklearn.pipeline import Pipeline
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import pickle, joblib
from scipy import cluster
from sklearn.cluster import dbscan

from wdmproject.entity.config_entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
        self.data = None
        self.training_report = {}
        

    ## Load transformed data for training
    def load_transformed_data(self):
        try:
            logger.info("Loading transformed PCA data")

            X = joblib.load(self.config.transformed_data_path)           
            
            logger.info(f"Transformed data loaded: {X.shape}")
            

            nan_count = np.isnan(X).sum()
            ## NaN Values
            if nan_count > 0:
                logger.error(f"NaN Values found in transformed data: {nan_count}")
                raise ValueError(f"NaN values detected: {nan_count}")
            
            ## Infinite Values
            inf_count = np.isinf(X).sum()
            if inf_count > 0:
                logger.error(f"Infinite Values found in transformed data: {inf_count}")
                raise ValueError(f"Infinite values detected: {inf_count}")


            self.training_report['dataset_load'] = {
                 "status" : "Success",
                 "rows" : X.shape[0],
                 "columns" : X.shape[1],
                 "nan_values" : int(nan_count),
                 "inf_values" : int(inf_count)

            }
            
            return X

        except Exception as e:
            logger.error(f"Failed loading transformed data: {e}")
            self.training_report['dataset_load'] = {
                 "status" : "Failed",
                 "error_msg" : "Error Loading Dataset.",
                 "error" : str(e),
            }
            raise e
        

    def evaluate_models(self,model, X, model_name):
        try:
            labels = model.fit_predict(X)

            if(len(set(labels))) > 1:
                sil_score = silhouette_score(X, labels) 
                #dv_score = davies_bouldin_score(X, labels)
                #ch_score = calinski_harabasz_score(X, labels)

            else:
                sil_score = -1

            self.training_report[model_name] = {
                "silhouete_score": float(sil_score),        
                "n_clusters": int(len(set(labels)))    
            }

            logger.info(f"Silhouete_score {sil_score}")

            return sil_score, labels

        except Exception as e:
        
            logger.error(f"training failed: {e}")

            self.training_report["model_name"] = {
                "status": "Failed",
                "error": str(e)
            }

            return -1, None

    ## Training all clustering models
    def train_models(self, X):
        try:
            params = self.config.model_params

            models = {

                "k_means": KMeans(
                    n_clusters=params.kmeans.n_clusters,
                    random_state=params.kmeans.random_state,
                    n_init=params.kmeans.n_init
                ),

                "hierarchical": AgglomerativeClustering(
                    n_clusters=params.hierarchical.n_clusters,
                    linkage=params.hierarchical.linkage
                ),

                "dbscan": DBSCAN(
                    eps=params.dbscan.eps,
                    min_samples=params.dbscan.min_samples
                ),

                "meanshift": MeanShift(
                    cluster_all=params.meanshift.cluster_all                
                ),

                "gmm": GaussianMixture(
                    n_components=params.gmm.n_components,
                    random_state=params.gmm.random_state 
                )
            }

            best_score = -1
            best_model = None
            best_model_name = None
            best_labels= None

            for name, model in models.items():

                logger.info(f"Training {name} model")

                score, labels = self.evaluate_models(model, X, name)

                if score > best_score:

                    best_score = score
                    best_model = model
                    best_model_name = name
                    best_labels=labels
            
            self.training_report["best_model"] = best_model_name
            self.training_report["best_score"] = float(best_score)
            self.training_report["clusters"] = len(set(best_labels))

            return best_model
        
        except Exception as e:
            logger.error(f"Training Models Failed : {str(e)}")
            raise e
            


    ## Saving Training Report 
    def save_training_report(self):

        report_path = self.config.TRAINING_REPORT

        with open(report_path, "w") as f:

            json.dump(self.training_report, f, indent=4)

        logger.info(f"Model Training report saved at {report_path}")



    ## Initialising Model Trainer Pipeline 

    def initiate_model_trainer(self):
        try: 
            
            ## Intiatining Model Trainer stage

            self.training_report["stage_metadata"] = {
                "stage_name" : "Model Trainer",
                "stage_status" : "Running",
                "start_time" : str(datetime.now())
            }

            logger.info("Initiating Model Trainer Stage.")

            ## Saving start_time
            start_time = datetime.now()


            ## Loading Dataset
            X = self.load_transformed_data()
            print(X)
            ## model_trainer
            self.train_models(X)

            ## Stage Success
            self.training_report["stage_metadata"]["stage_status"] = "Success"
            self.training_report["stage_metadata"]["end_time"] = str(datetime.now())

            ## Calculating Stage Duration
            stage_duration = (datetime.now() - start_time).total_seconds()
            self.training_report["stage_metadata"]["stage_duration"] = stage_duration
            
            # Saving Transformations Report JSON
            self.save_training_report()

            logger.info("Model Training Completed Successfully.")

        except Exception as e:
            
            logger.error(f"Model Training Error : {e}")

            end_time = datetime.now()

            self.training_report["stage_metadata"]["stage_status"] = "Failed"
            self.training_report["stage_metadata"]["end_time"] = str(end_time)
            self.training_report["stage_metadata"]["error"] = str(e)

            self.save_training_report()

            raise e


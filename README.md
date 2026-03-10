# End-to-end-Machine-Learning-World-Development-Measurement-Clustering-Analysis-with-MLFlow

### Workflows
1. Update config.yaml 
2. Update schema.yaml
3. Update params.yaml
4. Update the entity 
5. Update the configuration manager in src config 
6. Update the components
7. Update the pipeline
8. Update the main.py
9. Update the app.py

### Stage 1: Data Ingestion
1.1 Read data from the source.
1.2 Extract the data
1.3 Split the data with Train Test Split if required (ddepends on Supervised / Unsupervised Data) 
1.4 Save the data in data ingestion folder as raw data, train data and test data.


### Stage 2: Data Validation
1.1 Load the Dataset
1.2 Perform all Data Validation Checks 
1.2.1  Columns Count Check (Missing / Extra Columns)
1.2.2  Schema Validation Check
1.2.3  Datatype Validation Check
1.2.4  Missing Values Check
1.2.5  Duplicate Rows Check
1.2.6  Constant Column Check
1.3 Generate Validation Report (JSON Format)
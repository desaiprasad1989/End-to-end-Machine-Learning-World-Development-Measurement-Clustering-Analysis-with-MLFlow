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
1. Data Ingestion
   - 1.1 Read data from the source.
   - 1.2 Extract the data
   - 1.3 Split the data with Train Test Split if required (depends on Supervised / Unsupervised Data) 
   - 1.4 Save the data in data ingestion folder as raw data, train data and test data.
   - 1.5 Checking a Standard Column name for the dataset (Added common functions in utils to check the valid column names, removing any special characters, spaces from the column names and convert to standard format.)
   - 1.6 Save the clean dataset for data validation
   - 1.7 Generate the new schema after standard column name and update the schema.yaml file automatically for Data Validation
   - 1.8 Save the column remane_mapping file with json format for debugging and tracking at later stages. 
   - 1.9 Generate Ingestion Report (JSON Format)

   
### Stage 2: Data Validation
2. Data Validation
   - 2.1 Load the Dataset
   - 2.2 Perform all Data Validation Checks 
     - 2.2.1  Columns Count Check (Missing / Extra Columns)
     - 2.2.2  Schema Validation Check
     - 2.2.3  Datatype Validation Check
     - 2.2.4  Missing Values Check
     - 2.2.5  Duplicate Rows Check
     - 2.2.6  Constant Column Check
     - 2.2.7  Feature Distribution Check / Unvariate Analysis (mean, std, min, max, skewness, kurtosis, outlier percentage)
     - 2.2.8  Features Correlations Check
   - 2.3 Generate Validation Report (JSON Format)

### Stage 3: Data Transformation
3. Data Transformation
   - 3.1 Load Dataset
   - 3.2 Separate the country column for further analysis and drop it
   - 3.3 Data Cleanig. Coverted Object datatype columns to numeric
   - 3.4 Created preprocessor using ColumnTransformer, numeric pipeline with KNNImputer, PowerTransformer and RobustScaler
   - 3.5 Created Full pipeline with preprocessor and PCA
   - 3.6 Transformed data using fit_transform with complete pipeline.
   - 3.7 Analyzed before and after data transformation results
   - 3.8 Saved transformed data in artifacts/data_transformation
   - 3.9 Saved preprocessor object (preprocessor.pkl) in artifacts/data_transformation
   - 3.10 Generated Transformation Report (JSON Format)
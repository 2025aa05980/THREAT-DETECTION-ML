# Threat Detection using Network Traffic Features

## a. Problem statement

> Modern networks generate a large volume of traffic, and detecting malicious or suspicious activity in real time is a critical security requirement. Traditional rule-based systems often fail to generalize to new attack types or changing patterns.  The goal of this project is to build and compare multiple machine learning classification models that can distinguish between **benign/normal** and **malicious/suspicious** network flows using basic flow-level features (packet length, bytes sent/received, protocol, etc.). We then deploy an interactive **Streamlit web app** that allows users to upload test data, select a model, and visualize predictions and evaluation metrics.
---

## b. Dataset description

- **Dataset name:** ThreatDetectionDataset  
- **Source:** Custom/prepared minimal feature dataset (data\ThreatDetection_dataset.csv)   
- **Number of instances (rows):** 600 
- **Number of features (after preprocessing):** 15 

### Raw features (from CSV)

1. `Protocol` – categorical feature (`TCP`, `UDP`, `ICMP`)  
   (`Protocol_TCP`, `Protocol_UDP`, `Protocol_ICMP` – one-hot encoding of `Protocol`)

2. `Packet_Length` – size of the packet in bytes  

3. `Duration` – flow duration in seconds  

4. `Bytes_Sent` – number of bytes sent from source to destination  

5. `Bytes_Received` – number of bytes received  

6. `Flow_Packets/s` – number of packets per second in the traffic flow  

7. `Flow_Bytes/s` – bytes per second in the flow  

8. `Avg_Packet_Size` – average size of the packets during the connection  

9. `Total_Fwd_Packets` – total number of forward packets  

10. `Total_Bwd_Packets` – total number of backward packets  

11. `Fwd_Header_Length` – length of the forward packet headers  

12. `Bwd_Header_Length` – length of the backward packet headers  

13. `Sub_Flow_Fwd_Bytes` – bytes sent in the forward subflow  

14. `Sub_Flow_Bwd_Bytes` – bytes received in the backward subflow  

15. `Inbound` – 1 if inbound flow, 0 if outbound  

16. `Label` – target variable (1 = malicious/suspicious, 0 = benign)

### Engineered / preprocessed features
- **Train–test split:**  
  To evaluate model performance fairly, the dataset was divided into training and testing subsets using an 80/20 split. The training set is used to fit the machine learning models, while the test set is reserved exclusively for evaluating how well the models generalize to unseen data.
- **Feature scaling using StandardScaler:**  
  Many ML algorithms (e.g., Logistic Regression, kNN, SVM) are sensitive to differences in feature scales. To ensure all numerical features contribute equally, we applied **standardization**, which transforms each feature to have zero mean and unit variance. This prevents large‑scale features from dominating the learning process.
- **Encoding categorical variables:**  
  Apart from the `Protocol` column, any additional categorical features were converted into numerical format using encoding techniques such as one‑hot encoding. This ensures compatibility with ML models that require numerical inputs.
- **Separating features and target label:**  
  The dataset was split into input features (`X`) and the target variable (`Label`). The `Label` column indicates whether a network flow is **benign (0)** or **malicious (1)**, and is used for supervised learning.
- **Handling missing values:**  
  The dataset was checked for missing or invalid entries. Any missing values were either imputed or removed to maintain data quality and prevent model bias.
---

## c. Models used and evaluation metrics

Trained the following **6 classification models** on the same preprocessed dataset:

1. Logistic Regression  
2. Decision Tree Classifier  
3. K-Nearest Neighbors (kNN) Classifier  
4. Naive Bayes Classifier (Gaussian)  
5. Random Forest Classifier (Ensemble)  
6. XGBoost Classifier (Ensemble)

### Comparison table of evaluation metrics

| ML Model Name           |  Accuracy  |   AUC   | Precision | Recall |   F1    |   MCC   |
|-------------------------|------------|---------|-----------|--------|---------|---------|
| Logistic Regression     | 0.5417     | 0.5111  | 0.5263    | 0.5172 | 0.5217  | 0.0818  |
| Decision Tree           | 0.4167     | 0.4138  | 0.3800    | 0.3276 | 0.3519  | -0.1748 |
| kNN                     | 0.5667     | 0.5859  | 0.5625    | 0.4655 | 0.5094  | 0.1294  |
| Naive Bayes             | 0.5417     | 0.5159  | 0.5211    | 0.6379 | 0.5736  | 0.0910  |
| Random Forest (Ensemble)| 0.5667     | 0.6058  | 0.5682    | 0.4310 | 0.4902  | 0.1292  |
| XGBoost (Ensemble)      | 0.5750     | 0.5798  | 0.5636    | 0.5345 | 0.5487  | 0.1478  |

### Observations on Model Performance

| ML Model Name            | Observation about model performance  |
|--------------------------|--------------------------------------|
| Logistic Regression      | Shows balanced but weak performance across all metrics, indicating limited learning from the feature space. |
| Decision Tree            | Underperforms significantly with the lowest recall and negative MCC, suggesting overfitting or poor generalization. |
| kNN                      | Offers slightly better AUC and F1 than Logistic Regression, but suffers from low recall, hinting at sensitivity to class imbalance. |
| Naive Bayes              | Achieves the highest recall among all models, making it useful for detecting positives, though precision remains modest. |
| Random Forest (Ensemble) | Delivers strong AUC and precision, but low recall suggests it may be conservative in predicting positives. |
| XGBoost (Ensemble)       | Provides the best overall balance with highest accuracy and MCC, showing robust generalization and stable predictions. |

### Comparison Summary:

> XGBoost delivers the strongest overall performance with the highest accuracy and MCC, while Logistic Regression, kNN, and Naive Bayes show moderate but inconsistent results. The Decision Tree performs the weakest, indicating overfitting, and Random Forest offers decent precision but struggles with recall. 
---

## d. Streamlit app features

The Streamlit app includes the following:

1. **Dataset upload option (CSV)**  
   - Users can upload a test CSV file with the same schema as the training data (without the `Label` column if performing prediction only).

2. **Model selection dropdown**  
   - A dropdown allows the user to choose among: Logistic Regression, Decision Tree, kNN, Naive Bayes, Random Forest, and XGBoost.

3. **Display of evaluation metrics**  
   - After loading the pre-trained models, the app displays Accuracy, AUC, Precision, Recall, F1 Score, and MCC for the selected model on the test set.

4. **Confusion matrix / classification report**  
   - The app visualizes the confusion matrix as a heatmap and can also print a text-based classification report.
---
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
| Logistic Regression     | 0.5633     | 0.5795  | 0.5547    | 0.5052 | 0.5288  | 0.1241  |
| Decision Tree           | 0.8833     | 0.8828  | 0.8905    | 0.8660 | 0.8780  | 0.7665 |
| KNN                     | 0.6633     | 0.7111  | 0.6773    | 0.5842 | 0.6273  | 0.3263  |
| Naive Bayes             | 0.5683     | 0.5854  | 0.5471    | 0.6392 | 0.5895  | 0.1420  |
| Random Forest (Ensemble)| 0.9133     | 0.9842  | 0.9314    | 0.8866 | 0.9085  | 0.8272  |
| XGBoost (Ensemble)      | 0.9150     | 0.9745  | 0.9167    | 0.9072 | 0.9119  | 0.8298  |

### Observations on Model Performance

| ML Model Name            | Observation about model performance  |
|--------------------------|--------------------------------------|
| Logistic Regression      | Shows modest and balanced performance across all metrics. While stable, it struggles to capture complex nonlinear patterns in the dataset, resulting in only moderate predictive power. |
| Decision Tree            | Achieves very high accuracy and strong performance across all metrics, indicating that it fits the dataset extremely well. However, the large jump in performance compared to simpler models suggests possible overfitting. |
| KNN                      | Performs better than Logistic Regression but remains sensitive to feature scaling and local neighborhood structure. Its moderate recall and MCC indicate limited ability to generalize to more complex threat patterns. |
| Naive Bayes              | Delivers good recall and reasonable F1 performance, showing strength in detecting malicious flows. However, its simplifying assumptions limit precision and overall discriminative power. |
| Random Forest (Ensemble) | Demonstrates excellent performance across all metrics, with very high AUC and MCC. Its strong generalization suggests that ensemble averaging effectively reduces variance and captures complex relationships. |
| XGBoost (Ensemble)       | Provides the best overall performance with the highest accuracy, F1, and MCC. Its ability to model nonlinear interactions and handle feature importance makes it the most robust and reliable model for this dataset. |

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
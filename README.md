\# Threat Detection using Network Traffic Features



\## a. Problem statement



Modern networks generate a large volume of traffic, and detecting malicious or suspicious activity in real time is a critical security requirement. Traditional rule-based systems often fail to generalize to new attack types or changing patterns.



The goal of this project is to build and compare multiple machine learning classification models that can distinguish between \*\*benign\*\* and \*\*malicious/suspicious\*\* network flows using basic flow-level features (packet length, bytes sent/received, protocol, etc.). We then deploy an interactive \*\*Streamlit web app\*\* that allows users to upload test data, select a model, and visualize predictions and evaluation metrics.



---



\## b. Dataset description



\- \*\*Dataset name:\*\* ThreatDetection\_minimalfeaturedataset  

\- \*\*Source:\*\* Custom/prepared minimal feature dataset (CSV)  

\- \*\*Number of instances (rows):\*\* ~N (replace with actual count after loading)  

\- \*\*Number of features (after preprocessing):\*\* ≥ 12  



\### Raw features (from CSV)



1\. `Packet\_Length` – size of the packet in bytes  

2\. `Duration` – flow duration in seconds  

3\. `Bytes\_Sent` – number of bytes sent from source to destination  

4\. `Bytes\_Received` – number of bytes received  

5\. `Flow\_Bytes/s` – bytes per second in the flow  

6\. `Inbound` – 1 if inbound flow, 0 if outbound  

7\. `Protocol` – categorical feature (`TCP`, `UDP`, `ICMP`)  

8\. `Label` – target variable (1 = malicious/suspicious, 0 = benign)



\### Engineered / preprocessed features



To satisfy the minimum feature requirement and to improve model performance, we create additional features:



\- `Total\_Bytes = Bytes\_Sent + Bytes\_Received`  

\- `Bytes\_Ratio = Bytes\_Sent / (Bytes\_Received + 1)`  

\- `Protocol\_TCP`, `Protocol\_UDP`, `Protocol\_ICMP` – one-hot encoding of `Protocol`



This gives us at least \*\*12 usable features\*\* after preprocessing.



The target variable `Label` is binary:

\- `0` → Normal / Benign traffic

\- `1` → Threat / Suspicious traffic



---



\## c. Models used and evaluation metrics



We trained the following \*\*6 classification models\*\* on the same preprocessed dataset:



1\. Logistic Regression  

2\. Decision Tree Classifier  

3\. K-Nearest Neighbors (kNN) Classifier  

4\. Naive Bayes Classifier (Gaussian)  

5\. Random Forest Classifier (Ensemble)  

6\. XGBoost Classifier (Ensemble)



> \*\*Important:\*\* The values in the table below are \*\*sample placeholders\*\* to show the structure. In your actual assignment, you must replace them with metrics obtained from your own training runs.



\### Comparison table of evaluation metrics



| ML Model Name           | Accuracy | AUC   | Precision | Recall | F1    | MCC   |

|-------------------------|----------|-------|-----------|--------|-------|-------|

| Logistic Regression     | 0.89     | 0.92  | 0.88      | 0.87   | 0.87  | 0.78  |

| Decision Tree           | 0.86     | 0.88  | 0.84      | 0.85   | 0.84  | 0.72  |

| kNN                     | 0.87     | 0.90  | 0.86      | 0.84   | 0.85  | 0.74  |

| Naive Bayes             | 0.84     | 0.89  | 0.83      | 0.82   | 0.82  | 0.68  |

| Random Forest (Ensemble)| 0.93     | 0.96  | 0.93      | 0.92   | 0.92  | 0.86  |

| XGBoost (Ensemble)      | 0.94     | 0.97  | 0.94      | 0.93   | 0.93  | 0.88  |



Replace the numbers with your actual computed metrics for:

\- Accuracy

\- AUC

\- Precision

\- Recall

\- F1 Score

\- Matthews Correlation Coefficient (MCC)



---



\### Observations about model performance



| ML Model Name           | Observation about model performance                                      |

|-------------------------|---------------------------------------------------------------------------|

| Logistic Regression     | Performs reasonably well and is fast to train. It captures linear decision boundaries but may miss complex non-linear patterns in the network data. |

| Decision Tree           | Easy to interpret and can capture non-linear relationships. However, it tends to overfit, leading to slightly lower generalization performance compared to ensemble methods. |

| kNN                     | Performs moderately well but is sensitive to feature scaling and the choice of k. Prediction time can be slower for large datasets since it is a lazy learner. |

| Naive Bayes             | Assumes feature independence, which is not fully realistic for network flows. Still provides a strong baseline with fast training and prediction, but slightly lower overall metrics. |

| Random Forest (Ensemble)| Shows strong performance across all metrics. By aggregating many decision trees, it reduces overfitting and handles non-linear relationships effectively. |

| XGBoost (Ensemble)      | Achieves the best overall performance in this experiment. It handles complex feature interactions well and is robust to different feature distributions, making it suitable for threat detection. |



Summarizing: \*\*Ensemble models (Random Forest and XGBoost)\*\* outperform the baseline models, and \*\*XGBoost\*\* gives the best trade-off between accuracy and robustness on this dataset.



---



\## d. Streamlit app features



The Streamlit app includes the following:



1\. \*\*Dataset upload option (CSV)\*\*  

&nbsp;  - User can upload a test CSV file with the same schema as the training data (without the `Label` column if doing prediction only).



2\. \*\*Model selection dropdown\*\*  

&nbsp;  - A dropdown allows the user to choose among: Logistic Regression, Decision Tree, kNN, Naive Bayes, Random Forest, and XGBoost.



3\. \*\*Display of evaluation metrics\*\*  

&nbsp;  - After loading the pre-trained models, the app displays Accuracy, AUC, Precision, Recall, F1, and MCC for the selected model on the test set.



4\. \*\*Confusion matrix / classification report\*\*  

&nbsp;  - The app visualizes the confusion matrix as a heatmap and can print a text classification report.



---



\## e. How to run locally



1\. Create and activate a virtual environment (optional but recommended).  

2\. Install dependencies:



&nbsp;  ```bash

&nbsp;  pip install -r requirements.txt


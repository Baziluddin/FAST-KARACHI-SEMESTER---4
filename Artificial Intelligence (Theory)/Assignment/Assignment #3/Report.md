# Assignment 3: Machine Learning

## Student Information
- Name: Bazil Uddin Khan
- Roll No: 24k-0559
- Section: 4H
- Submission Date: 26 APRIL 2026

---

## 1. Competition Overview
- **Competition Name:** Irrigation Need Prediction  
- **Problem Type:** Multi-class Classification  
- **Evaluation Metric:** Accuracy  

**Brief understanding of the dataset:**  
The dataset contains agricultural and environmental features such as soil type, crop type, region, irrigation method, season, and water source. These features are used to predict irrigation requirement levels: Low, Medium, and High.

---

## 2. Data Preprocessing
- Checked for missing values (no major issues found)  
- Initially applied Label Encoding on categorical variables  
- Improved performance using One-Hot Encoding (`pd.get_dummies`)  
- Feature scaling was not required since tree-based models were used  
- Train-validation that split (80-20) used for model evaluation  

---

## 3. Models Attempted
- Decision Tree  
- Naive Bayes  
- Logistic Regression  
- K-Means (used as classifier)  
- Random Forest  
- Gradient Boosting (The final selected model)  

These all models that were tested to compare performance and understand different approaches.

---

## 4. Cross Validation Strategy
- Used train-validation split (80-20) for evaluation  
- K-Fold Cross Validation was explored earlier but not used in final implementation due to time constraints  
- Best validation accuracy observed around 0.94+  

---

## 5. Failed Attempts and Insights

**Decision Tree**
- Accuracy: ~0.97  
- Issue: Overfitting observed  
- Insight: The confusion matrix showed that the model memorized training data and did not generalize well.

**Naive Bayes**
- Accuracy: ~0.74  
- Issue: Could not capture complex relationships  
- Insight: The confusion matrix showed misclassification due to the assumption of feature independence.

**Logistic Regression**
- Accuracy: ~0.71  
- Issue: Underfitting and convergence limitations  
- Insight: The confusion matrix showed poor separation between classes.

**K-Means**
- Accuracy: ~0.33  
- Issue: Not suitable for supervised classification  
- Insight: The confusion matrix was highly scattered, indicating random predictions.

---

### What went wrong?
- Label Encoding got reduced model performance  
- Simpler models were not able to handle the complex feature interactions  

---

### What was improved?
- Switching to One-Hot Encoding  
- Used ensemble models for better and improved performance  

---

## Confusion Matrix

The confusion matrix shows how well the model predicts each class by comparing actual and predicted values.




---

## 6. Final Model Selection
- **Model:** Gradient Boosting Classifier  
- **Hyperparameters:**
  - n_estimators = 30  
  - learning_rate = 0.1  

- **Why selected?**  
The model provided the best balance of accuracy and generalization. It handled complex feature relationships effectively and produced stable results compared to other models.

- The model was first trained on training data for validation and then retrained on the full dataset before final submission.

---

## 7. Leaderboard Performance
- **Kaggle Score:** 0.95766  
- **Rank:** 2670  



---

## 8. Conclusion and Learnings
- I believe Proper preprocessing significantly improves model performance  
- Also One-Hot Encoding is more effective than Label Encoding for categorical data  
- Ensemble models (like Gradient Boosting) perform better than simple models  
- Model evaluation is important before final submission  

---

### Challenges faced
- Initial having low accuracy  
- Handling  the categorical data properly  
- The Model training time and performance optimization  

---

### Future improvements
- Improvement by doing Hyperparameter tuning.  
- Trying the advanced models (e.g., XGBoost)  
- Feature engineering for better accuracy.  

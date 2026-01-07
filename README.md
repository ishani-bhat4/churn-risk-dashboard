# 📉 Customer Churn Risk Prediction Dashboard

An end-to-end **machine learning decision-support system** that predicts customer churn, explains *why* a customer is at risk, and allows business users to experiment with decision thresholds.

🔗 **Live App**:  
👉 https://churn-risk-dashboard.streamlit.app  

🔗 **Backend API (FastAPI)**:  
👉 https://churn-backend-api-nxc0.onrender.com/docs  

---

## 🚀 Project Overview

Customer churn is a critical business problem where **false negatives are costly** , which means missing a customer who is about to leave can result in a loss in revenue.

This project goes beyond a simple classifier by:

- Predicting **churn probability**
- Supporting **threshold-based business decisions**
- Explaining predictions using **model feature contributions**
- Presenting results in a **clean, stakeholder-friendly UI**

---

## 🧠 Machine Learning Approach

- **Problem Type**: Binary classification (Churn / No Churn)
- **Model**: Logistic Regression (interpretable & regularized)
- **Evaluation Focus**:
  - Recall for churners
  - Precision–recall tradeoff via threshold tuning
- **Key Techniques**:
  - One-hot encoding for categorical features
  - Feature scaling for numerics
  - Pipeline + ColumnTransformer
  - Threshold-based decision logic
  - Feature-level contribution explanations

---

## 🖥️ Application Architecture

Streamlit Frontend ──────▶ FastAPI Backend ──────▶ ML Pipeline
(UI) (Inference) (Sklearn)

### Frontend
- Built with **Streamlit**
- Collects customer attributes
- Displays:
  - Churn probability
  - Risk classification (High / Low)
  - Explanation of key drivers
- Deployed on **Streamlit Community Cloud**

### Backend
- Built with **FastAPI**
- Loads trained ML pipeline
- Exposes `/predict` endpoint
- Returns JSON with:
  - Probability
  - Risk decision
  - Top risk & retention factors
- Deployed on **Render (Free Tier)**

---

## 🔍 Model Explainability

For each prediction, the system shows:

- 🔺 **Factors increasing churn risk**
- 🟢 **Factors reducing churn risk**

These are computed using:
feature contribution = model coefficient × transformed feature value

This allows stakeholders to understand *model reasoning*, not just outputs.

> Note: Explanations reflect **model logic**, not causal guarantees.

---

## 🧪 Try It Yourself

1. Open the app:  
   👉 https://churn-risk-dashboard.streamlit.app

2. Change inputs like:
   - Contract type
   - Payment method
   - Tenure

3. Adjust the **decision threshold** in the sidebar to see:
   - Recall vs precision tradeoff
   - Risk classification change

---

## 🛠️ Tech Stack

- Python
- Pandas, NumPy
- Scikit-learn
- FastAPI
- Streamlit
- Joblib
- Render (backend hosting)
- Streamlit Community Cloud (frontend hosting)

---

## 📈 Future Improvements

- Add SHAP explanations for non-linear models
- Cost-sensitive training
- Retention strategy recommendations
- Authentication for enterprise use

---

## 👩‍💻 Author

**Ishani Bhat**  


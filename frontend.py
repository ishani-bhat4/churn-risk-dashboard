import streamlit as st
import requests

# -----------------------------
# Page config + light styling
# -----------------------------
st.set_page_config(
    page_title="Churn Risk Dashboard",
    page_icon="📉",
    layout="wide",
)
def prettify_feature_name(raw_name: str) -> str:
    """
    Convert model feature names into human-readable explanations.
    Examples:
    cat__Contract_Month-to-month -> Contract: Month-to-month
    num__tenure -> Tenure (months)
    """
    # Remove transformer prefix
    if raw_name.startswith("num__"):
        name = raw_name.replace("num__", "")
        mapping = {
            "tenure": "Tenure (months)",
            "MonthlyCharges": "Monthly Charges",
            "TotalCharges": "Total Charges",
            "SeniorCitizen": "Senior Citizen"
        }
        return mapping.get(name, name.replace("_", " ").title())

    if raw_name.startswith("cat__"):
        name = raw_name.replace("cat__", "")
        if "_" in name:
            feature, value = name.split("_", 1)
            return f"{feature.replace('_', ' ').title()}: {value}"
        return name.replace("_", " ").title()

    # fallback
    return raw_name.replace("_", " ").title()

st.markdown(
    """
    <style>
      .small-muted { color: #6b7280; font-size: 0.9rem; }
      .card {
        border: 1px solid rgba(0,0,0,0.08);
        border-radius: 16px;
        padding: 18px;
        background: white;
        box-shadow: 0 6px 18px rgba(0,0,0,0.04);
      }
      .badge {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid rgba(0,0,0,0.10);
      }
      .badge-low { background: rgba(34,197,94,0.10); color: rgb(22,101,52); }
      .badge-high { background: rgba(239,68,68,0.10); color: rgb(153,27,27); }
      .label { font-weight: 600; margin-bottom: 6px; }
      .divider { height: 1px; background: rgba(0,0,0,0.08); margin: 10px 0 14px 0; }
      .list-item { margin: 6px 0; }
      .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Header
# -----------------------------
st.markdown("## 📉 Customer Churn Risk Dashboard")
st.markdown(
    '<div class="small-muted">A decision-support tool: probability + threshold + explanations (model reasoning, not causality).</div>',
    unsafe_allow_html=True
)

API_URL = "https://churn-risk-dashboard.streamlit.app/"


# -----------------------------
# Sidebar settings
# -----------------------------
with st.sidebar:
    st.markdown("### ⚙️ Decision Settings")
    threshold = st.slider(
        "Churn decision threshold",
        min_value=0.10,
        max_value=0.90,
        value=0.30,
        step=0.05,
        help="Lower threshold catches more churners (higher recall) but increases false positives."
    )

    st.markdown("### 🧪 Quick presets")
    colp1, colp2 = st.columns(2)
    if colp1.button("Recall-heavy (0.20)"):
        threshold = 0.20
    if colp2.button("Balanced (0.30)"):
        threshold = 0.30

    st.markdown("---")
    st.markdown("### ✅ What this shows")
    st.markdown(
        """
        - Probability of churn  
        - Risk decision at your threshold  
        - Top factors increasing / reducing risk  
        """
    )

# -----------------------------
# Input form (grouped)
# -----------------------------
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🧾 Customer Inputs")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    with st.form("customer_form"):
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown('<div class="label">Demographics</div>', unsafe_allow_html=True)
            gender = st.selectbox("Gender", ["Male", "Female"])
            SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
            Partner = st.selectbox("Partner", ["Yes", "No"])
            Dependents = st.selectbox("Dependents", ["Yes", "No"])
            tenure = st.number_input("Tenure (months)", 0, 100, 12)

        with c2:
            st.markdown('<div class="label">Services</div>', unsafe_allow_html=True)
            PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
            MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
            InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
            OnlineSecurity = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
            TechSupport = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])

        with c3:
            st.markdown('<div class="label">Billing & Add-ons</div>', unsafe_allow_html=True)
            OnlineBackup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
            DeviceProtection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
            StreamingTV = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
            StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
            Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
            PaymentMethod = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)"
                ]
            )

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        c4, c5 = st.columns(2)
        with c4:
            MonthlyCharges = st.number_input("Monthly Charges", 0.0, 200.0, 70.0)
        with c5:
            TotalCharges = st.number_input("Total Charges", 0.0, 10000.0, 1000.0)

        submitted = st.form_submit_button("🔮 Predict churn risk")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Results panel
# -----------------------------
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 Prediction")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="small-muted">Current decision threshold: <span class="mono">{threshold:.2f}</span></div>',
        unsafe_allow_html=True
    )

    result = None
    if submitted:
        payload = {
            "gender": gender,
            "SeniorCitizen": SeniorCitizen,
            "Partner": Partner,
            "Dependents": Dependents,
            "tenure": tenure,
            "PhoneService": PhoneService,
            "MultipleLines": MultipleLines,
            "InternetService": InternetService,
            "OnlineSecurity": OnlineSecurity,
            "OnlineBackup": OnlineBackup,
            "DeviceProtection": DeviceProtection,
            "TechSupport": TechSupport,
            "StreamingTV": StreamingTV,
            "StreamingMovies": StreamingMovies,
            "Contract": Contract,
            "PaperlessBilling": PaperlessBilling,
            "PaymentMethod": PaymentMethod,
            "MonthlyCharges": MonthlyCharges,
            "TotalCharges": TotalCharges
        }

        try:
            response = requests.post(
                API_URL,
                params={"threshold": threshold},
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
        except requests.RequestException as e:
            st.error(f"Backend error: {e}")

    if not submitted:
        st.info("Fill the form and click **Predict churn risk** to see results.")

    if result:
        prob = float(result.get("churn_probability", 0.0))
        risk = result.get("risk", "Unknown")

        badge_class = "badge-low" if risk.lower() == "low" else "badge-high"
        st.markdown(
            f'<div class="badge {badge_class}">Risk: {risk}</div>',
            unsafe_allow_html=True
        )

        st.metric("Churn probability", f"{prob*100:.2f}%")

        # A simple "gauge-like" bar using progress
        st.progress(min(max(prob, 0.0), 1.0))

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        tabs = st.tabs(["🔍 Explanation", "📦 Raw JSON"])

        with tabs[0]:
            cL, cR = st.columns(2)

            top_risk = result.get("top_risk_factors", [])
            top_protect = result.get("top_protective_factors", [])

            with cL:
                st.markdown("#### 🔺 Factors increasing churn risk")
                if top_risk:
                    for f in result["top_risk_factors"]:
                        pretty = prettify_feature_name(f)
                        st.markdown(
                        f'<div class="list-item">• {pretty}</div>',
                        unsafe_allow_html=True
                        )
                else:
                    st.markdown('<div class="small-muted">No explanation returned by API.</div>', unsafe_allow_html=True)

            with cR:
                st.markdown("#### 🟢 Factors reducing churn risk")
                if top_protect:
                    for f in result["top_protective_factors"]:
                        pretty = prettify_feature_name(f)
                        st.markdown(
                        f'<div class="list-item">• {pretty}</div>',
                        unsafe_allow_html=True
    )

                    
                else:
                    st.markdown('<div class="small-muted">No explanation returned by API.</div>', unsafe_allow_html=True)

            st.caption("These are feature contribution highlights from logistic regression (not causal guarantees).")

        with tabs[1]:
            st.json(result)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Footer tips
# -----------------------------
st.markdown("")
st.markdown(
    '<div class="small-muted">Tip: Try changing <b>Contract</b> to <i>Two year</i> or '
    '<b>PaymentMethod</b> to <i>Electronic check</i> and watch probability + explanations change.</div>',
    unsafe_allow_html=True
)

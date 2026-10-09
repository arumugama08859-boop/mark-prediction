"""
app.py - Student Marks Predictor Web Application
Built with Streamlit, scikit-learn, pandas, numpy, and matplotlib.

This application demonstrates a clean, end-to-end Machine Learning workflow:
Data exploration -> Train/Test split -> Linear Regression Training ->
Model Evaluation (MAE, MSE, RMSE, R²) -> Real-time Prediction with range clamping.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from data import load_dataset, get_dataset_summary, generate_sample_dataset
from model import train_linear_regression, predict_score

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Student Marks Predictor | ML Project",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS STYLING (Blue, Purple & Clean White Palette)
# ==========================================
st.markdown("""
<style>
    /* Global Typography & Background */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Gradient Header */
    .hero-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #7C3AED 100%);
        border-radius: 18px;
        padding: 32px 36px;
        color: #FFFFFF;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3), 0 8px 10px -6px rgba(124, 58, 237, 0.2);
        margin-bottom: 28px;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        font-weight: 400;
        opacity: 0.92;
        max-width: 820px;
        line-height: 1.5;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.12);
        border-color: #93C5FD;
    }
    
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 6px;
    }
    
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #1E293B;
        line-height: 1.2;
    }
    
    .metric-footer {
        font-size: 0.78rem;
        color: #94A3B8;
        margin-top: 6px;
    }
    
    /* Prediction Result Card */
    .prediction-box {
        background: linear-gradient(135deg, #EFF6FF 0%, #EEF2FF 100%);
        border: 2px solid #818CF8;
        border-radius: 16px;
        padding: 26px;
        margin-top: 20px;
        box-shadow: 0 10px 20px -5px rgba(99, 102, 241, 0.15);
    }
    
    .prediction-score-display {
        font-size: 3.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1E3A8A 0%, #4F46E5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        margin-bottom: 8px;
    }
    
    .pill-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
        color: white;
    }
    
    /* Feature Info Cards */
    .info-card {
        background: #F8FAFC;
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }
    
    /* Formula Card */
    .formula-card {
        background: linear-gradient(135deg, #1E1E38 0%, #2A2A4E 100%);
        color: #F8FAFC;
        border-radius: 14px;
        padding: 22px;
        font-family: 'Courier New', Courier, monospace;
        margin: 16px 0;
        box-shadow: 0 6px 15px -3px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Button primary */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.3px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #6D28D9 100%);
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.35);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA & MODEL CACHING
# ==========================================
@st.cache_data
def get_cached_data():
    """Loads dataset once and caches to avoid repeated disk reads."""
    return load_dataset()

@st.cache_resource
def get_trained_model(_df):
    """Trains model once and caches results for responsive user experience."""
    return train_linear_regression(_df)

try:
    df = get_cached_data()
    model_data = get_trained_model(df)
    dataset_summary = get_dataset_summary(df)
except Exception as e:
    st.error(f"⚠️ Error initializing application data or model: {str(e)}")
    st.stop()


# ==========================================
# SIDEBAR NAVIGATION & DETAILS
# ==========================================
with st.sidebar:
    st.markdown("### 🎓 Student Marks AI")
    st.caption("College Mini-Project in Machine Learning")
    
    navigation = st.radio(
        "Navigation Menu",
        [
            "🏠 Overview",
            "🎯 Predict Marks",
            "📊 Dataset Explorer",
            "📈 Model Evaluation",
            "🧠 How It Works"
        ],
        index=1  # Default directly to Predict Marks for immediate interaction
    )
    
    st.divider()
    
    st.markdown("#### 📌 Quick Project Info")
    st.write(f"• **Algorithm:** Simple Linear Regression")
    st.write(f"• **Target Metric:** Exam Marks (0–100%)")
    st.write(f"• **Input Feature:** Daily Study Hours")
    st.write(f"• **Model R² Score:** `{model_data['metrics']['R2']}` ({model_data['metrics']['R2_Percentage']}%)")
    st.write(f"• **Data Size:** `{dataset_summary['total_records']} Student Records`")
    
    st.divider()
    st.caption("Developed with Python, scikit-learn & Streamlit.")


# ==========================================
# HERO BANNER COMPONENT
# ==========================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">⚡ MACHINE LEARNING DEMONSTRATOR</div>
    <div class="hero-title">Student Marks Predictor</div>
    <div class="hero-subtitle">
        An interactive data science application that estimates student academic performance 
        based on daily study hours using a trained Ordinary Least Squares Linear Regression model.
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# TAB 1: OVERVIEW (HOME)
# ==========================================
if navigation == "🏠 Overview":
    st.markdown("### 🌟 Welcome to the Student Marks Predictor")
    st.write("""
    This project provides students, educators, and examiners with an interactive demonstration of 
    how **Supervised Machine Learning** can predict real-world outcomes based on continuous historical patterns.
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Dataset Size</div>
            <div class="metric-value">{dataset_summary['total_records']}</div>
            <div class="metric-footer">Student study records</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Model Accuracy (R²)</div>
            <div class="metric-value">{model_data['metrics']['R2_Percentage']}%</div>
            <div class="metric-footer">Variance explained by model</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Mean Abs Error (MAE)</div>
            <div class="metric-value">±{model_data['metrics']['MAE']}%</div>
            <div class="metric-footer">Average deviation on test set</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Correlation (r)</div>
            <div class="metric-value">{dataset_summary['correlation']}</div>
            <div class="metric-footer">Strong positive relationship</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    col_left, col_right = st.columns([1.1, 0.9])
    with col_left:
        st.markdown("#### 🎯 Core Objectives")
        st.markdown("""
        1. **End-to-End Supervised ML Pipeline:** Demonstrate feature selection, 80/20 train-test splitting, model fitting, and evaluation.
        2. **Real scikit-learn Model:** Compute actual weights using Ordinary Least Squares ($y = mx + c$) without fabricated predictions.
        3. **Physical Boundary Enforcement:** Keep predicted marks realistically clamped inside `[0%, 100%]`.
        4. **Live Visualization:** Graphically trace the best-fit line alongside real student samples.
        5. **No Data Leakage:** Ensure test records remain completely unseen during model fitting.
        """)
        
    with col_right:
        st.markdown("#### 🛠️ Technology Stack")
        st.markdown("""
        - **Python 3.14+**: Core programming logic.
        - **scikit-learn**: LinearRegression, train_test_split, evaluation metrics.
        - **pandas & NumPy**: Data wrangling and array operations.
        - **Matplotlib**: Regression plotting and custom visual styling.
        - **Streamlit**: Responsive, modern web interface.
        """)

    st.info("💡 **Ready to test?** Switch to the **🎯 Predict Marks** tab from the left sidebar to enter study hours!")


# ==========================================
# TAB 2: PREDICTION (MAIN FEATURE)
# ==========================================
elif navigation == "🎯 Predict Marks":
    st.markdown("### 🎯 Interactive Marks Prediction")
    st.write("Enter the number of hours you dedicate to studying each day to estimate your expected exam score.")
    
    col_input, col_display = st.columns([1, 1.2], gap="large")
    
    with col_input:
        st.markdown("#### ⏱️ Study Hours Input")
        
        # User input via slider and number input
        study_hours = st.slider(
            "Select Daily Study Hours:",
            min_value=0.0,
            max_value=14.0,
            value=6.0,
            step=0.25,
            help="Choose between 0.0 and 14.0 daily hours."
        )
        
        # Quick Preset Buttons for easy college viva / presentation demos
        st.markdown("<small style='color: #64748B;'>Quick Presets for Viva Demonstration:</small>", unsafe_allow_html=True)
        btn_cols = st.columns(4)
        if btn_cols[0].button("2.0 hrs"):
            study_hours = 2.0
        if btn_cols[1].button("5.0 hrs"):
            study_hours = 5.0
        if btn_cols[2].button("8.0 hrs"):
            study_hours = 8.0
        if btn_cols[3].button("11.5 hrs"):
            study_hours = 11.5
            
        predict_button = st.button("🔮 Calculate Predicted Marks", use_container_width=True)
        
        st.markdown("""
        <div class="info-card" style="margin-top: 15px;">
            <strong>ℹ️ How the model predicts:</strong><br>
            Using the trained linear equation:<br>
            <code>Marks = ({slope} × Hours) + {intercept}</code><br>
            Any outcome exceeding 100% or below 0% is automatically clamped within the valid range [0, 100].
        </div>
        """.format(slope=model_data['slope'], intercept=model_data['intercept']), unsafe_allow_html=True)

    # Perform prediction
    pred_res = predict_score(model_data["model"], study_hours)
    
    with col_display:
        st.markdown("#### 📊 Prediction Output")
        
        # Prediction Card Display
        st.markdown(f"""
        <div class="prediction-box">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-weight: 700; color: #475569; font-size: 0.95rem;">ESTIMATED SCORE</span>
                <span class="pill-badge" style="background-color: {pred_res['badge_color']};">{pred_res['category']}</span>
            </div>
            <div class="prediction-score-display">{pred_res['predicted_marks']}%</div>
            <div style="color: #334155; font-size: 0.95rem; margin-top: 6px;">
                For <strong>{study_hours:.2f} hours</strong> of focused daily study.
            </div>
            {f'<div style="color: #64748B; font-size: 0.8rem; margin-top: 4px;">(Raw linear calculation: {pred_res["raw_prediction"]}% - clamped to maximum 100%)</div>' if pred_res['is_clamped'] else ''}
            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid #CBD5E1; color: #1E293B; font-size: 0.9rem;">
                {pred_res['tip']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 📈 Linear Regression Line & Your Position")
    st.caption("The graph below shows the actual training/testing student data alongside the fitted regression line and your predicted coordinate.")
    
    # Matplotlib Regression Visualization
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=120)
    
    # Plot styling
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')
    ax.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
    
    # 1. Scatter points for Training data
    ax.scatter(
        model_data["train_data"]["X"], 
        model_data["train_data"]["y"], 
        color="#2563EB", 
        alpha=0.65, 
        s=55, 
        edgecolors='#1E3A8A', 
        linewidth=1.2,
        label=f"Training Samples (N={model_data['total_train_samples']})"
    )
    
    # 2. Scatter points for Testing data
    ax.scatter(
        model_data["test_data"]["X"], 
        model_data["test_data"]["y"], 
        color="#7C3AED", 
        alpha=0.85, 
        s=65, 
        marker='s',
        edgecolors='#4C1D95', 
        linewidth=1.2,
        label=f"Testing Samples (N={model_data['total_test_samples']})"
    )
    
    # 3. Fitted Regression Line
    x_vals = np.linspace(0, 12, 100)
    y_vals = model_data["slope"] * x_vals + model_data["intercept"]
    y_vals_clamped = np.clip(y_vals, 0, 100)
    ax.plot(
        x_vals, 
        y_vals_clamped, 
        color="#DC2626", 
        linewidth=2.5, 
        linestyle='-',
        label=f"Fit Line: y = {model_data['slope']}x + {model_data['intercept']}"
    )
    
    # 4. Highlight User's Prediction
    ax.scatter(
        [study_hours], 
        [pred_res["predicted_marks"]], 
        color="#F59E0B", 
        s=160, 
        zorder=5, 
        edgecolors='#B45309', 
        linewidth=2,
        label=f"Your Input ({study_hours} hrs → {pred_res['predicted_marks']}%)"
    )
    
    # Dashed reference lines to axes
    ax.axvline(x=study_hours, ymax=pred_res["predicted_marks"]/100, color="#F59E0B", linestyle=":", alpha=0.8, linewidth=1.5)
    ax.axhline(y=pred_res["predicted_marks"], xmax=study_hours/12, color="#F59E0B", linestyle=":", alpha=0.8, linewidth=1.5)
    
    # Labels & Title
    ax.set_title("Study Hours vs. Exam Marks (Linear Regression Model)", fontsize=13, fontweight='bold', color='#1E293B', pad=12)
    ax.set_xlabel("Daily Study Hours", fontsize=11, fontweight='600', color='#334155', labelpad=8)
    ax.set_ylabel("Marks Percentage (%)", fontsize=11, fontweight='600', color='#334155', labelpad=8)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 105)
    
    # Clean ticks
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=9, loc='upper left')
    
    plt.tight_layout()
    st.pyplot(fig)


# ==========================================
# TAB 3: DATASET EXPLORER
# ==========================================
elif navigation == "📊 Dataset Explorer":
    st.markdown("### 📊 Dataset Exploration & Descriptive Statistics")
    st.write("""
    The model is trained on a realistic, reproducible synthetic dataset simulating student study hours and corresponding examination percentages.
    """)
    
    # Dataset Summary Metrics Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Students", f"{dataset_summary['total_records']}")
    c2.metric("Average Study Hours", f"{dataset_summary['hours_mean']} hrs", f"Min: {dataset_summary['hours_min']} | Max: {dataset_summary['hours_max']}")
    c3.metric("Average Marks", f"{dataset_summary['marks_mean']}%", f"Min: {dataset_summary['marks_min']}% | Max: {dataset_summary['marks_max']}%")
    c4.metric("Correlation Coefficient", f"{dataset_summary['correlation']}", "Pearson's r")
    
    st.markdown("---")
    
    d_col1, d_col2 = st.columns([1, 1], gap="medium")
    
    with d_col1:
        st.markdown("#### 📋 Raw Student Records Table")
        st.caption("Displaying the dataset entries used for model splitting.")
        st.dataframe(
            df,
            column_config={
                "Hours_Studied": st.column_config.NumberColumn("Hours Studied", format="%.1f hrs"),
                "Marks_Percentage": st.column_config.ProgressColumn("Exam Marks (%)", min_value=0, max_value=100, format="%.1f%%")
            },
            height=380,
            use_container_width=True
        )
        
        # Download button for CSV
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Dataset (CSV)",
            data=csv_bytes,
            file_name="student_marks.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    with d_col2:
        st.markdown("#### 🔬 Distribution Statistics")
        desc = df.describe().round(2).T
        st.dataframe(desc, use_container_width=True)
        
        st.markdown("""
        <div class="info-card">
            <strong>💡 Data Insights:</strong><br>
            • The correlation coefficient is <strong>~0.97</strong>, indicating a strong direct proportional relationship between time spent studying and exam marks.<br>
            • To reflect real life, natural variance is present—two students studying the exact same hours may score slightly differently due to individual comprehension and focus.
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# TAB 4: MODEL EVALUATION
# ==========================================
elif navigation == "📈 Model Evaluation":
    st.markdown("### 📈 Machine Learning Model Performance & Metrics")
    st.write("""
    To avoid **data leakage** and ensure unbiased evaluation, the dataset is split into **80% Training Data** 
    and **20% Testing Data**. The metrics below are computed **strictly on the unseen test set**.
    """)
    
    # Metrics Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">R² Score (Coefficient of Determination)</div>
            <div class="metric-value">{model_data['metrics']['R2']}</div>
            <div class="metric-footer">{model_data['metrics']['R2_Percentage']}% variance explained</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Mean Absolute Error (MAE)</div>
            <div class="metric-value">{model_data['metrics']['MAE']}</div>
            <div class="metric-footer">Average absolute gap between truth and prediction</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Mean Squared Error (MSE)</div>
            <div class="metric-value">{model_data['metrics']['MSE']}</div>
            <div class="metric-footer">Penalizes larger outliers heavily</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Root Mean Squared Error (RMSE)</div>
            <div class="metric-value">{model_data['metrics']['RMSE']}</div>
            <div class="metric-footer">Standard deviation of the residuals</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Equation banner
    st.markdown(f"""
    <div class="formula-card">
        <strong>Learned Regression Equation:</strong><br><br>
        <span style="font-size: 1.3rem; color: #60A5FA;">{model_data['equation']}</span><br><br>
        • Slope (Coefficient m): <strong>{model_data['slope']}</strong> marks gained per additional hour.<br>
        • Intercept (Baseline c): <strong>{model_data['intercept']}</strong> marks predicted with 0 study hours.
    </div>
    """, unsafe_allow_html=True)

    # Actual vs Predicted on Test Set
    col_t1, col_t2 = st.columns([1, 1], gap="large")
    
    with col_t1:
        st.markdown("#### 🎯 Unseen Test Set: Actual vs. Predicted")
        st.caption("These records were never seen during model training.")
        st.dataframe(
            model_data["test_comparison"],
            column_config={
                "Study Hours": st.column_config.NumberColumn(format="%.1f hrs"),
                "Actual Marks (%)": st.column_config.NumberColumn(format="%.1f%%"),
                "Predicted Marks (%)": st.column_config.NumberColumn(format="%.1f%%"),
                "Absolute Error": st.column_config.NumberColumn(format="%.2f")
            },
            use_container_width=True
        )
        
    with col_t2:
        st.markdown("#### 📊 Residual Error Bar Chart")
        st.caption("Visualizing the error (Actual − Predicted) on each test record.")
        
        fig_err, ax_err = plt.subplots(figsize=(6, 3.8), dpi=110)
        test_df = model_data["test_comparison"]
        errors = test_df["Actual Marks (%)"] - test_df["Predicted Marks (%)"]
        
        bars = ax_err.bar(
            range(len(errors)),
            errors,
            color=['#10B981' if e >= 0 else '#EF4444' for e in errors],
            edgecolor='#1E293B',
            linewidth=0.8,
            width=0.5
        )
        ax_err.axhline(0, color='#64748B', linestyle='--', linewidth=1)
        ax_err.set_title("Test Set Residuals (Actual − Predicted)", fontsize=11, fontweight='bold', color='#1E293B')
        ax_err.set_xlabel("Test Record Index", fontsize=9, fontweight='600')
        ax_err.set_ylabel("Error in Marks (%)", fontsize=9, fontweight='600')
        ax_err.set_xticks(range(len(errors)))
        ax_err.set_xticklabels([f"#{i+1}" for i in range(len(errors))])
        ax_err.grid(axis='y', linestyle=':', alpha=0.5)
        plt.tight_layout()
        st.pyplot(fig_err)


# ==========================================
# TAB 5: HOW IT WORKS (ALGORITHM EXPLANATION)
# ==========================================
elif navigation == "🧠 How It Works":
    st.markdown("### 🧠 Understanding Linear Regression for Beginners")
    st.write("A student-friendly breakdown of Machine Learning fundamentals used in this project.")
    
    st.markdown("""
    #### 1. What is Linear Regression?
    Linear Regression is a fundamental **Supervised Machine Learning algorithm** used for predicting a continuous numerical value (like exam marks) 
    based on one or more input variables (like study hours).
    
    When we use a single input feature, it is called **Simple Linear Regression**, defined mathematically as:
    """)
    
    st.latex(r"y = m \cdot x + c")
    
    st.markdown("""
    Where:
    - **$y$ (Dependent Target):** The student's exam score to predict.
    - **$x$ (Independent Feature):** The daily study hours.
    - **$m$ (Slope / Weight):** How much the exam score increases for every additional study hour.
    - **$c$ (Y-Intercept / Bias):** The expected baseline score if a student studies 0 hours.
    """)
    
    st.markdown("---")
    
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown(r"""
        #### 2. How the Model Learns (Ordinary Least Squares)
        The algorithm tests millions of candidate lines to find the single line that minimizes the sum of squared differences 
        (residuals) between actual marks ($y$) and predicted marks ($\hat{y}$):
        """)
        st.latex(r"\text{Cost} = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2")
        st.markdown("""
        By minimizing this error, scikit-learn finds the optimal slope $m$ and intercept $c$.
        """)
        
    with col_w2:
        st.markdown("""
        #### 3. Preventing Data Leakage
        - **Training Set (80%):** Given to the algorithm to discover the relationship.
        - **Testing Set (20%):** Kept strictly hidden during training. Used only to evaluate how well the model generalizes to new students.
        - **Zero Leakage:** Training on the entire dataset would lead to misleadingly high accuracy.
        """)
        
    st.markdown("---")
    
    st.markdown(r"""
    #### 4. Understanding Evaluation Metrics
    | Metric | Formula | What It Tells You |
    | :--- | :--- | :--- |
    | **MAE (Mean Absolute Error)** | $\frac{1}{n} \sum |y - \hat{y}|$ | On average, how many marks is the prediction off by. |
    | **MSE (Mean Squared Error)** | $\frac{1}{n} \sum (y - \hat{y})^2$ | Magnifies and penalizes large prediction mistakes. |
    | **RMSE (Root Mean Squared Error)**| $\sqrt{\text{MSE}}$ | Error in the same units as the target variable (marks %). |
    | **$R^2$ Score** | $1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}}$ | Explains the proportion of variance captured by the model (1.0 = perfect fit). |
    """)
    
    st.markdown("---")
    
    st.markdown(r"""
    #### 5. Why Range Clamping [0, 100] is Essential
    A pure mathematical linear equation extends infinitely in both directions ($\lim_{x \to \infty} mx+c = \infty$). 
    If a student inputs 15 hours, the raw math might output 140 marks! 
    Since exams have physical bounds of **0 to 100%**, our engineering logic applies **range clipping**:
    """)
    st.code("final_prediction = min(max(raw_prediction, 0.0), 100.0)", language="python")


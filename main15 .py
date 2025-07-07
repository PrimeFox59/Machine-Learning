import streamlit as st
import pandas as pd
import pickle
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ======================
# PAGE CONFIGURATION
# ======================
st.set_page_config(
    page_title="Galih's ML Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# CUSTOM CSS STYLING
# ======================
st.markdown("""
<style>
    /* Style utama dengan gradien biru */
    .header {
        font-size: 36px !important;
        color: white !important;
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7db9e8 100%);
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    /* Efek gelombang di header */
    .header::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 10px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
        animation: wave 3s linear infinite;
    }
    
    @keyframes wave {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Style sidebar dengan nuansa biru muda */
    .sidebar .sidebar-content {
        background-color: #f0f8ff;
        background-image: linear-gradient(to bottom, #e6f2ff, #f0f8ff);
        border-right: 1px solid #cce0ff;
    }
    
    /* Style dropdown/selectbox dengan animasi */
    .stSelectbox > div > div > select {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px 15px;
        border: 2px solid #b3d1ff;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stSelectbox > div > div > select:hover {
        border-color: #4a90e2;
        box-shadow: 0 5px 15px rgba(74,144,226,0.2);
        transform: translateY(-2px);
    }
    .stSelectbox > div > div > select:focus {
        border-color: #1e3c72;
        box-shadow: 0 0 0 3px rgba(30,60,114,0.2);
    }
    .stSelectbox > label {
        font-weight: 600;
        color: #2a5298;
        margin-bottom: 8px;
        font-size: 14px;
    }
    
    /* Style button dengan animasi dan efek hover */
    .stButton>button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        font-weight: 600;
        transition: all 0.4s;
        width: 100%;
        box-shadow: 0 4px 6px rgba(30,60,114,0.2);
        position: relative;
        overflow: hidden;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        transform: translateY(-3px);
        box-shadow: 0 7px 14px rgba(30,60,114,0.3);
    }
    .stButton>button:active {
        transform: translateY(1px);
    }
    .stButton>button::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -60%;
        width: 200%;
        height: 200%;
        background: rgba(255,255,255,0.1);
        transform: rotate(30deg);
        transition: all 0.3s;
    }
    .stButton>button:hover::after {
        left: 100%;
    }
    
    /* Style prediction box dengan animasi masuk */
    .prediction-box {
        padding: 25px;
        border-radius: 15px;
        background-color: #1c1f26;
        color: #fff;
        margin-top: 20px;
        border-left: 6px solid #2a5298;
        transition: all 0.5s ease-out;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        animation: fadeIn 0.8s ease-out;
    }
    .prediction-box:hover {
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transform: translateY(-3px);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Style expander dengan ikon animasi */
    .stExpander > div > div {
        background: linear-gradient(to bottom, #f8fbff, #fff) !important;
        border-radius: 12px !important;
        border: 1px solid #d6e7ff !important;
    }
    .stExpander > div > div:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    .stExpander > label {
        font-weight: 600;
        color: #2a5298;
    }
    .stExpander > label:hover {
        color: #1e3c72;
    }
    .stExpander > label::after {
        content: "➕";
        transition: all 0.3s;
    }
    .stExpander > label:hover::after {
        transform: rotate(90deg);
    }
    
    /* Style social media icons dengan animasi */
    .social-media {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
    }
    .social-media a {
        font-size: 28px;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
        display: inline-block;
        width: 50px;
        height: 50px;
        line-height: 50px;
        text-align: center;
        border-radius: 50%;
        background: rgba(214,231,255,0.5);
    }
    .social-media a:hover {
        transform: scale(1.2) rotate(10deg);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .linkedin { 
        color: #0e76a8 !important;
        background: rgba(14,118,168,0.1) !important;
    }
    .linkedin:hover {
        background: rgba(14,118,168,0.2) !important;
    }
    .github { 
        color: #333 !important;
        background: rgba(51,51,51,0.1) !important;
    }
    .github:hover {
        background: rgba(51,51,51,0.2) !important;
    }
    .instagram { 
        color: transparent !important;
        background: radial-gradient(circle at 30% 107%, #fdf497 0%, #fdf497 5%, #fd5949 45%, #d6249f 60%, #285AEB 90%) !important;
        background-clip: text !important;
        -webkit-background-clip: text !important;
    }
    
    /* Animasi untuk kartu input */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .floating-card {
        animation: float 6s ease-in-out infinite;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Tooltip custom */
    .stTooltip {
        background-color: #2a5298 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }
    
    /* Surface Roughness Specific Styles */
    .input-section {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 30px;
    }
    
    .surface-prediction-box {
        padding: 30px;
        background-color: ##045F5F;
        border-radius: 12px;
        margin: 30px 0;
        border-left: 6px solid #388e3c;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .footer {
        text-align: center;
        color: #7f8c8d;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #eee;
        font-size: 0.9rem;
    }
    
    .parameter-value {
        font-weight: 600;
        color: #2c3e50;
    }
    
    .data-flow-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .header {
            font-size: 28px !important;
            padding: 15px;
        }
    }
    
    :root {
        --primary: #388e3c;
        --secondary: #2c3e50;
        --light-bg: #f8f9fa;
        --card-bg: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.markdown('<div class="header">🧠 Machine Learning Dashboard</div>', unsafe_allow_html=True)

# ======================
# SIDEBAR NAVIGATION
# ======================
with st.sidebar:
    st.image("icon head.png", width=200)
    st.markdown("### Navigation")
    
    # Dropdown untuk memilih model
    model_option = st.selectbox(
        "Select Prediction Model:",
        ("Iris Species Classifier", "Heart Disease Predictor", "Surface Roughness (Ra) Prediction"),
        key="model_select",
        help="Select prediction model to use"
    )
    
    st.markdown("---")
    
    # Dropdown untuk memilih metode input
    input_option = st.selectbox(
        "Input Method:",
        ("Manual Input", "Upload CSV"),
        key="input_method",
        help="Select input method"
    )
    # Ganti warna teks selectbox menjadi putih
    st.markdown("""
    <style>
    .stSelectbox > div > div > select, .stSelectbox > label {
        color: #fff !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.image("avatar.png", width=100)  # Gambar kecil dengan judul avatar.png
    st.markdown("### About Me")
    st.markdown("""
    **Galih Primananda**  
    Engineering Enthusiast  
    """)

    
    # Professional Profile
    st.markdown("""
    **Profile:**
    - Multidisciplinary Engineer (7+ years experience)
    - Specializations: 
      - Machining Process Optimization
      - industrial / Office System Development
      - Data Analysis & Machine Learning
    - Key Achievements:
      - 375% efficiency boost Document Automation
      - Kaizen QCC 1st Place Winner (2024)
      - Best Kaizen Idea (2024)
      - Machine Learning implementation in manufacturing
    - Technical Skills:
      - Advanced: Python, VBA, CAD/CAM
      - Manufacturing: FMEA, QCPC, GD&T
      - Emerging: Linear Regression
    <div class="currently-learning">
      <strong>Currently learning:</strong><br>
      <span class="currently-learning-arrow">&#8594;</span> Machine Learning (Deep Learning)<br>
      <span class="currently-learning-arrow">&#8594;</span> Web Application Development
    </div>
    - Education:
      - STIE Mahardhika (Operational Management)
      - SMKN 8 Malang (Mechatronics)
    """, unsafe_allow_html=True)

    # Tambahkan CSS untuk highlight "Currently learning" dengan warna gelap agar teks terang terlihat jelas
    st.markdown("""
    <style>
        .sidebar .sidebar-content .markdown-text-container {
            font-size: 14px;
            line-height: 1.6;
        }
        .sidebar .sidebar-content .markdown-text-container strong {
            color: #2a5298;
        }
        .currently-learning {
            background: linear-gradient(90deg, #232946, #2a5298);
            color: #fff !important;
            padding: 8px 12px;
            border-radius: 8px;
            margin: 8px 0;
            border-left: 3px solid #7db9e8;
        }
        .currently-learning-arrow {
            color: #7db9e8;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Social media icons with links
    st.markdown("""
    <div class="social-media">
        <a href="https://www.linkedin.com/in/galihprime/" class="linkedin" title="LinkedIn">
            <img src="https://cdn-icons-png.flaticon.com/128/3536/3536505.png" alt="LinkedIn" width="32" height="32" style="vertical-align:middle;">
        </a>
        <a href="https://github.com/PrimeFox59" class="github" title="GitHub">
            <img src="https://cdn-icons-png.flaticon.com/128/733/733553.png" alt="GitHub" width="32" height="32" style="vertical-align:middle;">
        </a>
        <a href="https://www.instagram.com/glh_prima/" class="instagram" title="Instagram">
            <img src="https://cdn-icons-png.flaticon.com/128/3955/3955024.png" alt="Instagram" width="32" height="32" style="vertical-align:middle;">
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <small>*Note: This is a demo application for educational purposes. 
    Always consult healthcare professionals for medical advice.*</small>
    """, unsafe_allow_html=True)

# ======================
# MODEL FUNCTIONS
# ======================

# Iris Prediction Function
def iris_prediction():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Iris Species Classification 🌸
        Predict the species of an Iris flower based on its measurements.
        
        Data obtained from the famous [Iris dataset](https://www.kaggle.com/uciml/iris) by UCIML.
        """)
        
    with col2:
        try:
            img = Image.open("iris.JPG")
            st.image(img, use_container_width=True, caption="Iris Flower Species")
        except:
            st.image("https://archive.ics.uci.edu/static/public/53/iris.jpg", 
                    use_container_width=True, caption="Iris Flower Species")
    
    # Input data
    st.markdown("### Input Features")
    
    if st.session_state.input_method == "Upload CSV":
        uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])
        if uploaded_file is not None:
            input_df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            st.dataframe(input_df)
        else:
            st.info("Please upload a CSV file or switch to manual input.")
            st.stop()
    else:
        with st.expander("Adjust Flower Measurements", expanded=True):
            cols = st.columns(2)
            with cols[0]:
                SepalLengthCm = st.slider('Sepal Length (cm)', 4.3, 10.0, 5.8, 0.1)
                SepalWidthCm = st.slider('Sepal Width (cm)', 2.0, 5.0, 3.0, 0.1)
            with cols[1]:
                PetalLengthCm = st.slider('Petal Length (cm)', 1.0, 9.0, 3.8, 0.1)
                PetalWidthCm = st.slider('Petal Width (cm)', 0.1, 5.0, 1.2, 0.1)
            
            data = {
                'SepalLengthCm': SepalLengthCm,
                'SepalWidthCm': SepalWidthCm,
                'PetalLengthCm': PetalLengthCm,
                'PetalWidthCm': PetalWidthCm
            }
            input_df = pd.DataFrame(data, index=[0])
        
        st.markdown("**Current Measurements:**")
        st.dataframe(input_df.style.highlight_max(axis=0, color="#508cfa"))
    
    # Prediction
    if st.button('Predict Species'):
        with st.spinner('Analyzing flower measurements...'):
            time.sleep(2)
            
            try:
                # Simulasi model (dalam implementasi nyata, gunakan model yang sudah di-trained)
                def mock_predict(input_data):
                    if input_data['PetalLengthCm'][0] < 2.5:
                        return 0  # Iris-setosa
                    elif input_data['PetalWidthCm'][0] < 1.8:
                        return 1  # Iris-versicolor
                    else:
                        return 2  # Iris-virginica
                
                prediction = mock_predict(input_df)
                
                # Map prediction ke nama spesies
                species_map = {
                    0: ("Iris-setosa", "🌱", "#51cf66"),
                    1: ("Iris-versicolor", "🌸", "#339af0"),
                    2: ("Iris-virginica", "💮", "#ff6b6b")
                }
                species, emoji, color = species_map[prediction]
                
                # Tampilkan hasil
                st.markdown("### Prediction Result")
                st.markdown(f"""
                <div class="prediction-box" style="background-color: #1c1f26; border-left-color: {color}; color: white;">
                    <h2 style="color:{color}; text-align:center;">
                        {emoji} {species} {emoji}
                    </h2>
                    <p style="text-align:center;">The model predicts this is an <strong>{species}</strong> iris flower.</p>
                </div>
                """, unsafe_allow_html=True)

                
                # Visualisasi fitur penting
                st.markdown("**Feature Importance:**")
                feature_importance = pd.DataFrame({
                    'Feature': ['Petal Length', 'Petal Width', 'Sepal Length', 'Sepal Width'],
                    'Importance': [0.45, 0.35, 0.15, 0.05]
                })
                st.bar_chart(feature_importance.set_index('Feature'))
                
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")

# Heart Disease Prediction Function
def heart_disease_prediction():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Heart Disease Risk Assessment ❤️
        Predict the likelihood of heart disease based on health indicators.
        
        Data obtained from the [Heart Disease dataset](https://archive.ics.uci.edu/dataset/45/heart+disease) by UCIML.
        """)
        
        st.warning("""
        **Disclaimer:** This is not a medical diagnosis tool. 
        Always consult with healthcare professionals for medical advice.
        """)
        
    with col2:
        try:
            img = Image.open("heart-disease.jpg")
            st.image(img, use_container_width=True, caption="Heart Health Indicators")
        except:
            st.image("https://www.heart.org/-/media/Images/Health-Topics/Heart-Disease/HeartDiseaseContentImage.jpg", 
                   use_container_width=True, caption="Heart Health Indicators")
    
    # Input data
    st.markdown("### Patient Information")
    
    if st.session_state.input_method == "Upload CSV":
        uploaded_file = st.file_uploader("Upload patient data CSV", type=["csv"])
        if uploaded_file is not None:
            input_df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            st.dataframe(input_df)
        else:
            st.info("Please upload a CSV file or switch to manual input.")
            st.stop()
    else:
        with st.expander("Patient Details", expanded=True):
            cols = st.columns(2)
            with cols[0]:
                age = st.slider("Age", 29, 77, 50)
                sex = st.selectbox("Gender", ("Female", "Male"))
                sex = 0 if sex == "Female" else 1
                
                cp_options = {
                    "Typical angina": 1,
                    "Atypical angina": 2,
                    "Non-anginal pain": 3,
                    "Asymptomatic": 4
                }
                cp = st.selectbox("Chest Pain Type", list(cp_options.keys()))
                cp = cp_options[cp]
                
            with cols[1]:
                thalach = st.slider("Max Heart Rate Achieved", 71, 202, 150)
                exang = st.selectbox("Exercise Induced Angina", ("No", "Yes"))
                exang = 1 if exang == "Yes" else 0
                
                oldpeak = st.slider("ST Depression Induced by Exercise", 0.0, 6.2, 1.0, 0.1)
            
            st.markdown("---")
            
            cols2 = st.columns(3)
            with cols2[0]:
                slope = st.slider("Slope of Peak Exercise ST Segment", 0, 2, 1)
            with cols2[1]:
                ca = st.slider("Number of Major Vessels Colored by Fluoroscopy", 0, 3, 1)
            with cols2[2]:
                thal_options = {
                    "Normal": 1,
                    "Fixed Defect": 2,
                    "Reversible Defect": 3
                }
                thal = st.selectbox("Thalassemia Result", list(thal_options.keys()))
                thal = thal_options[thal]
            
            data = {
                'age': age,
                'sex': sex,
                'cp': cp,
                'thalach': thalach,
                'exang': exang,
                'oldpeak': oldpeak,
                'slope': slope,
                'ca': ca,
                'thal': thal
            }
            input_df = pd.DataFrame(data, index=[0])
        
        st.markdown("**Current Patient Data:**")
        st.dataframe(input_df.style.apply(lambda x: ['background: #ffcccc' if x.name in ['cp', 'exang', 'ca'] else '' for i in x], axis=1))
    
    # Prediction
    if st.button('Assess Heart Disease Risk'):
        with st.spinner('Analyzing health indicators...'):
            time.sleep(3)
            
            try:
                # Simulasi model (dalam implementasi nyata, gunakan model yang sudah di-trained)
                def mock_predict(input_data):
                    risk_score = 0
                    risk_score += input_data['age'][0] / 77 * 0.3
                    risk_score += (input_data['cp'][0] / 4) * 0.25
                    risk_score += (input_data['thalach'][0] < 130) * 0.2
                    risk_score += (input_data['exang'][0]) * 0.15
                    risk_score += (input_data['oldpeak'][0] > 1.5) * 0.1
                    return 1 if risk_score > 0.5 else 0
                
                prediction = mock_predict(input_df)
                proba = [0.3, 0.7] if prediction == 1 else [0.7, 0.3]  # Simulasi probability
                
                # Tampilkan hasil
                st.markdown("### Risk Assessment Result")
                if prediction == 1:
                    st.markdown(f"""
                    <div class="prediction-box" style="border-left-color: #ff6b6b">
                        <h2 style="color:#ff6b6b; text-align:center;">
                            ❗ High Risk of Heart Disease ({(proba[1]*100):.1f}%) ❗
                        </h2>
                        <p style="text-align:center;">
                            The model suggests this patient may be at risk of heart disease.
                            Please consult with a cardiologist for further evaluation.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Rekomendasi
                    st.markdown("**Recommendations:**")
                    st.markdown("""
                    - Schedule an appointment with a cardiologist
                    - Consider lifestyle changes (diet, exercise)
                    - Monitor blood pressure regularly
                    - Avoid smoking and excessive alcohol
                    """)
                else:
                    st.markdown(f"""
                    <div class="prediction-box" style="border-left-color: #51cf66">
                        <h2 style="color:#51cf66; text-align:center;">
                            ✅ Low Risk of Heart Disease ({(proba[0]*100):.1f}%) ✅
                        </h2>
                        <p style="text-align:center;">
                            The model suggests this patient has a low risk of heart disease.
                            Maintain healthy habits for continued heart health.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Visualisasi faktor risiko
                st.markdown("**Risk Factors Analysis:**")
                risk_factors = pd.DataFrame({
                    'Factor': ['Age', 'Chest Pain', 'Heart Rate', 'Exercise Angina', 'ST Depression'],
                    'Score': [
                        age / 77 * 100,
                        cp / 4 * 100,
                        (202 - thalach) / (202-71) * 100,
                        exang * 100,
                        oldpeak / 6.2 * 100
                    ]
                })
                st.bar_chart(risk_factors.set_index('Factor'))
                
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")

# Surface Roughness Prediction Function
def surface_roughness_prediction():
    # DATA PROCESSING FLOW DOCUMENTATION
    # Data Flow section removed as requested

    # APP HEADER
    col1, col2 = st.columns([1, 3])
    with col2:
        st.markdown('<h1 class="header-text">Surface Roughness (Ra) Prediction</h1>', unsafe_allow_html=True)
        st.markdown("""
        Predict the surface roughness (Ra) of machined parts using our advanced Random Forest algorithm. 
        Adjust the machining parameters below and click **Predict** to get instant results.
        """)

    # MODEL LOADING
    @st.cache_resource
    def load_model():
        try:
            with st.spinner('🔍 Loading prediction model...'):
                with open('random_forest_model.pkl', 'rb') as f:
                    model = pickle.load(f)
            st.success('✅ Model loaded successfully!')
            return model
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            return None

    model = load_model()


    # INPUT SECTION
    with st.container():
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Machining Parameters")

        # Use sidebar selection for input method
        input_method = st.session_state.get('input_method', 'Manual Input')

        if input_method == "Upload CSV":
            uploaded_file = st.file_uploader("Upload your machining parameters CSV file", type=["csv"])
            if uploaded_file is not None:
                try:
                    input_df = pd.read_csv(uploaded_file)
                    st.success("File uploaded successfully!")
                    st.dataframe(input_df)
                except Exception as e:
                    st.error(f"Error reading CSV: {str(e)}")
                    st.stop()
            else:
                st.info("Please upload a CSV file with columns: f, Fy, Fx, Replica, Fz, Tool_ID")
                st.markdown('</div>', unsafe_allow_html=True)
                st.stop()
        else:
            cols = st.columns(2)
            with cols[0]:
                Tool_ID = st.selectbox(
                    '**Tool ID**', 
                    ['21', '31', '41', '51', '61', '71'],
                    help="Select the cutting tool identifier",
                    index=0
                )
                f = st.number_input(
                    '**Feed Rate (f) [mm/rev]**', 
                    value=0.1, 
                    min_value=0.01, 
                    max_value=1.0, 
                    step=0.01,
                    format="%.2f",
                    help="Feed rate in millimeters per revolution"
                )
            with cols[1]:
                replica_map = {'Replica 1': 1, 'Replica 2': 2}
                replica_display = st.selectbox(
                    '**Replication**',
                    list(replica_map.keys()),
                    help="Experimental replication number",
                    index=0
                )
                Replica = replica_map[replica_display]
                st.markdown("### ⚡ Cutting Forces")
                Fx = st.number_input(
                    '**Fx (N)**', 
                    value=0.0, 
                    step=0.1,
                    format="%.1f",
                    help="Cutting force in X direction"
                )
                Fy = st.number_input(
                    '**Fy (N)**', 
                    value=0.0, 
                    step=0.1,
                    format="%.1f",
                    help="Cutting force in Y direction"
                )
                Fz = st.number_input(
                    '**Fz (N)**', 
                    value=0.0, 
                    step=0.1,
                    format="%.1f",
                    help="Cutting force in Z direction"
                )
            input_dict = {
                'f': [f],
                'Fy': [Fy],
                'Fx': [Fx],
                'Replica': [Replica],
                'Fz': [Fz],
                'Tool_ID': [Tool_ID]
            }
            feature_order = ['f', 'Fy', 'Fx', 'Replica', 'Fz', 'Tool_ID']
            input_df = pd.DataFrame(input_dict)[feature_order]
        st.markdown('</div>', unsafe_allow_html=True)

    # PREDICTION BUTTON & RESULTS
    if st.button('🔮 Predict Ra', use_container_width=True, type="primary"):
        if model is None:
            st.error("Model not loaded. Cannot make predictions.")
        else:
            try:
                with st.spinner('🧠 Calculating prediction...'):
                    prediction = model.predict(input_df)
                    st.balloons()
                # Display prediction and quality scale side by side
                result_col, scale_col = st.columns([2, 2])
                with result_col:
                    st.markdown(f"""
    <div class="surface-prediction-box" style="background-color: #23272f; color: #fff;">
        <h2 style="color: #fff; font-size: 2.5rem; font-weight: 900; text-align:center; margin-bottom: 0.5em;">
            📊 Prediction Result
        </h2>
        <p style="font-size: 3.2rem; font-weight: bold; color: #4caf50; text-align:center; margin-bottom: 0.2em;">
            {prediction[0]:.4f} <span style='font-size:1.5rem;'>μm</span>
        </p>
        <div style="margin-top: 35px;">
            <p style="font-weight: 600; font-size:1.2rem; border-bottom: 1px solid #444; padding-bottom: 8px; color: #fff;">
                Parameters Used:
            </p>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 15px;">
                <div>
                    <p style="margin-bottom: 5px; color: #fff;"><b>🔧 Tool ID:</b></p>
                    <p class="parameter-value" style="color: #fff;">{Tool_ID}</p>
                </div>
                <div>
                    <p style="margin-bottom: 5px; color: #fff;"><b>🔄 Replica:</b></p>
                    <p class="parameter-value" style="color: #fff;">{Replica}</p>
                </div>
                <div>
                    <p style="margin-bottom: 5px; color: #fff;"><b>⚙️ Feed Rate:</b></p>
                    <p class="parameter-value" style="color: #fff;">{f:.2f} mm/rev</p>
                </div>
                <div>
                    <p style="margin-bottom: 5px; color: #fff;"><b>💪 Forces:</b></p>
                    <p class="parameter-value" style="color: #fff;">Fx={Fx:.1f} N, Fy={Fy:.1f} N, Fz={Fz:.1f} N</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

                with scale_col:
                    st.markdown("### 📏 Surface Quality Scale")
                    fig, ax = plt.subplots(figsize=(6, 2))
                    # Define quality ranges and colors (Standard removed)
                    ranges = [0, 0.4, 1.6, 2.5]
                    labels = ['Very Smooth', 'Rough', 'Very Rough']
                    colors = ['#81c784', '#ffd54f', '#e57373']
                    
                    # Create the quality bar
                    for i in range(len(ranges)-1):
                        ax.barh(0, ranges[i+1]-ranges[i], left=ranges[i], 
                               color=colors[i], height=0.5, edgecolor='white')
                    # Add prediction indicator
                    ax.axvline(prediction[0], color='#1976d2', linestyle='-', 
                              linewidth=3, label=f'Predicted Ra: {prediction[0]:.4f} μm')
                    # Customize the plot
                    ax.set_xlim(0, 2.5)
                    ax.set_yticks([])
                    ax.set_xlabel('Surface Roughness (Ra) in micrometers (μm)', fontsize=12)
                    ax.set_title('Surface Quality Classification', fontsize=14, pad=15)
                    # Add quality labels
                    for i in range(len(labels)):
                        xpos = (ranges[i] + ranges[i+1]) / 2
                        ax.text(xpos, 0, labels[i], ha='center', va='center', 
                              fontsize=8, fontweight='bold', color='#2c3e50')
                    ax.legend(loc='upper right', framealpha=1)
                    plt.tight_layout()
                    st.pyplot(fig)
                # Quality interpretation
                quality_text = ""
                if prediction[0] < 0.4:
                    quality_text = "Excellent surface finish (Very Smooth)"
                elif 0.4 <= prediction[0] < 0.8:
                    quality_text = "Good surface finish (Standard)"
                elif 0.8 <= prediction[0] < 1.6:
                    quality_text = "Moderate surface finish (Rough)"
                else:
                    quality_text = "Poor surface finish (Very Rough)"
                st.info(f"**Quality Interpretation:** {quality_text}")
            except Exception as e:
                st.error(f"❌ Prediction failed: {str(e)}")

    # INFORMATION SECTION
    with st.expander("ℹ️ About this tool", expanded=False):
        tab1, tab2, tab3 = st.tabs(["Guide", "Technical", "Interpretation"])
        
        with tab1:
            st.markdown("""
            ### How to Use This Tool
            
            1. **Select Tool ID** - Choose the appropriate cutting tool from the dropdown
            2. **Set Replication** - Select the experimental replication number
            3. **Enter Feed Rate** - Input the machining feed rate in mm/rev
            4. **Input Cutting Forces** - Provide the measured forces in X, Y, and Z directions
            5. **Click Predict** - Get instant surface roughness prediction
            
            The system will display:
            - Predicted Ra value in micrometers (μm)
            - Visual quality scale showing where your result falls
            - Detailed parameter summary
            """)
        
        with tab2:
            st.markdown("""
            ### Technical Specifications

            **Data Source**
            - This model was trained using the [CNC Turning Roughness, Forces, and Tool Wear dataset](https://www.kaggle.com/datasets/adorigueto/cnc-turning-roughness-forces-and-tool-wear) from Kaggle.
            - The dataset contains detailed measurements from CNC turning experiments, including surface roughness (Ra), cutting forces (Fx, Fy, Fz), tool wear, and machining parameters.

            **Model Architecture**
            - Type: Random Forest Regressor
            - Estimators: 200 trees
            - Max Depth: 20 levels

            **Input Features**
            - Tool ID (categorical)
            - Replication number
            - Feed rate (f) in mm/rev
            - Cutting forces (Fx, Fy, Fz) in Newtons

            **Parameter Ranges Used in Training Dataset**
            - **Init_diameter:** 94, 93.5, 92.5, 90.9, 90.4, 89.4 (mm)
            - **Final_diameter:** 93.5, 92.5, 90.9, 90.4, 89.4, 87.8 (mm)
            - **ap (depth of cut):** 0.25, 0.5, 0.8 (mm)
            - **vc (cutting speed):** 310, 350, 390 (m/min)

            **Performance Metrics**
            - R² Score: 0.9515
            - Mean Absolute Error: 0.0413 μm
            - Cross-Validation Score: 0.94

            **Training Data**
            - 300+ machining experiments
            - 6 different tool types
            """)
        
        with tab3:
            st.markdown("""
            ### Surface Quality Interpretation
            
            | Ra Value (μm) | Classification | Typical Application |
            |--------------|----------------|---------------------|
            | < 0.4 | Very Smooth | Precision components, optical surfaces |
            | 0.4 - 1.6 | Rough | General engineering components |
            | > 1.6 | Very Rough | Rough castings, unfinished surfaces |
            
            **Factors Affecting Surface Finish:**
            - Higher feed rates generally increase roughness
            - Tool wear degrades surface quality over time
            - Optimal cutting forces produce better finishes
            - Tool geometry significantly impacts results
            """)

    # FOOTER
    st.markdown("""
    <div class="footer">
        <p>Surface Roughness Prediction Tool v1.1</p>
        <p>© 2025 by Galih Primananda | MAI1714</p>
        <p>Powered by Random Forest</p>
    </div>
    """, unsafe_allow_html=True)

# ======================
# MAIN APP LOGIC
# ======================
if st.session_state.model_select == "Iris Species Classifier":
    iris_prediction()
elif st.session_state.model_select == "Heart Disease Predictor":
    heart_disease_prediction()
elif st.session_state.model_select == "Surface Roughness (Ra) Prediction":
    surface_roughness_prediction()

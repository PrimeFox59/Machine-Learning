import streamlit as st
import pandas as pd
import pickle
import time
from PIL import Image

# Konfigurasi halaman
st.set_page_config(
    page_title="Galih's ML Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS kustom untuk styling dengan nuansa biru dan animasi unik
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
        background: linear-gradient(to right, #f8fbff, #f0f8ff);
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
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .header {
            font-size: 28px !important;
            padding: 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header">🧠 Galih Primananda\'s ML Dashboard</div>', unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.image("icon head.png", width=200)
    st.markdown("### Navigation")
    
    # Dropdown untuk memilih model
    model_option = st.selectbox(
        "Select Prediction Model:",
        ("Iris Species Classifier", "Heart Disease Predictor"),
        key="model_select",
        help="Pilih model prediksi yang ingin digunakan"
    )
    
    st.markdown("---")
    
    # Dropdown untuk memilih metode input
    input_option = st.selectbox(
        "Input Method:",
        ("Manual Input", "Upload CSV"),
        key="input_method",
        help="Pilih metode input data"
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
    st.markdown("### About Me")
    st.markdown("""
    **Galih Primananda**  
    Machine Learning Enthusiast  
    """)
    
    # Social media icons with links
    st.markdown("""
    <div class="social-media">
        <a href="https://www.linkedin.com/in/galihprime/" class="linkedin" title="LinkedIn">👔</a>
        <a href="https://github.com/PrimeFox59" class="github" title="GitHub">🐙</a>
        <a href="https://www.instagram.com/glh_prima/" class="instagram" title="Instagram">📷</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <small>*Note: This is a demo application for educational purposes. 
    Always consult healthcare professionals for medical advice.*</small>
    """, unsafe_allow_html=True)

# Fungsi untuk prediksi Iris
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
            st.image(img, use_container_width=True, caption="Iris Flower Species")  # Diubah ke use_container_width
        except:
            st.image("https://archive.ics.uci.edu/static/public/53/iris.jpg", 
                    use_container_width=True, caption="Iris Flower Species")  # Diubah ke use_container_width
    
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
        st.dataframe(input_df.style.highlight_max(axis=0, color="#d4f1f9"))
    
    # Prediksi
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
                <div class="prediction-box" style="border-left-color: {color}">
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

# Fungsi untuk prediksi Heart Disease
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
            st.image(img, use_container_width=True, caption="Heart Health Indicators")  # Diubah ke use_container_width
        except:
            st.image("https://www.heart.org/-/media/Images/Health-Topics/Heart-Disease/HeartDiseaseContentImage.jpg", 
                   use_container_width=True, caption="Heart Health Indicators")  # Diubah ke use_container_width
    
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
    
    # Prediksi
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

# Jalankan aplikasi berdasarkan pilihan
if st.session_state.model_select == "Iris Species Classifier":
    iris_prediction()
elif st.session_state.model_select == "Heart Disease Predictor":
    heart_disease_prediction()
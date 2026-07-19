import streamlit as st
import pandas as pd
import joblib
import time


# Page Config 

st.set_page_config(page_title="PropTech Elite", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }

    /* Glassmorphism Containers */
    div[data-testid="stVerticalBlock"] > div:has(div.element-container) {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
    }

    /* Hide default Streamlit elements for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom Titles */
    .main-title {
        font-size: 3rem !important;
        font-weight: 800;
        background: linear-gradient(to right, #00dbde, #fc00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }

    /* Price Card */
    .price-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        border: 2px solid #00dbde;
        box-shadow: 0 0 20px rgba(0, 219, 222, 0.2);
        animation: fadeIn 1s ease-in;
    }

    /* Price per m² pill */
    .ppm-wrapper {
        margin-top: 18px;
        display: flex;
        justify-content: center;
    }

    .ppm-chip {
        padding: 10px 24px;
        border-radius: 999px;
        background: radial-gradient(circle at 0% 0%, rgba(0,219,222,0.3), rgba(252,0,255,0.15));
        border: 1px solid rgba(0,219,222,0.8);
        box-shadow: 0 0 18px rgba(0, 219, 222, 0.35);
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        gap: 2px;
        min-width: 230px;
    }

    .ppm-label {
        font-size: 0.7rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #9be8ff;
    }

    .ppm-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #00dbde, #fc00ff) !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        padding: 1rem !important;
        border-radius: 15px !important;
        transition: 0.3s all ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(252, 0, 255, 0.3);
    }
    
    /* Input Labels */
    label {
        color: #00dbde !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load Assets

@st.cache_resource
def load_all():
    
    try:
        m_sale = joblib.load("xgboost_sale_model.pkl")
        m_rent = joblib.load("linear_regression_rent_model.pkl")
        e_sale = joblib.load("encoders_sale.pkl")
        e_rent = joblib.load("encoders_rent.pkl")
        return m_sale, m_rent, e_sale, e_rent
    except:
        st.error("Model files not found. Please ensure .pkl files are in the directory.")
        return None, None, None, None

m_sale, m_rent, e_sale, e_rent = load_all()

@st.cache_data
def load_city_sector_map(market: str):
    csv_path = "cleaned_apartments_sale.csv" if market == "Sale" else "cleaned_apartments_rent.csv"
    df = pd.read_csv(csv_path)
    return (
        df.groupby("ville")["secteur"]
          .apply(lambda s: sorted(s.dropna().unique()))
          .to_dict()
    )


# Sidebar UI

with st.sidebar:
    st.markdown("<h2 style='color: #fc00ff;'>💎 PropTech Elite</h2>", unsafe_allow_html=True)
    property_type = st.segmented_control("Market Mode", ["Sale", "Rent"], default="Sale")
    
    st.markdown("---")
    st.markdown("### 📊 Market Context")
    st.write(f"Predicting prices for **{property_type}** listings.")
    st.progress(65 if property_type == "Sale" else 40)
    st.caption("Model Confidence: High")

# Assign model/encoder based on selection
model, encoders = (m_sale, e_sale) if property_type == "Sale" else (m_rent, e_rent)
city_sector_map = load_city_sector_map(property_type) if encoders else {}
ville_values = list(encoders["ville"].classes_) if encoders else []

# Main Layout

st.markdown("<h1 class='main-title'>AI Real Estate Valuation</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; margin-bottom: 40px;'>Professional Grade Property Appraisal using XGBoost & Linear Regressions</p>", unsafe_allow_html=True)

# Input Grid
col1, col2, col3 = st.columns([1.5, 1.5, 1], gap="medium")

with col1:
    st.markdown("#### 📍 Location")

    if encoders and ville_values:
        ville = st.selectbox("City", ville_values)
        available_sectors = city_sector_map.get(ville)
        if available_sectors:
            secteur_options = available_sectors
        else:
            secteur_options = list(encoders["secteur"].classes_)
        secteur = st.selectbox("Sector", secteur_options)
    else:
        ville = st.selectbox("City", ["Loading..."])
        secteur = st.selectbox("Sector", ["Loading..."])

    surface = st.number_input("Surface Area (m²)", 10, 1000, 120, step=5)

with col2:
    st.markdown("#### 📐 Specifications")
    chambres = st.slider("Bedrooms", 0, 10, 2)
    salledebain = st.slider("Bathrooms", 0, 10, 1)
    salons = st.slider("Living Rooms", 0, 10, 1)

with col3:
    st.markdown("#### 🏢 Building")
    etage = st.number_input("Floor Level", 0, 50, 2)
    st.write("")
    st.markdown(f"""
        <div style='background: rgba(0,219,222,0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #00dbde;'>
            <strong>Current Selection:</strong><br>
            {ville}<br>
            {surface} m²
        </div>
    """, unsafe_allow_html=True)


# Execution

st.markdown("<br>", unsafe_allow_html=True)
if st.button("GENERATE AI VALUATION"):
    with st.spinner("Analyzing market data points..."):
        time.sleep(1.2) # Adding a small delay 
        
        # Prepare Data
        input_data = pd.DataFrame({
            "ville": [ville], "chambres": [chambres], "salledebain": [salledebain],
            "secteur": [secteur], "salons": [salons], "etage": [etage], "surface": [surface]
        })

        # Encode & Predict
        input_data["ville"] = encoders["ville"].transform(input_data["ville"])
        input_data["secteur"] = encoders["secteur"].transform(input_data["secteur"])
        input_data = input_data[['ville', 'chambres', 'salledebain', 'secteur', 'salons', 'etage', 'surface']]
        
        prediction = model.predict(input_data)[0]
        formatted_price = f"{int(round(prediction)):,} MAD"

        # Big Result Display
        st.markdown(f"""
            <div class="price-container">
                <p style="color: #aaa; text-transform: uppercase; letter-spacing: 2px;">Estimated Market Value</p>
                <h1 style="font-size: 4rem; margin: 0; color: #fff;">{formatted_price}</h1>
                <p style="color: #00dbde;">Property Type: <strong>{property_type}</strong> | Location: <strong>{secteur}, {ville}</strong></p>
            </div>
        """, unsafe_allow_html=True)

        price_per_m2 = int(prediction / surface)

        #  price per m² pill
        st.markdown(f"""
            <div class="ppm-wrapper">
                <div class="ppm-chip">
                    <div class="ppm-label">Unit Price</div>
                    <div class="ppm-value">{price_per_m2:,} MAD / m²</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><p style='text-align: center; color: #555;'>PropTech Elite v2.0 • Powered by Advanced Machine Learning</p>", unsafe_allow_html=True)
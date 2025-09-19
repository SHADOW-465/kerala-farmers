import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from PIL import Image
import requests
import base64
import io

# Import custom modules
from modules.disease_detection import DiseaseDetection
from modules.crop_recommendation import CropRecommendation
from modules.ai_chatbot import AIChatbot
from modules.weather_analytics import WeatherAnalytics
from modules.farm_management import FarmManagement
from modules.market_prices import MarketPrices
from modules.soil_health import SoilHealthAssessment
from modules.government_schemes import GovernmentSchemes
from modules.community_platform import CommunityPlatform

# Page configuration
st.set_page_config(
    page_title="Kerala Farmers Hub",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dashboard styling
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Root variables */
    :root {
        --primary-color: #1A3636;
        --secondary-color: #224444;
        --accent-color: #2C5555;
        --text-primary: #FFFFFF;
        --text-secondary: #E0E0E0;
        --success-color: #4CAF50;
        --warning-color: #FF9800;
        --danger-color: #F44336;
        --gradient-primary: linear-gradient(135deg, #1A3636 0%, #224444 100%);
        --gradient-accent: linear-gradient(135deg, #2C5555 0%, #3A6666 100%);
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.15);
    }

    /* Global styles */
    .main {
        padding: 0 !important;
        background: linear-gradient(135deg, #0F1F1F 0%, #1A2A2A 100%);
        min-height: 100vh;
    }

    .stApp {
        background: linear-gradient(135deg, #0F1F1F 0%, #1A2A2A 100%);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: var(--gradient-primary) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    .css-1d391kg .css-1v0mbdj {
        color: var(--text-primary) !important;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Logo and branding */
    .logo {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 2rem;
        text-align: center;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }

    /* Navigation */
    .nav-section {
        margin-bottom: 2rem;
    }

    .nav-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }

    .nav-item {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: var(--text-primary);
        text-decoration: none;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }

    .nav-item:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(4px);
    }

    .nav-item.active {
        background: rgba(255, 255, 255, 0.15);
        border-left: 3px solid var(--success-color);
    }

    .nav-icon {
        margin-right: 0.75rem;
        font-size: 1.1rem;
    }

    /* User account section */
    .user-account {
        margin-top: auto;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .user-profile {
        display: flex;
        align-items: center;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: var(--success-color);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 0.75rem;
        color: white;
        font-weight: 600;
    }

    .user-info h4 {
        margin: 0;
        color: var(--text-primary);
        font-size: 0.9rem;
        font-weight: 600;
    }

    .user-info p {
        margin: 0;
        color: var(--text-secondary);
        font-size: 0.75rem;
    }

    /* Main content styling */
    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .page-title {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }

    .add-widget-btn {
        background: var(--gradient-accent);
        color: var(--text-primary);
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }

    .add-widget-btn:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    /* Metrics cards */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .metric-card {
        background: var(--gradient-accent);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }

    .metric-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        font-weight: 500;
    }

    .metric-value {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .metric-trend {
        display: flex;
        align-items: center;
        font-size: 1rem;
        color: var(--text-secondary);
    }

    .trend-up {
        color: var(--success-color);
    }

    .trend-down {
        color: var(--danger-color);
    }

    .trend-icon {
        margin-right: 0.25rem;
    }

    /* Charts and visualizations */
    .chart-container {
        background: var(--gradient-accent);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .chart-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }

    /* Community card */
    .community-card {
        background: linear-gradient(135deg, #2C5555 0%, #3A6666 100%);
        border-radius: 12px;
        padding: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-lg);
    }

    .community-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50 0L60 40L100 50L60 60L50 100L40 60L0 50L40 40Z" fill="rgba(255,255,255,0.1)"/></svg>') no-repeat;
        background-size: contain;
        opacity: 0.3;
    }

    .community-content {
        position: relative;
        z-index: 1;
    }

    .community-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }

    .community-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
    }

    .community-stats {
        display: flex;
        align-items: center;
        color: var(--text-primary);
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    .community-badges {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .badge {
        background: rgba(255, 255, 255, 0.2);
        color: var(--text-primary);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .metrics-grid {
            grid-template-columns: 1fr;
        }
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# Load CSS
load_css()

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

def render_dashboard():
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">Dashboard</h1>
        <button class="add-widget-btn">Add Custom Widget</button>
    </div>
    """, unsafe_allow_html=True)

    # Metrics Grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Crop Health Index</div>
            <div class="metric-value">85.2%</div>
            <div class="metric-trend trend-up">
                <span class="trend-icon">↗</span>
                3.2% than last month
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Soil Quality Score</div>
            <div class="metric-value">78.5/100</div>
            <div class="metric-trend trend-down">
                <span class="trend-icon">↘</span>
                1.4% than last month
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Market Revenue</div>
            <div class="metric-value">₹2,45,670</div>
            <div class="metric-trend trend-up">
                <span class="trend-icon">↗</span>
                5.1% than last month
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container():
            st.markdown("""
            <div class="chart-container">
                <div class="chart-title">Crop Yield Progress</div>
            </div>
            """, unsafe_allow_html=True)
            # Placeholder for chart
            chart_data = pd.DataFrame(
                np.random.randn(20, 3),
                columns=['Rice', 'Wheat', 'Coconut'])
            st.line_chart(chart_data)

    with col2:
        with st.container():
            st.markdown("""
            <div class="chart-container">
                <div class="chart-title">Weather Forecast</div>
            </div>
            """, unsafe_allow_html=True)
            weather_analytics = WeatherAnalytics()
            forecast_data = weather_analytics.get_weather_forecast("Kozhikode")
            daily_forecast = weather_analytics._process_forecast_data(forecast_data)
            weather_analytics._render_weather_chart(daily_forecast)

    with col3:
        with st.container():
            st.markdown("""
            <div class="chart-container">
                <div class="chart-title">Market Prices</div>
            </div>
            """, unsafe_allow_html=True)
            market_prices = MarketPrices()
            trend_df = market_prices.get_price_trends("Rice")
            fig = px.line(
                trend_df,
                x="date",
                y="price_per_kg",
                title="Rice Price Trend",
                markers=True
            )
            fig.update_layout(
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_color='white',
                xaxis_title="Date",
                yaxis_title="Price (₹/kg)"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        with st.container():
            st.markdown("""
            <div class="chart-container">
                <div class="chart-title">Disease Detection</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔬 Go to Disease Detection"):
                st.session_state.current_page = 'disease'
                st.rerun()

        with st.container():
            st.markdown("""
            <div class="chart-container">
                <div class="chart-title">Government Schemes</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🏛️ Find Government Schemes"):
                st.session_state.current_page = 'schemes'
                st.rerun()
    with col2:
        st.markdown("""
        <div class="community-card">
            <div class="community-content">
                <div class="community-title">🌾 Kerala Farmers Hub</div>
                <div class="community-text">Let's join our community</div>
                <div class="community-stats">
                    <span>👥 15k+ farmers</span>
                </div>
                <div class="community-badges">
                    <span class="badge">AI Assistant</span>
                    <span class="badge">Expert Network</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👥 Join Community"):
            st.session_state.current_page = 'community'
            st.rerun()

# Sidebar navigation
def render_sidebar():
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1A3636 0%, #224444 100%); border-radius: 12px; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0;">🌾 Kerala Farmers Hub</h2>
    </div>
    """, unsafe_allow_html=True)

    # Navigation menu
    st.sidebar.markdown("### Navigation")

    pages = {
        "📊 Dashboard": "dashboard",
        "🔬 Disease Detection": "disease",
        "🌱 Crop Recommendations": "crops",
        "🌤️ Weather Analytics": "weather",
        "🏡 Farm Management": "farm",
        "💰 Market Prices": "market",
        "🌱 Soil Health": "soil",
        "🏛️ Government Schemes": "schemes",
        "👥 Community": "community",
        "🤖 AI Assistant": "chatbot"
    }

    for page_name, page_key in pages.items():
        if st.sidebar.button(page_name, use_container_width=True):
            st.session_state.current_page = page_key
            st.rerun()

    # User account section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### User Account")
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">
        <div style="width: 40px; height: 40px; border-radius: 50%; background: #4CAF50; display: flex; align-items: center; justify-content: center; margin-right: 10px; color: white; font-weight: bold;">👤</div>
        <div>
            <div style="color: white; font-weight: bold;">Alex Williamson</div>
            <div style="color: #B0B0B0; font-size: 0.8rem;">#farmer-1974</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content area
def render_main_content():
    # Page routing
    if st.session_state.current_page == 'dashboard':
        render_dashboard()
    elif st.session_state.current_page == 'disease':
        disease_detector = DiseaseDetection()
        disease_detector.render_disease_detection_ui()
    elif st.session_state.current_page == 'crops':
        crop_recommender = CropRecommendation()
        crop_recommender.render_crop_recommendation_ui()
    elif st.session_state.current_page == 'weather':
        weather_analytics = WeatherAnalytics()
        weather_analytics.render_weather_dashboard()
    elif st.session_state.current_page == 'farm':
        farm_manager = FarmManagement()
        farm_manager.render_farm_dashboard()
    elif st.session_state.current_page == 'market':
        market_prices = MarketPrices()
        market_prices.render_market_dashboard()
    elif st.session_state.current_page == 'soil':
        soil_health = SoilHealthAssessment()
        soil_health.render_soil_health_ui()
    elif st.session_state.current_page == 'schemes':
        government_schemes = GovernmentSchemes()
        government_schemes.render_schemes_dashboard()
    elif st.session_state.current_page == 'community':
        community_platform = CommunityPlatform()
        community_platform.render_community_dashboard()
    elif st.session_state.current_page == 'chatbot':
        ai_chatbot = AIChatbot()
        ai_chatbot.render_chatbot_ui()

# Main app
def main():
    render_sidebar()
    render_main_content()

if __name__ == "__main__":
    main()

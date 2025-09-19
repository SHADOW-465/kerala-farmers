import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

class CropRecommendation:
    def __init__(self):
        self.kerala_crops = {
            "Rice": {
                "seasons": ["Kharif", "Rabi"],
                "soil_types": ["Clay", "Loam", "Sandy Loam"],
                "ph_range": [5.5, 7.0],
                "rainfall_min": 1000,
                "temperature_range": [20, 35],
                "market_demand": "High",
                "profitability": "Medium"
            },
            "Coconut": {
                "seasons": ["Year-round"],
                "soil_types": ["Sandy", "Sandy Loam", "Red Soil"],
                "ph_range": [5.0, 8.0],
                "rainfall_min": 1200,
                "temperature_range": [20, 32],
                "market_demand": "High",
                "profitability": "High"
            },
            "Black Pepper": {
                "seasons": ["Year-round"],
                "soil_types": ["Red Soil", "Laterite"],
                "ph_range": [5.5, 6.5],
                "rainfall_min": 1500,
                "temperature_range": [20, 30],
                "market_demand": "Very High",
                "profitability": "Very High"
            },
            "Cardamom": {
                "seasons": ["Year-round"],
                "soil_types": ["Forest Soil", "Red Soil"],
                "ph_range": [5.0, 6.5],
                "rainfall_min": 2000,
                "temperature_range": [15, 25],
                "market_demand": "High",
                "profitability": "High"
            },
            "Rubber": {
                "seasons": ["Year-round"],
                "soil_types": ["Red Soil", "Laterite"],
                "ph_range": [4.5, 6.5],
                "rainfall_min": 1800,
                "temperature_range": [20, 35],
                "market_demand": "Medium",
                "profitability": "Medium"
            },
            "Cashew": {
                "seasons": ["Year-round"],
                "soil_types": ["Sandy", "Sandy Loam"],
                "ph_range": [5.5, 7.0],
                "rainfall_min": 800,
                "temperature_range": [20, 35],
                "market_demand": "High",
                "profitability": "High"
            },
            "Banana": {
                "seasons": ["Year-round"],
                "soil_types": ["Clay", "Loam", "Sandy Loam"],
                "ph_range": [6.0, 7.5],
                "rainfall_min": 1000,
                "temperature_range": [20, 35],
                "market_demand": "High",
                "profitability": "Medium"
            },
            "Tapioca": {
                "seasons": ["Kharif", "Rabi"],
                "soil_types": ["Sandy", "Sandy Loam", "Red Soil"],
                "ph_range": [5.0, 7.0],
                "rainfall_min": 600,
                "temperature_range": [20, 35],
                "market_demand": "Medium",
                "profitability": "Medium"
            },
            "Ginger": {
                "seasons": ["Kharif"],
                "soil_types": ["Loam", "Sandy Loam"],
                "ph_range": [6.0, 7.0],
                "rainfall_min": 1000,
                "temperature_range": [20, 30],
                "market_demand": "High",
                "profitability": "High"
            },
            "Turmeric": {
                "seasons": ["Kharif"],
                "soil_types": ["Loam", "Sandy Loam", "Red Soil"],
                "ph_range": [6.0, 7.5],
                "rainfall_min": 1000,
                "temperature_range": [20, 30],
                "market_demand": "High",
                "profitability": "High"
            }
        }
    
    def calculate_crop_suitability(self, soil_ph, soil_type, rainfall, temperature, season, location):
        """
        Calculate suitability score for each crop based on input parameters
        """
        recommendations = []
        
        for crop_name, crop_data in self.kerala_crops.items():
            score = 0
            factors = []
            
            # pH suitability (40% weight)
            ph_min, ph_max = crop_data["ph_range"]
            if ph_min <= soil_ph <= ph_max:
                ph_score = 100
            else:
                ph_score = max(0, 100 - abs(soil_ph - (ph_min + ph_max) / 2) * 20)
            score += ph_score * 0.4
            factors.append(f"pH: {ph_score:.0f}%")
            
            # Soil type suitability (20% weight)
            if soil_type in crop_data["soil_types"]:
                soil_score = 100
            else:
                soil_score = 60  # Partial match
            score += soil_score * 0.2
            factors.append(f"Soil: {soil_score:.0f}%")
            
            # Rainfall suitability (20% weight)
            if rainfall >= crop_data["rainfall_min"]:
                rain_score = 100
            else:
                rain_score = max(0, (rainfall / crop_data["rainfall_min"]) * 100)
            score += rain_score * 0.2
            factors.append(f"Rainfall: {rain_score:.0f}%")
            
            # Temperature suitability (10% weight)
            temp_min, temp_max = crop_data["temperature_range"]
            if temp_min <= temperature <= temp_max:
                temp_score = 100
            else:
                temp_score = max(0, 100 - abs(temperature - (temp_min + temp_max) / 2) * 5)
            score += temp_score * 0.1
            factors.append(f"Temperature: {temp_score:.0f}%")
            
            # Season suitability (10% weight)
            if season in crop_data["seasons"] or "Year-round" in crop_data["seasons"]:
                season_score = 100
            else:
                season_score = 50
            score += season_score * 0.1
            factors.append(f"Season: {season_score:.0f}%")
            
            recommendations.append({
                "crop": crop_name,
                "score": round(score, 1),
                "factors": factors,
                "market_demand": crop_data["market_demand"],
                "profitability": crop_data["profitability"],
                "seasons": crop_data["seasons"],
                "soil_types": crop_data["soil_types"]
            })
        
        # Sort by score (descending)
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations
    
    def render_crop_recommendation_ui(self):
        """
        Render the crop recommendation UI
        """
        st.markdown("""
        <div class="chart-container">
            <div class="chart-title">🌱 Smart Crop Recommendation</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Input form
        with st.form("crop_recommendation_form"):
            st.markdown("### 📋 Farm Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                soil_ph = st.slider("Soil pH Level", 4.0, 8.0, 6.5, 0.1)
                soil_type = st.selectbox(
                    "Soil Type",
                    ["Clay", "Loam", "Sandy Loam", "Sandy", "Red Soil", "Laterite", "Forest Soil"]
                )
                rainfall = st.number_input("Annual Rainfall (mm)", 500, 3000, 1500)
            
            with col2:
                temperature = st.number_input("Average Temperature (°C)", 15, 40, 28)
                season = st.selectbox(
                    "Planting Season",
                    ["Kharif", "Rabi", "Year-round"]
                )
                location = st.selectbox(
                    "Location in Kerala",
                    ["Coastal Kerala", "Midland Kerala", "Highland Kerala"]
                )
            
            submitted = st.form_submit_button("🌱 Get Recommendations", type="primary")
            
            if submitted:
                with st.spinner("Analyzing conditions and generating recommendations..."):
                    recommendations = self.calculate_crop_suitability(
                        soil_ph, soil_type, rainfall, temperature, season, location
                    )
                
                # Display top recommendations
                st.markdown("### 🏆 Top Crop Recommendations")
                
                for i, rec in enumerate(recommendations[:5]):
                    with st.expander(f"{i+1}. {rec['crop']} - {rec['score']:.1f}% Suitability", expanded=i<3):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Suitability Score", f"{rec['score']:.1f}%")
                            st.metric("Market Demand", rec['market_demand'])
                        
                        with col2:
                            st.metric("Profitability", rec['profitability'])
                            st.metric("Best Seasons", ", ".join(rec['seasons']))
                        
                        with col3:
                            st.metric("Soil Types", ", ".join(rec['soil_types']))
                        
                        # Suitability factors
                        st.markdown("**Suitability Breakdown:**")
                        for factor in rec['factors']:
                            st.markdown(f"• {factor}")
                        
                        # Additional recommendations
                        if rec['score'] > 80:
                            st.success("✅ Excellent choice for your farm conditions!")
                        elif rec['score'] > 60:
                            st.warning("⚠️ Good choice with some considerations needed.")
                        else:
                            st.info("ℹ️ Consider improving farm conditions for better results.")
                
                # Visualization
                self._render_recommendation_chart(recommendations[:10])
                
                # Seasonal calendar
                self._render_seasonal_calendar()
    
    def _render_recommendation_chart(self, recommendations):
        """
        Render a chart showing crop recommendations
        """
        st.markdown("### 📊 Suitability Comparison")
        
        df = pd.DataFrame(recommendations)
        
        fig = px.bar(
            df, 
            x='score', 
            y='crop',
            orientation='h',
            color='score',
            color_continuous_scale='RdYlGn',
            title="Crop Suitability Scores"
        )
        
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            xaxis_title="Suitability Score (%)",
            yaxis_title="Crop"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_seasonal_calendar(self):
        """
        Render seasonal planting calendar
        """
        st.markdown("### 📅 Kerala Crop Calendar")
        
        calendar_data = {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "Kharif Crops": ["Rice", "Rice", "Rice", "Rice", "Rice", "Rice", "Rice", "Rice", "Rice", "Rice", "Rice", "Rice"],
            "Rabi Crops": ["Wheat", "Wheat", "Wheat", "Wheat", "Wheat", "Wheat", "Wheat", "Wheat", "Wheat", "Wheat", "Wheat", "Wheat"],
            "Year-round": ["Coconut", "Coconut", "Coconut", "Coconut", "Coconut", "Coconut", "Coconut", "Coconut", "Coconut", "Coconut", "Coconut", "Coconut"]
        }
        
        df_calendar = pd.DataFrame(calendar_data)
        
        fig = px.imshow(
            df_calendar.set_index('Month').T,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            title="Monthly Crop Planting Guide"
        )
        
        st.plotly_chart(fig, use_container_width=True)

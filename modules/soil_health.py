import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

class SoilHealthAssessment:
    def __init__(self):
        self.nutrient_ranges = {
            "pH": {"optimal": (6.0, 7.5), "acceptable": (5.5, 8.0)},
            "Nitrogen": {"optimal": (20, 40), "acceptable": (15, 50)},
            "Phosphorus": {"optimal": (15, 30), "acceptable": (10, 40)},
            "Potassium": {"optimal": (150, 250), "acceptable": (100, 300)},
            "Organic Matter": {"optimal": (3.0, 5.0), "acceptable": (2.0, 6.0)},
            "Calcium": {"optimal": (2000, 4000), "acceptable": (1500, 5000)},
            "Magnesium": {"optimal": (200, 400), "acceptable": (150, 500)},
            "Sulfur": {"optimal": (10, 20), "acceptable": (8, 25)}
        }
        
        self.soil_types = [
            "Clay", "Loam", "Sandy Loam", "Sandy", "Red Soil", 
            "Laterite", "Forest Soil", "Alluvial", "Black Soil"
        ]
        
        self.crop_requirements = {
            "Rice": {
                "pH": (5.5, 7.0),
                "Nitrogen": (25, 35),
                "Phosphorus": (20, 30),
                "Potassium": (200, 300)
            },
            "Coconut": {
                "pH": (5.0, 8.0),
                "Nitrogen": (15, 25),
                "Phosphorus": (10, 20),
                "Potassium": (100, 200)
            },
            "Black Pepper": {
                "pH": (5.5, 6.5),
                "Nitrogen": (20, 30),
                "Phosphorus": (15, 25),
                "Potassium": (150, 250)
            },
            "Cardamom": {
                "pH": (5.0, 6.5),
                "Nitrogen": (25, 35),
                "Phosphorus": (20, 30),
                "Potassium": (200, 300)
            },
            "Rubber": {
                "pH": (4.5, 6.5),
                "Nitrogen": (20, 30),
                "Phosphorus": (15, 25),
                "Potassium": (150, 250)
            }
        }
    
    def assess_soil_health(self, soil_data):
        """
        Assess soil health based on test results
        """
        assessment = {
            "overall_score": 0,
            "nutrient_scores": {},
            "recommendations": [],
            "crop_suitability": {}
        }
        
        total_score = 0
        nutrient_count = 0
        
        # Assess each nutrient
        for nutrient, value in soil_data.items():
            if nutrient in self.nutrient_ranges and value is not None:
                optimal_range = self.nutrient_ranges[nutrient]["optimal"]
                acceptable_range = self.nutrient_ranges[nutrient]["acceptable"]
                
                if optimal_range[0] <= value <= optimal_range[1]:
                    score = 100
                    status = "Optimal"
                elif acceptable_range[0] <= value <= acceptable_range[1]:
                    score = 70
                    status = "Acceptable"
                else:
                    score = 30
                    status = "Deficient" if value < acceptable_range[0] else "Excessive"
                
                assessment["nutrient_scores"][nutrient] = {
                    "score": score,
                    "status": status,
                    "value": value
                }
                
                total_score += score
                nutrient_count += 1
                
                # Add recommendations
                if score < 70:
                    if value < acceptable_range[0]:
                        assessment["recommendations"].append(
                            f"Add {nutrient} - Current: {value}, Target: {optimal_range[0]}-{optimal_range[1]}"
                        )
                    else:
                        assessment["recommendations"].append(
                            f"Reduce {nutrient} - Current: {value}, Target: {optimal_range[0]}-{optimal_range[1]}"
                        )
        
        # Calculate overall score
        if nutrient_count > 0:
            assessment["overall_score"] = total_score / nutrient_count
        
        # Assess crop suitability
        for crop, requirements in self.crop_requirements.items():
            crop_score = 0
            crop_nutrients = 0
            
            for nutrient, value in soil_data.items():
                if nutrient in requirements and value is not None:
                    req_range = requirements[nutrient]
                    if req_range[0] <= value <= req_range[1]:
                        crop_score += 100
                    else:
                        # Calculate how far from optimal
                        if value < req_range[0]:
                            crop_score += max(0, (value / req_range[0]) * 100)
                        else:
                            crop_score += max(0, (req_range[1] / value) * 100)
                    crop_nutrients += 1
            
            if crop_nutrients > 0:
                assessment["crop_suitability"][crop] = crop_score / crop_nutrients
        
        return assessment
    
    def get_fertilizer_recommendations(self, soil_data, crop=None):
        """
        Get fertilizer recommendations based on soil test results
        """
        recommendations = []
        
        # Nitrogen recommendations
        if soil_data.get("Nitrogen", 0) < 20:
            n_deficit = 20 - soil_data.get("Nitrogen", 0)
            recommendations.append({
                "nutrient": "Nitrogen",
                "fertilizer": "Urea (46-0-0)",
                "amount_kg_per_acre": round(n_deficit * 0.5, 1),
                "application": "Split application - 50% at planting, 50% at tillering"
            })
        
        # Phosphorus recommendations
        if soil_data.get("Phosphorus", 0) < 15:
            p_deficit = 15 - soil_data.get("Phosphorus", 0)
            recommendations.append({
                "nutrient": "Phosphorus",
                "fertilizer": "DAP (18-46-0) or SSP (0-16-0)",
                "amount_kg_per_acre": round(p_deficit * 0.8, 1),
                "application": "Apply at planting time, mix with soil"
            })
        
        # Potassium recommendations
        if soil_data.get("Potassium", 0) < 150:
            k_deficit = 150 - soil_data.get("Potassium", 0)
            recommendations.append({
                "nutrient": "Potassium",
                "fertilizer": "MOP (0-0-60) or SOP (0-0-50)",
                "amount_kg_per_acre": round(k_deficit * 0.3, 1),
                "application": "Apply before planting, mix with soil"
            })
        
        # Organic matter recommendations
        if soil_data.get("Organic Matter", 0) < 3.0:
            recommendations.append({
                "nutrient": "Organic Matter",
                "fertilizer": "Farmyard Manure or Compost",
                "amount_kg_per_acre": 5000,
                "application": "Apply 2-3 months before planting, mix with soil"
            })
        
        # pH adjustment
        if soil_data.get("pH", 7) < 6.0:
            recommendations.append({
                "nutrient": "pH",
                "fertilizer": "Lime (Calcium Carbonate)",
                "amount_kg_per_acre": round((6.5 - soil_data.get("pH", 7)) * 1000, 1),
                "application": "Apply 2-3 months before planting, mix with soil"
            })
        elif soil_data.get("pH", 7) > 7.5:
            recommendations.append({
                "nutrient": "pH",
                "fertilizer": "Sulfur or Gypsum",
                "amount_kg_per_acre": round((soil_data.get("pH", 7) - 7.0) * 500, 1),
                "application": "Apply 2-3 months before planting, mix with soil"
            })
        
        return recommendations
    
    def render_soil_health_ui(self):
        """
        Render the soil health assessment UI
        """
        st.markdown("""
        <div class="chart-container">
            <div class="chart-title">🌱 Soil Health Assessment</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Soil test input form
        with st.form("soil_test_form"):
            st.markdown("### 📋 Soil Test Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Basic Properties**")
                ph = st.number_input("pH Level", 4.0, 9.0, 6.5, 0.1)
                organic_matter = st.number_input("Organic Matter (%)", 0.0, 10.0, 3.0, 0.1)
                soil_type = st.selectbox("Soil Type", self.soil_types)
            
            with col2:
                st.markdown("**Nutrient Levels (ppm)**")
                nitrogen = st.number_input("Nitrogen (N)", 0, 100, 25)
                phosphorus = st.number_input("Phosphorus (P)", 0, 100, 20)
                potassium = st.number_input("Potassium (K)", 0, 500, 200)
            
            col3, col4 = st.columns(2)
            
            with col3:
                calcium = st.number_input("Calcium (Ca)", 0, 10000, 3000)
                magnesium = st.number_input("Magnesium (Mg)", 0, 1000, 300)
            
            with col4:
                sulfur = st.number_input("Sulfur (S)", 0, 50, 15)
                crop_selection = st.selectbox("Target Crop", ["None"] + list(self.crop_requirements.keys()))
            
            submitted = st.form_submit_button("🔍 Assess Soil Health", type="primary")
            
            if submitted:
                # Prepare soil data
                soil_data = {
                    "pH": ph,
                    "Nitrogen": nitrogen,
                    "Phosphorus": phosphorus,
                    "Potassium": potassium,
                    "Organic Matter": organic_matter,
                    "Calcium": calcium,
                    "Magnesium": magnesium,
                    "Sulfur": sulfur
                }
                
                # Assess soil health
                assessment = self.assess_soil_health(soil_data)
                
                # Display results
                self._display_assessment_results(assessment, soil_data, crop_selection)
    
    def _display_assessment_results(self, assessment, soil_data, crop_selection):
        """
        Display soil health assessment results
        """
        # Overall score
        st.markdown("### 📊 Soil Health Score")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            score = assessment["overall_score"]
            if score >= 80:
                st.success(f"🟢 Excellent: {score:.1f}%")
            elif score >= 60:
                st.warning(f"🟡 Good: {score:.1f}%")
            else:
                st.error(f"🔴 Needs Improvement: {score:.1f}%")
        
        with col2:
            st.metric("Overall Score", f"{score:.1f}%")
        
        with col3:
            st.metric("Nutrients Tested", len(assessment["nutrient_scores"]))
        
        # Nutrient breakdown
        st.markdown("### 🌿 Nutrient Analysis")
        
        nutrient_df = pd.DataFrame([
            {
                "Nutrient": nutrient,
                "Value": data["value"],
                "Score": data["score"],
                "Status": data["status"]
            }
            for nutrient, data in assessment["nutrient_scores"].items()
        ])
        
        # Display nutrient table
        for _, row in nutrient_df.iterrows():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.markdown(row["Nutrient"])
            
            with col2:
                st.markdown(f"{row['Value']}")
            
            with col3:
                st.markdown(f"{row['Score']:.0f}%")
            
            with col4:
                if row["Status"] == "Optimal":
                    st.success("✅ Optimal")
                elif row["Status"] == "Acceptable":
                    st.warning("⚠️ Acceptable")
                else:
                    st.error("❌ Deficient/Excessive")
        
        # Visual representation
        self._render_nutrient_chart(nutrient_df)
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        
        if assessment["recommendations"]:
            for rec in assessment["recommendations"]:
                st.info(rec)
        else:
            st.success("✅ All nutrients are within optimal ranges!")
        
        # Fertilizer recommendations
        st.markdown("### 🧪 Fertilizer Recommendations")
        
        fertilizer_recs = self.get_fertilizer_recommendations(soil_data, crop_selection)
        
        if fertilizer_recs:
            for rec in fertilizer_recs:
                with st.expander(f"{rec['nutrient']} - {rec['fertilizer']}", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Amount:** {rec['amount_kg_per_acre']} kg/acre")
                    
                    with col2:
                        st.markdown(f"**Application:** {rec['application']}")
        else:
            st.success("✅ No additional fertilizers needed!")
        
        # Crop suitability
        if crop_selection != "None":
            st.markdown("### 🌾 Crop Suitability")
            
            crop_score = assessment["crop_suitability"].get(crop_selection, 0)
            
            if crop_score >= 80:
                st.success(f"✅ {crop_selection} is highly suitable for your soil (Score: {crop_score:.1f}%)")
            elif crop_score >= 60:
                st.warning(f"⚠️ {crop_selection} is moderately suitable for your soil (Score: {crop_score:.1f}%)")
            else:
                st.error(f"❌ {crop_selection} is not suitable for your soil (Score: {crop_score:.1f}%)")
        
        # General crop suitability
        st.markdown("### 🌱 Best Crops for Your Soil")
        
        suitable_crops = sorted(
            assessment["crop_suitability"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for crop, score in suitable_crops[:5]:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(crop)
            
            with col2:
                if score >= 80:
                    st.success(f"{score:.1f}%")
                elif score >= 60:
                    st.warning(f"{score:.1f}%")
                else:
                    st.error(f"{score:.1f}%")
    
    def _render_nutrient_chart(self, nutrient_df):
        """
        Render nutrient analysis chart
        """
        fig = px.bar(
            nutrient_df,
            x="Nutrient",
            y="Score",
            color="Score",
            color_continuous_scale=["red", "yellow", "green"],
            title="Nutrient Health Scores"
        )
        
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            xaxis_title="Nutrient",
            yaxis_title="Health Score (%)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_soil_test_guide(self):
        """
        Render soil testing guide
        """
        st.markdown("### 📖 How to Test Your Soil")
        
        st.markdown("""
        **Step 1: Sample Collection**
        - Collect soil samples from 10-15 different spots in your field
        - Take samples from 0-6 inches depth
        - Mix all samples thoroughly in a clean container
        
        **Step 2: Sample Preparation**
        - Remove stones, roots, and debris
        - Air dry the sample for 2-3 days
        - Crush and sieve through 2mm mesh
        
        **Step 3: Laboratory Testing**
        - Send sample to nearest soil testing laboratory
        - Request analysis for pH, NPK, organic matter, and micronutrients
        - Results usually available in 7-10 days
        
        **Step 4: Interpretation**
        - Use this tool to interpret your results
        - Get personalized recommendations
        - Plan your fertilizer application
        """)
        
        st.info("💡 **Tip**: Test your soil every 2-3 years or when changing crops for best results.")

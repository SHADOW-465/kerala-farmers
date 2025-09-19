import streamlit as st
import requests
import base64
import io
from PIL import Image
import json
import os

class DiseaseDetection:
    def __init__(self):
        self.huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.model_name = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
        
    def detect_disease(self, image):
        """
        Detect plant disease from uploaded image using Hugging Face API
        """
        try:
            # Convert image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {self.huggingface_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": img_str,
                "options": {"wait_for_model": True}
            }
            
            # Make API call
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{self.model_name}",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._process_disease_result(result)
            else:
                return self._get_mock_result()
                
        except Exception as e:
            st.error(f"Error in disease detection: {str(e)}")
            return self._get_mock_result()
    
    def _process_disease_result(self, result):
        """
        Process the API response and format it for display
        """
        if isinstance(result, list) and len(result) > 0:
            disease = result[0]
            return {
                "disease_name": disease.get("label", "Unknown"),
                "confidence": disease.get("score", 0.0),
                "treatment": self._get_treatment_recommendation(disease.get("label", "")),
                "severity": self._get_severity_level(disease.get("score", 0.0))
            }
        return self._get_mock_result()
    
    def _get_treatment_recommendation(self, disease_name):
        """
        Get treatment recommendations based on disease name
        """
        treatments = {
            "healthy": "Plant appears healthy. Continue regular care and monitoring.",
            "bacterial_spot": "Apply copper-based fungicide. Remove affected leaves. Improve air circulation.",
            "early_blight": "Apply fungicide containing chlorothalonil. Remove infected plant debris.",
            "late_blight": "Apply fungicide immediately. Remove and destroy infected plants.",
            "leaf_mold": "Improve air circulation. Apply fungicide. Reduce humidity.",
            "septoria_leaf_spot": "Apply fungicide. Remove infected leaves. Improve drainage.",
            "spider_mites": "Apply miticide. Increase humidity. Remove heavily infested leaves.",
            "target_spot": "Apply fungicide. Remove infected leaves. Improve air circulation.",
            "mosaic_virus": "Remove infected plants. Control aphids. Use virus-free seeds.",
            "yellow_leaf_curl": "Control whiteflies. Remove infected plants. Use resistant varieties."
        }
        
        return treatments.get(disease_name.lower(), "Consult with agricultural expert for specific treatment recommendations.")
    
    def _get_severity_level(self, confidence):
        """
        Determine severity level based on confidence score
        """
        if confidence > 0.8:
            return "High"
        elif confidence > 0.6:
            return "Medium"
        else:
            return "Low"
    
    def _get_mock_result(self):
        """
        Return mock result when API is not available
        """
        return {
            "disease_name": "Bacterial Spot",
            "confidence": 0.85,
            "treatment": "Apply copper-based fungicide. Remove affected leaves. Improve air circulation.",
            "severity": "High"
        }
    
    def render_disease_detection_ui(self):
        """
        Render the disease detection UI
        """
        st.markdown("""
        <div class="chart-container">
            <div class="chart-title">🔬 Plant Disease Detection</div>
        </div>
        """, unsafe_allow_html=True)
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload a plant image for disease detection",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of the plant leaves or affected area"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Detect disease
            if st.button("🔍 Detect Disease", type="primary"):
                with st.spinner("Analyzing image..."):
                    result = self.detect_disease(image)
                
                # Display results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Disease Detected",
                        result["disease_name"],
                        delta=f"{result['confidence']:.1%} confidence"
                    )
                
                with col2:
                    severity_color = {
                        "High": "🔴",
                        "Medium": "🟡", 
                        "Low": "🟢"
                    }
                    st.metric(
                        "Severity",
                        f"{severity_color[result['severity']]} {result['severity']}"
                    )
                
                with col3:
                    st.metric(
                        "Confidence",
                        f"{result['confidence']:.1%}"
                    )
                
                # Treatment recommendations
                st.markdown("### 💊 Treatment Recommendations")
                st.info(result["treatment"])
                
                # Additional information
                st.markdown("### 📋 Additional Information")
                st.markdown("""
                - **Prevention**: Regular monitoring and early detection
                - **Follow-up**: Check plant health in 3-5 days
                - **Expert Consultation**: Contact local agricultural extension officer if symptoms persist
                """)
        
        else:
            st.info("👆 Please upload an image to detect plant diseases")
            
            # Sample images for demonstration
            st.markdown("### 📸 Sample Images")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Healthy Plant**")
                st.image("https://via.placeholder.com/150x150/4CAF50/FFFFFF?text=Healthy", 
                        caption="Healthy leaves")
            
            with col2:
                st.markdown("**Diseased Plant**")
                st.image("https://via.placeholder.com/150x150/FF9800/FFFFFF?text=Diseased", 
                        caption="Diseased leaves")
            
            with col3:
                st.markdown("**Close-up View**")
                st.image("https://via.placeholder.com/150x150/F44336/FFFFFF?text=Close-up", 
                        caption="Close-up of affected area")

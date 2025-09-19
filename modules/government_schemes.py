import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

class GovernmentSchemes:
    def __init__(self):
        self.schemes = [
            {
                "id": 1,
                "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
                "description": "Direct income support of ₹6,000 per year to all landholding farmer families",
                "eligibility": [
                    "Landholding farmers",
                    "Small and marginal farmers",
                    "All categories of farmers"
                ],
                "benefits": [
                    "₹6,000 per year in three installments",
                    "Direct bank transfer",
                    "No middlemen involved"
                ],
                "documents_required": [
                    "Aadhaar card",
                    "Land records",
                    "Bank account details",
                    "Mobile number"
                ],
                "application_process": [
                    "Visit PM-KISAN portal",
                    "Register with Aadhaar",
                    "Upload land records",
                    "Link bank account"
                ],
                "status": "Active",
                "deadline": "Ongoing",
                "category": "Income Support"
            },
            {
                "id": 2,
                "name": "Soil Health Card Scheme",
                "description": "Free soil testing and recommendations for farmers",
                "eligibility": [
                    "All farmers",
                    "Landholding farmers",
                    "Small and marginal farmers"
                ],
                "benefits": [
                    "Free soil testing",
                    "Soil health card",
                    "Fertilizer recommendations",
                    "Crop-specific advice"
                ],
                "documents_required": [
                    "Aadhaar card",
                    "Land records",
                    "Mobile number"
                ],
                "application_process": [
                    "Visit nearest soil testing lab",
                    "Submit soil sample",
                    "Receive soil health card",
                    "Follow recommendations"
                ],
                "status": "Active",
                "deadline": "Ongoing",
                "category": "Soil Health"
            },
            {
                "id": 3,
                "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
                "description": "Crop insurance scheme for farmers",
                "eligibility": [
                    "All farmers growing notified crops",
                    "Landholding farmers",
                    "Tenant farmers"
                ],
                "benefits": [
                    "Crop insurance coverage",
                    "Premium subsidy",
                    "Quick claim settlement",
                    "Weather-based insurance"
                ],
                "documents_required": [
                    "Aadhaar card",
                    "Land records",
                    "Bank account details",
                    "Crop details"
                ],
                "application_process": [
                    "Visit insurance company",
                    "Fill application form",
                    "Pay premium",
                    "Receive policy document"
                ],
                "status": "Active",
                "deadline": "Before sowing season",
                "category": "Insurance"
            },
            {
                "id": 4,
                "name": "Kisan Credit Card (KCC)",
                "description": "Credit facility for farmers",
                "eligibility": [
                    "All farmers",
                    "Landholding farmers",
                    "Tenant farmers",
                    "Oral lessees"
                ],
                "benefits": [
                    "Credit up to ₹3 lakh",
                    "Low interest rate",
                    "Flexible repayment",
                    "Insurance coverage"
                ],
                "documents_required": [
                    "Aadhaar card",
                    "Land records",
                    "Income certificate",
                    "Bank account details"
                ],
                "application_process": [
                    "Visit nearest bank",
                    "Fill KCC application",
                    "Submit documents",
                    "Get credit card"
                ],
                "status": "Active",
                "deadline": "Ongoing",
                "category": "Credit"
            },
            {
                "id": 5,
                "name": "Pradhan Mantri Kisan Sampada Yojana",
                "description": "Scheme for food processing and value addition",
                "eligibility": [
                    "Food processing units",
                    "Farmer producer organizations",
                    "Self-help groups",
                    "Cooperatives"
                ],
                "benefits": [
                    "Capital investment subsidy",
                    "Technology upgradation",
                    "Market linkage",
                    "Skill development"
                ],
                "documents_required": [
                    "Project proposal",
                    "Financial statements",
                    "Land documents",
                    "Technical details"
                ],
                "application_process": [
                    "Prepare project proposal",
                    "Submit to ministry",
                    "Get approval",
                    "Implement project"
                ],
                "status": "Active",
                "deadline": "31st March 2024",
                "category": "Food Processing"
            },
            {
                "id": 6,
                "name": "Kerala State Agricultural Development Project",
                "description": "State-specific agricultural development scheme",
                "eligibility": [
                    "Kerala farmers",
                    "Landholding farmers",
                    "Small and marginal farmers"
                ],
                "benefits": [
                    "Subsidy for inputs",
                    "Technology support",
                    "Training programs",
                    "Market linkage"
                ],
                "documents_required": [
                    "Aadhaar card",
                    "Land records",
                    "Bank account details",
                    "Crop details"
                ],
                "application_process": [
                    "Visit agriculture office",
                    "Fill application form",
                    "Submit documents",
                    "Get approval"
                ],
                "status": "Active",
                "deadline": "Ongoing",
                "category": "State Scheme"
            }
        ]
        
        self.categories = list(set(scheme["category"] for scheme in self.schemes))
    
    def get_eligible_schemes(self, farmer_profile):
        """
        Get schemes eligible for a farmer based on their profile
        """
        eligible_schemes = []
        
        for scheme in self.schemes:
            eligibility_score = 0
            total_criteria = 0
            
            # Check landholding criteria
            if "landholding" in farmer_profile:
                if farmer_profile["landholding"] > 0:
                    eligibility_score += 1
                total_criteria += 1
            
            # Check farmer type
            if "farmer_type" in farmer_profile:
                if farmer_profile["farmer_type"] in ["Small", "Marginal", "All"]:
                    eligibility_score += 1
                total_criteria += 1
            
            # Check state
            if "state" in farmer_profile:
                if farmer_profile["state"] == "Kerala":
                    eligibility_score += 1
                total_criteria += 1
            
            # Check crop type
            if "crop_type" in farmer_profile:
                if farmer_profile["crop_type"] in ["Food Crops", "Cash Crops", "All"]:
                    eligibility_score += 1
                total_criteria += 1
            
            # Calculate eligibility percentage
            if total_criteria > 0:
                eligibility_percentage = (eligibility_score / total_criteria) * 100
                
                if eligibility_percentage >= 50:  # At least 50% match
                    scheme_copy = scheme.copy()
                    scheme_copy["eligibility_score"] = eligibility_percentage
                    eligible_schemes.append(scheme_copy)
        
        # Sort by eligibility score
        eligible_schemes.sort(key=lambda x: x["eligibility_score"], reverse=True)
        
        return eligible_schemes
    
    def render_schemes_dashboard(self):
        """
        Render the government schemes dashboard
        """
        st.markdown("""
        <div class="chart-container">
            <div class="chart-title">🏛️ Government Schemes Matcher</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Farmer profile form
        with st.form("farmer_profile_form"):
            st.markdown("### 👤 Farmer Profile")
            
            col1, col2 = st.columns(2)
            
            with col1:
                farmer_type = st.selectbox(
                    "Farmer Type",
                    ["Small", "Marginal", "Medium", "Large", "All"]
                )
                
                landholding = st.number_input(
                    "Landholding (acres)",
                    0.0, 100.0, 2.5, 0.1
                )
                
                state = st.selectbox(
                    "State",
                    ["Kerala", "Tamil Nadu", "Karnataka", "Other"]
                )
            
            with col2:
                crop_type = st.selectbox(
                    "Primary Crop Type",
                    ["Food Crops", "Cash Crops", "Horticulture", "All"]
                )
                
                annual_income = st.selectbox(
                    "Annual Income Range",
                    ["Below ₹1 lakh", "₹1-2 lakh", "₹2-5 lakh", "Above ₹5 lakh"]
                )
                
                has_bank_account = st.selectbox(
                    "Bank Account",
                    ["Yes", "No"]
                )
            
            submitted = st.form_submit_button("🔍 Find Eligible Schemes", type="primary")
            
            if submitted:
                # Create farmer profile
                farmer_profile = {
                    "farmer_type": farmer_type,
                    "landholding": landholding,
                    "state": state,
                    "crop_type": crop_type,
                    "annual_income": annual_income,
                    "has_bank_account": has_bank_account
                }
                
                # Get eligible schemes
                eligible_schemes = self.get_eligible_schemes(farmer_profile)
                
                # Display results
                self._display_eligible_schemes(eligible_schemes, farmer_profile)
        
        # Browse all schemes
        st.markdown("### 📋 Browse All Schemes")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            category_filter = st.selectbox(
                "Filter by Category",
                ["All Categories"] + self.categories
            )
        
        with col2:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Active", "Closed"]
            )
        
        # Display schemes
        filtered_schemes = self.schemes
        
        if category_filter != "All Categories":
            filtered_schemes = [s for s in filtered_schemes if s["category"] == category_filter]
        
        if status_filter != "All":
            filtered_schemes = [s for s in filtered_schemes if s["status"] == status_filter]
        
        for scheme in filtered_schemes:
            with st.expander(f"{scheme['name']} - {scheme['category']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description:** {scheme['description']}")
                    st.markdown(f"**Status:** {scheme['status']}")
                    st.markdown(f"**Deadline:** {scheme['deadline']}")
                
                with col2:
                    st.markdown(f"**Category:** {scheme['category']}")
                    if scheme['status'] == 'Active':
                        st.success("✅ Active")
                    else:
                        st.warning("⚠️ Closed")
                
                # Eligibility criteria
                st.markdown("**Eligibility Criteria:**")
                for criteria in scheme['eligibility']:
                    st.text(f"• {criteria}")
                
                # Benefits
                st.markdown("**Benefits:**")
                for benefit in scheme['benefits']:
                    st.text(f"• {benefit}")
                
                # Documents required
                st.markdown("**Documents Required:**")
                for doc in scheme['documents_required']:
                    st.text(f"• {doc}")
                
                # Application process
                st.markdown("**Application Process:**")
                for step in scheme['application_process']:
                    st.text(f"• {step}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"Apply Now", key=f"apply_{scheme['id']}"):
                        st.info("Application form would open here")
                
                with col2:
                    if st.button(f"Learn More", key=f"learn_{scheme['id']}"):
                        st.info("Detailed information would be shown here")
                
                with col3:
                    if st.button(f"Save", key=f"save_{scheme['id']}"):
                        st.success("Scheme saved to your list")
    
    def _display_eligible_schemes(self, eligible_schemes, farmer_profile):
        """
        Display eligible schemes for a farmer
        """
        st.markdown("### 🎯 Your Eligible Schemes")
        
        if not eligible_schemes:
            st.warning("No schemes found matching your profile. Try adjusting your criteria.")
            return
        
        # Display top 3 eligible schemes
        for i, scheme in enumerate(eligible_schemes[:3]):
            with st.expander(f"{i+1}. {scheme['name']} - {scheme['eligibility_score']:.0f}% Match", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description:** {scheme['description']}")
                    st.markdown(f"**Category:** {scheme['category']}")
                    st.markdown(f"**Status:** {scheme['status']}")
                
                with col2:
                    st.metric("Eligibility", f"{scheme['eligibility_score']:.0f}%")
                    if scheme['status'] == 'Active':
                        st.success("✅ Active")
                    else:
                        st.warning("⚠️ Closed")
                
                # Benefits
                st.markdown("**Key Benefits:**")
                for benefit in scheme['benefits'][:3]:  # Show first 3 benefits
                    st.text(f"• {benefit}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"Apply Now", key=f"apply_eligible_{scheme['id']}"):
                        st.info("Application form would open here")
                
                with col2:
                    if st.button(f"View Details", key=f"details_{scheme['id']}"):
                        st.info("Detailed information would be shown here")
                
                with col3:
                    if st.button(f"Save", key=f"save_eligible_{scheme['id']}"):
                        st.success("Scheme saved to your list")
        
        # Show all eligible schemes in a table
        if len(eligible_schemes) > 3:
            st.markdown("### 📊 All Eligible Schemes")
            
            df = pd.DataFrame([
                {
                    "Scheme Name": scheme["name"],
                    "Category": scheme["category"],
                    "Eligibility": f"{scheme['eligibility_score']:.0f}%",
                    "Status": scheme["status"],
                    "Deadline": scheme["deadline"]
                }
                for scheme in eligible_schemes
            ])
            
            st.dataframe(df, use_container_width=True)
    
    def render_application_tracker(self):
        """
        Render application tracking interface
        """
        st.markdown("### 📋 Application Tracker")
        
        # Sample application data
        applications = [
            {
                "scheme_name": "PM-KISAN",
                "application_id": "PMK001234",
                "applied_date": "2024-01-15",
                "status": "Under Review",
                "last_updated": "2024-01-20",
                "expected_decision": "2024-02-15"
            },
            {
                "scheme_name": "Soil Health Card",
                "application_id": "SHC005678",
                "applied_date": "2024-01-10",
                "status": "Approved",
                "last_updated": "2024-01-18",
                "expected_decision": "2024-01-25"
            }
        ]
        
        for app in applications:
            with st.expander(f"{app['scheme_name']} - {app['application_id']}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Status:** {app['status']}")
                    st.markdown(f"**Applied:** {app['applied_date']}")
                
                with col2:
                    st.markdown(f"**Last Updated:** {app['last_updated']}")
                    st.markdown(f"**Expected Decision:** {app['expected_decision']}")
                
                with col3:
                    if app['status'] == 'Approved':
                        st.success("✅ Approved")
                    elif app['status'] == 'Under Review':
                        st.warning("⏳ Under Review")
                    elif app['status'] == 'Rejected':
                        st.error("❌ Rejected")
                    else:
                        st.info("ℹ️ Pending")
                
                # Progress bar
                if app['status'] == 'Under Review':
                    progress = 0.6
                elif app['status'] == 'Approved':
                    progress = 1.0
                else:
                    progress = 0.3
                
                st.progress(progress)
                
                # Action buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"View Details", key=f"view_{app['application_id']}"):
                        st.info("Application details would be shown here")
                
                with col2:
                    if st.button(f"Download Certificate", key=f"download_{app['application_id']}"):
                        st.info("Certificate download would start here")

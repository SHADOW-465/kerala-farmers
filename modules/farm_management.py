import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

class FarmManagement:
    def __init__(self):
        self.farm_data = {
            "farms": [],
            "crops": [],
            "expenses": [],
            "harvests": []
        }
        self.load_sample_data()
    
    def load_sample_data(self):
        """
        Load sample farm data for demonstration
        """
        # Sample farms
        self.farm_data["farms"] = [
            {
                "id": 1,
                "name": "Green Valley Farm",
                "location": "Thrissur, Kerala",
                "area_acres": 5.2,
                "soil_type": "Loam",
                "established": "2020-01-15",
                "owner": "Alex Williamson"
            },
            {
                "id": 2,
                "name": "Coconut Grove",
                "location": "Kozhikode, Kerala", 
                "area_acres": 3.8,
                "soil_type": "Sandy Loam",
                "established": "2019-03-20",
                "owner": "Alex Williamson"
            }
        ]
        
        # Sample crops
        self.farm_data["crops"] = [
            {
                "id": 1,
                "farm_id": 1,
                "crop_name": "Rice",
                "variety": "Jyothi",
                "planting_date": "2024-01-15",
                "expected_harvest": "2024-04-15",
                "area_acres": 2.0,
                "status": "Growing",
                "yield_expected": 3000,
                "yield_actual": None
            },
            {
                "id": 2,
                "farm_id": 1,
                "crop_name": "Coconut",
                "variety": "West Coast Tall",
                "planting_date": "2020-01-15",
                "expected_harvest": "2024-12-31",
                "area_acres": 1.5,
                "status": "Mature",
                "yield_expected": 120,
                "yield_actual": 95
            },
            {
                "id": 3,
                "farm_id": 2,
                "crop_name": "Black Pepper",
                "variety": "Panniyur-1",
                "planting_date": "2023-06-01",
                "expected_harvest": "2024-12-31",
                "area_acres": 1.0,
                "status": "Growing",
                "yield_expected": 200,
                "yield_actual": None
            }
        ]
        
        # Sample expenses
        self.farm_data["expenses"] = [
            {
                "id": 1,
                "farm_id": 1,
                "date": "2024-01-10",
                "category": "Seeds",
                "description": "Rice seeds - Jyothi variety",
                "amount": 2500,
                "quantity": 50,
                "unit": "kg"
            },
            {
                "id": 2,
                "farm_id": 1,
                "date": "2024-01-15",
                "category": "Fertilizer",
                "description": "NPK 19:19:19",
                "amount": 1800,
                "quantity": 100,
                "unit": "kg"
            },
            {
                "id": 3,
                "farm_id": 1,
                "date": "2024-01-20",
                "category": "Labor",
                "description": "Land preparation and planting",
                "amount": 3500,
                "quantity": 5,
                "unit": "days"
            },
            {
                "id": 4,
                "farm_id": 2,
                "date": "2024-01-05",
                "category": "Pesticides",
                "description": "Organic pest control",
                "amount": 1200,
                "quantity": 10,
                "unit": "liters"
            }
        ]
        
        # Sample harvests
        self.farm_data["harvests"] = [
            {
                "id": 1,
                "farm_id": 1,
                "crop_id": 2,
                "harvest_date": "2023-12-15",
                "quantity": 95,
                "unit": "kg",
                "price_per_unit": 45,
                "total_value": 4275,
                "quality": "Good"
            },
            {
                "id": 2,
                "farm_id": 1,
                "crop_id": 1,
                "harvest_date": "2023-10-20",
                "quantity": 2800,
                "unit": "kg",
                "price_per_unit": 32,
                "total_value": 89600,
                "quality": "Excellent"
            }
        ]
    
    def get_farm_summary(self, farm_id):
        """
        Get summary statistics for a farm
        """
        farm = next((f for f in self.farm_data["farms"] if f["id"] == farm_id), None)
        if not farm:
            return None
        
        # Get crops for this farm
        farm_crops = [c for c in self.farm_data["crops"] if c["farm_id"] == farm_id]
        
        # Get expenses for this farm
        farm_expenses = [e for e in self.farm_data["expenses"] if e["farm_id"] == farm_id]
        
        # Get harvests for this farm
        farm_harvests = [h for h in self.farm_data["harvests"] if h["farm_id"] == farm_id]
        
        # Calculate statistics
        total_expenses = sum(e["amount"] for e in farm_expenses)
        total_revenue = sum(h["total_value"] for h in farm_harvests)
        net_profit = total_revenue - total_expenses
        
        active_crops = len([c for c in farm_crops if c["status"] == "Growing"])
        mature_crops = len([c for c in farm_crops if c["status"] == "Mature"])
        
        return {
            "farm": farm,
            "total_area": farm["area_acres"],
            "active_crops": active_crops,
            "mature_crops": mature_crops,
            "total_expenses": total_expenses,
            "total_revenue": total_revenue,
            "net_profit": net_profit,
            "profit_margin": (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        }
    
    def render_farm_dashboard(self):
        """
        Render the farm management dashboard
        """
        st.markdown("""
        <div class="chart-container">
            <div class="chart-title">🏡 Farm Management Dashboard</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Farm selection
        farm_options = {f"{f['name']} - {f['location']}": f["id"] for f in self.farm_data["farms"]}
        selected_farm = st.selectbox("Select Farm", list(farm_options.keys()))
        farm_id = farm_options[selected_farm]
        
        # Get farm summary
        summary = self.get_farm_summary(farm_id)
        
        if summary:
            # Display farm overview
            st.markdown("### 📊 Farm Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Area",
                    f"{summary['total_area']} acres",
                    f"{summary['active_crops']} active crops"
                )
            
            with col2:
                st.metric(
                    "Total Revenue",
                    f"₹{summary['total_revenue']:,}",
                    f"₹{summary['net_profit']:,} profit"
                )
            
            with col3:
                st.metric(
                    "Total Expenses",
                    f"₹{summary['total_expenses']:,}",
                    f"{summary['profit_margin']:.1f}% margin"
                )
            
            with col4:
                st.metric(
                    "Crop Status",
                    f"{summary['active_crops']} Growing",
                    f"{summary['mature_crops']} Mature"
                )
            
            # Farm details
            st.markdown("### 🏡 Farm Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Farm Name:** {summary['farm']['name']}  
                **Location:** {summary['farm']['location']}  
                **Soil Type:** {summary['farm']['soil_type']}  
                **Established:** {summary['farm']['established']}
                """)
            
            with col2:
                st.markdown(f"""
                **Owner:** {summary['farm']['owner']}  
                **Area:** {summary['farm']['area_acres']} acres  
                **Farm ID:** #{summary['farm']['id']}
                """)
            
            # Crops section
            self._render_crops_section(farm_id)
            
            # Expenses section
            self._render_expenses_section(farm_id)
            
            # Harvest section
            self._render_harvest_section(farm_id)
            
            # Analytics charts
            self._render_analytics_charts(farm_id)
    
    def _render_crops_section(self, farm_id):
        """
        Render crops section
        """
        st.markdown("### 🌱 Current Crops")
        
        farm_crops = [c for c in self.farm_data["crops"] if c["farm_id"] == farm_id]
        
        if farm_crops:
            for crop in farm_crops:
                with st.expander(f"{crop['crop_name']} - {crop['variety']} ({crop['status']})", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        **Area:** {crop['area_acres']} acres  
                        **Planting Date:** {crop['planting_date']}  
                        **Expected Harvest:** {crop['expected_harvest']}
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        **Status:** {crop['status']}  
                        **Expected Yield:** {crop['yield_expected']} kg  
                        **Actual Yield:** {crop['yield_actual'] or 'Not harvested'}
                        """)
                    
                    with col3:
                        if crop['status'] == 'Growing':
                            st.success("🌱 Growing well")
                        elif crop['status'] == 'Mature':
                            st.info("🌾 Ready for harvest")
                        else:
                            st.warning("⚠️ Needs attention")
        else:
            st.info("No crops found for this farm. Add crops to get started.")
    
    def _render_expenses_section(self, farm_id):
        """
        Render expenses section
        """
        st.markdown("### 💰 Recent Expenses")
        
        farm_expenses = [e for e in self.farm_data["expenses"] if e["farm_id"] == farm_id]
        farm_expenses.sort(key=lambda x: x["date"], reverse=True)
        
        if farm_expenses:
            # Display recent expenses
            for expense in farm_expenses[:5]:
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.text(f"{expense['category']} - {expense['description']}")
                
                with col2:
                    st.text(f"{expense['quantity']} {expense['unit']}")
                
                with col3:
                    st.text(f"₹{expense['amount']:,}")
                
                with col4:
                    st.text(expense['date'])
            
            # Add new expense button
            if st.button("➕ Add New Expense", type="primary"):
                st.info("Expense form would open here")
        else:
            st.info("No expenses recorded yet.")
    
    def _render_harvest_section(self, farm_id):
        """
        Render harvest section
        """
        st.markdown("### 🌾 Harvest Records")
        
        farm_harvests = [h for h in self.farm_data["harvests"] if h["farm_id"] == farm_id]
        farm_harvests.sort(key=lambda x: x["harvest_date"], reverse=True)
        
        if farm_harvests:
            for harvest in farm_harvests:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    crop = next((c for c in self.farm_data["crops"] if c["id"] == harvest["crop_id"]), None)
                    crop_name = crop["crop_name"] if crop else "Unknown"
                    st.text(f"{crop_name} - {harvest['harvest_date']}")
                
                with col2:
                    st.text(f"{harvest['quantity']} {harvest['unit']}")
                
                with col3:
                    st.text(f"₹{harvest['price_per_unit']}/{harvest['unit']}")
                
                with col4:
                    st.text(f"₹{harvest['total_value']:,}")
        else:
            st.info("No harvest records yet.")
    
    def _render_analytics_charts(self, farm_id):
        """
        Render analytics charts
        """
        st.markdown("### 📈 Farm Analytics")
        
        # Revenue vs Expenses chart
        farm_expenses = [e for e in self.farm_data["expenses"] if e["farm_id"] == farm_id]
        farm_harvests = [h for h in self.farm_data["harvests"] if h["farm_id"] == farm_id]
        
        if farm_expenses and farm_harvests:
            # Prepare data for charts
            expense_data = []
            for expense in farm_expenses:
                expense_data.append({
                    "Date": expense["date"],
                    "Amount": expense["amount"],
                    "Type": "Expense",
                    "Category": expense["category"]
                })
            
            revenue_data = []
            for harvest in farm_harvests:
                revenue_data.append({
                    "Date": harvest["harvest_date"],
                    "Amount": harvest["total_value"],
                    "Type": "Revenue",
                    "Category": "Harvest"
                })
            
            # Combine data
            chart_data = expense_data + revenue_data
            df = pd.DataFrame(chart_data)
            
            # Create chart
            fig = px.bar(
                df,
                x="Date",
                y="Amount",
                color="Type",
                title="Revenue vs Expenses Over Time",
                color_discrete_map={"Expense": "#FF6B6B", "Revenue": "#4ECDC4"}
            )
            
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_color='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Crop yield chart
        farm_crops = [c for c in self.farm_data["crops"] if c["farm_id"] == farm_id and c["yield_actual"]]
        
        if farm_crops:
            crop_data = []
            for crop in farm_crops:
                crop_data.append({
                    "Crop": crop["crop_name"],
                    "Expected": crop["yield_expected"],
                    "Actual": crop["yield_actual"]
                })
            
            df_crops = pd.DataFrame(crop_data)
            
            fig = px.bar(
                df_crops,
                x="Crop",
                y=["Expected", "Actual"],
                title="Expected vs Actual Yield",
                barmode="group"
            )
            
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_color='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)

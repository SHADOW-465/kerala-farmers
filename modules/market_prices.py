import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import json

class MarketPrices:
    def __init__(self):
        self.kerala_markets = [
            "Thiruvananthapuram",
            "Kollam", 
            "Pathanamthitta",
            "Alappuzha",
            "Kottayam",
            "Idukki",
            "Ernakulam",
            "Thrissur",
            "Palakkad",
            "Malappuram",
            "Kozhikode",
            "Wayanad",
            "Kannur",
            "Kasaragod"
        ]
        
        self.crops = [
            "Rice", "Coconut", "Black Pepper", "Cardamom", "Rubber",
            "Cashew", "Banana", "Tapioca", "Ginger", "Turmeric",
            "Tea", "Coffee", "Cocoa", "Arecanut", "Tamarind"
        ]
        
        self.price_data = self._generate_sample_price_data()
    
    def _generate_sample_price_data(self):
        """
        Generate sample price data for demonstration
        """
        price_data = []
        base_date = datetime.now() - timedelta(days=30)
        
        # Base prices for different crops
        base_prices = {
            "Rice": 35,
            "Coconut": 25,
            "Black Pepper": 450,
            "Cardamom": 1200,
            "Rubber": 180,
            "Cashew": 120,
            "Banana": 30,
            "Tapioca": 15,
            "Ginger": 80,
            "Turmeric": 60,
            "Tea": 200,
            "Coffee": 300,
            "Cocoa": 250,
            "Arecanut": 200,
            "Tamarind": 40
        }
        
        for i in range(30):
            date = base_date + timedelta(days=i)
            
            for crop in self.crops:
                for market in self.kerala_markets[:5]:  # Use first 5 markets for demo
                    # Add some random variation to prices
                    base_price = base_prices[crop]
                    variation = np.random.normal(0, 0.1)  # 10% standard deviation
                    price = base_price * (1 + variation)
                    
                    # Add seasonal variation
                    if crop == "Rice" and date.month in [10, 11, 12]:
                        price *= 1.2  # Higher prices during harvest season
                    elif crop == "Black Pepper" and date.month in [3, 4, 5]:
                        price *= 1.15  # Higher prices during peak season
                    
                    price_data.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "crop": crop,
                        "market": market,
                        "price_per_kg": round(price, 2),
                        "volume_kg": np.random.randint(100, 1000),
                        "quality": np.random.choice(["A", "B", "C"], p=[0.6, 0.3, 0.1])
                    })
        
        return price_data
    
    def get_current_prices(self, crop=None, market=None):
        """
        Get current prices for crops
        """
        df = pd.DataFrame(self.price_data)
        
        # Filter by crop and market if specified
        if crop:
            df = df[df["crop"] == crop]
        if market:
            df = df[df["market"] == market]
        
        # Get latest prices (last 7 days)
        latest_date = df["date"].max()
        latest_df = df[df["date"] == latest_date]
        
        return latest_df
    
    def get_price_trends(self, crop, market=None, days=30):
        """
        Get price trends for a specific crop
        """
        df = pd.DataFrame(self.price_data)
        df = df[df["crop"] == crop]
        
        if market:
            df = df[df["market"] == market]
        
        # Get last N days of data
        latest_date = pd.to_datetime(df["date"]).max()
        start_date = latest_date - timedelta(days=days)
        df = df[pd.to_datetime(df["date"]) >= start_date]
        
        # Group by date and calculate average price
        trend_df = df.groupby("date")["price_per_kg"].mean().reset_index()
        trend_df["date"] = pd.to_datetime(trend_df["date"])
        
        return trend_df
    
    def predict_prices(self, crop, days_ahead=7):
        """
        Simple price prediction using trend analysis
        """
        trend_df = self.get_price_trends(crop, days=30)
        
        if len(trend_df) < 7:
            return None
        
        # Simple linear regression for prediction
        x = np.arange(len(trend_df))
        y = trend_df["price_per_kg"].values
        
        # Calculate trend
        slope = np.polyfit(x, y, 1)[0]
        intercept = np.polyfit(x, y, 1)[1]
        
        # Predict future prices
        predictions = []
        last_date = trend_df["date"].iloc[-1]
        
        for i in range(1, days_ahead + 1):
            future_x = len(trend_df) + i - 1
            predicted_price = slope * future_x + intercept
            
            # Add some randomness to make it more realistic
            noise = np.random.normal(0, predicted_price * 0.05)
            predicted_price += noise
            
            predictions.append({
                "date": (last_date + timedelta(days=i)).strftime("%Y-%m-%d"),
                "predicted_price": max(0, round(predicted_price, 2)),
                "confidence": max(0.5, min(0.95, 1 - (i * 0.1)))  # Decreasing confidence
            })
        
        return predictions
    
    def get_market_insights(self):
        """
        Get market insights and recommendations
        """
        df = pd.DataFrame(self.price_data)
        
        # Calculate price changes
        latest_prices = df.groupby("crop")["price_per_kg"].last()
        week_ago_prices = df[df["date"] == (pd.to_datetime(df["date"]).max() - timedelta(days=7))].groupby("crop")["price_per_kg"].mean()
        
        price_changes = {}
        for crop in latest_prices.index:
            if crop in week_ago_prices.index:
                change = ((latest_prices[crop] - week_ago_prices[crop]) / week_ago_prices[crop]) * 100
                price_changes[crop] = change
        
        # Sort by price change
        sorted_changes = sorted(price_changes.items(), key=lambda x: x[1], reverse=True)
        
        insights = {
            "top_gainers": sorted_changes[:3],
            "top_losers": sorted_changes[-3:],
            "stable_crops": [crop for crop, change in price_changes.items() if abs(change) < 2]
        }
        
        return insights
    
    def render_market_dashboard(self):
        """
        Render the market prices dashboard
        """
        st.markdown("""
        <div class="chart-container">
            <div class="chart-title">💰 Market Price Intelligence</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Market and crop selection
        col1, col2 = st.columns(2)
        
        with col1:
            selected_market = st.selectbox("Select Market", ["All Markets"] + self.kerala_markets)
        
        with col2:
            selected_crop = st.selectbox("Select Crop", ["All Crops"] + self.crops)
        
        # Get current prices
        market_filter = selected_market if selected_market != "All Markets" else None
        crop_filter = selected_crop if selected_crop != "All Crops" else None
        
        current_prices = self.get_current_prices(crop_filter, market_filter)
        
        if not current_prices.empty:
            # Display current prices
            st.markdown("### 📊 Current Market Prices")
            
            # Top 10 prices
            top_prices = current_prices.nlargest(10, "price_per_kg")
            
            for _, row in top_prices.iterrows():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.text(f"{row['crop']} - {row['market']}")
                
                with col2:
                    st.text(f"₹{row['price_per_kg']}/kg")
                
                with col3:
                    st.text(f"{row['volume_kg']} kg")
                
                with col4:
                    quality_color = {"A": "🟢", "B": "🟡", "C": "🔴"}
                    st.text(f"{quality_color[row['quality']]} {row['quality']}")
        
        # Price trends
        if selected_crop != "All Crops":
            st.markdown("### 📈 Price Trends")
            
            trend_df = self.get_price_trends(selected_crop, market_filter if selected_market != "All Markets" else None)
            
            if not trend_df.empty:
                fig = px.line(
                    trend_df,
                    x="date",
                    y="price_per_kg",
                    title=f"{selected_crop} Price Trend",
                    markers=True
                )
                
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    title_font_color='white',
                    xaxis_title="Date",
                    yaxis_title="Price (₹/kg)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Price prediction
                st.markdown("### 🔮 Price Prediction")
                
                predictions = self.predict_prices(selected_crop, 7)
                
                if predictions:
                    pred_df = pd.DataFrame(predictions)
                    
                    fig = px.line(
                        pred_df,
                        x="date",
                        y="predicted_price",
                        title=f"{selected_crop} Price Prediction (Next 7 Days)",
                        markers=True
                    )
                    
                    fig.update_layout(
                        height=300,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white',
                        title_font_color='white',
                        xaxis_title="Date",
                        yaxis_title="Predicted Price (₹/kg)"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show prediction details
                    st.markdown("**Prediction Details:**")
                    for pred in predictions:
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.text(f"Date: {pred['date']}")
                        
                        with col2:
                            st.text(f"Price: ₹{pred['predicted_price']}/kg")
                        
                        with col3:
                            st.text(f"Confidence: {pred['confidence']:.1%}")
        
        # Market insights
        st.markdown("### 💡 Market Insights")
        
        insights = self.get_market_insights()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📈 Top Gainers**")
            for crop, change in insights["top_gainers"]:
                st.text(f"{crop}: +{change:.1f}%")
        
        with col2:
            st.markdown("**📉 Top Losers**")
            for crop, change in insights["top_losers"]:
                st.text(f"{crop}: {change:.1f}%")
        
        with col3:
            st.markdown("**📊 Stable Crops**")
            for crop in insights["stable_crops"][:3]:
                st.text(f"{crop}: Stable")
        
        # Market recommendations
        st.markdown("### 🎯 Market Recommendations")
        
        if selected_crop != "All Crops":
            trend_df = self.get_price_trends(selected_crop, days=7)
            
            if not trend_df.empty:
                current_price = trend_df["price_per_kg"].iloc[-1]
                week_ago_price = trend_df["price_per_kg"].iloc[0]
                price_change = ((current_price - week_ago_price) / week_ago_price) * 100
                
                if price_change > 5:
                    st.success(f"📈 **Sell Now**: {selected_crop} prices are up {price_change:.1f}% this week. Consider selling soon.")
                elif price_change < -5:
                    st.warning(f"📉 **Hold**: {selected_crop} prices are down {abs(price_change):.1f}% this week. Wait for better prices.")
                else:
                    st.info(f"📊 **Stable**: {selected_crop} prices are stable. Monitor for better opportunities.")
        
        # Best selling times
        st.markdown("### ⏰ Best Selling Times")
        
        best_times = {
            "Rice": "October - December (Harvest season)",
            "Coconut": "Year-round (Peak: March - May)",
            "Black Pepper": "March - May (Peak season)",
            "Cardamom": "October - December (Harvest season)",
            "Rubber": "Year-round (Peak: March - May)",
            "Banana": "Year-round (Peak: Summer months)",
            "Ginger": "December - February (Harvest season)",
            "Turmeric": "February - April (Harvest season)"
        }
        
        if selected_crop in best_times:
            st.info(f"**{selected_crop}**: {best_times[selected_crop]}")
        else:
            st.info("Select a specific crop to see best selling times.")

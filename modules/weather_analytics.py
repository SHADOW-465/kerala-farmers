import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

class WeatherAnalytics:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        # Kerala districts coordinates
        self.kerala_districts = {
            "Thiruvananthapuram": {"lat": 8.5241, "lon": 76.9366},
            "Kollam": {"lat": 8.8932, "lon": 76.6141},
            "Pathanamthitta": {"lat": 9.2648, "lon": 76.7870},
            "Alappuzha": {"lat": 9.4981, "lon": 76.3388},
            "Kottayam": {"lat": 9.5900, "lon": 76.5222},
            "Idukki": {"lat": 9.8445, "lon": 76.9398},
            "Ernakulam": {"lat": 9.9816, "lon": 76.2999},
            "Thrissur": {"lat": 10.5276, "lon": 76.2144},
            "Palakkad": {"lat": 10.7867, "lon": 76.6548},
            "Malappuram": {"lat": 11.0404, "lon": 76.0810},
            "Kozhikode": {"lat": 11.2588, "lon": 75.7804},
            "Wayanad": {"lat": 11.6850, "lon": 76.1319},
            "Kannur": {"lat": 11.8745, "lon": 75.3704},
            "Kasaragod": {"lat": 12.4991, "lon": 74.9891}
        }
    
    def get_current_weather(self, district):
        """
        Get current weather for a specific district
        """
        try:
            if self.api_key and district in self.kerala_districts:
                coords = self.kerala_districts[district]
                url = f"{self.base_url}/weather"
                params = {
                    "lat": coords["lat"],
                    "lon": coords["lon"],
                    "appid": self.api_key,
                    "units": "metric"
                }
                
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    return response.json()
            
            # Return mock data if API key not available
            return self._get_mock_current_weather()
            
        except Exception as e:
            st.error(f"Error fetching weather data: {str(e)}")
            return self._get_mock_current_weather()
    
    def get_weather_forecast(self, district, days=7):
        """
        Get weather forecast for a specific district
        """
        try:
            if self.api_key and district in self.kerala_districts:
                coords = self.kerala_districts[district]
                url = f"{self.base_url}/forecast"
                params = {
                    "lat": coords["lat"],
                    "lon": coords["lon"],
                    "appid": self.api_key,
                    "units": "metric"
                }
                
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    return response.json()
            
            # Return mock data if API key not available
            return self._get_mock_forecast(days)
            
        except Exception as e:
            st.error(f"Error fetching forecast data: {str(e)}")
            return self._get_mock_forecast(days)
    
    def _get_mock_current_weather(self):
        """
        Return mock current weather data
        """
        return {
            "main": {
                "temp": 28.5,
                "feels_like": 32.1,
                "humidity": 78,
                "pressure": 1013
            },
            "weather": [{
                "main": "Rain",
                "description": "moderate rain",
                "icon": "10d"
            }],
            "wind": {
                "speed": 3.2,
                "deg": 180
            },
            "visibility": 10000,
            "name": "Kerala"
        }
    
    def _get_mock_forecast(self, days=7):
        """
        Return mock forecast data
        """
        forecast_data = {
            "list": []
        }
        
        for i in range(days * 8):  # 8 forecasts per day (every 3 hours)
            dt = datetime.now() + timedelta(hours=i*3)
            forecast_data["list"].append({
                "dt": int(dt.timestamp()),
                "main": {
                    "temp": 25 + (i % 10) - 5,  # Temperature variation
                    "humidity": 70 + (i % 20),
                    "pressure": 1010 + (i % 10)
                },
                "weather": [{
                    "main": ["Clear", "Clouds", "Rain"][i % 3],
                    "description": ["clear sky", "few clouds", "moderate rain"][i % 3],
                    "icon": ["01d", "02d", "10d"][i % 3]
                }],
                "wind": {
                    "speed": 2 + (i % 5),
                    "deg": 180 + (i * 30) % 360
                },
                "pop": 0.1 + (i % 5) * 0.1  # Probability of precipitation
            })
        
        return forecast_data
    
    def get_farming_recommendations(self, weather_data):
        """
        Get farming recommendations based on weather data
        """
        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        weather_condition = weather_data["weather"][0]["main"]
        wind_speed = weather_data["wind"]["speed"]
        
        recommendations = []
        
        # Temperature-based recommendations
        if temp > 35:
            recommendations.append("🌡️ High temperature - Increase irrigation frequency and provide shade for sensitive crops")
        elif temp < 20:
            recommendations.append("❄️ Low temperature - Protect young plants and consider covering crops")
        else:
            recommendations.append("✅ Optimal temperature for most crops")
        
        # Humidity-based recommendations
        if humidity > 80:
            recommendations.append("💧 High humidity - Watch for fungal diseases, ensure good air circulation")
        elif humidity < 40:
            recommendations.append("🏜️ Low humidity - Increase irrigation and consider mulching")
        else:
            recommendations.append("✅ Good humidity levels for plant growth")
        
        # Weather condition recommendations
        if weather_condition == "Rain":
            recommendations.append("🌧️ Rainy weather - Avoid field work, check drainage, prevent waterlogging")
        elif weather_condition == "Clear":
            recommendations.append("☀️ Clear weather - Good for field work, planting, and harvesting")
        elif weather_condition == "Clouds":
            recommendations.append("☁️ Cloudy weather - Good for transplanting and sensitive operations")
        
        # Wind-based recommendations
        if wind_speed > 10:
            recommendations.append("💨 Strong winds - Avoid spraying, protect young plants, check trellises")
        else:
            recommendations.append("✅ Calm conditions - Good for spraying and field operations")
        
        return recommendations
    
    def render_weather_dashboard(self):
        """
        Render the weather analytics dashboard
        """
        st.markdown("""
        <div class="chart-container">
            <div class="chart-title">🌤️ Weather Analytics Dashboard</div>
        </div>
        """, unsafe_allow_html=True)
        
        # District selection
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_district = st.selectbox(
                "Select District",
                list(self.kerala_districts.keys()),
                index=0
            )
        
        with col2:
            st.markdown("### Current Weather Conditions")
        
        # Get current weather
        current_weather = self.get_current_weather(selected_district)
        
        # Display current weather
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Temperature",
                f"{current_weather['main']['temp']:.1f}°C",
                f"Feels like {current_weather['main']['feels_like']:.1f}°C"
            )
        
        with col2:
            st.metric(
                "Humidity",
                f"{current_weather['main']['humidity']}%",
                "Relative humidity"
            )
        
        with col3:
            st.metric(
                "Pressure",
                f"{current_weather['main']['pressure']} hPa",
                "Atmospheric pressure"
            )
        
        with col4:
            st.metric(
                "Wind Speed",
                f"{current_weather['wind']['speed']} m/s",
                f"Direction: {current_weather['wind']['deg']}°"
            )
        
        # Weather condition
        weather_condition = current_weather['weather'][0]
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 12px; margin: 20px 0;">
            <h3 style="color: white; margin: 0;">{weather_condition['description'].title()}</h3>
            <p style="color: #B0B0B0; margin: 5px 0;">Current conditions in {selected_district}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 7-day forecast
        st.markdown("### 📅 7-Day Weather Forecast")
        
        forecast_data = self.get_weather_forecast(selected_district, 7)
        
        # Process forecast data for display
        daily_forecast = self._process_forecast_data(forecast_data)
        
        # Display forecast cards
        cols = st.columns(7)
        
        for i, day in enumerate(daily_forecast):
            with cols[i]:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px;">
                    <h4 style="color: white; margin: 0 0 10px 0;">{day['date']}</h4>
                    <p style="color: #B0B0B0; margin: 0 0 10px 0;">{day['condition']}</p>
                    <h3 style="color: white; margin: 0 0 5px 0;">{day['temp_max']}°</h3>
                    <p style="color: #B0B0B0; margin: 0 0 10px 0;">{day['temp_min']}°</p>
                    <p style="color: #B0B0B0; margin: 0; font-size: 0.8rem;">{day['humidity']}% humidity</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Weather chart
        self._render_weather_chart(daily_forecast)
        
        # Farming recommendations
        st.markdown("### 🌾 Farming Recommendations")
        
        recommendations = self.get_farming_recommendations(current_weather)
        
        for rec in recommendations:
            st.info(rec)
        
        # Weather alerts
        self._render_weather_alerts(current_weather)
    
    def _process_forecast_data(self, forecast_data):
        """
        Process forecast data to get daily summaries
        """
        daily_data = {}
        
        for item in forecast_data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            day_name = datetime.fromtimestamp(item['dt']).strftime('%a')
            
            if date not in daily_data:
                daily_data[date] = {
                    'date': day_name,
                    'temps': [],
                    'humidity': [],
                    'conditions': []
                }
            
            daily_data[date]['temps'].append(item['main']['temp'])
            daily_data[date]['humidity'].append(item['main']['humidity'])
            daily_data[date]['conditions'].append(item['weather'][0]['main'])
        
        # Calculate daily summaries
        daily_forecast = []
        for date, data in daily_data.items():
            daily_forecast.append({
                'date': data['date'],
                'temp_max': max(data['temps']),
                'temp_min': min(data['temps']),
                'humidity': round(sum(data['humidity']) / len(data['humidity'])),
                'condition': max(set(data['conditions']), key=data['conditions'].count)
            })
        
        return daily_forecast[:7]  # Return first 7 days
    
    def _render_weather_chart(self, daily_forecast):
        """
        Render weather chart
        """
        df = pd.DataFrame(daily_forecast)
        
        fig = go.Figure()
        
        # Add temperature lines
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['temp_max'],
            mode='lines+markers',
            name='Max Temperature',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['temp_min'],
            mode='lines+markers',
            name='Min Temperature',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=8),
            fill='tonexty'
        ))
        
        fig.update_layout(
            title="Temperature Forecast",
            xaxis_title="Day",
            yaxis_title="Temperature (°C)",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_weather_alerts(self, weather_data):
        """
        Render weather alerts
        """
        alerts = []
        
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        weather_condition = weather_data['weather'][0]['main']
        
        if temp > 35:
            alerts.append({
                "type": "warning",
                "message": "🌡️ Heat Alert: High temperature detected. Take precautions for crops and workers."
            })
        
        if humidity > 85:
            alerts.append({
                "type": "info",
                "message": "💧 High Humidity: Risk of fungal diseases. Monitor crops closely."
            })
        
        if wind_speed > 15:
            alerts.append({
                "type": "error",
                "message": "💨 Wind Alert: Strong winds detected. Avoid field work and protect crops."
            })
        
        if weather_condition == "Rain":
            alerts.append({
                "type": "info",
                "message": "🌧️ Rain Alert: Wet conditions. Avoid field work and check drainage."
            })
        
        if alerts:
            st.markdown("### ⚠️ Weather Alerts")
            for alert in alerts:
                if alert["type"] == "error":
                    st.error(alert["message"])
                elif alert["type"] == "warning":
                    st.warning(alert["message"])
                else:
                    st.info(alert["message"])
        else:
            st.success("✅ No weather alerts. Conditions are favorable for farming activities.")

# 🌾 Kerala Farmers Hub - Streamlit Dashboard

A comprehensive AI-powered farming assistant dashboard built with Streamlit, designed specifically for Kerala farmers. This application provides intelligent crop recommendations, disease detection, weather analytics, market intelligence, and community support.

## ✨ Features

### 🤖 AI-Powered Features
- **Plant Disease Detection**: Upload images to identify plant diseases with AI
- **Smart Crop Recommendations**: Get personalized crop suggestions based on soil and weather conditions
- **AI Chatbot**: Multilingual support (English, Malayalam, Tamil, Hindi) for farming queries
- **Weather Analytics**: Real-time weather data and farming recommendations

### 🏡 Farm Management
- **Farm Profile Management**: Create and manage multiple farm profiles
- **Crop Tracking**: Monitor crop growth and health
- **Expense Tracking**: Track farming expenses and budget
- **Harvest Records**: Record and analyze harvest data

### 🌐 Community Platform
- **Discussion Forum**: Ask questions and share knowledge
- **Expert Advice**: Connect with agricultural experts
- **Success Stories**: Learn from successful farmers
- **Knowledge Sharing**: Access farming guides and best practices

### 📊 Market Intelligence
- **Price Predictions**: AI-powered crop price forecasting
- **Market Insights**: Real-time market trends and analysis
- **Government Schemes**: Find and apply for relevant schemes

### 🌱 Soil Health
- **Soil Assessment**: Analyze soil test results
- **Fertilizer Recommendations**: Get personalized fertilizer suggestions
- **Crop Suitability**: Check which crops are best for your soil

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd keralafarm
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:8501`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory for API keys:

```env
# Optional API Keys (app works with mock data without these)
HUGGINGFACE_API_KEY=your_huggingface_key
OPENWEATHER_API_KEY=your_openweather_key
```

### Features

The application works with mock data by default. To enable real-time features:

1. **Weather Data**: Add your OpenWeatherMap API key to get real weather data
2. **Disease Detection**: Add your Hugging Face API key for AI-powered disease detection

## 📱 Features Overview

### Dashboard
- Overview of farm metrics and KPIs
- Quick access to all features
- Real-time data visualization

### Disease Detection
- Upload plant images for AI analysis
- Get disease identification and treatment recommendations
- Confidence scores and severity levels

### Crop Recommendations
- Input soil and weather conditions
- Get AI-powered crop suggestions
- Suitability scoring and seasonal calendar

### Weather Analytics
- 7-day weather forecast
- Farming recommendations based on weather
- Weather alerts and warnings

### Farm Management
- Track multiple farms
- Monitor crops and expenses
- Analyze harvest data and profitability

### Market Prices
- Real-time crop prices
- Price trend analysis
- Market predictions and insights

### Soil Health
- Analyze soil test results
- Get fertilizer recommendations
- Check crop suitability

### Government Schemes
- Find eligible schemes
- Application tracking
- Document management

### Community Platform
- Q&A forum
- Expert network
- Success stories sharing

### AI Assistant
- Multilingual chatbot
- Quick action buttons
- Farming advice and support

## 🎨 UI Design

The application features a modern, dark-themed dashboard inspired by the provided design:

- **Color Scheme**: Dark green/teal theme with white text
- **Layout**: Sidebar navigation with main content area
- **Components**: Cards, charts, and interactive elements
- **Responsive**: Mobile-friendly design
- **Custom CSS**: Styled with `unsafe_allow_html` for modern UI effects

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **Data Visualization**: Plotly, Pandas
- **AI/ML**: Hugging Face API, Scikit-learn
- **Image Processing**: Pillow, OpenCV
- **Weather Data**: OpenWeatherMap API
- **Styling**: Custom CSS with HTML components

## 📁 Project Structure

```
keralafarm/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── modules/                        # Feature modules
│   ├── disease_detection.py       # Plant disease detection
│   ├── crop_recommendation.py     # Crop recommendation engine
│   ├── ai_chatbot.py             # AI chatbot assistant
│   ├── weather_analytics.py      # Weather analytics
│   ├── farm_management.py        # Farm management
│   ├── market_prices.py          # Market price intelligence
│   ├── soil_health.py            # Soil health assessment
│   ├── government_schemes.py     # Government schemes
│   └── community_platform.py     # Community platform
└── .env                          # Environment variables (create this)
```

## 🌾 Kerala-Specific Features

### Crops Supported
- Rice (Kerala varieties)
- Coconut
- Black Pepper
- Cardamom
- Rubber
- Cashew
- Banana
- Tapioca
- Ginger
- Turmeric

### Languages
- English
- Malayalam (മലയാളം)
- Tamil (தமிழ்)
- Hindi (हिन्दी)

### Regions
- Coastal Kerala
- Midland Kerala
- Highland Kerala

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
1. Deploy to Streamlit Cloud, Heroku, or AWS
2. Set environment variables
3. Configure API keys
4. Deploy the application

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- Real-time IoT sensor integration
- Advanced ML models
- Mobile app development
- Blockchain integration
- Advanced analytics

---

**Built with ❤️ for Kerala Farmers**

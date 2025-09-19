import streamlit as st
import json
import random
from datetime import datetime
import os

class AIChatbot:
    def __init__(self):
        self.conversation_history = []
        self.languages = {
            "English": "en",
            "Malayalam": "ml", 
            "Tamil": "ta",
            "Hindi": "hi"
        }
        
        # Predefined responses for common farming queries
        self.responses = {
            "en": {
                "greeting": [
                    "Hello! I'm your AI farming assistant. How can I help you today?",
                    "Hi there! Ready to help with your farming questions.",
                    "Welcome! What farming advice do you need today?"
                ],
                "weather": [
                    "For weather-related farming advice, I recommend checking the weather forecast section. Generally, avoid planting during heavy rains and ensure proper drainage.",
                    "Weather plays a crucial role in farming. Check the 7-day forecast and plan your activities accordingly.",
                    "Monitor weather conditions regularly. Use the weather analytics section for detailed forecasts and farming recommendations."
                ],
                "disease": [
                    "For plant disease detection, use the disease detection tool to upload images of affected plants. I can help identify common diseases and suggest treatments.",
                    "Plant diseases can be identified through visual symptoms. Upload clear images of affected leaves or plants for accurate diagnosis.",
                    "Early detection is key to managing plant diseases. Use the AI-powered disease detection feature for quick identification."
                ],
                "crop": [
                    "For crop recommendations, use the crop recommendation tool. It considers your soil type, climate, and other factors to suggest the best crops.",
                    "Crop selection depends on soil conditions, climate, and market demand. The recommendation engine can help you choose the right crops.",
                    "I can help you select crops based on your farm's specific conditions. Use the crop recommendation feature for personalized suggestions."
                ],
                "soil": [
                    "Soil health is crucial for good yields. Get your soil tested regularly and use the soil health assessment tool for recommendations.",
                    "Healthy soil contains the right balance of nutrients. Use the soil health tool to analyze your soil test results.",
                    "Soil testing helps identify nutrient deficiencies. The soil health assessment can guide you on fertilizer applications."
                ],
                "market": [
                    "Check the market prices section for current crop prices and trends. This helps in planning when to sell your produce.",
                    "Market intelligence is important for maximizing profits. Use the price prediction feature to plan your sales strategy.",
                    "Stay updated with market trends to get the best prices for your crops. The market section provides real-time price data."
                ],
                "government": [
                    "Check the government schemes section to find relevant agricultural schemes and subsidies for your farm.",
                    "Many government schemes are available for farmers. Use the scheme matcher to find programs you're eligible for.",
                    "Government support can help reduce farming costs. The scheme matcher identifies relevant programs based on your farm profile."
                ],
                "default": [
                    "I understand you're asking about farming. Could you be more specific about what you need help with?",
                    "That's an interesting question about farming. Let me help you find the right information.",
                    "I'm here to help with your farming needs. Could you provide more details about your specific question?"
                ]
            },
            "ml": {
                "greeting": [
                    "നമസ്കാരം! ഞാൻ നിങ്ങളുടെ കൃഷി സഹായി. എങ്ങനെ സഹായിക്കാം?",
                    "ഹലോ! കൃഷി സംബന്ധമായ ചോദ്യങ്ങൾക്ക് ഞാൻ ഇവിടെയുണ്ട്.",
                    "സ്വാഗതം! ഇന്ന് എന്ത് കൃഷി ഉപദേശം വേണം?"
                ],
                "default": [
                    "കൃഷി സംബന്ധമായ ചോദ്യമാണെന്ന് മനസ്സിലാക്കുന്നു. കൂടുതൽ വിശദാംശങ്ങൾ പറയാമോ?",
                    "ഇത് രസകരമായ ഒരു ചോദ്യമാണ്. ശരിയായ വിവരം കണ്ടെത്താൻ സഹായിക്കാം.",
                    "നിങ്ങളുടെ കൃഷി ആവശ്യങ്ങൾക്ക് ഞാൻ ഇവിടെയുണ്ട്. കൂടുതൽ വിശദാംശങ്ങൾ പറയാമോ?"
                ]
            },
            "ta": {
                "greeting": [
                    "வணக்கம்! நான் உங்கள் விவசாய உதவியாளர். எப்படி உதவ முடியும்?",
                    "ஹலோ! விவசாய கேள்விகளுக்கு நான் இங்கே இருக்கிறேன்.",
                    "வரவேற்கிறேன்! இன்று என்ன விவசாய ஆலோசனை வேண்டும்?"
                ],
                "default": [
                    "விவசாயம் பற்றிய கேள்வி என்று புரிகிறது. மேலும் விவரங்கள் சொல்ல முடியுமா?",
                    "இது சுவாரஸ்யமான கேள்வி. சரியான தகவலை கண்டுபிடிக்க உதவுகிறேன்.",
                    "உங்கள் விவசாய தேவைகளுக்கு நான் இங்கே இருக்கிறேன். மேலும் விவரங்கள் சொல்ல முடியுமா?"
                ]
            },
            "hi": {
                "greeting": [
                    "नमस्ते! मैं आपका कृषि सहायक हूं। कैसे मदद कर सकता हूं?",
                    "हैलो! कृषि संबंधी सवालों के लिए मैं यहां हूं।",
                    "स्वागत है! आज क्या कृषि सलाह चाहिए?"
                ],
                "default": [
                    "समझ गया कि यह कृषि के बारे में सवाल है। और विवरण दे सकते हैं?",
                    "यह एक दिलचस्प सवाल है। सही जानकारी खोजने में मदद करता हूं।",
                    "आपकी कृषि जरूरतों के लिए मैं यहां हूं। और विवरण दे सकते हैं?"
                ]
            }
        }
    
    def get_response(self, user_input, language="en"):
        """
        Get AI response based on user input and language
        """
        user_input_lower = user_input.lower()
        
        # Determine response category
        if any(word in user_input_lower for word in ["hello", "hi", "namaste", "vanakkam", "namaskaram"]):
            category = "greeting"
        elif any(word in user_input_lower for word in ["weather", "rain", "temperature", "മഴ", "வானிலை", "मौसम"]):
            category = "weather"
        elif any(word in user_input_lower for word in ["disease", "sick", "problem", "രോഗം", "நோய்", "रोग"]):
            category = "disease"
        elif any(word in user_input_lower for word in ["crop", "plant", "cultivate", "വിള", "பயிர்", "फसल"]):
            category = "crop"
        elif any(word in user_input_lower for word in ["soil", "fertilizer", "nutrient", "മണ്ണ്", "மண்", "मिट्टी"]):
            category = "soil"
        elif any(word in user_input_lower for word in ["market", "price", "sell", "വില", "விலை", "बाजार"]):
            category = "market"
        elif any(word in user_input_lower for word in ["government", "scheme", "subsidy", "സർക്കാർ", "அரசு", "सरकार"]):
            category = "government"
        else:
            category = "default"
        
        # Get response in selected language
        if language in self.responses and category in self.responses[language]:
            response = random.choice(self.responses[language][category])
        else:
            response = random.choice(self.responses["en"]["default"])
        
        return response
    
    def add_to_history(self, user_input, bot_response, language="en"):
        """
        Add conversation to history
        """
        self.conversation_history.append({
            "timestamp": datetime.now().strftime("%H:%M"),
            "user": user_input,
            "bot": bot_response,
            "language": language
        })
    
    def render_chatbot_ui(self):
        """
        Render the AI chatbot UI
        """
        st.markdown("""
        <div class="chart-container">
            <div class="chart-title">🤖 AI Farming Assistant</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Language selection
        col1, col2 = st.columns([1, 3])
        
        with col1:
            selected_language = st.selectbox(
                "Language",
                list(self.languages.keys()),
                index=0
            )
        
        with col2:
            st.markdown("### 💬 Chat with AI Assistant")
        
        # Chat interface
        chat_container = st.container()
        
        with chat_container:
            # Display conversation history
            for message in self.conversation_history[-10:]:  # Show last 10 messages
                if message["user"]:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                        <div style="background: #2C5555; color: white; padding: 10px 15px; border-radius: 18px 18px 5px 18px; max-width: 70%; word-wrap: break-word;">
                            {message["user"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if message["bot"]:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                        <div style="background: #1A3636; color: white; padding: 10px 15px; border-radius: 18px 18px 18px 5px; max-width: 70%; word-wrap: break-word;">
                            {message["bot"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Quick action buttons
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🌤️ Weather Advice", use_container_width=True):
                self._handle_quick_action("weather", selected_language)
        
        with col2:
            if st.button("🔬 Disease Help", use_container_width=True):
                self._handle_quick_action("disease", selected_language)
        
        with col3:
            if st.button("🌱 Crop Selection", use_container_width=True):
                self._handle_quick_action("crop", selected_language)
        
        with col4:
            if st.button("💰 Market Info", use_container_width=True):
                self._handle_quick_action("market", selected_language)
        
        # Chat input
        user_input = st.text_input(
            "Type your farming question here...",
            placeholder="Ask me anything about farming!",
            key="chat_input"
        )
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            send_button = st.button("Send", type="primary", use_container_width=True)
        
        with col2:
            if st.button("Clear Chat", use_container_width=True):
                self.conversation_history = []
                st.rerun()
        
        # Handle user input
        if send_button and user_input:
            language_code = self.languages[selected_language]
            bot_response = self.get_response(user_input, language_code)
            
            self.add_to_history(user_input, bot_response, language_code)
            st.rerun()
    
    def _handle_quick_action(self, action, language):
        """
        Handle quick action button clicks
        """
        language_code = self.languages[language]
        response = self.get_response(action, language_code)
        
        self.add_to_history(f"Quick action: {action}", response, language_code)
        st.rerun()
    
    def get_conversation_summary(self):
        """
        Get a summary of the conversation
        """
        if not self.conversation_history:
            return "No conversation yet."
        
        topics = []
        for message in self.conversation_history:
            if message["user"]:
                user_input = message["user"].lower()
                if any(word in user_input for word in ["weather", "rain", "temperature"]):
                    topics.append("Weather")
                elif any(word in user_input for word in ["disease", "sick", "problem"]):
                    topics.append("Disease")
                elif any(word in user_input for word in ["crop", "plant", "cultivate"]):
                    topics.append("Crop Selection")
                elif any(word in user_input for word in ["soil", "fertilizer", "nutrient"]):
                    topics.append("Soil Health")
                elif any(word in user_input for word in ["market", "price", "sell"]):
                    topics.append("Market")
        
        if topics:
            return f"Discussed topics: {', '.join(set(topics))}"
        else:
            return "General farming discussion"

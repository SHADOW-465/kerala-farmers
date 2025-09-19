import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

class CommunityPlatform:
    def __init__(self):
        self.questions = []
        self.answers = []
        self.experts = []
        self.load_sample_data()
    
    def load_sample_data(self):
        """
        Load sample community data
        """
        # Sample questions
        self.questions = [
            {
                "id": 1,
                "title": "How to control coconut mite infestation?",
                "description": "My coconut trees are showing signs of mite infestation. The leaves are turning yellow and there are small webs. What's the best way to control this?",
                "author": "Rajesh Kumar",
                "date": "2024-01-20",
                "category": "Pest Control",
                "tags": ["coconut", "mite", "pest control"],
                "votes": 15,
                "answers_count": 3,
                "solved": False
            },
            {
                "id": 2,
                "title": "Best time to plant black pepper in Kerala?",
                "description": "I'm planning to start black pepper cultivation. What's the best time to plant and what are the key requirements?",
                "author": "Priya Menon",
                "date": "2024-01-18",
                "category": "Crop Cultivation",
                "tags": ["black pepper", "planting", "kerala"],
                "votes": 8,
                "answers_count": 5,
                "solved": True
            },
            {
                "id": 3,
                "title": "Organic fertilizer recommendations for rice",
                "description": "I want to switch to organic farming for my rice crop. What organic fertilizers would you recommend?",
                "author": "Suresh Nair",
                "date": "2024-01-15",
                "category": "Organic Farming",
                "tags": ["rice", "organic", "fertilizer"],
                "votes": 12,
                "answers_count": 4,
                "solved": False
            },
            {
                "id": 4,
                "title": "Weather impact on cardamom yield",
                "description": "How does the recent heavy rainfall affect cardamom plants? Should I be concerned about the yield?",
                "author": "Anita Devi",
                "date": "2024-01-12",
                "category": "Weather Impact",
                "tags": ["cardamom", "weather", "yield"],
                "votes": 6,
                "answers_count": 2,
                "solved": False
            }
        ]
        
        # Sample answers
        self.answers = [
            {
                "id": 1,
                "question_id": 1,
                "author": "Dr. Sreekumar (Agricultural Expert)",
                "date": "2024-01-21",
                "content": "Coconut mite infestation can be controlled using neem oil spray (2ml per liter) or acaricides like dicofol. Apply twice at 15-day intervals. Also, ensure proper drainage and avoid waterlogging.",
                "votes": 8,
                "is_expert": True
            },
            {
                "id": 2,
                "question_id": 1,
                "author": "Mohan Das",
                "date": "2024-01-22",
                "content": "I had similar issue last year. Used neem oil + soap solution. Worked well. Also removed affected leaves and burned them.",
                "votes": 5,
                "is_expert": False
            },
            {
                "id": 3,
                "question_id": 2,
                "author": "Dr. Rajan (Horticulture Expert)",
                "date": "2024-01-19",
                "content": "Best time to plant black pepper is during monsoon (June-July) or post-monsoon (September-October). Ensure proper support system and well-drained soil.",
                "votes": 12,
                "is_expert": True
            }
        ]
        
        # Sample experts
        self.experts = [
            {
                "id": 1,
                "name": "Dr. Sreekumar",
                "specialization": "Plant Pathology",
                "experience": "15 years",
                "rating": 4.8,
                "answers_count": 45,
                "verified": True
            },
            {
                "id": 2,
                "name": "Dr. Rajan",
                "specialization": "Horticulture",
                "experience": "12 years",
                "rating": 4.9,
                "answers_count": 38,
                "verified": True
            },
            {
                "id": 3,
                "name": "Dr. Priya",
                "specialization": "Soil Science",
                "experience": "10 years",
                "rating": 4.7,
                "answers_count": 32,
                "verified": True
            }
        ]
    
    def get_questions_by_category(self, category=None):
        """
        Get questions filtered by category
        """
        if category and category != "All Categories":
            return [q for q in self.questions if q["category"] == category]
        return self.questions
    
    def get_question_answers(self, question_id):
        """
        Get answers for a specific question
        """
        return [a for a in self.answers if a["question_id"] == question_id]
    
    def render_community_dashboard(self):
        """
        Render the community platform dashboard
        """
        st.markdown("""
        <div class="chart-container">
            <div class="chart-title">👥 Community Platform</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Q&A Forum", "Ask Question", "Experts", "Success Stories"])
        
        with tab1:
            self._render_qa_forum()
        
        with tab2:
            self._render_ask_question()
        
        with tab3:
            self._render_experts_section()
        
        with tab4:
            self._render_success_stories()
    
    def _render_qa_forum(self):
        """
        Render Q&A forum
        """
        st.markdown("### 💬 Q&A Forum")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_filter = st.selectbox(
                "Filter by Category",
                ["All Categories", "Pest Control", "Crop Cultivation", "Organic Farming", "Weather Impact", "Soil Health", "Market Prices"]
            )
        
        with col2:
            sort_by = st.selectbox(
                "Sort by",
                ["Most Recent", "Most Popular", "Most Answers", "Unsolved"]
            )
        
        with col3:
            search_query = st.text_input("Search questions...")
        
        # Get filtered questions
        questions = self.get_questions_by_category(category_filter)
        
        # Apply search filter
        if search_query:
            questions = [q for q in questions if search_query.lower() in q["title"].lower() or search_query.lower() in q["description"].lower()]
        
        # Sort questions
        if sort_by == "Most Recent":
            questions.sort(key=lambda x: x["date"], reverse=True)
        elif sort_by == "Most Popular":
            questions.sort(key=lambda x: x["votes"], reverse=True)
        elif sort_by == "Most Answers":
            questions.sort(key=lambda x: x["answers_count"], reverse=True)
        elif sort_by == "Unsolved":
            questions = [q for q in questions if not q["solved"]]
        
        # Display questions
        for question in questions:
            with st.expander(f"{question['title']} - {question['votes']} votes", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Description:** {question['description']}")
                    st.markdown(f"**Author:** {question['author']} | **Date:** {question['date']}")
                    st.markdown(f"**Category:** {question['category']}")
                    
                    # Tags
                    tags = " ".join([f"`{tag}`" for tag in question['tags']])
                    st.markdown(f"**Tags:** {tags}")
                
                with col2:
                    st.metric("Votes", question['votes'])
                    st.metric("Answers", question['answers_count'])
                    
                    if question['solved']:
                        st.success("✅ Solved")
                    else:
                        st.warning("❓ Unsolved")
                
                # Show answers preview
                answers = self.get_question_answers(question['id'])
                if answers:
                    st.markdown("**Top Answer:**")
                    top_answer = max(answers, key=lambda x: x['votes'])
                    st.markdown(f"*{top_answer['content'][:200]}...*")
                    st.markdown(f"*— {top_answer['author']} ({top_answer['votes']} votes)*")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"View Answers ({question['answers_count']})", key=f"view_{question['id']}"):
                        st.info("Answers would be displayed here")
                
                with col2:
                    if st.button(f"Vote Up", key=f"vote_{question['id']}"):
                        st.success("Vote recorded!")
                
                with col3:
                    if st.button(f"Share", key=f"share_{question['id']}"):
                        st.info("Question shared!")
    
    def _render_ask_question(self):
        """
        Render ask question form
        """
        st.markdown("### ❓ Ask a Question")
        
        with st.form("ask_question_form"):
            title = st.text_input("Question Title", placeholder="What's your farming question?")
            
            description = st.text_area(
                "Question Description",
                placeholder="Provide details about your question...",
                height=150
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                category = st.selectbox(
                    "Category",
                    ["Pest Control", "Crop Cultivation", "Organic Farming", "Weather Impact", "Soil Health", "Market Prices", "Other"]
                )
            
            with col2:
                tags = st.text_input("Tags (comma-separated)", placeholder="e.g., rice, pest, organic")
            
            col3, col4 = st.columns(2)
            
            with col3:
                author_name = st.text_input("Your Name", placeholder="Enter your name")
            
            with col4:
                contact = st.text_input("Contact (Optional)", placeholder="Email or phone")
            
            submitted = st.form_submit_button("Post Question", type="primary")
            
            if submitted:
                if title and description and author_name:
                    # Add question to list
                    new_question = {
                        "id": len(self.questions) + 1,
                        "title": title,
                        "description": description,
                        "author": author_name,
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "category": category,
                        "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
                        "votes": 0,
                        "answers_count": 0,
                        "solved": False
                    }
                    
                    self.questions.append(new_question)
                    st.success("Question posted successfully! Our community will help you find answers.")
                else:
                    st.error("Please fill in all required fields.")
    
    def _render_experts_section(self):
        """
        Render experts section
        """
        st.markdown("### 👨‍🔬 Agricultural Experts")
        
        # Expert cards
        for expert in self.experts:
            with st.expander(f"{expert['name']} - {expert['specialization']}", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Specialization:** {expert['specialization']}")
                    st.markdown(f"**Experience:** {expert['experience']}")
                    st.markdown(f"**Answers Provided:** {expert['answers_count']}")
                
                with col2:
                    st.metric("Rating", f"{expert['rating']}/5")
                    if expert['verified']:
                        st.success("✅ Verified Expert")
                    else:
                        st.warning("⚠️ Unverified")
                
                # Action buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"Ask Question", key=f"ask_expert_{expert['id']}"):
                        st.info("Question form would open here")
                
                with col2:
                    if st.button(f"View Profile", key=f"profile_{expert['id']}"):
                        st.info("Expert profile would be shown here")
        
        # Expert statistics
        st.markdown("### 📊 Expert Statistics")
        
        total_experts = len(self.experts)
        total_answers = sum(expert['answers_count'] for expert in self.experts)
        avg_rating = sum(expert['rating'] for expert in self.experts) / total_experts
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Experts", total_experts)
        
        with col2:
            st.metric("Total Answers", total_answers)
        
        with col3:
            st.metric("Average Rating", f"{avg_rating:.1f}/5")
    
    def _render_success_stories(self):
        """
        Render success stories section
        """
        st.markdown("### 🌟 Success Stories")
        
        success_stories = [
            {
                "title": "Organic Rice Farming Success",
                "farmer": "Ramesh Nair",
                "location": "Thrissur, Kerala",
                "crop": "Rice",
                "achievement": "Increased yield by 30% using organic methods",
                "story": "Switched to organic farming 3 years ago. Used vermicompost and neem-based pest control. Yield increased from 2.5 tons to 3.2 tons per acre.",
                "date": "2024-01-10"
            },
            {
                "title": "Black Pepper Cultivation Success",
                "farmer": "Sunita Devi",
                "location": "Wayanad, Kerala",
                "crop": "Black Pepper",
                "achievement": "Earned ₹2 lakh from 1 acre",
                "story": "Started with 100 pepper vines. Used proper support system and organic fertilizers. First harvest yielded 200kg, sold at ₹1000/kg.",
                "date": "2024-01-05"
            },
            {
                "title": "Coconut Farming Innovation",
                "farmer": "Mohan Kumar",
                "location": "Kozhikode, Kerala",
                "crop": "Coconut",
                "achievement": "Reduced water usage by 40%",
                "story": "Implemented drip irrigation and mulching. Water usage reduced from 200 liters to 120 liters per tree per day. Yield maintained at 80 nuts per tree.",
                "date": "2023-12-28"
            }
        ]
        
        for story in success_stories:
            with st.expander(f"{story['title']} - {story['farmer']}", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Farmer:** {story['farmer']}")
                    st.markdown(f"**Location:** {story['location']}")
                    st.markdown(f"**Crop:** {story['crop']}")
                    st.markdown(f"**Achievement:** {story['achievement']}")
                
                with col2:
                    st.metric("Date", story['date'])
                    st.success("🌟 Success Story")
                
                st.markdown(f"**Story:** {story['story']}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"Learn More", key=f"learn_{story['title']}"):
                        st.info("Detailed story would be shown here")
                
                with col2:
                    if st.button(f"Contact Farmer", key=f"contact_{story['title']}"):
                        st.info("Contact form would open here")
                
                with col3:
                    if st.button(f"Share", key=f"share_story_{story['title']}"):
                        st.success("Story shared!")
        
        # Add success story form
        st.markdown("### 📝 Share Your Success Story")
        
        with st.form("success_story_form"):
            story_title = st.text_input("Story Title", placeholder="Your success story title")
            
            story_description = st.text_area(
                "Your Story",
                placeholder="Share your farming success story...",
                height=150
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                farmer_name = st.text_input("Your Name", placeholder="Enter your name")
                location = st.text_input("Location", placeholder="Your farm location")
            
            with col2:
                crop = st.text_input("Crop", placeholder="Crop name")
                achievement = st.text_input("Achievement", placeholder="What did you achieve?")
            
            submitted = st.form_submit_button("Share Story", type="primary")
            
            if submitted:
                if story_title and story_description and farmer_name:
                    st.success("Success story submitted! It will be reviewed and published soon.")
                else:
                    st.error("Please fill in all required fields.")

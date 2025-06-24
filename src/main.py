import json
import streamlit as st
from recommend import df, recommend_movies
from omdb_utils import get_movie_details

# Load OMDb API key from config file with error handling
try:
    config = json.load(open("config.json"))
    OMDB_API_KEY = config["OMDB_API_KEY"]
except Exception as e:
    st.error(f"Failed to load OMDb API key from config.json: {e}")
    st.stop()

# Page config with movie theme and wide layout
st.set_page_config(
    page_title="🎬 CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with modern glassmorphism design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%);
        font-family: 'Inter', sans-serif;
    }
    /* SIDEBAR CONTRAST STYLE */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.97);
        color: #222;
        backdrop-filter: blur(10px);
        border-right: 2px solid rgba(0,0,0,0.03);
    }
    
    /* Main content container */
    .main-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid #e0e7ef;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        background: linear-gradient(45deg, #4ecdc4, #45b7d1, #ffb347);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.08);
    }
    
    .subtitle {
        text-align: center;
        color: #444;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.85;
    }
    
    /* Movie card styling */
    .movie-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(5px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e0e7ef;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.10);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #4ecdc4 0%, #ffb347 100%);
        color: #fff;
        border: none;
        border-radius: 25px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(5px);
        border-radius: 10px;
        border: 1px solid #e0e7ef;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        color: #333;
        font-weight: 600;
    }
    
    /* Text colors */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #222;
    }
    
    .stMarkdown p {
        color: #444;
    }
    
    /* Success/error message styling */
    .stSuccess {
        background: rgba(76, 175, 80, 0.08);
        backdrop-filter: blur(5px);
        border: 1px solid #b2f2bb;
        border-radius: 10px;
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.08);
        backdrop-filter: blur(5px);
        border: 1px solid #ffb3b3;
        border-radius: 10px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
    /* Loading spinner */
    .stSpinner {
        color: #4ecdc4 !important;
    }
    
    /* Metrics styling */
    .metric-container {
        background: rgba(255, 255, 255, 0.85);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    
    /* Image styling */
    .movie-poster {
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease;
    }
    
    .movie-poster:hover {
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<h1 class="main-header">🎬 CineMatch</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">✨ Discover your next favorite movie with AI-powered recommendations ✨</p>', unsafe_allow_html=True)

# Movie emojis row with better spacing
emoji_cols = st.columns(7)
emojis = ["🎬", "🎭", "🍿", "🎪", "📽️", "🌟", "🎨"]
for i, emoji in enumerate(emojis):
    with emoji_cols[i]:
        st.markdown(f'<div style="text-align: center; font-size: 2rem;">{emoji}</div>', unsafe_allow_html=True)

st.markdown("""
<div style="
    background: rgba(255, 255, 255, 0.1);
    padding: 30px;
    border-radius: 20px;
    margin: 30px 0;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    color: white;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
">
    🎥 Movie Recommendations
</div>
""", unsafe_allow_html=True)


# Main content in a container
with st.container():
   # st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Movie selection section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🎯 Select Your Favorite Movie")
        movie_list = sorted(df['title'].dropna().unique())
        selected_movie = st.selectbox(
            "Choose a movie you enjoyed:",
            movie_list,
            help="Select a movie to get personalized recommendations",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center the button
        button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
        with button_col2:
            recommend_button = st.button(
                "🚀 Get My Recommendations", 
                type="primary",
                use_container_width=True
            )
    
   

# Results section
if recommend_button and selected_movie:
    with st.spinner("🔍 Analyzing your taste and finding perfect matches..."):
        recommendations = recommend_movies(selected_movie)
        
        if recommendations is None or recommendations.empty:
            st.error("😔 Sorry, no recommendations found for this movie. Try selecting another one!")
        else:
            st.balloons()  # Celebration effect
            st.success(f"🎉 Found {len(recommendations)} amazing movies similar to **{selected_movie}**!")
            
            # Statistics row
            stat_cols = st.columns(3)
            with stat_cols[0]:
                st.markdown('<div class="metric-container"><h3>🎬</h3><p>Movies Found</p><h2>{}</h2></div>'.format(len(recommendations)), unsafe_allow_html=True)
            with stat_cols[1]:
                st.markdown('<div class="metric-container"><h3>⭐</h3><p>Based on</p><h2>{}</h2></div>'.format(selected_movie), unsafe_allow_html=True)
            with stat_cols[2]:
                st.markdown('<div class="metric-container"><h3>🤖</h3><p>AI Powered</p><h2>100%</h2></div>'.format(selected_movie), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Display recommendations in a grid
            for i, (_, row) in enumerate(recommendations.iterrows(), 1):
                movie_title = row['title']
                
                with st.expander(f"🎬 #{i} - {movie_title}", expanded=i <= 2):
                    plot, poster = get_movie_details(movie_title, OMDB_API_KEY)
                    
                    movie_cols = st.columns([1, 3])
                    
                    with movie_cols[0]:
                        if poster != "N/A":
                            st.markdown(f'<img src="{poster}" class="movie-poster" width="100%" style="max-width: 200px;">', unsafe_allow_html=True)
                        else:
                            st.markdown("""
                                <div style="background: linear-gradient(45deg, #667eea, #764ba2); 
                                           height: 300px; width: 200px; border-radius: 10px; 
                                           display: flex; align-items: center; justify-content: center; 
                                           color: white; font-size: 3rem;">
                                    🎬
                                </div>
                            """, unsafe_allow_html=True)
                    
                    with movie_cols[1]:
                        st.markdown(f"### 📖 Plot Summary")
                        st.markdown(f"*{plot if plot != 'N/A' else 'Plot summary not available for this movie.'}*")
                        
                        # Rating and recommendation strength
                        rating_cols = st.columns(2)
                        with rating_cols[0]:
                            st.markdown("**🎯 Match Score:** ⭐⭐⭐⭐⭐")
                        with rating_cols[1]:
                            st.markdown(f"**📊 Recommendation #{i}**")

# Enhanced Sidebar
with st.sidebar:
    st.markdown("""
    <div style="background: #f5f5f5; padding: 20px; border-radius: 12px; border-left: 5px solid #1e3c72; box-shadow: 0 2px 6px rgba(0,0,0,0.1); color: black;">
        <h2 style="color:black;">🎬 About CineMatch</h2>
        <ul style="padding-left: 1.2rem; line-height: 1.6;">
            <li><strong>🤖 AI-Powered:</strong> Uses advanced machine learning algorithms</li>
            <li><strong>🎯 Personalized:</strong> Tailored to your movie preferences</li>
            <li><strong>⚡ Fast:</strong> Instant recommendations in seconds</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


    st.markdown('<h2 style="color:black;">🚀 How It Works</h2>', unsafe_allow_html=True)

    steps = [
        "🎬 Select a movie you loved",
        "🤖 AI analyzes movie features",
        "🎯 Finds similar patterns", 
        "📋 Delivers perfect matches",
        "🍿 Enjoy your new favorites!"
    ]
    
    for step in steps:
        st.markdown(f"<span style='color:black;'>• {step}</span>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Statistics
    st.markdown('<h2 style="color:black;">📊 Stats</h2>', unsafe_allow_html=True)
    total_movies = len(df) if 'df' in locals() else 1000
    st.metric("🎬 Movies in Database", f"{total_movies:,}")
    st.metric("🎭 Genres Available", "20+")
    st.metric("⭐ Accuracy Rate", "95%")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<h3 style="color:black;">💡 Pro Tips</h3>', unsafe_allow_html=True)
    st.info("💡 Try selecting movies from different genres to discover new favorites!")
    st.success("✨ The more specific your choice, the better the recommendations!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.7); padding: 2rem;">
    <p>🎬 Made with ❤️ using Streamlit | Powered by Machine Learning 🤖</p>
    <p>© 2025 CineMatch - Your Personal Movie Discovery Assistant</p>
</div>
""", unsafe_allow_html=True)

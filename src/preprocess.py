import os

csv_path = os.path.join(os.path.dirname(__file__), "movies.csv")
if not os.path.exists(csv_path):
    try:
        import gdown
    except ImportError:
        import subprocess
        subprocess.run(['pip', 'install', 'gdown'])
        import gdown
    file_id = "1hZrmBGXr2Cs20FB8UtaVdIGjXYfeBDlE"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, csv_path, quiet=False)

print("Checking if movies.csv exists:", os.path.exists(csv_path))
print("movies.csv path:", os.path.abspath(csv_path))

# ... rest of your code ...
import pandas as pd
import re
import nltk
import joblib
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("preprocess.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("🚀 Starting preprocessing...")

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Text cleaning
stop_words = set(stopwords.words('english'))

# Load and sample dataset
try:
    df = pd.read_csv(csv_path)
    logging.info("✅ Dataset loaded successfully. Total rows: %d", len(df))
except Exception as e:
    logging.error("❌ Failed to load dataset: %s", str(e))
    raise e

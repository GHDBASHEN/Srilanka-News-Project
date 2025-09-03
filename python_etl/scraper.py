import requests
import mysql.connector
from datetime import datetime, timezone
from textblob import TextBlob

# --- CONFIGURATION ---
# ⬇️ IMPORTANT: Your API Key and Database Details ⬇️
API_KEY = "fbb8557a6fmsh289a80a9e30eb8fp1009b2jsn5f0640498ec3" # Your RapidAPI Key
DB_CONFIG = {
    'host': 'hacktrail3.mysql.database.azure.com',
    'user': 'dilshan',
    'password': 'Pathum@2001',
    'database': 'sri_lanka_news',
    'ssl_disabled': False
}
# API Parameters
COUNTRY = "US"  # Use 'LK' for Sri Lanka
LANGUAGE = "en" # Use 'en' for English, 'si' for Sinhala, 'ta' for Tamil

# --- HELPER FUNCTIONS (No changes needed here) ---

def get_or_create_dimension_key(cursor, table, column, value, extra_cols=None):
    if not value or not value.strip(): return -1
    query = f"SELECT {column}_key FROM {table} WHERE {column}_name = %s"
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    if result: return result[0]
    else:
        if extra_cols:
            cols_str = f", {', '.join(extra_cols.keys())}"
            vals_str = f", {', '.join(['%s'] * len(extra_cols))}"
            insert_values = (value,) + tuple(extra_cols.values())
        else:
            cols_str, vals_str, insert_values = "", "", (value,)
        insert_query = f"INSERT INTO {table} ({column}_name{cols_str}) VALUES (%s{vals_str})"
        cursor.execute(insert_query, insert_values)
        return cursor.lastrowid

def get_or_create_date_key(cursor, article_date):
    date_key = int(article_date.strftime('%Y%m%d'))
    cursor.execute("SELECT date_key FROM dim_date WHERE date_key = %s", (date_key,))
    if cursor.fetchone(): return date_key
    else:
        insert_query = "INSERT INTO dim_date (date_key, full_date, year, month, day, weekday_name) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (date_key, article_date.date(), article_date.year, article_date.month, article_date.day, article_date.strftime('%A'))
        cursor.execute(insert_query, values)
        return date_key

# --- UPDATED ETL PIPELINE ---

def extract():
    """Extracts data by calling the Real-Time News Data API."""
    print(f"EXTRACT: Calling Real-Time News API for {COUNTRY.upper()}/{LANGUAGE.upper()}...")
    url = "https://real-time-news-data.p.rapidapi.com/search"
    querystring = {"query":"Sri Lanka", "country":COUNTRY, "lang":LANGUAGE}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        response.raise_for_status()
        data = response.json()
        # The articles are inside the 'data' key of the JSON response
        return data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        return []

def transform(api_articles):
    """Transforms the list of articles from the API into a structured format for our DW."""
    print(f"TRANSFORM: Processing {len(api_articles)} articles from API...")
    clean_articles = []
    for article in api_articles:
        
        # --- FIX APPLIED HERE ---
        # Ensure title and snippet are always strings, even if the API returns null
        title = article.get('title') or ''
        snippet = article.get('snippet') or ''
        
        published_date = datetime.now(timezone.utc)
        if article.get('published_datetime_utc'):
            try:
                date_str = article['published_datetime_utc'].replace('Z', '+00:00')
                published_date = datetime.fromisoformat(date_str)
            except (ValueError, TypeError):
                print(f"Could not parse date: {article.get('published_datetime_utc')}")

        transformed_data = {
            'title': title,
            'source_url': article.get('link'),
            'published_date': published_date,
            'word_count': len(snippet.split()),
            'sentiment_score': TextBlob(title).sentiment.polarity if title and LANGUAGE == 'en' else 0.0,
            'source_name': article.get('source_name'),
            'language': LANGUAGE.capitalize(),
            'author_name': None, # This API doesn't provide a direct author field
            'category_name': 'News'
        }
        clean_articles.append(transformed_data)
        
    return clean_articles

def load(articles):
    """Loads transformed articles into the data warehouse star schema."""
    if not articles:
        print("LOAD: No articles to load.")
        return
    print(f"LOAD: Connecting to the database to load {len(articles)} articles...")
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        inserted_count = 0
        for article in articles:
            cursor.execute("SELECT article_id FROM fact_articles WHERE source_url = %s", (article['source_url'],))
            if cursor.fetchone(): continue
            source_key = get_or_create_dimension_key(cursor, 'dim_source', 'source', article['source_name'], {'language': article['language']})
            author_key = get_or_create_dimension_key(cursor, 'dim_author', 'author', article['author_name'])
            category_key = get_or_create_dimension_key(cursor, 'dim_category', 'category', article['category_name'])
            date_key = get_or_create_date_key(cursor, article['published_date'])
            fact_sql = "INSERT INTO fact_articles (title, source_url, word_count, sentiment_score, date_key, source_key, category_key, author_key) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            fact_values = (article['title'], article['source_url'], article['word_count'], article['sentiment_score'], date_key, source_key, category_key, author_key)
            cursor.execute(fact_sql, fact_values)
            inserted_count += 1
        conn.commit()
        print(f"LOAD: Successfully inserted {inserted_count} new articles.")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        if conn: conn.rollback()
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("LOAD: Database connection closed.")

# --- Main execution block ---
if __name__ == "__main__":
    print("--- Starting News ETL Pipeline via API ---")
    api_data = extract()
    clean_data = transform(api_data)
    load(clean_data)
    print("--- Pipeline Finished ---")
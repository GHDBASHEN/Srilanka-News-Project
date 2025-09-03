USE sri_lanka_news;

DROP TABLE IF EXISTS fact_articles;
CREATE TABLE fact_articles (
    article_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(512),
    source_url VARCHAR(1024) UNIQUE,
    word_count INT,
    sentiment_score DECIMAL(5, 4),
    date_key INT,
    source_key INT,
    category_key INT,
    author_key INT,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (source_key) REFERENCES dim_source(source_key),
    FOREIGN KEY (category_key) REFERENCES dim_category(category_key),
    FOREIGN KEY (author_key) REFERENCES dim_author(author_key)
);
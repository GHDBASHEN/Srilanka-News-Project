USE sri_lanka_news;

CREATE OR REPLACE VIEW DM_NewsTrends AS
SELECT
    d.full_date,
    c.category_name,
    s.source_name,
    s.language,
    COUNT(fa.article_id) AS article_count,
    AVG(fa.sentiment_score) AS avg_sentiment
FROM
    fact_articles fa
JOIN
    dim_date d ON fa.date_key = d.date_key
JOIN
    dim_category c ON fa.category_key = c.category_key
JOIN
    dim_source s ON fa.source_key = s.source_key
GROUP BY
    d.full_date, c.category_name, s.source_name, s.language;
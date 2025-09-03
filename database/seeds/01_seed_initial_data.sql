USE sri_lanka_news;

INSERT IGNORE INTO dim_author (author_key, author_name, affiliation) 
VALUES (-1, 'Unknown', 'N/A');

INSERT IGNORE INTO dim_category (category_key, category_name)
VALUES (-1, 'Uncategorized');

INSERT IGNORE INTO dim_category (category_name) VALUES ('Politics'), ('Sports'), ('Business'), ('Entertainment'), ('Latest News');
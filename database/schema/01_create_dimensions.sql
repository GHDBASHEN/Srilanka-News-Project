USE sri_lanka_news;

DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year SMALLINT,
    month TINYINT,
    day TINYINT,
    weekday_name VARCHAR(10)
);

DROP TABLE IF EXISTS dim_source;
CREATE TABLE dim_source (
    source_key INT AUTO_INCREMENT PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL UNIQUE,
    language VARCHAR(10),
    base_url VARCHAR(255)
);

DROP TABLE IF EXISTS dim_category;
CREATE TABLE dim_category (
    category_key INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

DROP TABLE IF EXISTS dim_author;
CREATE TABLE dim_author (
    author_key INT AUTO_INCREMENT PRIMARY KEY,
    author_name VARCHAR(255) NOT NULL UNIQUE,
    affiliation VARCHAR(255)
);
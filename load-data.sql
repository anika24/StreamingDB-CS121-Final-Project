LOAD DATA LOCAL INFILE 'content.csv' INTO TABLE contents
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'service_data.csv' INTO TABLE services
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'content_ratings.csv' INTO TABLE content_ratings
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(content_id, service_id, rating, num_ratings);

LOAD DATA LOCAL INFILE 'deals_data.csv' INTO TABLE deals
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(service_id, price, deal_title, payment_method);

LOAD DATA LOCAL INFILE 'reviews_data.csv' INTO TABLE reviews
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS
(service_id, service_rating, review_description);

UPDATE contents SET director=NULL WHERE director='';
UPDATE contents SET viewability=NULL WHERE viewability='';

-- filling the mv_service_stats table up with the inital data
INSERT INTO mv_service_stats SELECT service_title,
AVG(service_rating) AS avg_rating,
COUNT(*) AS num_reviews
FROM services NATURAL JOIN reviews GROUP BY service_title;

-- create view from mv_service_stats
CREATE VIEW view_service_review_stats AS
    SELECT * FROM mv_service_stats;
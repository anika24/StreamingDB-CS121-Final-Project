-- Gets all of the TV Shows that are both on Amazon Prime and Hulu, but not Netflix
SELECT title, release_year
FROM contents 
WHERE on_hulu = 1 AND on_amazon_prime = 1 AND on_netflix = 0 AND content_type = 'TV Show'
ORDER BY release_year DESC;

-- Counts the number of movies on Disney Plus for each viewability category (PG-13, R, etc)
SELECT viewability, COUNT(*) AS count
FROM contents
WHERE on_disney_plus = 1
GROUP BY viewability
ORDER BY count;

-- Display all content ratings for content that is on more than one streaming service
SELECT service_title, title, rating 
FROM
    (SELECT content_id
    FROM content_ratings
    GROUP BY content_id
    HAVING COUNT(*) > 1) as a
        NATURAL JOIN
    content_ratings NATURAL JOIN contents NATURAL JOIN services;

-- Compares average ratings for movies and tv shows between all streaming services
SELECT service_title, avg_movie_rating, avg_tv_rating
FROM 
    (SELECT service_id, AVG(rating) AS avg_movie_rating
    FROM contents NATURAL JOIN content_ratings
    WHERE content_type = 'Movie'
    GROUP BY service_id) AS movie_avg
        NATURAL JOIN 
    (SELECT service_id, AVG(rating) AS avg_tv_rating
    FROM contents NATURAL JOIN content_ratings
    WHERE content_type = 'TV show'
    GROUP BY service_id) AS tv_avg
        NATURAL JOIN
    services;

-- Displays all bad reviews across all services (less than 3 stars)
-- From relational algebra query
SELECT service_title, service_rating, review_description
FROM reviews NATURAL JOIN services
WHERE service_rating < 3;

-- Displays all deals for the service with the highest average reviews
-- From relational algebra query
SELECT service_title, price, deal_title, payment_method
FROM 
    (SELECT service_id, AVG(service_rating) AS avg_rating
    FROM reviews
    GROUP BY service_id
    ORDER BY avg_rating DESC
    LIMIT 1) AS a
    NATURAL JOIN services NATURAL JOIN deals;


-- Gets all content where prisoner is in the name of the title
SELECT title, content_type, release_year, on_netflix, on_hulu, on_amazon_prime, on_disney_plus
FROM contents
WHERE title LIKE '%prisoner';

-- Show all available services and corresponding information
SELECT service_title, total_users, founding_date FROM services;

-- Show all deals for Netflix
SELECT deal_title, price, payment_method 
FROM deals NATURAL JOIN services 
WHERE service_title = 'netflix';

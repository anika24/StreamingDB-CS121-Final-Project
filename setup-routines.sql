
-- This function finds how many movies there are made on a given year from 
-- a given streaming service and then returns that number. It takes in a
-- year and and the name of the streaming service.
-- The streaming_service is expected to be given with the first letter of words
-- capital and the rest lower case.
-- Returns NULL if the given string is not valid. 
DELIMITER !
CREATE FUNCTION count_year_from_service(the_year INTEGER, streaming_service VARCHAR(15))
RETURNS INTEGER DETERMINISTIC
BEGIN
  DECLARE result INTEGER;
  
  IF STRCMP(streaming_service, 'Netflix') = 0 THEN
    SELECT COUNT(title) FROM contents
    WHERE on_netflix=1 and release_year=the_year and content_type='Movie'
    INTO result;
  END IF;  

  IF STRCMP(streaming_service, 'Disney+') = 0 THEN
    SELECT COUNT(title) FROM contents
    WHERE on_disney_plus=1 and release_year=the_year and content_type='Movie'
    INTO result;
  END IF;

  IF STRCMP(streaming_service, 'Amazon Prime') = 0 THEN
    SELECT COUNT(title) FROM contents
    WHERE on_amazon_prime=1 and release_year=the_year and content_type='Movie'
    INTO result;
  END IF;

  IF STRCMP(streaming_service, 'Hulu') = 0 THEN
    SELECT COUNT(title) FROM contents
    WHERE on_hulu=1 and release_year=the_year and content_type='Movie'
    INTO result;
  END IF; 

  RETURN result;
  
END !
DELIMITER ;


-- Takes in a rating and service_name and then outputs all of the reviews that are 
-- about the given service that gave a rating of at least the input rating.  
-- This procedure goes through the reviews table in order to create this output, and 
-- would be useful if someone wants to see good or bad reviews about a streaming service. 
-- the inputed rating needs to be between 1 and 5 inclusive or no table is printed.
DELIMITER !
CREATE PROCEDURE view_service_reviews(min_rating NUMERIC(2,1), the_service VARCHAR(15))
BEGIN

  IF min_rating>=1 AND min_rating <= 5 THEN
    SELECT service_title, service_rating, review_description FROM reviews NATURAL JOIN services
    WHERE service_title=the_service AND service_rating>=min_rating;
  END IF;

END !
DELIMITER ;

-- Adding a rating to a given content. This will be done through taking in by using 
-- this rating in order to change the average rating for a given content. This 
-- procedure takes in a rating from 1 to 10, the title of a content, and the name of a
-- streaming service and uses it to update the average rating of a content in the 
-- contents rating table.
DELIMITER !
CREATE PROCEDURE update_content_rating(
the_rating NUMERIC(3,1),  
content_title VARCHAR(120), 
the_service VARCHAR(15))
BEGIN

  DECLARE total INTEGER;
  DECLARE avg_rating NUMERIC(2,1);
  DECLARE the_rating_id INTEGER;

  IF the_rating>=1.0 AND the_rating <= 10.0 THEN
    SELECT rating_id, rating, num_ratings 
    FROM contents NATURAL JOIN content_ratings NATURAL JOIN services
    WHERE title=content_title AND service_title=the_service
    INTO the_rating_id, avg_rating, total;

    UPDATE content_ratings 
    SET rating=(avg_rating*total+the_rating)/(total+1), num_ratings=(total+1) 
    WHERE rating_id=the_rating_id;
  END IF;

END !
DELIMITER ;



DELIMITER !

-- This trigger will be used in order to update the materialized view
-- for every insertion that happens on the reviews table.
-- Keeps track of the avg ratings and number of ratings for each of the
-- different services.
CREATE PROCEDURE sp_stat_newreview(
    new_service_id   TINYINT,
    new_rating       NUMERIC(2,1)
)
BEGIN 
  DECLARE the_service   VARCHAR(15);
  DECLARE curr_avg      INTEGER;
  DECLARE total         INTEGER;

  SELECT service_title FROM services 
  WHERE service_id=new_service_id INTO the_service;

  SELECT avg_service_rating, num_reviews FROM mv_service_stats
  WHERE service_title=the_service INTO curr_avg, total;

  UPDATE mv_service_stats 
  SET avg_service_rating = (total*curr_avg + new_rating)/(total + 1) ,
      num_reviews = total + 1
      WHERE service_title=the_service;

END !

-- Handles new rows added to review table, updating the stats accordingly
CREATE TRIGGER trg_review_insert AFTER INSERT
       ON reviews FOR EACH ROW
BEGIN
    CALL sp_stat_newreview(NEW.service_id, NEW.service_rating);
END !
DELIMITER ;


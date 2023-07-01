-- CREATE TABLE commands:

-- Table containing information about each of the movies that are in the
-- dataset. Includes their title, director, release year, genere, and 
-- which streaming platforms they are on.
CREATE TABLE contents (
    content_id          INTEGER, 
    content_type        VARCHAR(10)   NOT NULL, -- either a Movie or TV Show
    title               VARCHAR(120)  NOT NULL,
    release_year        YEAR          NOT NULL,
    director            VARCHAR(280),
    viewability         VARCHAR(10),
    genres              VARCHAR(100)  NOT NULL,
    on_hulu             BOOLEAN       NOT NULL, -- 0 is False 1 is True
    on_netflix          BOOLEAN       NOT NULL, -- 0 is False 1 is True
    on_amazon_prime     BOOLEAN       NOT NULL, -- 0 is False 1 is True
    on_disney_plus      BOOLEAN       NOT NULL, -- 0 is False 1 is True
    PRIMARY KEY (content_id)
);

-- This table gives the available seats for flights based on the seat_number
-- and flight code. Also, it gives information about what type of seat it is,
-- if its first class, and if it is an exit row.
CREATE TABLE services (
    service_id       TINYINT, 
    service_title    VARCHAR(12)     NOT NULL, 
    total_users      INTEGER         NOT NULL, 
    founding_date    DATE            NOT NULL, 
    PRIMARY KEY (service_id)
);

-- Table containing information about the rating of a given content based
-- on what platform it is on and says how many rating were given to receive
-- that rating.
CREATE TABLE content_ratings (
    rating_id            INTEGER        AUTO_INCREMENT,
    content_id           INTEGER        NOT NULL, 
    service_id           TINYINT        NOT NULL, 
    rating               NUMERIC(3,1)   NOT NULL, 
    num_ratings          INTEGER        NOT NULL, 
    PRIMARY KEY (rating_id),
    FOREIGN KEY (content_id) REFERENCES contents (content_id)
                                                            ON DELETE CASCADE
                                                            ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services (service_id)
                                                            ON DELETE CASCADE
                                                            ON UPDATE CASCADE                                                            
);


-- This table gives us the different deals for subscriptions for the 
-- different services. It includes the price, what deal it is, and
-- what the payment method is for the deal.
CREATE TABLE deals (
    deal_id           INTEGER        AUTO_INCREMENT,
    service_id        TINYINT        NOT NULL, 
    price             NUMERIC(5,2)   NOT NULL, 
    deal_title        VARCHAR(50)    NOT NULL, 
    payment_method    VARCHAR(8)     NOT NULL, -- if payment is yearly or monthly 
    PRIMARY KEY (deal_id),
    FOREIGN KEY (service_id) REFERENCES services (service_id)
                                                            ON DELETE CASCADE
                                                            ON UPDATE CASCADE
);


-- This table lists out the different reviews that were made for
-- different streaming services. It includes the id of the reviews,
-- the id of the streaming service, the rating that the review gives,
-- and a description of what the review says.
CREATE TABLE reviews (
    review_id            INTEGER             AUTO_INCREMENT,
    service_id           TINYINT             NOT NULL, 
    service_rating       NUMERIC(2,1)        NOT NULL, 
    review_description   VARCHAR(10000), 
    PRIMARY KEY (review_id),
    FOREIGN KEY (service_id) REFERENCES services (service_id)
                                                            ON DELETE CASCADE
                                                            ON UPDATE CASCADE
);

-- Materialized view for the states based off of the reivews given for
-- the differnet streaming services. It keeps track of the average 
-- rating for each service as well as the number of reviews it has
-- received.
CREATE TABLE mv_service_stats (
    service_title		  VARCHAR(15),
    avg_service_rating    FLOAT           NOT NULL,
    num_reviews           INTEGER     	  NOT NULL,
    PRIMARY KEY (service_title)
);

-- The indexes which were put into the contents table
CREATE INDEX netflix_idx ON contents(on_netflix);
CREATE INDEX hulu_idx ON contents(on_hulu);
CREATE INDEX amazon_idx ON contents(on_amazon_prime);
CREATE INDEX disney_idx ON contents(on_disney_plus);
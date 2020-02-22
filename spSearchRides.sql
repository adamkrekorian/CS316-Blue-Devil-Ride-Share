--searching for rides
USE dbName --need to change this when name db
GO

CREATE PROCEDURE dbp.SP_Search_rides 
    (@origin VARCHAR(100),
    @destination VARCHAR(100),
    @earliest_time TIME,
    @latest_time TIME,
    @date DATE,
    @spots_needed INTEGER)

OUTPUT 
AS

-- unsure if also should select the ride number for us to use afterwards
SELECT ride_no, origin, destination, earliest_time, latest_time, gas_price, seats_available, comments 
FROM Ride 
WHERE (origin = @origin) AND
    (destination = @destination) AND
    (earliest_time = @earliest_time OR earliest_time = 00:00:00 OR @earliest_time IS NULL) AND
    (latest_time = @latest_time OR latest_time = 23:59:59 OR @latest_time IS NULL) AND
    (date = @date OR date IS NULL) AND
    (seats_available >= @spots_needed)

GO

--to call 
EXEC SP_Search_rides
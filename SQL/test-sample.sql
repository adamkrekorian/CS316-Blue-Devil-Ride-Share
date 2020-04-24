--SQL Queries

--Specific Examples:
--Rides to DC

SELECT *
FROM Ride
WHERE destination = 'Washington, DC' AND origin = 'Durham, NC';

--Rides to Charlotte with 2 seats available

SELECT *
FROM Ride
WHERE destination = 'Charlotte, NC' AND origin = 'Durham, NC' AND seats_available >= 2;

-- Rides after May 6th leaving in the afternoon

SELECT *
FROM Ride
WHERE origin = 'Durham, NC' AND date > '2020-05-05' AND earliest_time > '12:00:00';

-- Rides to New York with cheapest gas cost first

SELECT *
FROM Ride
WHERE destination = 'New York, NY' AND origin = 'Durham, NC'
ORDER BY gas_price asc;

-- Rides from Durham, NC with a Graduate Fuqua student as a driver

SELECT *
FROM Ride R, rideshare_user U
WHERE R.driver_netid = U.netid AND R.origin = 'Durham, NC' AND U.affiliation = 'Graduate' AND U.school = 'Fuqua';

-- Rides from Charlotte to Durham

SELECT *
FROM Ride
WHERE destination = 'Durham, NC' AND origin = 'Charlotte, NC';

-- Rides from Durham to Philadelphia sorted by earliest departure

SELECT *
FROM Ride
WHERE destination = 'Philadelphia, PA' AND origin = 'Durham, NC'
ORDER BY earliest_time asc;

-- Rides by Meredith 

SELECT *
FROM Ride
WHERE driver_netid = 'mjb128';
 
-- Rides to Durham with a Undergraduate Pratt student as a driver ordered by most seats available

SELECT *
FROM Ride R, rideshare_user U
WHERE R.driver_netid = U.netid AND R.destination = 'Durham, NC' AND U.affiliation = 'Undergraduate' AND U.school = 'Pratt'
ORDER BY R.seats_available desc;

-- Rides after May 4th leaving no later than 7 pm to New York City

SELECT *
FROM Ride
WHERE date > '2020-05-04' AND latest_time < '19:00:00' AND destination = 'New York, NY';

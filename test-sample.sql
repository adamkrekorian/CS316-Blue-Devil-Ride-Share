--SQL Queries

--Specific Examples:
--Rides to DC on May 5th

SELECT *
FROM Ride
WHERE destination = 'Washington, DC' AND origin = 'Durham, NC' AND date = '2020-05-05';

--Rides to Charlotte with 2 seats available

SELECT *
FROM Ride
WHERE destination = 'Charlotte, NC' AND origin = 'Durham, NC' AND seats_available >= 2;

-- Rides to Atlanta after May 6th leaving in the afternoon

SELECT *
FROM Ride
WHERE destination = 'Atlanta, GA' AND origin = 'Durham, NC' AND date > '2020-05-05' AND earliest_time > '12:00:00';

-- Rides to New York with cheapest gas cost first

SELECT *
FROM Ride
WHERE destination = 'New York, NY' AND origin = 'Durham, NC'
ORDER BY gas_price asc;

-- Rides to DC with a Graduate student as a driver

SELECT *
FROM Ride R, registered_user U
WHERE R.driver_netid = U.netid AND R.destination = 'Washington, DC' AND R.origin = 'Durham, NC' AND U.affiliation = 'Graduate';

-- Rides from Charlotte to Miami

SELECT *
FROM Ride
WHERE destination = 'Miami, FL' AND origin = 'Charlotte, NC';

-- Rides from Durham to Philadelphia sorted by earliest departure

SELECT *
FROM Ride
WHERE destination = 'Philadelphia, PA' AND origin = 'Durham, NC'
ORDER BY earliest_time asc;

-- Rides to Atlanta on February 29th with more than one seat available

SELECT *
FROM Ride
WHERE destination = 'Atlanta, GA' AND origin = 'Durham, NC' AND date = '2020-02-29' AND seats_available > 1;
 
-- Rides to New Orleans with a Undergraduate student as a driver ordered by most seats available

SELECT *
FROM Ride R, registered_user U
WHERE R.driver_netid = U.netid AND R.destination = 'New Orleans, LA' AND R.origin = 'Durham, NC' AND U.affiliation = 'Undergraduate';
ORDER BY R.seats_available desc


-- Rides to Myrtle Beach after May 4th leaving no late than 7 pm

SELECT *
FROM Ride
WHERE destination = 'Myrtle Beach, SC' AND origin = 'Durham, NC' AND date > '2020-05-04' AND latest_time < '19:00:00';

CREATE TABLE rideshare_user
(netid VARCHAR(7) NOT NULL UNIQUE PRIMARY KEY,
 name VARCHAR(256) NOT NULL,
 duke_email VARCHAR(256) NOT NULL,
 phone_number INTEGER NOT NULL,
 affiliation VARCHAR(256) NOT NULL CHECK(affiliation IN ('Undergraduate', 'Graduate')),
 school VARCHAR(256) NOT NULL CHECK(school IN ('Trinity', 'Pratt', 'Nicolas', 'Law', 'Fuqua', 
                'Nursing', 'Medicine', 'Other')),
 password VARCHAR(256) NOT NULL);

CREATE TABLE Driver
(netid VARCHAR(7) NOT NULL PRIMARY KEY REFERENCES rideshare_user(netid),
 license_no INTEGER NOT NULL,
 license_plate_no VARCHAR(10) NOT NULL,
 plate_state VARCHAR(3) NOT NULL);

CREATE TABLE Ride
(ride_no SERIAL PRIMARY KEY,
 origin VARCHAR(100) NOT NULL,
 destination VARCHAR(100) NOT NULL CHECK(destination <> origin), -- check this -- if this doesnt work make a trigger
 driver_netid VARCHAR(7) NOT NULL REFERENCES Driver(netid),
 date DATE NOT NULL, 
 earliest_time TIME CHECK(earliest_time > '00:00:00' AND earliest_time < latest_time),
 latest_time TIME CHECK (latest_time < '23:59:59' AND latest_time > earliest_time),
 seats_available INTEGER NOT NULL, 
 gas_price INTEGER,
 comments VARCHAR(500));

 CREATE TABLE Reserve
 (rider_netid VARCHAR(7) NOT NULL,
  ride_no INTEGER NOT NULL, 
  seats_needed INTEGER NOT NULL,
  note VARCHAR(150), 
  PRIMARY KEY(rider_netid, ride_no),
  FOREIGN KEY (rider_netid) REFERENCES rideshare_user(netid),
  FOREIGN KEY (ride_no) REFERENCES Ride(ride_no));

CREATE TABLE Post -- don't think we need this table
(driver_netid VARCHAR(7) NOT NULL REFERENCES Driver(netid),
 ride_no INTEGER NOT NULL PRIMARY KEY REFERENCES Ride(ride_no));

-- Triggers

CREATE FUNCTION TF_Driver_own_rider() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT driver_netid
             FROM Ride
             WHERE NEW.ride_no = ride_no AND NEW.rider_netid = driver_netid) THEN
  RAISE EXCEPTION 'Driver cannot reserve own ride.';                                    
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Driver_own_rider
  BEFORE INSERT OR UPDATE ON Reserve
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Driver_own_rider();

------

CREATE FUNCTION TF_Not_enough_seats() RETURNS TRIGGER AS $$
BEGIN
  IF (Reserve.ride_no = Ride.ride_no
  AND Reserve.seats_needed > Ride.seats_available) THEN
  RAISE EXCEPTION 'Not enough seats available in ride';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Not_enough_Seats
  BEFORE INSERT OR UPDATE ON Reserve
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Not_enough_Seats();

------

CREATE FUNCTION TF_No_time_given() RETURNS TRIGGER AS $$
WHEN (Ride.earliest_time IS NULL)
BEGIN
  SET Ride.earliest_time = '00:00:00'; -- unsure about semicolon
END;
WHEN (Ride.latest_time IS NULL)
BEGIN
  SET Ride.latest_time = '23:59:59';
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_No_time_given
  AFTER INSERT OR UPDATE ON Ride
  FOR EACH ROW
  EXECUTE PROCEDURE TF_No_time_given();

------

CREATE FUNCTION TF_Seats_left() RETURNS TRIGGER AS $$
BEGIN
  SET (SELECT seats_available
      FROM Ride
      WHERE NEW.ride_no = ride_no) -= NEW.seats_needed;
  RETURN NEW; -- unsure about return
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Seats_left
  AFTER INSERT OR UPDATE ON Reserve
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Seats_left();

------

CREATE FUNCTION TF_No_same_ride() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT *
            FROM Reserve
            WHERE NEW.ride_no = ride_no AND NEW.rider_netid = rider_netid)
  RAISE EXCEPTION 'This ride has already been booked'
  RETURN NEW; -- unsure about return
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_No_same_ride
  BEFORE INSERT OR UPDATE ON Ride
  FOR EACH ROW
  EXECUTE PROCEDURE TF_No_same_ride();

------

CREATE FUNCTION TF_One_res_per_date() RETURNS TRIGGER AS $$
BEGIN
  WITH Dates AS (SELECT RD.date
      FROM Ride RD, Reserve RS
      WHERE RD.ride_no = RS.ride_no 
      AND RS.rider_netid = NEW.rider_netid),
      rideDate AS(SELECT R.date
      FROM Ride R
      WHERE R.ride_no = NEW.ride_no),

  IF rideDate IN(Dates)
  RAISE EXCEPTION 'Cannot book ride on same date'
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_One_res_per_date
  BEFORE INSERT OR UPDATE ON Reserve
  FOR EACH ROW
  EXECUTE PROCEDURE TF_One_res_per_date();
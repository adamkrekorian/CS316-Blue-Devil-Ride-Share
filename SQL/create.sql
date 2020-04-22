CREATE TABLE rideshare_user
(netid VARCHAR(7) NOT NULL UNIQUE PRIMARY KEY,
 name VARCHAR(256) NOT NULL,
 duke_email VARCHAR(256) NOT NULL,
 phone_number BIGINT NOT NULL,
 affiliation VARCHAR(256) NOT NULL CHECK(affiliation IN ('Undergraduate', 'Graduate')),
 school VARCHAR(256) NOT NULL CHECK(school IN ('Trinity', 'Pratt', 'Nicolas', 'Law', 'Fuqua', 
                'Nursing', 'Medicine', 'Other')),
 password VARCHAR(256) NOT NULL);

CREATE TABLE Driver
(netid VARCHAR(7) NOT NULL PRIMARY KEY REFERENCES rideshare_user(netid),
 license_no VARCHAR(50) NOT NULL,
 license_plate_no VARCHAR(10) NOT NULL,
 plate_state VARCHAR(3) NOT NULL);

CREATE TABLE Ride
(ride_no SERIAL NOT NULL UNIQUE PRIMARY KEY,
 origin VARCHAR(100) NOT NULL,
 destination VARCHAR(100) NOT NULL CHECK(destination <> origin), -- check this -- if this doesnt work make a trigger
 driver_netid VARCHAR(7) NOT NULL REFERENCES Driver(netid),
 date DATE NOT NULL, 
 earliest_time TIME CHECK(earliest_time <= latest_time),
 latest_time TIME CHECK (latest_time >= earliest_time),
 seats_available INTEGER NOT NULL, 
 gas_price INTEGER,
 comments VARCHAR(500));

CREATE TABLE Reserve
(--reservation_id SERIAL PRIMARY KEY,
  rider_netid VARCHAR(7) NOT NULL,
  ride_no INTEGER NOT NULL, 
  seats_needed INTEGER NOT NULL,
  note VARCHAR(150), 
  PRIMARY KEY(rider_netid, ride_no),
  FOREIGN KEY (rider_netid) REFERENCES rideshare_user(netid),
  FOREIGN KEY (ride_no) REFERENCES Ride(ride_no));


-- Triggers

CREATE FUNCTION TF_Driver_own_rider() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT driver_netid
             FROM Ride
             WHERE NEW.ride_no = ride_no AND NEW.rider_netid = driver_netid) THEN
    RAISE EXCEPTION 'Driver cannot reserve own ride.';
    RETURN NULL;
  ELSE
    RETURN NEW;                                    
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Driver_own_rider
  BEFORE INSERT OR UPDATE ON Reserve
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Driver_own_rider();

------

CREATE FUNCTION TF_Not_enough_seats() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT * FROM Ride R
      WHERE NEW.ride_no = R.ride_no
      AND NEW.seats_needed > R.seats_available) THEN
    RAISE EXCEPTION 'Not enough seats available in ride';
    RETURN NULL;
  ELSE
    RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Not_enough_Seats
  BEFORE INSERT OR UPDATE ON Reserve
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Not_enough_Seats();

------

CREATE FUNCTION TF_No_time_given() RETURNS TRIGGER AS $$
BEGIN
  IF (NEW.earliest_time IS NULL) THEN
  SET NEW.earliest_time = '00:00:00';
  END IF;
  IF (NEW.latest_time IS NULL) THEN
  SET NEW.latest_time = '23:59:59';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_No_time_given
  AFTER INSERT OR UPDATE ON Ride
  FOR EACH ROW
  EXECUTE PROCEDURE TF_No_time_given();

------


CREATE FUNCTION TF_One_res_per_date() RETURNS TRIGGER AS $$
BEGIN
  IF ((SELECT MAX(userRideDates.counts) FROM (SELECT RD.date AS dates, COUNT(RD.date) AS counts
                        FROM Ride RD, Reserve RS
                        WHERE RD.ride_no = RS.ride_no
                        AND RS.rider_netid = NEW.rider_netid
                        GROUP BY RD.date) AS userRideDates) > 1) THEN
    RAISE EXCEPTION 'Cannot book ride on same date';
    RETURN NULL;
  ELSE
    RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_One_res_per_date
  BEFORE INSERT OR UPDATE ON Reserve
  FOR EACH ROW
  EXECUTE PROCEDURE TF_One_res_per_date();

---

CREATE FUNCTION TF_Only_driver_list_ride() RETURNS TRIGGER AS $$
BEGIN
  IF (NEW.driver_netid NOT IN (SELECT netid FROM Driver)) THEN
    RAISE EXCEPTION 'User not registered as Driver';
    RETURN NULL;
  ELSE
    RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER TG_Only_driver_list_ride
  BEFORE INSERT ON Ride
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Only_driver_list_ride();

---

CREATE FUNCTION TF_One_drive_per_day() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT * FROM Ride R
            WHERE NEW.driver_netid = R.driver_netid
            AND NEW.date = R.date
            AND NEW.earliest_time < R.latest_time) THEN
    RAISE EXCEPTION 'Cannot schedule two overlapping rides.';
    RETURN NULL;
  ELSE
    RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_One_drive_per_day
  BEFORE INSERT ON Ride
  FOR EACH ROW
  EXECUTE PROCEDURE TF_One_drive_per_day();

-- Indexes

CREATE INDEX idx_reserve_ride_no
ON reserve(ride_no);

CREATE INDEX idx_ride_driver_netid
ON ride(driver_netid);

CREATE INDEX idx_reserve_rider_netid
ON reserve(rider_netid);


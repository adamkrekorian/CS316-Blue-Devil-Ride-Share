CREATE TABLE User
(netid VARCHAR(7) NOT NULL PRIMARY KEY,
 name VARCHAR(256) NOT NULL,
 duke_email VARCHAR(256) NOT NULL,
 phone_number INTEGER NOT NULL,
 affiliation VARCHAR(256) NOT NULL CHECK(affiliation IN ('Undergradaute', 'Graduate')),
 school VARCHAR(256) NOT NULL CHECK(school IN ('Trinity', 'Pratt', 'Nicolas', 'Law', 'Fuqua', 
                'Nursing', 'Medicine', 'Other')),
  password VARCHAR(256) NOT NULL);

CREATE TABLE Driver
(netid VARCHAR(7) NOT NULL PRIMARY KEY REFERENCES User(netid),
 license_no INTEGER NOT NULL,
 license_plate_no VARCHAR(10) NOT NULL,
 plate_state VARCHAR(3) NOT NULL);

CREATE TABLE Ride
(ride_no INTEGER NOT NULL PRIMARY KEY,
 origin VARCHAR(100) NOT NULL,
 destination VARCHAR(100) NOT NULL CHECK(destination <> origin), -- check this
 driver_netid VARCHAR(7) NOT NULL REFERENCES Driver(netid),
 date DATE NOT NULL, 
 earliest_time VARCHAR(6) NOT NULL,
 latest_time VARCHAR(6) NOT NULL,
 seats_available INTEGER NOT NULL, 
 gas_price INTEGER,
 comments VARCHAR(500));

 CREATE TABLE Reserve
 (rider_netid VARCHAR(7) NOT NULL,
  ride_no INTEGER NOT NULL, 
  seats_needed INTEGER NOT NULL,
  note VARCHAR(150), 
  PRIMARY KEY(rider_netid, ride_no),
  FOREIGN KEY rider_netid REFERENCES User(netid),
  FOREIGN KEY ride_no REFERENCES Ride(ride_no));

  CREATE TABLE Post -- don't think we need this table
  (driver_netid VARCHAR(7) NOT NULL REFERENCES Driver(netid),
   ride_no INTEGER NOT NULL PRIMARY KEY REFERENCES Ride(ride_no)
  );

-- Triggers

CREATE FUNCTION TF_Driver_own_rider() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT driver_netid
             FROM Ride
             WHERE NEW.ride_no = ride_no AND NEW.rider_netid == driver_netid) THEN
  RAISE EXCEPTION 'Driver cannot reserve own ride.';                                    
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Driver_own_rider
  BEFORE INSERT OR UPDATE ON Reserve
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Driver_own_rider();

-- Need to change below

CREATE FUNCTION TF_Automobile_no_selfie() RETURNS TRIGGER AS $$
BEGIN
  IF
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Automobile_no_selfie
  BEFORE INSERT OR UPDATE ON Automobile
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Automobile_no_selfie();






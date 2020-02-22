CREATE PROCEDURE SP_User_details
    (@netid VARCHAR(7),
    @license_no INTEGER,
    @license_plate_no VARCHAR(10),
    @plate_state VARCHAR(3))

AS
BEGIN

    UPDATE Driver
    SET license_no = @license_no,
        license_plate_no = @license_plate_no,
        plate_state = @plate_state

    WHERE netid = @netid

END
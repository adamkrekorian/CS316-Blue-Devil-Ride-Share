

CREATE PROCEDURE SP_User_details
    (@netid VARCHAR(7),
    @name VARCHAR(256),
    @duke_email VARCHAR(256),
    @phone_number INTEGER,
    @affiliation VARCHAR(256),
    @school VARCHAR(256),
    @password VARCHAR(256))

AS
BEGIN

SET NOCOUNT ON

    UPDATE User
    SET name = @name,
        duke_email = @duke_email,
        phone_number = @phone_number,
        affiliation = @affiliation,
        school = @school,
        password = @password

    WHERE netid = @netid

END
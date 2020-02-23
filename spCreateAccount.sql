

CREATE PROCEDURE SP_Create_account
    (@netid VARCHAR(7),
    @name VARCHAR(256),
    @duke_email VARCHAR(256),
    @phone_number INTEGER,
    @affiliation VARCHAR(256),
    @school VARCHAR(256),
    @password VARCHAR(256),
    @license_no INTEGER,
    @license_plate_no VARCHAR(10),
    @plate_state VARCHAR(3))

AS
BEGIN

SET NOCOUNT ON

INSERT INTO [dbo].[User]
    ([netid],
    [name],
    [duke_email],
    [phone_number],
    [affiliation],
    [school],
    [password])
    VALUES
    (@netid,
    @name,
    @duke_email,
    @phone_number,
    @affiliation,
    @school,
    @password);

IF @license_no IS NOT NULL
    INSERT INTO [dbo].[Driver]
        ([netid],
        [license_no],
        [license_plate_no],
        [plate_state])
        VALUES
        (@netid,
        @license_no,
        @license_plate_no,
        @plate_state);

GO

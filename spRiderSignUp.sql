

CREATE PROCEDURE SP_Rider_sign_up
    (@ride_no INTEGER,
    @rider_netid VARCHAR(7),
    @seats_needed INTEGER,
    @note VARCHAR(150))

AS 
BEGIN

SET NOCOUNT ON

INSERT INTO [dbo].[Reserve]
    ([ride_no],
    [rider_netid],
    [seats_needed],
    [note])
    VALUES
    (@ride_no,
    @rider_netid,
    @seats_needed,
    @note);

UPDATE Ride SET [seats_available] -= @seats_needed
WHERE ride_no = @ride_no;

GO

    
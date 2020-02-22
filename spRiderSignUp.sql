CREATE PROCEDURE SP_Rider_sign_up
    (@ride_no INTEGER,
    @rider_netid VARCHAR(7),
    @seats_needed INTEGER,
    @note VARCHAR(150))

AS BEGIN

INSERT INTO [dbo].[Reserve]
    ([ride_no],
    [rider_netid],
    [seats_needed],
    [note])
    VALUES
    (@ride_no,
    @rider_netid,
    @seats_needed,
    @note)

GO

    
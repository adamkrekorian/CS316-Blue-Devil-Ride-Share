

CREATE PROCEDURE SP_Driver_cancel_ride
    (@ride_no INTEGER)

AS

SET NOCOUNT ON

DELETE FROM Ride 
WHERE ride_no = @ride_no;
GO
DELETE FROM Post
WHERE ride_no = @ride_no;

GO
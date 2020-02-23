

CREATE PROCEDURE SP_Driver_list_ride
    (@ride_no INTEGER,
    @origin VARCHAR(100),
    @destination VARCHAR(100),
    @driver_netid VARCHAR(7),
    @date DATE,
    @earliest_time TIME,
    @latest_time TIME,
    @seats_available INTEGER,
    @gas_price INTEGER,
    @comments VARCHAR(500))
    
AS 
BEGIN

SET NOCOUNT ON

INSERT INTO [dbo].[Ride]
    ([ride_no],
    [origin],
    [destination],
    [driver_netid],
    [date],
    [earliest_time],
    [latest_time],
    [seats_available],
    [gas_price],
    [comments])
    VALUES
    (@ride_no,
    @origin,
    @destination,
    @driver_netid,
    @date,
    @earliest_time,
    @latest_time,
    @seats_available,
    @gas_price,
    @comments);

INSERT INTO [dbo].[Post]
    ([driver_netid],
    [ride_no])
    VALUES
    (@driver_netid,
    @ride_no);

GO
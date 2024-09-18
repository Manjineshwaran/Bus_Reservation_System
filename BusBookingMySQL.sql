create database bus_booking;
use bus_booking;
CREATE TABLE buses (
    id INT PRIMARY KEY,
    ac BOOLEAN,
    capacity INT
);

CREATE TABLE bookings (
    bookingid INT AUTO_INCREMENT PRIMARY KEY,
    busid INT,
    date DATE,
    regno INT
);
CREATE TABLE waiting_list (
    bookingid INT AUTO_INCREMENT PRIMARY KEY,
    busid INT,
    date DATE,
    regno INT
);

insert into buses(id,ac,capacity) values
(1,True,3),
(2,False,4),
(3,True,3);

select * from bookings;
select * from waiting_list
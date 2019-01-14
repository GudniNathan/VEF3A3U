delimiter $$
drop procedure if exists NewStudent $$

create procedure NewStudent
(
    user_name char(10),
    user_pass varchar(255),
    student_track int
)
begin
  
	insert into Students(userName,userPassword,studentTrack,registerDate)
	values(user_name,user_pass,student_track,date(now()));
        
end $$
delimiter ;


delimiter $$
drop procedure if exists SingleStudent $$

create procedure SingleStudent(user_name int)
begin
	select S.userName,S.registerDate,T.trackID,T.trackName 
    from Students S
    inner join Tracks T on S.studentTrack = T.trackID
    and S.userName = user_name;
end $$
delimiter ;


delimiter $$
drop procedure if exists StudentList $$

create procedure StudentList()
begin
	select S.userName, T.trackName from Students S
    inner join Tracks T on S.studentTrack = T.trackID;
end $$
delimiter ;


delimiter $$
drop procedure if exists UpdateStudent $$

create procedure UpdateStudent
(
    user_name varchar(15),
    user_pass varchar(15),
    student_track int,
    out num_rows int
)
begin
	update Students
	set studentTrack = student_track, userPassword = user_pass
	where userName = user_name;
        
	set num_rows = row_count();
end $$
delimiter ;



DROP FUNCTION IF EXISTS getPass;
DELIMITER //

CREATE FUNCTION getPass(user_name char(10)) RETURNS TEXT
BEGIN
    RETURN(SELECT userPassword FROM Students WHERE userName = username);
END//

DELIMITER ;

DROP PROCEDURE IF EXISTS updatePass;
DELIMITER //

CREATE PROCEDURE updatePass(user_name char(10), pass varchar(255))
BEGIN
    UPDATE Students
		SET userPassword = pass
        WHERE userName = user_name;
END//

DELIMITER ;

Call NewStudent('1234567890', 'dfgjdifojgdoifg', 9);

SELECT * FROM Tracks;
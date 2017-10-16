delimiter $$
drop procedure if exists NewStudent $$

create procedure NewStudent
(
	first_name varchar(55),
    last_name varchar(55),
    date_of_birth date,
    student_email varchar(95),
    user_name varchar(15),
    user_pass varchar(15),
    student_track int,
    out new_student_id int
)
begin
	declare student_id int;
    
	insert into Students(firstName,lastName,dob,email,userName,userPassword,studentTrack,registerDate)
	values(first_name,last_name,member_email,user_name,aes_encrypt(user_pass,'xAklwzVY3Q?Jk'),team,date(now()));
        
	set student_id = last_insert_id();
    
    set new_student_id = student_id;
end $$
delimiter ;


delimiter $$
drop procedure if exists SingleStudent $$

create procedure SingleStudent(student_id int)
begin
	select S.studentID,S.firstName,S.lastName,S.dob,S.email,S.userName,S.registerDate,T.trackID,T.trackName 
    from Students S
    inner join Tracks T on S.studentTrack = T.trackID
    and S.studentID = student_id;
end $$
delimiter ;


delimiter $$
drop procedure if exists StudentList $$

create procedure StudentList()
begin
	select studentID,firstName,lastName,dob,email from Students order by firstName,lastName;
end $$
delimiter ;


delimiter $$
drop procedure if exists UpdateStudent $$

create procedure UpdateStudent
(
	student_id int,
	first_name varchar(55),
    last_name varchar(55),
    date_of_birth date,
    student_email varchar(95),
    user_name varchar(15),
    user_pass varchar(15),
    student_track int,
    out num_rows int
)
begin
	if (select userPassword from Students where studentID = student_id) = aes_encrypt(user_pass,'xAklwzVY3Q?Jk') then
		update Students
        set firstName = first_name,lastName = last_name,dob = date_of_birth,email = student_email,studentTrack = student_track
        where studentID = student_id;
        
		set num_rows = row_count();
	end if;
end $$
delimiter ;
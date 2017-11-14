drop database if exists ProgressTracker;

create database ProgressTracker
	default character set utf8
	default collate utf8_general_ci;

set default_storage_engine = innodb;
set sql_mode = 'STRICT_ALL_TABLES';

use ProgressTracker;

create table Semesters
(
	semesterID int auto_increment not null,
    semesterName char(10) not null,
    semesterStarts date not null,
    semesterEnds date not null,
    constraint semester_PK primary key(semesterID)
);

-- School information
create table Schools
(
	schoolID int auto_increment,
    schoolName varchar(75),
    constraint school_PK primary key(schoolID)
);

-- Divisions belonging to certain scool(s)
create table Divisions
(
	divisionID int auto_increment,
    divisionName varchar(75) not null,
    schoolID int not null,
    constraint division_PK primary key(divisionID),
    constraint division_school_FK foreign key(schoolID) references Schools(schoolID)
);

-- Each division has at least one track
create table Tracks
(
	trackID int auto_increment,
    trackName varchar(75),
    validFrom date,
    divisionID int not null,
    constraint track_PK primary key(trackID),
    constraint track_division_FK foreign key(divisionID) references Divisions(divisionID)
);

-- All the courses in the database
-- minCredits: The minimum number of credits you are required to have to be able to take this course.
-- minCredits works independantly per division.
create table Courses 
(
	courseNumber char(11),
	courseName varchar(75) not null,
	courseCredits int not null default 3,
    minCredits int not null default 0,
	constraint course_PK primary key(courseNumber)
);

-- A course may or may not have restrictors applied to them
-- 1: Undanfari				-- Þessi áfangi er undanfari 
-- 2: Samhliða					-- Þennan áfanga má taka samhliða
-- 3: Samhliða(bundið)		-- Þennan áfanga VERÐUR að taka samhliða
-- 4: Staðgengill				-- Þessi áfangi kemur í staðinn
create table Restrictors 
(
	ID int auto_increment,
	restrictorID char(11) not null,
    courseNumber char(11) not null,
	restrictorType char(1) default '1',
	constraint restrictor_PK primary key(ID),
	constraint restrictor_courseNum_UK unique key (courseNumber,restrictorID),
	constraint course_course_FK foreign key (courseNumber) references Courses (courseNumber),
	constraint restrictor_course_FK foreign key (courseNumber) references Courses (courseNumber)
);

-- Courses belonging to a certain track. A track can belong to more then one track(N:M)
create table TrackCourses
(
	ID int auto_increment,
	trackID int not null,
    courseNumber char(10) not null,
    semesterOfStudy tinyint unsigned null,
    mandatory tinyint unsigned,
	constraint trackcourse_PK primary key(ID),
    constraint trackcourse_UQ unique key(trackID,courseNumber),
    constraint track_course_tracks_FK foreign key(trackID) references Tracks(trackID),
    constraint track_course_courses_FK foreign key(courseNumber) references Courses(courseNumber)
);

create table Students
(
	studentID int auto_increment not null,                                                                                                                   
    firstName varchar(45) not null,
    lastName varchar(45) not null,
    dob date not null,
    email varchar(125) null,
    userName varchar(15) not null,
    userPassword blob,
    studentTrack int not null,
    registerDate date null,
    constraint student_PK primary key(studentID),
    constraint student_track_FK foreign key(studentTrack) references Tracks(trackID)
);

create table StudentCourses
(
	studentCourseID int auto_increment not null,
    grade tinyint,
    semesterTaken int not null,
    studentID int not null,
    courseNumber char(10) not null,
    constraint studentcourse_PK primary key(studentCourseID),
    constraint studentcourse_semester foreign key(semesterTaken) references Semesters(semesterID),
    constraint studentcourse_student foreign key(studentID) references Students(studentID),
    constraint studentcourse_trackcourse_FK foreign key(courseNumber) references TrackCourses(courseNumber)
);
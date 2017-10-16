# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Schools(models.Model):
    schoolid = models.AutoField(db_column='schoolID', primary_key=True)  # Field name made lowercase.
    schoolname = models.CharField(db_column='schoolName', max_length=75, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Schools'

class Divisions(models.Model):
    divisionid = models.AutoField(db_column='divisionID', primary_key=True)  # Field name made lowercase.
    divisionname = models.CharField(db_column='divisionName', max_length=75)  # Field name made lowercase.
    schoolid = models.ForeignKey('Schools', db_column='schoolID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Divisions'


class Courses(models.Model):
    coursenumber = models.CharField(db_column='courseNumber', primary_key=True, max_length=11)  # Field name made lowercase.
    coursename = models.CharField(db_column='courseName', max_length=75)  # Field name made lowercase.
    coursecredits = models.IntegerField(db_column='courseCredits')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Courses'


class Restrictors(models.Model):
    restrictorid = models.CharField(db_column='restrictorID', max_length=11, primary_key=True)  # Field name made lowercase.
    coursenumber = models.ForeignKey(Courses, db_column='courseNumber')  # Field name made lowercase.
    restrictortype = models.CharField(db_column='restrictorType', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Restrictors'
        unique_together = (('courseNumber', 'restrictorID'),)


class Semesters(models.Model):
    semesterid = models.AutoField(db_column='semesterID', primary_key=True)  # Field name made lowercase.
    semestername = models.CharField(db_column='semesterName', max_length=10)  # Field name made lowercase.
    semesterstarts = models.DateField(db_column='semesterStarts')  # Field name made lowercase.
    semesterends = models.DateField(db_column='semesterEnds')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Semesters'


class Tracks(models.Model):
    trackid = models.AutoField(db_column='trackID', primary_key=True)  # Field name made lowercase.
    trackname = models.CharField(db_column='trackName', max_length=75, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateField(db_column='validFrom', blank=True, null=True)  # Field name made lowercase.
    divisionid = models.ForeignKey(Divisions, db_column='divisionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tracks'



class Students(models.Model):
    studentid = models.AutoField(db_column='studentID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=45)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=45)  # Field name made lowercase.
    dob = models.DateField()
    email = models.CharField(max_length=125, blank=True, null=True)
    username = models.CharField(db_column='userName', max_length=15)  # Field name made lowercase.
    userpassword = models.TextField(db_column='userPassword', blank=True, null=True)  # Field name made lowercase.
    studenttrack = models.ForeignKey('Tracks', db_column='studentTrack')  # Field name made lowercase.
    registerdate = models.DateField(db_column='registerDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Students'


class Trackcourses(models.Model):
    trackid = models.ForeignKey('Tracks', db_column='trackID')  # Field name made lowercase.
    coursenumber = models.ForeignKey(Courses, db_column='courseNumber')  # Field name made lowercase.
    semesterofstudy = models.IntegerField(db_column='semesterOfStudy', blank=True, null=True)  # Field name made lowercase.
    mandatory = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TrackCourses'
        unique_together = (('trackID', 'courseNumber'),)


class Studentcourses(models.Model):
    studentcourseid = models.AutoField(db_column='studentCourseID', primary_key=True)  # Field name made lowercase.
    grade = models.IntegerField(blank=True, null=True)
    semestertaken = models.ForeignKey(Semesters, db_column='semesterTaken')  # Field name made lowercase.
    studentid = models.ForeignKey('Students', db_column='studentID')  # Field name made lowercase.
    trackid = models.ForeignKey('Trackcourses', db_column='trackID')  # Field name made lowercase.
    coursenumber = models.ForeignKey('Trackcourses', db_column='courseNumber')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'StudentCourses'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

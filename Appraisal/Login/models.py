# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Answer(models.Model):
    answer_id = models.IntegerField(primary_key=True)
    answer = models.TextField()
    modified_by = models.ForeignKey('UserDetails', null=True, db_column='modified_by', blank=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'answer'

class AppraisalContent(models.Model):
    appraisal_content_id = models.IntegerField(primary_key=True)
    appresment = models.ForeignKey('Appraisment')
    question = models.ForeignKey('Question')
    answer = models.ForeignKey(Answer)
    modified_by = models.ForeignKey('UserDetails', db_column='modified_by')
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'appraisal_content'

class Appraisment(models.Model):
    appraisment_id = models.IntegerField(primary_key=True)
    appraiser = models.ForeignKey('UserDetails', db_column='appraiser')
    appraisee = models.ForeignKey('UserDetails', db_column='appraisee')
    modified_by = models.ForeignKey('UserDetails', db_column='modified_by')
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'appraisment'

class Designation(models.Model):
    designation_id = models.IntegerField(primary_key=True)
    designation = models.CharField(max_length=200L)
    modified_by = models.ForeignKey('UserDetails', db_column='modified_by')
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'designation'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40L, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class Event(models.Model):
    event_id = models.IntegerField(primary_key=True)
    description = models.TextField()
    category = models.CharField(max_length=50L, blank=True)
    event_date = models.DateField(null=True, blank=True)
    modified_by = models.ForeignKey('UserDetails', db_column='modified_by')
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'event'

class Language(models.Model):
    language_id = models.IntegerField(primary_key=True)
    language = models.CharField(max_length=100L)
    description = models.TextField(blank=True)
    modified_by = models.ForeignKey('UserDetails', db_column='modified_by')
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'language'

class Option(models.Model):
    option_id = models.IntegerField(primary_key=True)
    option_header = models.ForeignKey('OptionHeader')
    option_text = models.TextField()
    order = models.IntegerField(null=True, blank=True)
    modified_by = models.ForeignKey('UserDetails', db_column='modified_by')
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'option'

class OptionHeader(models.Model):
    option_header_id = models.IntegerField(primary_key=True)
    title = models.TextField(blank=True)
    modified_by = models.ForeignKey('UserDetails', db_column='modified_by')
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'option_header'

class Project(models.Model):
    project_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200L)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.TextField(blank=True)
    contact_person = models.IntegerField(null=True, blank=True)
    modified_by = models.ForeignKey('UserDetails', db_column='modified_by')
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'project'

class ProjectDesignation(models.Model):
    project = models.ForeignKey(Project)
    designation = models.ForeignKey(Designation)
    modified_by = models.ForeignKey('UserDetails', db_column='modified_by')
    modified_on = models.CharField(max_length=45L)
    class Meta:
        db_table = 'project_designation'

class Question(models.Model):
    question_id = models.IntegerField(primary_key=True)
    question = models.TextField()
    level = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=45L)
    category = models.CharField(max_length=45L, blank=True)
    info = models.TextField(blank=True)
    intent = models.IntegerField(null=True, blank=True)
    modified_by = models.ForeignKey('UserDetails', db_column='modified_by')
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'question'

class Technology(models.Model):
    technology_id = models.IntegerField(primary_key=True)
    technology = models.CharField(max_length=100L)
    description = models.TextField(blank=True)
    modified_by = models.ForeignKey('UserDetails', db_column='modified_by')
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'technology'

class UserAttributes(models.Model):
    user = models.ForeignKey('UserDetails')
    tech_lang = models.ForeignKey(Technology)
    tech_working = models.IntegerField(null=True, blank=True)
    tech_known = models.IntegerField(null=True, blank=True)
    tech_willing = models.IntegerField(null=True, blank=True)
    language_working = models.IntegerField(null=True, blank=True)
    language_known = models.IntegerField(null=True, blank=True)
    language_willing = models.IntegerField(null=True, blank=True)
    modified_by = models.IntegerField()
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'user_attributes'

class UserDetails(models.Model):
    user_id = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=45L)
    lastname = models.CharField(max_length=45L)
    password = models.CharField(max_length=45L)
    emailid = models.CharField(max_length=45L, blank=True)
    user_level = models.IntegerField(null=True, blank=True)
    user_weight = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=45L, blank=True)
    modified_by = models.IntegerField(null=True, blank=True)
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'user_details'

class UserEvent(models.Model):
    user = models.ForeignKey(UserDetails)
    event = models.ForeignKey(Event)
    modified_by = models.ForeignKey(UserDetails, db_column='modified_by')
    modified_on = models.DateTimeField()
    class Meta:
        db_table = 'user_event'

class UserProject(models.Model):
    user = models.ForeignKey(UserDetails)
    project = models.ForeignKey(Project)
    designation = models.ForeignKey(Designation)
    class Meta:
        db_table = 'user_project'


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField,SelectField,URLField,IntegerField,DateField,TextAreaField
from wtforms import DateTimeLocalField,FileField,TelField,TimeField,DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from flask_wtf.file import FileField,FileRequired,FileAllowed

class DpForm(FlaskForm):
    photo=FileField(validators=[FileRequired(),FileAllowed(['jpg','png','jpeg'],'ONLY IMAGES ARE ALLOWED')])
    uploadbtn=SubmitField('Upload Picture')

class RegistrationForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired('Please enter your first name')])
    lname = StringField('Last Name', validators=[DataRequired('Please enter your last name')])
    email = EmailField('Email', validators=[DataRequired('Email is required'), Email('Please enter a valid email')])
    phone = TelField('Phone Number')
    pass1 = PasswordField('Password', validators=[DataRequired('Password is required')])
    pass2=PasswordField(' Confirm Password', validators=[DataRequired('Password is required'),EqualTo('pass1')])
    user_type = SelectField('User Type', choices=[('freelancer', 'Freelancer'), ('client', 'Client')], validators=[DataRequired()])
    submit = SubmitField('Create Account')
    

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired('Email is required'), Email('Please enter a valid email')])
    password = PasswordField('Password', validators=[DataRequired('Password is required')])
    submit = SubmitField('Login')



class ProfileForm(FlaskForm):
   business_name = StringField('Business name', validators=[DataRequired('Please enter your business name')])
   industry = StringField('Industry', validators=[DataRequired('Please enter the industry you belong to')])
   hiring_needs = StringField('Hiring needs', validators=[DataRequired('Please enter your last name')])
   submit = SubmitField('Save & Continue')
   submit2 = SubmitField('Save & Continue')
   email = EmailField('Email', validators=[DataRequired('Email is required'), Email('Please enter a valid email')])
   job_title= StringField('Job title', validators=[DataRequired('Please enter your Job title')])
   skills = StringField('skills', validators=[DataRequired('Please enter your skills')])
   experience =IntegerField('Experience(YEARS)', validators=[DataRequired('Please enter a numeric value')])
   portfolio= URLField('portfolio link', validators=[DataRequired('Please enter your business name')])


class JobPostForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired(), Length(max=100)])
    job_description = TextAreaField('Job Description', validators=[DataRequired(), Length(max=500)])
    required_skills = StringField('Required Skills', validators=[DataRequired(), Length(max=200)])
    budget = IntegerField('Budget ($)', validators=[DataRequired(), NumberRange(min=1)])
    deadline = DateField('Deadline', validators=[DataRequired()])
    submit = SubmitField('Post Job')






class JobApplicationForm(FlaskForm):
    proposal = TextAreaField('Proposal', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Submit Application')
    email = EmailField('email', validators=[DataRequired(), Length(max=500)])





class ClientProfileForm(FlaskForm):
    business_name = StringField('Business Name', validators=[DataRequired()])
    industry = StringField('Industry', validators=[DataRequired()])
    hiring_needs = TextAreaField('Hiring Needs', validators=[DataRequired()])
    submit = SubmitField('Submit')


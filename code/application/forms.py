from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField

from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from application.models import User,Customer,Account

class LoginForm(FlaskForm):
    mail   = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6,max=15),])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    name   = StringField("Name", validators=[DataRequired(),Length(min=3,max=15)])
    mail = StringField("Email Id", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15),EqualTo('password')])
    submit = SubmitField("Register")

class CustomerForm(FlaskForm):
    SSN   = StringField("SSN ID", validators=[DataRequired(),Length(min=9,max=9)])
    cname = StringField("Customer Name", validators=[DataRequired()])
    age = StringField("Age", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AccountForm(FlaskForm):
    cid   = StringField("Customer ID", validators=[DataRequired(),Length(min=9,max=9)])
    acid = StringField("Account ID", validators=[DataRequired(),Length(min=9,max=9)])
    actype = StringField("Account Type(Savings/Current)", validators=[DataRequired()])
    damount = StringField("Minimum deposit to create account(Enter amount between 500-1000)", validators=[DataRequired()])
    submit = SubmitField("Submit")

class CustomerupdateForm(FlaskForm):
    SSN   = StringField("Enter SSN ID of the customer to be updated", validators=[DataRequired(),Length(min=9,max=9)])
    cname = StringField("New Customer Name", validators=[DataRequired()])
    age = StringField("New Age", validators=[DataRequired()])
    address = StringField("New Address", validators=[DataRequired()])
    state = StringField("New State", validators=[DataRequired()])
    city = StringField("New City", validators=[DataRequired()])
    submit = SubmitField("Update")
    

class CustomerdeleteForm(FlaskForm):
    SSN   = StringField("Enter SSN ID of the customer to be deleted", validators=[DataRequired(),Length(min=9,max=9)])
    
    submit = SubmitField("Delete")

class CustomersearchForm(FlaskForm):
    SSN   = StringField("Enter SSN ID of the customer to be searched", validators=[DataRequired(),Length(min=9,max=9)])
    
    submit = SubmitField("Search")

    

class AccountdeleteForm(FlaskForm):
    acid   = StringField("Enter Account ID of the Account to be deleted", validators=[DataRequired(),Length(min=9,max=9)])
    
    submit = SubmitField("Delete")   

class AccountsearchForm(FlaskForm):
    acid   = StringField("Enter Account ID of the Account to be searched", validators=[DataRequired(),Length(min=9,max=9)])
    
    submit = SubmitField("Search")   

class DepositForm(FlaskForm):
    
    acid = StringField("Enter the Account ID of the account", validators=[DataRequired(),Length(min=9,max=9)])
    
    damount = StringField("Enter the amount to be deposited", validators=[DataRequired()])
    submit = SubmitField("Deposit")

class WithdrawForm(FlaskForm):
    
    acid = StringField("Enter the Account ID of the account", validators=[DataRequired(),Length(min=9,max=9)])
    
    damount = StringField("Enter the amount to be withdrawn", validators=[DataRequired()])
    submit = SubmitField("Withdraw")

class TransferForm(FlaskForm):
    acid1 = StringField("Enter the Account ID of the sender", validators=[DataRequired(),Length(min=9,max=9)])
    acid2 = StringField("Enter the Account ID of the receiver", validators=[DataRequired(),Length(min=9,max=9)])
    
    damount = StringField("Enter the amount to be transferred", validators=[DataRequired()])
 
    submit = SubmitField("Transfer")


      

    def validate_mail(self,mail):
        user = User.objects(mail=mail.data).first()
        if user:
            raise ValidationError("Email is already in use. Pick another one.")

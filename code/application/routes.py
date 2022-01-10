from application import app, db

from application.models import User,Customer,Account
from flask import render_template, request, json, Response,url_for,flash,redirect,json,session,jsonify
from application.forms import LoginForm,RegisterForm,CustomerForm,WithdrawForm,TransferForm,DepositForm,AccountsearchForm,AccountForm,CustomerupdateForm,CustomersearchForm,CustomerdeleteForm,AccountdeleteForm
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bankwebsite"]
mycustomercoll = mydb["customer"]
myaccountcoll = mydb["account"]

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/login",methods=['GET','POST'])
def login():
    if session.get('mail'):
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        mail       = form.mail.data
        password    = form.password.data

        user = User.objects(mail=mail).first()
        if user and user.password:
            flash(f"{user.name}, you are successfully logged in!", "success")
            
            session['mail'] = user.mail
            return redirect("/")
        else:
            flash("Sorry, something went wrong, Enter valid details","danger")
    return render_template("login.html", form=form, login=True )
@app.route("/logout")
def logout():
    session['mail']=False
    session.pop('mail',None)
    
    flash(f"you are logged out","success")
    return redirect(url_for('home'))


@app.route("/layout",methods=['GET','POST'])
def layout():
         
    return render_template("layout.html")

@app.route("/createcustomer",methods=['POST','GET'])
def cc():
    if not session.get('mail'):
        return redirect(url_for('login'))
    form=CustomerForm()
    if form.validate_on_submit():
        SSN= form.SSN.data
        cname       = form.cname.data
        age    = form.age.data
        address  = form.address.data
        state       = form.state.data
        city    = form.city.data
        customer = Customer(SSN=SSN,cname=cname,age=age,address=address,state=state,city=city)
        
        customer.save()
        flash("Customer creation initiated successfully","success")
        return redirect(url_for('home'))
    return render_template("createcustomer.html", form=form, createcustomer=True)

@app.route("/createaccount",methods=['POST','GET'])
def createaccount():
    if not session.get('mail'):
        return redirect(url_for('login'))
    form=AccountForm()
    if form.validate_on_submit():
        cid= form.cid.data
        acid      = form.acid.data
        actype    = form.actype.data
        damount  = form.damount.data
        
        account = Account(cid=cid,acid=acid,actype=actype,damount=damount)
        
        account.save()
        flash("Account creation initiated successfully","success")
        return redirect(url_for('home'))
    return render_template("createaccount.html", form=form, createaccount=True)
@app.route("/customerstatus")
def customerstatus():
    if not session.get('mail'):
        return redirect(url_for('login'))
    
    customers = Customer.objects.all()
    return render_template("customer.html", customers=customers)

@app.route("/accountstatus")
def accountstatus():
    if not session.get('mail'):
        return redirect(url_for('login'))
    
    accounts = Account.objects.all()
    return render_template("account.html", accounts=accounts)




@app.route("/register", methods=['POST','GET'])
def register():
    if session.get('mail'):
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
       
        name  = form.name.data
        mail       = form.mail.data
        password    = form.password.data
        
        

        user = User(name=name,mail=mail,password=password)
        
        user.save()
        flash("You are successfully registered!","success")
        return redirect(url_for('home'))
    return render_template("register.html", form=form, register=True)

@app.route("/updatecustomer", methods=['POST','GET'])    
def updatecustomer():    
    #Updating a Task with various references    
    if not session.get('mail'):
        return redirect(url_for('login'))
    form=CustomerupdateForm()
    if form.validate_on_submit():
        SSN= form.SSN.data
        cname = form.cname.data
        age    = form.age.data
        address  = form.address.data
        state   = form.state.data
        city    = form.city.data  
    
        myquery = { "SSN": SSN }
        newvalues = { "$set": { "cname": cname,"age":age,"address":address,"state":state,"city":city} }

        mycustomercoll.update_one(myquery, newvalues)
        flash("Customer details are updated successfully","success")
        return redirect(url_for('home'))
        
    return render_template("updatecustomer.html",form=form,updatecustomer=True)


@app.route("/deposit", methods=['POST','GET'])    
def deposit():    
    #Updating a Task with various references    
    if not session.get('mail'):
        return redirect(url_for('login'))
    form=DepositForm()
    if form.validate_on_submit():
        acid= form.acid.data
        damount = (int)(form.damount.data)

        
    
        myquery = { "acid": acid }
        newvalues = { "$inc":{"Depositedamount": damount} }
        #up={ 'upsert':True}

        myaccountcoll.update_one(myquery, newvalues)
        account = Account.objects(acid=acid).first()
        flash(f"Amount deposited successfully to the mentioned Account. Available balance in the account after deposit is {account.Depositedamount} ","success")
        return redirect(url_for('home'))
        
    return render_template("deposit.html",form=form,deposit=True)

@app.route("/withdraw", methods=['POST','GET'])    
def withdraw():    
    #Updating a Task with various references    
    if not session.get('mail'):
        return redirect(url_for('login'))
    form=WithdrawForm()
    if form.validate_on_submit():
        acid= form.acid.data
        damount = (int)(form.damount.data)
        
    
        myquery = { "acid": acid }
        newvalues = { "$inc":{"Depositedamount": -damount} }
        #up={ 'upsert':True}

        myaccountcoll.update_one(myquery, newvalues)
        account = Account.objects(acid=acid).first()
        flash(f"Amount Withdrawn successfully from the mentioned Account, Available balance in the account after withdraw is {account.Depositedamount}","success")
        return redirect(url_for('home'))
        
    return render_template("withdraw.html",form=form,withdraw=True)

@app.route("/transfer", methods=['POST','GET'])    
def transfer():    
    #Updating a Task with various references    
    if not session.get('mail'):
        return redirect(url_for('login'))
    form=TransferForm()
    if form.validate_on_submit():
        acid1= form.acid1.data
        acid2= form.acid2.data
        damount = (int)(form.damount.data)
        
    
        myquery1 = { "acid": acid1 }
        newvalues1 = { "$inc":{"Depositedamount": -damount} }
        myaccountcoll.update_one(myquery1, newvalues1)
        
        myquery2 = { "acid": acid2 }
        newvalues2 = { "$inc":{"Depositedamount": damount} }
        myaccountcoll.update_one(myquery2, newvalues2)

        account1 = Account.objects(acid=acid1).first()
        account2 = Account.objects(acid=acid2).first()
        flash(f"Amount transferred successfully , Available balance in the Sender account is {account1.Depositedamount} , Available balance in the receiver account is {account2.Depositedamount} ","success")
        return redirect(url_for('home'))
        
    return render_template("transfer.html",form=form,transfer=True)


@app.route("/deletecustomer", methods=['POST','GET'])    
def deletecustomer():    
       
    if not session.get('mail'):
        return redirect(url_for('login'))
    form=CustomerdeleteForm()
    if form.validate_on_submit():
        SSN= form.SSN.data

        myquery = { "SSN": SSN }

        mycustomercoll.delete_one(myquery)
        flash("Customer details are deleted successfully","success")
        return redirect(url_for('home'))

    return render_template("deletecustomer.html",form=form,deletecustomer=True)

@app.route("/customersearch", methods=['POST','GET'])    
def customersearch():    
       
    if not session.get('mail'):
        return redirect(url_for('login'))
    form=CustomersearchForm()
    if form.validate_on_submit():
        SSN= form.SSN.data

        myquery = { "SSN": SSN }

        x=mycustomercoll.find(myquery)
        #customer = Customer(SSN=SSN)
        
        

        return render_template('customersearchdisplay.html', x=x)
    return render_template("customersearch.html",form=form,customersearch=True)
    

@app.route("/accountsearch", methods=['POST','GET'])    
def accountsearch():    
       
    if not session.get('mail'):
        return redirect(url_for('login'))
    form=AccountsearchForm()
    if form.validate_on_submit():
        acid= form.acid.data

        myquery = { "acid": acid }

        x=myaccountcoll.find(myquery)
        
        
        

        return render_template('accountsearchdisplay.html', x=x)
        
    return render_template("accountsearch.html",form=form,accountsearch=True)

@app.route("/accountstatement", methods=['POST','GET'])    
def accountstatement():    
       
    if not session.get('mail'):
        return redirect(url_for('login'))
    form=AccountsearchForm()
    if form.validate_on_submit():
        acid= form.acid.data

        myquery = { "acid": acid }

        x=myaccountcoll.find(myquery)
        return render_template('accountstatementdisplay.html', x=x)
        
        
    return render_template("accountstatement.html",form=form,accountstatement=True)

@app.route("/deleteaccount", methods=['POST','GET'])    
def deleteaccount():    
       
    if not session.get('mail'):
        return redirect(url_for('login'))
    form=AccountdeleteForm()
    if form.validate_on_submit():
        acid= form.acid.data

        myquery = { "acid": acid }

        myaccountcoll.delete_one(myquery)
        flash("Account deletion initiated successfully","success")
        return redirect(url_for('home'))

    return render_template("deleteaccount.html",form=form,deleteaccount=True)



@app.route("/user")
def user():
    
    
    users = User.objects.all()
    return render_template("user.html", users=users)

@app.route("/customer")
def customer():
    
    
    customers = Customer.objects.all()
    return render_template("customer.html", customers=customers)

@app.route("/account")
def account():
    
    
    accounts = Account.objects.all()
    return render_template("account.html", accounts=accounts)
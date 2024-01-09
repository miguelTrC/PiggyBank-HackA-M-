from backend.views import views
from flask import render_template, request,session, redirect, url_for
from backend.models import AccountInfo
from flask_login import login_required
from backend import db

""" Home page """
@views.route('/')
def index():
    return render_template('StartPage.html')

""" Parents home page """
@views.route('/home-parents', methods=['GET', 'POST'])
@login_required
def home_parents():

    # verifies parent is logged in
    if "parent_username" not in session:
        return redirect(url_for('authn.parentLogin'))

    # get info from database
    user = AccountInfo.query.filter_by(parent_username=session['parent_username']).first()

    # edit database
    if request.method == "POST":

        # withdraw
        withdraw = request.form.get('withdraw')

        print('after:' + withdraw)

        if withdraw:
            wBalance = int(user.balance) - int(withdraw)
            user.balance = wBalance

        # adding
        adding = request.form.get('adding')
        if adding:
            aBalance = int(user.balance) + int(adding)
            user.balance = aBalance
            user.last_deposit = int(adding)

        if adding or withdraw:
            db.session.commit()
            
        else:
            return render_template('ParentMainPage.html')
            

    return render_template('ParentMainPage.html', balance=user.balance, last_deposit=user.last_deposit, parent_email=user.parent_email, username=session['parent_username'])

""" Child home page """
@views.route('/home-child')
@login_required
def home_child():

    if "child_username" not in session:
        return redirect(url_for('authn.childrenLogin'))

    child = AccountInfo.query.filter_by(child_username=session['child_username']).first()
    print(session['child_username'])
    print(child.balance)
    return render_template('ChildMainPage.html', username=session['child_username'], balance=child.balance, last_deposit=child.last_deposit, child_email=child.child_email)
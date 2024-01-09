from backend.views import authn
from flask import render_template, redirect, url_for
from .. import db
from backend.models import AccountInfo

from flask import request, session, flash
from flask_login import login_user, logout_user, login_required

# sign up (parent)
@authn.route('/sign-up', methods=['GET', 'POST'])
def sign_Up():

    # If already logged in, send user to home page
    if 'parent_username' in session:
        return redirect(url_for('views.home'))

    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            rePassword = request.form.get('checkPassword')
            username = request.form.get('username')

            check_username = AccountInfo.query.filter_by(parent_username=username).first()
            check_email = AccountInfo.query.filter_by(parent_email=email).first()
            
            """ check alredy exising credentials and verify credential length"""
            if check_email:
                print('\nThis email is already registered with an account\n')
            
            elif check_username:
                print('\nUsername is already taken\n')

            elif len(username) < 3:
                print('\nInvalid username! Use at least 3 characters.\n')

            elif len(password) < 3:
                print('\nPassword is to short\n')
            
            elif password != rePassword:
                print("Password does not match")

            # if all good, create new user and add it to db
            else:
                new_parent = AccountInfo(parent_username=username, parent_email=email, parent_password=password, balance=0, last_deposit=0)
                db.session.add(new_parent)
                db.session.commit()

                # login user
                #login_user(new_parent, remember=True)
                print('\nAccount created!\n')
                return redirect(url_for('authn.parentLogin'))

            return render_template('signUp.html')

        else:
            return render_template('signUp.html')

# sign up (parent)
@authn.route('/child_sign-up', methods=['GET', 'POST'])
def child_sign_Up():

    # If already logged in, send user to home page
    if 'parent_username' not in session:
        return redirect(url_for('authn.parentLogin'))

    else:
        if request.method == 'POST':
            child_email = request.form.get('email')
            child_password = request.form.get('password')
            child_rePassword = request.form.get('checkPassword')
            child_username = request.form.get('username')

            check_username = AccountInfo.query.filter_by(child_username=child_username).first()
            check_email = AccountInfo.query.filter_by(child_email=child_email).first()
            
            """ check alredy exising credentials and verify credential length"""
            if check_email:
                print('\nThis email is already registered with an account\n')
            
            elif check_username:
                print('\nUsername is already taken\n')

            elif len(child_username) < 3:
                print('\nInvalid username! Use at least 3 characters.\n')

            elif len(child_password) < 3:
                print('\nPassword is to short\n')
            
            elif child_password != child_rePassword:
                print("Password does not match")

            # if all good, create new user and add it to db
            else:
                parent = AccountInfo.query.filter_by(parent_username=session['parent_username']).first()
                parent.child_email = child_email
                parent.child_username = child_username
                parent.child_password = child_password
                db.session.commit()

                # login user
                #login_user(new_parent, remember=True)
                print('\nAccount created!\n')
                return redirect(url_for('authn.childrenLogin'))

            return render_template('signUp.html')

        else:
            return render_template('signUp.html')

# login parent
@authn.route('/parent-login', methods=['GET', 'POST'])
def parentLogin():

    # if already logged in, redirect to parent home page
    if "parent_username" in session:
        return redirect(url_for('views.home_parents'))
    
    # if not logged in, enter credentials
    # if not logged in, login user
    else:
        if request.method == 'POST':

            email = request.form.get('email', '')
            password = request.form.get('password','')

            if password == '' and email == '':
                return render_template('ParentLogin.html')

            else:
                # check if user exists
                user = AccountInfo.query.filter_by(parent_email=email).first()

                if user:

                    # if exist, check password
                    if password == user.parent_password:

                        # if right credentials, log in user
                        session['parent_username'] = user.parent_username
                        print(session['parent_username'])
                        login_user(user, remember=True)
                        return redirect(url_for('views.home_parents'))

                    # if wrong password, flash message
                    else:
                        flash('Incorrect password', category='error')
                        return render_template('ParentLogin.html')

                # if email is not registered, flash message
                else:
                    flash('Email does not exist', category='error')
                    return render_template('ParentLogin.html')

        else:
            return render_template('ParentLogin.html')

#login children
@authn.route('/children-login', methods=['GET', 'POST'])
def childrenLogin():
    # if already logged in, redirect to parent home page
    if "child_username" in session:
        return redirect(url_for('views.home_child'))
    
    # if not logged in, enter credentials
    # if not logged in, login user
    else:
        if request.method == 'POST':

            email = request.form.get('email', '')
            password = request.form.get('password','')

            if password == '' and email == '':
                return render_template('ChildLogin.html')

            else:
                # check if user exists
                user = AccountInfo.query.filter_by(child_email=email).first()

                if user:

                    # if exist, check password
                    if password == user.child_password:

                        # if right credentials, log in user
                        session['child_username'] = user.child_username
                        print(session['child_username'])
                        login_user(user, remember=True)
                        return redirect(url_for('views.home_child'))

                    # if wrong password, flash message
                    else:
                        flash('Incorrect password', category='error')
                        return render_template('ChildLogin.html')

                # if email is not registered, flash message
                else:
                    flash('Email does not exist', category='error')
                    return render_template('ChildLogin.html')

        else:
            return render_template('ChildLogin.html')

# logout 
@authn.route('/logout')
@login_required
def logout():
    """ logout user """
    try:
        session.pop('parent_username')
        session.pop('child_username')
    except:
        print('user does not exits')

    logout_user()
    return redirect(url_for('views.index'))
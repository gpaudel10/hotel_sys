#app/auth/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.models import User
# from werkzeug.urls import url_parse
from urllib.parse import urlparse


@bp.route('/register', methods=['GET', 'POST'])

def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('booking.index'))
    
    if request.method == 'POST':
        
        user = User(
            username=request.form['username'],
            email=request.form['email']
        )
        user.set_password(request.form['password'])
        
        db.session.add(user)
        try:
            db.session.commit()
            flash('congratulations, you are now a registered user!')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            
            flash(f'Error occurred: {str(e)}')
            flash('Error occured please use a different username or email.')

            return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('booking.index'))
        
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None or not user.check_password(request.form['password']):
            flash('invalid username or password')
            return redirect(url_for('auth.login'))
            
        login_user(user)
        next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('booking.index')
        return redirect(next_page)
        
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
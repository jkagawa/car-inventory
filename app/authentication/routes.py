from forms import UserLoginForm
from models import User, db
from flask import Blueprint, render_template, request, redirect, url_for, flash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully createed a user account {email}', 'User-created')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid form data: Please check your form')
    
    return render_template('sign_up.html', form=form)
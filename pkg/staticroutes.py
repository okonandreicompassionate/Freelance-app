from flask import render_template,request,flash,url_for,redirect,session
from werkzeug.security import generate_password_hash,check_password_hash

from pkg import app,forms
from pkg.models import db,User,ClientProfileTable,Message,Conversation,FreelancerProfileTable,Notifications,JobApplicationsTable,Jobs




@app.route("/")
def home():
   return render_template("stat/index.html",)



@app.route('/register/',methods=['GET','POST'])
def register():
    regform=forms.RegistrationForm()
    if request.method=='GET':
        return render_template('stat/signup.html',regform=regform)
    else:
      if regform.validate_on_submit():
        fname=regform.fname.data
        lname=regform.lname.data
        email=regform.email.data
        pass1=regform.pass1.data
        user_type = regform.user_type.data
        hashed_password=generate_password_hash(pass1)
        user=User(user_fname=fname,user_lname=lname,user_email=email,user_type=user_type,user_pwd=hashed_password)
        db.session.add(user)
        db.session.commit()
        id=user.user_id
        if id:
           flash ('An account has been created for you',category='success')
           return redirect(url_for('login'))
        else:
           flash('An error occured ,please try again',category='failed')
           return redirect(url_for('register'))
      else:
         return render_template('stat/signup.html',regform=regform)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    regform = forms.LoginForm()
    if request.method == 'GET':
        return render_template("stat/signin.html", regform=regform)
    
    # Retrieve form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Query the database
    deets = db.session.query(User).filter(User.user_email == email).first()
    if deets:
        stored_password = deets.user_pwd
        check = check_password_hash(stored_password, password)  # returns True or False

        if check:  # Password is correct
            session['useronline'] = deets.user_id

            

            # Redirect based on user type
            if deets.user_type == "client":
                return redirect(url_for("client_dashboard"))
            elif deets.user_type == "freelancer":
                return redirect(url_for("freelancer_dashboard"))
            else:
                flash("Unknown user type", category="failed")
                return redirect(url_for('home'))
        else:
            flash("Wrong password", category="failed")
            return redirect(url_for('login'))
    else:
        flash(message="Wrong email", category="failed")
        return redirect(url_for('login'))
    








@app.route('/change_password_freelancer/', methods=['GET', 'POST'])
def change_password_freelancer():
    form =forms.RegistrationForm()
    user_id = session.get('useronline')
    if not user_id:
        flash('You must be logged in to view this page.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        user = User.query.get(user_id)
        if not check_password_hash(user.user_pwd, current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('change_password_freelancer'))

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('change_password_freelancer'))

        user.user_pwd = generate_password_hash(new_password)
        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('general_settings_freelancer'))

    return render_template('freelancer/change_password_freelancer.html',form=form)




@app.route('/notifications/')
def notifications():
    user_id = session.get('useronline')
    if not user_id:
        flash('You must be logged in to view this page.', 'danger')
        return redirect(url_for('login'))

    user_notifications = Notifications.query.filter_by(user_id=user_id).order_by(Notifications.created_at.desc()).all()
    return render_template('stat/notifications.html', notifications=user_notifications)


@app.route('/settings/', methods=['GET', 'POST'])
def settings():
    user_id = session.get('useronline')
    if not user_id:
        flash('You must be logged in to view this page.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Example: Update privacy settings (you can expand this logic as needed)
        allow_email_visibility = request.form.get('allow_email_visibility') == 'on'
        # Save privacy settings to the database (if applicable)
        flash('Privacy settings updated successfully!', 'success')
        return redirect(url_for('privacy_settings'))

    return render_template('stat/settings.html')




@app.route('/delete_account_client/', methods=['GET', 'POST'])
def delete_account_client():
    user_id = session.get('useronline')
    if not user_id:
        flash('You must be logged in to perform this action.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        user = User.query.get(user_id)
        if user:
            # Delete all jobs associated with the client
            if user.user_type == 'client':
                Jobs.query.filter_by(client_id=user_id).delete()

            # Delete all job applications associated with the user
            JobApplicationsTable.query.filter_by(user_id=user_id).delete()

            # Delete the user
            db.session.delete(user)
            db.session.commit()
            session.clear()
            flash('Your account has been deleted.', 'success')
            return redirect(url_for('home'))
        flash('Account not found.', 'danger')
        return redirect(url_for('general_settings_client'))

    return render_template('stat/delete_account_client.html')





@app.route('/general_settings_client/', methods=['GET', 'POST'])
def general_settings_client():
    user_id = session.get('useronline')
    if not user_id:
        flash('You must be logged in to view this page.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Example: Update general settings (you can expand this logic as needed)
        enable_notifications = request.form.get('enable_notifications') == 'on'
        # Save general settings to the database (if applicable)
        flash('General settings updated successfully!', 'success')
        return redirect(url_for('general_settings_client'))

    return render_template('stat/general_settings_client.html')
    
@app.route('/profile_setup_client/', methods=['GET', 'POST'])
def profile_setup_client():
    regform = forms.ProfileForm()
    if request.method == 'POST':
        # Get form data
        user_id = session.get('useronline')
        business_name = request.form.get('business_name')
        industry = request.form.get('industry')
        hiring_needs = request.form.get('hiring_needs')

        # Validate required fields
        if not business_name or not industry or not hiring_needs:
            flash('All fields are required.', 'danger')
            return redirect(url_for('profile_setup_client'))

        # Create a new client profile        <a href="{{ url_for('profile') }}" class="btn btn-link mt-3 d-block text-center">Back to Profile</a>
        client_profile = ClientProfileTable(
            user_id=user_id,
            business_name=business_name,
            industry=industry,
            hiring_needs=hiring_needs
        )

        # Save the client profile to the database
        db.session.add(client_profile)
        db.session.commit()

        # Update the user's first_login field to False
        user = User.query.get(user_id)
        if user:
            user.first_login = False
            db.session.commit()

        flash('Profile setup completed successfully!', 'success')
        return redirect(url_for('client_dashboard'))

    return render_template('stat/profile_setup_client.html', regform=regform)



@app.route('/profile_setup_freelancer/', methods=['GET', 'POST'])
def profile_setup_freelancer():
    regform = forms.ProfileForm()
    if request.method == 'POST':
        # Get form data
        user_id = session.get('useronline')
        job_title = request.form.get('job_title')
        skills = request.form.get('skills')
        experience = request.form.get('experience')
        portfolio = request.form.get('portfolio')
        about_me = request.form.get('about_me')

        # Validate required fields
        if not job_title or not skills or not experience or not portfolio:
            flash('All fields are required.', 'danger')
            return redirect(url_for('profile_setup_freelancer'))

        # Create a new freelancer profile
        freelancer_profile = FreelancerProfileTable(
            user_id=user_id,
            job_title=job_title,
            skills=skills,
            experience=int(experience),
            portfolio=portfolio,
            about_me=about_me
        )

        # Save the freelancer profile to the database
        db.session.add(freelancer_profile)
        db.session.commit()

        # Update the user's first_login field to False
        user = User.query.get(user_id)
        if user:
            user.first_login = False
            db.session.commit()

        flash('Profile setup completed successfully!', 'success')
        return redirect(url_for('freelancer_dashboard'))

    return render_template('stat/profile_setup_freelancer.html', regform=regform)













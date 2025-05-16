from flask import render_template,request,flash,url_for,redirect,session
from werkzeug.security import generate_password_hash,check_password_hash

from pkg import app,forms
from pkg.models import db,User,Jobs,JobApplicationsTable,Notifications,FreelancerProfileTable



@app.route("/freelancer_dashboard/")
def freelancer_dashboard():
    user_id = session.get("useronline")  # Check if the user is logged in
    if not user_id:
        flash("You must be logged in to view this page.", category="failed")
        return redirect(url_for('home'))

    # Fetch user details
    deets = db.session.query(User).get(user_id)
    if not deets:
        flash("User not found. Please log in again.", category="failed")
        return redirect(url_for('logout'))

    # Check if it's the user's first login
    if deets.first_login:  # Assuming `first_login` is a boolean field in the User model
        # Redirect to profile setup route
        return redirect(url_for("profile_setup_freelancer"))

    # Render the freelancer dashboard
    return render_template("freelancer/freelancer_dashboard.html", deets=deets)
    

      



@app.route('/job_details/<int:job_id>/', methods=['GET'])
def job_details(job_id):
    # Fetch the job details from the database
    job = db.session.query(Jobs).filter_by(jobs_id=job_id).first()

    if not job:
        flash("Job not found.", category="failed")
        return redirect(url_for('jobs'))  # Redirect to the jobs listing page if the job doesn't exist

    # Access the client's full name and last name via the relationship
    client_name = f"{job.client.user_fname} {job.client.user_lname}"

    return render_template('freelancer/job_details.html', job=job, client_name=client_name)

@app.route('/jobs/')
def jobs():
    jobs = Jobs.query.all()
    return render_template('freelancer/jobs.html', jobs=jobs)





@app.route('/apply_job/<int:job_id>/', methods=['GET', 'POST'])
def apply_job(job_id):
    user_id = session.get('useronline')  # Check if the user is logged in
    if not user_id:
        flash("You must be logged in to apply for a job.", category="failed")
        return redirect(url_for('login'))

    # Check if the job exists
    job = db.session.query(Jobs).filter_by(jobs_id=job_id).first()
    if not job:
        flash("Job not found.", category="failed")
        return redirect(url_for('jobs'))

    # Check if the user has already applied for the job
    existing_application = db.session.query(JobApplicationsTable).filter_by(jobs_id=job_id, user_id=user_id).first()
    if existing_application:
        flash("You have already applied for this job.", category="failed")
        return redirect(url_for('job_details', job_id=job_id))

    form = forms.JobApplicationForm()
    if form.validate_on_submit():
        proposal = form.proposal.data
        email = form.email.data

        # Save the application to the database
        application = JobApplicationsTable(
            jobs_id=job_id,
            user_id=user_id,
            proposal=proposal,
            email=email,
            status='pending'  # Default status
        )
        db.session.add(application)
        db.session.commit()

        flash("Application submitted successfully!", category="success")

        # Redirect to the messaging route (assuming a messaging route exists)
        return redirect(url_for('jobs'))

    return render_template('freelancer/apply_job.html', form=form, job=job, )



@app.route("/comingsoon2/")
def comingsoon2():
    user_id = session.get("useronline")  # Check if the user is logged in
    if not user_id:
        flash("You must be logged in to view this page.", category="failed")
        return redirect(url_for('login'))

    deets = db.session.query(User).get(user_id)
    return render_template("client/comingsoon.html", deets=deets)


@app.route('/job_details2/<int:job_id>/')
def job_details2(job_id):
    user_id = session.get('useronline')  # Check if the user is logged in
    if not user_id:
        flash("You must be logged in to view this page.", category="failed")
        return redirect(url_for('login'))

    # Fetch the job details by job_id
    job = Jobs.query.get_or_404(job_id)
    if job.client_id != user_id:
        flash("You are not authorized to view this job.", category="failed")
        return redirect(url_for('my_posted_jobs'))

    return render_template('freelancer/job_details.html', job=job)


@app.route('/general_settings_freelancer/', methods=['GET', 'POST'])
def general_settings_freelancer():
    user_id = session.get('useronline')
    if not user_id:
        flash('You must be logged in to view this page.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Example: Update general settings (you can expand this logic as needed)
        enable_notifications = request.form.get('enable_notifications') == 'on'
        # Save general settings to the database (if applicable)
        flash('General settings updated successfully!', 'success')
        return redirect(url_for('general_settings_freelancer'))

    # Render the general settings page for GET requests
    return render_template('freelancer/general_settings_freelancer.html')





@app.route('/notifications_freelancer/')
def notifications_freelancer():
    user_id = session.get('useronline')
    if not user_id:
        flash('You must be logged in to view this page.', 'danger')
        return redirect(url_for('login'))

    user_notifications = Notifications.query.filter_by(user_id=user_id).order_by(Notifications.created_at.desc()).all()
    return render_template('freelancer/notifications_freelancer.html', notifications=user_notifications)



@app.route('/my_applications/')
def my_applications():
    user_id = session.get('useronline')  # Check if the user is logged in
    if not user_id:
        flash('You must be logged in to view your applications.', 'danger')
        return redirect(url_for('login'))

    # Fetch applications for the logged-in freelancer
    applications = db.session.query(
        JobApplicationsTable.jobs_id.label('job_id'),
        JobApplicationsTable.proposal,
        Jobs.title.label('job_title'),
        Jobs.description.label('job_description'),  # Explicitly include job_description
        Jobs.budget.label('job_budget')
    ).join(Jobs, JobApplicationsTable.jobs_id == Jobs.jobs_id) \
     .filter(JobApplicationsTable.user_id == user_id) \
     .all()

    return render_template('freelancer/my_applications.html', applications=applications)





@app.route('/delete_account_freelancer/', methods=['GET', 'POST'])
def delete_account_freelancer():
    user_id = session.get('useronline')
    if not user_id:
        flash('You must be logged in to perform this action.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        user = User.query.get(user_id)
        if user:
            try:
                # Delete all jobs associated with the client
                if user.user_type == 'client':
                    Jobs.query.filter_by(client_id=user_id).delete()

                # Delete all job applications associated with the user
                JobApplicationsTable.query.filter_by(user_id=user_id).delete()

                # Delete freelancer profile if the user is a freelancer
                if user.user_type == 'freelancer':
                    FreelancerProfileTable.query.filter_by(user_id=user_id).delete()

                # Delete notifications associated with the user
                Notifications.query.filter_by(user_id=user_id).delete()

                # Delete the user
                db.session.delete(user)
                db.session.commit()

                # Clear the session and redirect
                session.clear()
                flash('Your account has been deleted.', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()  # Rollback in case of an error
                flash(f'An error occurred while deleting your account: {str(e)}', 'danger')
                return redirect(url_for('settings'))
        else:
            flash('Account not found.', 'danger')
            return redirect(url_for('settings'))

    return render_template('freelancer/delete_account_freelancer.html')





   

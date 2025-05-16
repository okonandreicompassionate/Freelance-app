from flask import render_template,request,flash,url_for,redirect,session
from werkzeug.security import generate_password_hash,check_password_hash
from pkg import app,forms
from pkg.models import db,User,Jobs,ClientProfileTable,JobApplicationsTable,FreelancerProfileTable,Messages,Reviews,Notifications
from datetime import datetime














@app.route("/profile/")
def profile():
    user = session.get("useronline") #None if not logged in
    if user:

        deets = db.session.query(User).get(user)
        return render_template("client/client_profile.html",deets=deets)
    else:
        flash("You must be logged in to view this page", category="failed")
        return redirect(url_for('home'))
    



   

@app.route('/logout/')
def logout():
    user_id = session.get("useronline")  # Retrieve the logged-in user's ID
    if user_id:  # Check if the user is logged in
        session.pop('useronline', None)  # Remove the user ID from the session
        flash("You have been logged out successfully.", category="success")
        return redirect(url_for('home'))  # Redirect to the home page
    else:
        flash("You are not logged in.", category="failed")
        return redirect(url_for('home'))  # Redirect to the home page
    

@app.route("/client_dashboard/")
def client_dashboard():
    user_id = session.get("useronline")  # None if not logged in
    if user_id:
        deets = db.session.query(User).get(user_id)

        # Check if it's the user's first login
        if deets.first_login:  # Assuming `first_login` is a boolean field in the User model
            # Redirect to profile setup route
            return redirect(url_for("profile_setup_client"))
        

        # Fetch job applications for jobs posted by the logged-in client
        job_applications = db.session.query(
            JobApplicationsTable.jobs_id,
            JobApplicationsTable.proposal,
            JobApplicationsTable.email,
            User.user_fname.label('freelancer_name'),
            Jobs.title.label('job_title')
        ).join(User, JobApplicationsTable.user_id == User.user_id) \
         .join(Jobs, JobApplicationsTable.jobs_id == Jobs.jobs_id) \
         .filter(Jobs.client_id == user_id) \
         .all()

        return render_template("client/client_dashboard.html", deets=deets, job_applications=job_applications)
        

    else:
        flash("You must be logged in to view this page", category="failed")
        return redirect(url_for('home'))
    

@app.route('/post_job/', methods=['GET', 'POST'])
def post_job():
    user_id = session.get('useronline')  # Check if the user is logged in
    if not user_id:
        flash("You must be logged in to post a job.", category="failed")
        return redirect(url_for('login'))

    form = forms.JobPostForm()
    if form.validate_on_submit():
        title = form.job_title.data
        description = form.job_description.data
        skills = form.required_skills.data
        budget = form.budget.data
        deadline = form.deadline.data

        # Save the job post to the database
        job = Jobs(
            title=title,
            description=description,
            required_skills=skills,
            budget=budget,
            deadline=deadline,
            client_id=user_id  # Associate with the logged-in client
        )
        db.session.add(job)
        db.session.commit()

        flash("Job posted successfully!", category="success")
        return redirect(url_for('my_posted_jobs'))

    return render_template('client/post_jobs.html', form=form)


@app.route("/comingsoon/")
def comingsoon():
    user_id = session.get("useronline")  # Check if the user is logged in
    if not user_id:
        flash("You must be logged in to view this page.", category="failed")
        return redirect(url_for('login'))

    deets = db.session.query(User).get(user_id)
    return render_template("client/comingsoon.html", deets=deets)












@app.route('/freelancers/')
def freelancers():
    # Fetch all freelancer profiles
    freelancer_profile_table = FreelancerProfileTable.query.all()

    # Create a list to store freelancer names
    freelancer_names = [] # Correctly define the list before using it
    for profile in freelancer_profile_table:
        # Ensure the user relationship exists before accessing attributes
        if profile.user:
            client_name = f"{profile.user.user_fname} "
            freelancer_names.append(client_name)  # Add the name to the list
            print(client_name)  # Debugging: Print the name to the console

    # Pass the list of freelancer names to the template
    return render_template('client/freelancers.html', free=freelancer_profile_table, freelancer_names=freelancer_names)


@app.route('/my_posted_jobs/')
def my_posted_jobs():
    user_id = session.get('useronline')  # Check if the user is logged in
    if not user_id:
        flash("You must be logged in to view this page.", category="failed")
        return redirect(url_for('login'))

    # Fetch all jobs posted by the logged-in user
    posted_jobs = Jobs.query.filter_by(client_id=user_id).all()
    return render_template('client/my_posted_jobs.html', posted_jobs=posted_jobs)



@app.route('/delete_job/<int:job_id>/', methods=['POST'])
def delete_job(job_id):
    user_id = session.get('useronline')  # Check if the user is logged in
    if not user_id:
        flash("You must be logged in to perform this action.", category="failed")
        return redirect(url_for('login'))

    # Fetch the job to delete
    job = Jobs.query.get_or_404(job_id)
    if job.client_id != user_id:
        flash("You are not authorized to delete this job.", category="failed")
        return redirect(url_for('my_posted_jobs'))

    # Fetch all applicants for the job
    applicants = JobApplicationsTable.query.filter_by(jobs_id=job_id).all()

    # Send a notification to each applicant
    for application in applicants:
        applicant_id = application.user_id  # Assuming `user_id` is the foreign key to the freelancer
        notification = Notifications(
            user_id=applicant_id,
            content=f"We regret to inform you that the job '{job.title}' has been deleted. We appreciate your interest and encourage you to apply for other opportunities."
        )
        db.session.add(notification)

    # Delete related rows in job_applications_table
    JobApplicationsTable.query.filter_by(jobs_id=job_id).delete()

    # Delete the job
    db.session.delete(job)
    db.session.commit()

    flash("Job deleted successfully, and all applicants have been notified.", category="success")
    return redirect(url_for('my_posted_jobs'))






@app.route('/manage_applications/')
def manage_applications():
    # Fetch job applications with freelancer details and job title
    applications = db.session.query(
        JobApplicationsTable.proposal,
        JobApplicationsTable.email,
        User.user_fname.label('freelancer_name'),
        Jobs.title.label('job_title')  # Include the job title
    ).join(User, JobApplicationsTable.user_id == User.user_id) \
     .join(Jobs, JobApplicationsTable.jobs_id == Jobs.jobs_id) \
     .all()

    return render_template('client/manage_applications.html', applications=applications)





@app.route('/change_password_client/', methods=['GET', 'POST'])
def change_password_client():
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
            return redirect(url_for('change_password_client'))

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('change_password_client'))

        user.user_pwd = generate_password_hash(new_password)
        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('general_settings_client'))

    return render_template('client/change_password_client.html',form=form)




@app.route('/freelancer_profile/<int:user_id>')
def freelancer_profile(user_id):
    # Fetch the freelancer profile by user ID
    freelancer = FreelancerProfileTable.query.filter_by(user_id=user_id).first_or_404()

    # Ensure the user relationship exists
    if not freelancer.user:
        flash("Freelancer profile not found.", category="failed")
        return redirect(url_for('freelancers'))

    # Pass the freelancer profile to the template
    return render_template('client/freelancer_profile.html', freelancer=freelancer)

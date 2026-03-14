from flask import request, jsonify, redirect, flash, render_template
from flask_login import login_required
from . import admin_blueprint
from auth.decorators import admin_required
from auth.auth_manager import AuthManager
from auth.models import User



@admin_blueprint.route('/users/search', methods=['POST'])
@login_required
@admin_required

def search_users():
    auth_manager = admin_blueprint.auth_manager # <-- Imported instance from app.py, needed to create self-object on AuthManager class
    user_searchstr = request.form['email_str']
    if user_searchstr is None:
        print("❌ Ingen data tas emot från front end")
    #username = auth_manager.search_user(user_searchstr) # <-- Skapar user object
    user_object_list = auth_manager.search_user(user_searchstr) # <-- Skapar user object
    user_list = []
    if not user_object_list: # If no user 
        return jsonify({"error": "Inga användare hittades"})
    else:
        for object in user_object_list:
            user = {
                "username": object.username,
                "email": object.email
                }
            user_list.append(user)
        print(user_list)
        return jsonify(user_list)
    
@admin_blueprint.route('/users/get-user/<username>', methods=['GET'])
@login_required
@admin_required
def retrieve_user_data(username):
    auth_manager = admin_blueprint.auth_manager
    user_data = auth_manager.get_user(username)
    if user_data is None:
        return jsonify({"error": "Ingen användardata hittades"})
    else:
        data = {
                "username": user_data.username,
                "email": user_data.email,
                "User Active": user_data.active_user,
                "Admin role": user_data.is_admin,
                "Created at": user_data.created_at
                }
        return jsonify(data)
    

@admin_blueprint.route('/users/save', methods=['POST'])
@login_required
@admin_required
def save_user_data():
    auth_manager = admin_blueprint.auth_manager

    username = request.form['detail-username']
    email = request.form['detail-email']
    active_user = request.form.get('detail-active') == 'on'
    is_admin = request.form.get('detail-admin') == 'on'

    auth_manager.update_user(username, active_user, email, is_admin)
    flash('✅ Användarinformation uppdaterad')
    return redirect('/admin-page')
    
@admin_blueprint.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    auth_manager = admin_blueprint.auth_manager
    # Handle the password change form submission
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        active_user = request.form.get('active') == 'on'
        is_admin = request.form.get('admin') == 'on'
        password    = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate that the two new-password fields agree before hitting the DB
        if password != confirm_password:
            flash(' ❌ Lösenorden matchar inte.')
            return redirect('/users/create')

        # Delegate verification and DB update to auth_manager
        success = auth_manager.create_user(username, password, email, is_admin, active_user )

        if success:
            # Password updated — send the user back to the dashboard
            flash(' ✅ Användaren har skapats.')
            return redirect('/admin-page')
        else:
            # Old password was wrong
            flash(' ❌ Fel gammalt lösenord.')
            return redirect('/users/create')

    # GET request — just render the empty form
    return render_template('admin_page.html')

@admin_blueprint.route('/users/passwordupdate', methods=['POST']) #removed 'GET'
@login_required     
@admin_required
def update_password():
    auth_manager = admin_blueprint.auth_manager
    # Handle the password change form submission
    #if request.method == 'POST':
    username = request.form['detail-username-value']
    print(username)
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    # Validate that the two new-password fields agree before hitting the DB
    if new_password != confirm_password:
        flash('De lösenorden matchar inte.')
        return redirect('/users/passwordupdate')

    # Delegate verification and DB update to auth_manager
    # success = 
    auth_manager.update_password(username, new_password)

    #if success:
        # Password updated — send the user back to the dashboard
    flash('✅ Lösenordet har uppdaterats.')
    return redirect('/admin-page')
    #else:
    #    flash(' ❌ Något gick fel.')
    #    return redirect('/change-password')

    # GET request — just render the empty form
    # return render_template('change_password.html')
    
from flask import request, jsonify, redirect, flash
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
    

    
from flask import Blueprint, request, jsonify,render_template
from .models import User, Activity, db
from .tracker import start_tracking, stop_tracking
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,set_access_cookies,unset_jwt_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .middleware import get_current_user, jwt_required
from flask_login import current_user, login_required
from flask import session, redirect,url_for
auth_bp = Blueprint('auth', __name__, template_folder='templates',static_folder='static')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='scrypt')
    new_user = User(username=data['username'], password=hashed_password, is_admin=data.get('is_admin', False))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@auth_bp.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response

@auth_bp.route('/dashboard', methods=['GET'])
@jwt_required
def dashboard():
    user = get_current_user()
    if user is None:
        return redirect('/login')

    if user['is_admin']:
        users = User.query.filter_by(is_admin=False).all()
        return render_template('admin_dashboard.html', users=users)
    else:
        return render_template('employee_dashboard.html')




@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify(message="Missing username or password"), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password,password):
        access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'is_admin': user.is_admin})
        redirect_url='/dashboard'
        response = jsonify({'message': 'User registered successfully', 'redirect_url': redirect_url})
        print(response)
        set_access_cookies(response, access_token)
        return response, 200
    else:
        return jsonify(message="Invalid username or password"), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    response = jsonify(message="Logout successful")
    unset_jwt_cookies(response)
    return response, 200

@auth_bp.route('/start_tracking', methods=['POST'])
@jwt_required
def start_tracking_route():
    user = get_current_user()
    if user:
        start_tracking(user['id'])
        return jsonify(message="Tracking started"), 200
    return jsonify(message="Failed to start tracking"), 400

@auth_bp.route('/stop_tracking', methods=['POST'])
@jwt_required
def stop_tracking_route():
    stop_tracking()
    return jsonify(message="Tracking stopped"), 200

@auth_bp.route('/activities', methods=['GET'])
@jwt_required
def get_activities():
    user = get_current_user()
    if user is None:
        return jsonify(message="Unauthorized"), 401

    activities = Activity.query.filter_by(user_id=user['id']).all()
    activities_data = [
        {
            'start_time': activity.start_time,
            'end_time': activity.end_time,
            'activity': activity.activity
        }
        for activity in activities
    ]
    return jsonify(activities_data), 200

@auth_bp.route('/employee_activities', methods=['GET'])
@jwt_required
def get_employee_activities():
    user = get_current_user()
    if user is None or not user['is_admin']:
        return jsonify(message="Unauthorized"), 401

    employee_id = request.args.get('employee_id')
    if not employee_id:
        return jsonify(message="Missing employee_id"), 400

    activities = Activity.query.filter_by(user_id=employee_id).all()
    activities_data = [
        {
            'start_time': activity.start_time,
            'end_time': activity.end_time,
            'activity': activity.activity
        }
        for activity in activities
    ]
    return jsonify(activities_data), 200
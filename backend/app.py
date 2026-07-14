"""
Main Flask backend for the Complaint Management System.

This backend provides:
 - User registration, login, logout and session handling
 - Role-based protected routes for user and admin
 - Complaint CRUD and admin management
 - Profile editing
 - Dashboard analytics for both users and admins
"""

from flask import Flask, request, jsonify, send_from_directory, session, redirect
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from backend.db_connect import get_connection 
from functools import wraps
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
STATIC_DIR = os.path.join(BASE_DIR, 'static')


app = Flask(__name__, static_folder=FRONTEND_DIR, template_folder=FRONTEND_DIR)
app.secret_key = 'replace_with_a_secure_random_key'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
CORS(app)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        return func(*args, **kwargs)
    return wrapper


def get_session_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT user_id, name, email, role FROM users WHERE user_id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


@app.errorhandler(Exception)
def handle_all_errors(e):
    if isinstance(e, HTTPException):
        return jsonify({'success': False, 'error': e.description}), e.code
    return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/')
def index_page():
    return redirect('/login')


@app.route('/login')
def login_page():
    return send_from_directory(FRONTEND_DIR, 'login.html')


@app.route('/register')
def register_page():
    return send_from_directory(FRONTEND_DIR, 'register.html')


@app.route('/user_dashboard')
def user_dashboard_page():
    if 'user_id' not in session:
        return redirect('/login')
    return send_from_directory(FRONTEND_DIR, 'user_dashboard.html')


@app.route('/admin_dashboard')
def admin_dashboard_page():
    if session.get('role') != 'admin':
        return redirect('/login')
    return send_from_directory(FRONTEND_DIR, 'admin_dashboard.html')


@app.route('/add_complaint')
def add_complaint_page():
    if 'user_id' not in session:
        return redirect('/login')
    return send_from_directory(FRONTEND_DIR, 'add_complaint.html')


@app.route('/add')
def add_short_link():
    if 'user_id' not in session:
        return redirect('/login')
    return send_from_directory(FRONTEND_DIR, 'add_complaint.html')


@app.route('/complaints')
def complaints_page():
    if 'user_id' not in session:
        return redirect('/login')
    return send_from_directory(FRONTEND_DIR, 'complaints.html')


@app.route('/my_complaints')
def my_complaints_page():
    if 'user_id' not in session:
        return redirect('/login')
    return send_from_directory(FRONTEND_DIR, 'my_complaints.html')


@app.route('/manage_complaints')
def manage_complaints_page():
    if session.get('role') != 'admin':
        return redirect('/login')
    return send_from_directory(FRONTEND_DIR, 'manage_complaints.html')


@app.route('/track_complaint')
def track_complaint_page():
    if 'user_id' not in session:
        return redirect('/login')
    return send_from_directory(FRONTEND_DIR, 'track_complaint.html')


@app.route('/profile')
def profile_page():
    if 'user_id' not in session:
        return redirect('/login')
    return send_from_directory(FRONTEND_DIR, 'profile.html')


@app.route('/admin_users')
def admin_users_page():
    if session.get('role') != 'admin':
        return redirect('/login')
    return send_from_directory(FRONTEND_DIR, 'admin_users.html')


@app.route('/admin_departments')
def admin_departments_page():
    if session.get('role') != 'admin':
        return redirect('/login')
    return send_from_directory(FRONTEND_DIR, 'admin_departments.html')


@app.route('/admin_categories')
def admin_categories_page():
    if session.get('role') != 'admin':
        return redirect('/login')
    return send_from_directory(FRONTEND_DIR, 'admin_categories.html')


@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(STATIC_DIR, filename)


@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not name or not email or not password:
        return jsonify({'success': False, 'error': 'Name, email and password are required'}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT user_id FROM users WHERE email = %s', (email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Email already registered'}), 400

    hashed_password = generate_password_hash(password)
    cur.execute(
        'INSERT INTO users (name, email, password, role, created_at) VALUES (%s, %s, %s, %s, NOW())',
        (name, email, hashed_password, 'user')
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Account created successfully. Please login.'}), 201


@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password are required'}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT user_id, name, email, password, role FROM users WHERE email = %s', (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'success': False, 'error': 'Invalid login credentials'}), 401

    session['user_id'] = user['user_id']
    session['role'] = user['role']
    session['name'] = user['name']
    session['email'] = user['email']
    return jsonify({'success': True, 'role': user['role'], 'name': user['name']})


@app.route('/api/auth/session', methods=['GET'])
def api_session():
    user = get_session_user()
    if not user:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    return jsonify({'success': True, 'user': user})


@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@app.route('/api/user/profile', methods=['GET', 'PUT'])
@login_required
def api_user_profile():
    user = get_session_user()
    if not user:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    if request.method == 'GET':
        cur.execute('SELECT user_id, name, email, role, created_at FROM users WHERE user_id = %s', (user['user_id'],))
        profile = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'profile': profile})

    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not name or not email:
        return jsonify({'success': False, 'error': 'Name and email are required'}), 400

    cur.execute('SELECT user_id FROM users WHERE email = %s AND user_id != %s', (email, user['user_id']))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Email already in use'}), 400

    if password:
        hashed_password = generate_password_hash(password)
        cur.execute('UPDATE users SET name = %s, email = %s, password = %s WHERE user_id = %s', (name, email, hashed_password, user['user_id']))
    else:
        cur.execute('UPDATE users SET name = %s, email = %s WHERE user_id = %s', (name, email, user['user_id']))

    conn.commit()
    cur.close()
    conn.close()
    session['name'] = name
    session['email'] = email
    return jsonify({'success': True, 'message': 'Profile updated successfully'})


@app.route('/api/users', methods=['GET'])
@login_required
def api_users():
    user = get_session_user()
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    if user['role'] == 'admin':
        cur.execute('SELECT user_id, name, email, role FROM users ORDER BY name')
        rows = cur.fetchall()
    else:
        rows = [{'user_id': user['user_id'], 'name': user['name'], 'email': user['email'], 'role': user['role']}]
    cur.close()
    conn.close()
    return jsonify({'success': True, 'users': rows, 'data': rows})


@app.route('/api/departments', methods=['GET'])
def api_departments():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT dept_id, dept_name FROM departments ORDER BY dept_name')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'departments': rows})


@app.route('/api/categories', methods=['GET'])
def api_categories():
    dept_id = request.args.get('dept_id')
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    if dept_id:
        cur.execute('SELECT category_id, category_name, dept_id FROM categories WHERE dept_id = %s ORDER BY category_name', (dept_id,))
    else:
        cur.execute('SELECT category_id, category_name, dept_id FROM categories ORDER BY category_name')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'categories': rows})


@app.route('/api/status', methods=['GET'])
def api_status():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT status_id, status_name FROM status ORDER BY status_id')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'status': rows})


@app.route('/api/complaints', methods=['GET', 'POST'])
@login_required
def api_complaints():
    user = get_session_user()
    admin = user['role'] == 'admin'

    if request.method == 'POST':
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        dept_id = data.get('dept_id')
        category_id = data.get('category_id')
        priority = data.get('priority', '').strip().capitalize()
        if priority not in ['Low', 'Medium', 'High']:
            priority = 'Low'
        assigned_user_id = data.get('user_id') if admin else None
        user_id = assigned_user_id if admin and assigned_user_id else user['user_id']

        if not title or not description or not dept_id or not category_id:
            return jsonify({'success': False, 'error': 'All fields are required'}), 400

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            'INSERT INTO complaints (user_id, dept_id, category_id, status_id, title, description, priority, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())',
            (user_id, dept_id, category_id, 1, title, description, priority)
        )
        conn.commit()
        complaint_id = cur.lastrowid
        cur.close()
        conn.close()
        return jsonify({'success': True, 'complaint_id': complaint_id}), 201

    q = request.args.get('q', '').strip()
    dept = request.args.get('dept')
    priority = request.args.get('priority')
    status = request.args.get('status')
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc').lower()
    allowed_sort = {'created_at', 'priority', 'title'}
    if sort_by not in allowed_sort:
        sort_by = 'created_at'
    if order not in ('asc', 'desc'):
        order = 'desc'

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    query = '''SELECT c.complaint_id, c.title, c.description, c.priority, c.created_at,
                      u.user_id, u.name AS user_name, u.email AS user_email,
                      d.dept_id, d.dept_name,
                      cat.category_id, cat.category_name,
                      s.status_id, s.status_name
               FROM complaints c
               LEFT JOIN users u ON c.user_id = u.user_id
               LEFT JOIN departments d ON c.dept_id = d.dept_id
               LEFT JOIN categories cat ON c.category_id = cat.category_id
               LEFT JOIN status s ON c.status_id = s.status_id'''

    filters = []
    params = []
    if not admin:
        filters.append('c.user_id = %s')
        params.append(user['user_id'])
    if q:
        filters.append('(c.title LIKE %s OR c.description LIKE %s)')
        params.extend([f'%{q}%', f'%{q}%'])
    if dept:
        filters.append('c.dept_id = %s')
        params.append(dept)
    if priority:
        filters.append('c.priority = %s')
        params.append(priority)
    if status:
        filters.append('c.status_id = %s')
        params.append(status)

    if filters:
        query += ' WHERE ' + ' AND '.join(filters)
    query += f' ORDER BY c.{sort_by} {order.upper()}'

    cur.execute(query, tuple(params))
    complaints = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'complaints': complaints, 'data': complaints})


@app.route('/api/complaints/<int:complaint_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_complaint_detail(complaint_id):
    user = get_session_user()
    admin = user['role'] == 'admin'
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM complaints WHERE complaint_id = %s', (complaint_id,))
    complaint = cur.fetchone()
    if not complaint:
        cur.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Complaint not found'}), 404
    if not admin and complaint['user_id'] != user['user_id']:
        cur.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Permission denied'}), 403

    if request.method == 'GET':
        cur.execute('SELECT status_name FROM status WHERE status_id = %s', (complaint['status_id'],))
        status_row = cur.fetchone()
        complaint['status_name'] = status_row['status_name'] if status_row else 'Unknown'
        
        cur.execute('''
            SELECT cu.update_id, cu.update_message, cu.created_at, s.status_name, u.name as admin_name
            FROM complaint_updates cu
            LEFT JOIN status s ON cu.status_id = s.status_id
            LEFT JOIN users u ON cu.updated_by_admin = u.user_id
            WHERE cu.complaint_id = %s
            ORDER BY cu.created_at DESC
        ''', (complaint_id,))
        complaint['updates'] = cur.fetchall()
        
        cur.close()
        conn.close()
        return jsonify({'success': True, 'complaint': complaint})

    if request.method == 'DELETE':
        if not admin:
            cur.close()
            conn.close()
            return jsonify({'success': False, 'error': 'Admin only'}), 403
        cur.execute('DELETE FROM complaints WHERE complaint_id = %s', (complaint_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Complaint deleted successfully'})

    data = request.get_json() or {}
    updates = []
    params = []

    status_changed = False
    new_status_id = None
    if admin and data.get('status_id'):
        updates.append('status_id = %s')
        params.append(data['status_id'])
        status_changed = True
        new_status_id = data['status_id']
    if admin and data.get('dept_id'):
        updates.append('dept_id = %s')
        params.append(data['dept_id'])
    if admin and data.get('category_id'):
        updates.append('category_id = %s')
        params.append(data['category_id'])
    if data.get('title'):
        updates.append('title = %s')
        params.append(data['title'])
    if data.get('description'):
        updates.append('description = %s')
        params.append(data['description'])
    if admin and data.get('priority') in ['Low', 'Medium', 'High']:
        updates.append('priority = %s')
        params.append(data['priority'])

    if not updates and not (admin and (status_changed or data.get('remark'))):
        cur.close()
        conn.close()
        return jsonify({'success': False, 'error': 'No valid fields to update'}), 400

    if updates:
        params.append(complaint_id)
        cur.execute(f"UPDATE complaints SET {', '.join(updates)} WHERE complaint_id = %s", tuple(params))
        
    if admin and (status_changed or data.get('remark')):
        insert_status = new_status_id if status_changed else complaint['status_id']
        cur.execute('INSERT INTO complaint_updates (complaint_id, updated_by_admin, status_id, update_message) VALUES (%s, %s, %s, %s)', 
                    (complaint_id, user['user_id'], insert_status, data.get('remark', '')))
        
        # Add Notification for User
        notification_msg = f"Your complaint '#{complaint_id}: {complaint['title']}' has been updated."
        cur.execute('INSERT INTO notifications (user_id, message) VALUES (%s, %s)', (complaint['user_id'], notification_msg))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Complaint updated successfully'})

@app.route('/api/notifications', methods=['GET'])
@login_required
def get_notifications():
    user = get_session_user()
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC LIMIT 50', (user['user_id'],))
    notes = cur.fetchall()
    cur.execute('SELECT COUNT(*) as unread FROM notifications WHERE user_id = %s AND is_read = 0', (user['user_id'],))
    unread = cur.fetchone()['unread']
    cur.close()
    conn.close()
    return jsonify({'success': True, 'notifications': notes, 'unread': unread})

@app.route('/api/notifications/read', methods=['POST'])
@login_required
def mark_notifications_read():
    user = get_session_user()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE notifications SET is_read = 1 WHERE user_id = %s', (user['user_id'],))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})


@app.route('/api/user/dashboard', methods=['GET'])
@login_required
def api_user_dashboard():
    user = get_session_user()
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT COUNT(*) AS total FROM complaints WHERE user_id = %s', (user['user_id'],))
    total = cur.fetchone()['total']
    cur.execute('SELECT COUNT(*) AS pending FROM complaints c JOIN status s ON c.status_id = s.status_id WHERE c.user_id = %s AND s.status_name != %s', (user['user_id'], 'Resolved'))
    pending = cur.fetchone()['pending']
    cur.execute('SELECT COUNT(*) AS resolved FROM complaints c JOIN status s ON c.status_id = s.status_id WHERE c.user_id = %s AND s.status_name = %s', (user['user_id'], 'Resolved'))
    resolved = cur.fetchone()['resolved']
    cur.execute('''SELECT c.complaint_id, c.title, c.priority, c.created_at, s.status_name
                   FROM complaints c
                   JOIN status s ON c.status_id = s.status_id
                   WHERE c.user_id = %s
                   ORDER BY c.created_at DESC
                   LIMIT 5''', (user['user_id'],))
    recent = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'total': total, 'pending': pending, 'resolved': resolved, 'recent': recent})


@app.route('/api/admin/dashboard', methods=['GET'])
@admin_required
def api_admin_dashboard():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT COUNT(*) AS total_users FROM users')
    users = cur.fetchone()['total_users']
    cur.execute('SELECT COUNT(*) AS total_complaints FROM complaints')
    complaints = cur.fetchone()['total_complaints']
    cur.execute('SELECT COUNT(*) AS pending_complaints FROM complaints c JOIN status s ON c.status_id = s.status_id WHERE s.status_name != %s', ('Resolved',))
    pending = cur.fetchone()['pending_complaints']
    cur.execute('SELECT COUNT(*) AS resolved_complaints FROM complaints c JOIN status s ON c.status_id = s.status_id WHERE s.status_name = %s', ('Resolved',))
    resolved = cur.fetchone()['resolved_complaints']
    cur.execute('''SELECT d.dept_name, COUNT(c.complaint_id) AS total
                   FROM departments d
                   LEFT JOIN complaints c ON c.dept_id = d.dept_id
                   GROUP BY d.dept_id
                   ORDER BY total DESC''')
    department_stats = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'users': users, 'complaints': complaints, 'pending': pending, 'resolved': resolved, 'department_stats': department_stats})


@app.route('/api/admin/users', methods=['GET'])
@admin_required
def api_admin_users():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT user_id, name, email, role, created_at FROM users ORDER BY created_at DESC')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'users': users})


@app.route('/api/admin/departments', methods=['GET', 'POST'])
@admin_required
def api_admin_departments():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    if request.method == 'GET':
        cur.execute('SELECT dept_id, dept_name, description FROM departments ORDER BY dept_name')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'departments': rows})
    data = request.get_json() or {}
    name = data.get('dept_name', '').strip()
    description = data.get('description', '').strip()
    if not name:
        cur.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Department name is required'}), 400
    cur.execute('INSERT INTO departments (dept_name, description) VALUES (%s, %s)', (name, description))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Department created successfully'})

@app.route('/api/admin/departments/<int:dept_id>', methods=['DELETE'])
@admin_required
def delete_department(dept_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM departments WHERE dept_id = %s', (dept_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Department deleted successfully'})


@app.route('/api/admin/categories', methods=['GET', 'POST'])
@admin_required
def api_admin_categories():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    if request.method == 'GET':
        cur.execute('SELECT category_id, category_name, dept_id FROM categories ORDER BY category_name')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'categories': rows})
    data = request.get_json() or {}
    name = data.get('category_name', '').strip()
    dept_id = data.get('dept_id')
    if not name or not dept_id:
        cur.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Category name and department are required'}), 400
    cur.execute('INSERT INTO categories (category_name, dept_id) VALUES (%s, %s)', (name, dept_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Category created successfully'})

@app.route('/api/admin/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM categories WHERE category_id = %s', (category_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Category deleted successfully'})



@app.route('/api/admin/trends', methods=['GET'])
@login_required
def api_admin_trends():
    user = get_session_user()
    if user['role'] != 'admin':
        return jsonify({'success': False, 'error': 'Admin only'}), 403
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('''
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM complaints
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        LIMIT 7
    ''')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'trends': data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

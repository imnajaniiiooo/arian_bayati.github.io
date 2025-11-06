from flask import Flask, render_template, request, redirect, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'blog_admin_2024'

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"

# فایل ذخیره سازی
DATA_FILE = 'blog_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'settings': {
            'site_title': 'وبلاگ شخصی من',
            'site_description': 'این وبلاگ شخصی من است',
            'primary_color': '#4a6fa5',
            'secondary_color': '#6b8cbc',
            'accent_color': '#ff7e5f'
        },
        'posts': [
            {
                'id': 1,
                'title': 'مقاله اول من',
                'content': 'این اولین مقاله من است...',
                'category': 'عمومی',
                'date': '۱۴۰۲/۰۸/۲۰',
                'image': '/static/images/post1.jpg'
            }
        ]
    }

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/admin')
        else:
            return "نام کاربری یا رمز عبور اشتباه!"
    
    return '''
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>ورود مدیریت</title>
        <style>
            body {
                font-family: Tahoma;
                background: linear-gradient(135deg, #4a6fa5, #6b8cbc);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
            }
            .login-box {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                width: 350px;
                text-align: center;
            }
            input {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-sizing: border-box;
            }
            button {
                width: 100%;
                padding: 12px;
                background: #4a6fa5;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }
            .info {
                margin-top: 20px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 8px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>🔐 ورود به پنل مدیریت</h2>
            <form method="post">
                <input type="text" name="username" placeholder="نام کاربری" required>
                <input type="password" name="password" placeholder="رمز عبور" required>
                <button type="submit">ورود به پنل</button>
            </form>
            <div class="info">
                <strong>اطلاعات تست:</strong><br>
                نام کاربری: <strong>admin</strong><br>
                رمز عبور: <strong>123456</strong>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/admin/login')
    
    data = load_data()
    
    return f'''
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>پنل مدیریت</title>
        <style>
            body {{
                font-family: Tahoma;
                background: #f8f9fa;
                margin: 0;
                padding: 0;
            }}
            .header {{
                background: white;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin: 30px 0;
            }}
            .stat-box {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border-left: 4px solid {data['settings']['accent_color']};
            }}
            .menu {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin: 40px 0;
            }}
            .menu-item {{
                background: {data['settings']['primary_color']};
                color: white;
                padding: 25px;
                text-align: center;
                border-radius: 10px;
                text-decoration: none;
                font-size: 18px;
                transition: 0.3s;
            }}
            .menu-item:hover {{
                background: {data['settings']['secondary_color']};
                transform: translateY(-3px);
            }}
            .logout {{
                background: #dc3545 !important;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 پنل مدیریت {data['settings']['site_title']}</h1>
            <p>خوش آمدید! اینجا می‌توانید سایت خود را مدیریت کنید.</p>
        </div>
        
        <div class="container">
            <div class="stats">
                <div class="stat-box">
                    <h3>📊 مقالات</h3>
                    <p style="font-size: 24px; margin: 10px 0;">{len(data['posts'])} مقاله</p>
                    <small>مقالات منتشر شده</small>
                </div>
                <div class="stat-box">
                    <h3>👥 کاربران</h3>
                    <p style="font-size: 24px; margin: 10px 0;">۴۵ کاربر</p>
                    <small>کاربران ثبت‌نام شده</small>
                </div>
                <div class="stat-box">
                    <h3>💬 نظرات</h3>
                    <p style="font-size: 24px; margin: 10px 0;">۲۳ نظر</p>
                    <small>نظرات تایید نشده</small>
                </div>
            </div>
            
            <div class="menu">
                <a href="/admin/posts" class="menu-item">📝 مدیریت مقالات</a>
                <a href="/admin/users" class="menu-item">👥 مدیریت کاربران</a>
                <a href="/admin/comments" class="menu-item">💬 مدیریت نظرات</a>
                <a href="/admin/settings" class="menu-item">⚙️ تنظیمات سایت</a>
                <a href="/" class="menu-item" style="background: #28a745;">🏠 مشاهده سایت</a>
                <a href="/admin/logout" class="menu-item logout">🚪 خروج از سیستم</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/admin/posts')
def manage_posts():
    if not session.get('admin'):
        return redirect('/admin/login')
    
    data = load_data()
    
    posts_html = ""
    for post in data['posts']:
        posts_html += f'''
        <tr>
            <td>{post['title']}</td>
            <td>{post['category']}</td>
            <td>{post['date']}</td>
            <td>
                <button style="background: #17a2b8; color: white; padding: 5px 10px; border: none; border-radius: 3px; margin: 0 2px;">ویرایش</button>
                <button style="background: #dc3545; color: white; padding: 5px 10px; border: none; border-radius: 3px; margin: 0 2px;">حذف</button>
            </td>
        </tr>
        '''
    
    return f'''
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>مدیریت مقالات</title>
        <style>
            body {{
                font-family: Tahoma;
                background: #f8f9fa;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                padding: 12px;
                border: 1px solid #ddd;
                text-align: right;
            }}
            th {{
                background: #4a6fa5;
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📝 مدیریت مقالات</h1>
            <button style="background: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 5px; margin: 10px 0; cursor: pointer;">➕ مقاله جدید</button>
            
            <table>
                <tr>
                    <th>عنوان مقاله</th>
                    <th>دسته‌بندی</th>
                    <th>تاریخ</th>
                    <th>عملیات</th>
                </tr>
                {posts_html}
            </table>
            
            <br>
            <a href="/admin" style="color: #4a6fa5; text-decoration: none;">↩️ بازگشت به پنل مدیریت</a>
        </div>
    </body>
    </html>
    '''

@app.route('/admin/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

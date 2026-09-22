import os
import sqlite3
import webview

class ClinicApi:
    def __init__(self):
        self.init_db()

    def init_db(self):
        # إنشاء قاعدة بيانات خفيفة SQLite لتخزين بيانات المستخدمين والحجوزات
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE,
                password TEXT,
                is_verified INTEGER DEFAULT 1
            )
        ''')
        # إضافة مستخدم تجريبي افتراضي للاختبار
        cursor.execute("OR IGNORE INTO users (phone, password, is_verified) VALUES ('07700000000', '123456', 1)")
        conn.commit()
        conn.close()

    def handle_login(self, phone, password):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE phone = ? AND password = ?", (phone, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {"status": "success", "message": "تم تسجيل الدخول بنجاح إلى نظام العيادة!"}
        return {"status": "error", "message": "رقم الهاتف أو كلمة المرور غير صحيحة"}

    def send_sms_recovery(self, phone):
        # هنا سنقوم لاحقاً بربط API إرسال الـ SMS الحقيقي (مثل Twilio أو Infobip)
        print(f"تم إرسال كود الاستعادة عبر الـ SMS إلى الرقم: {phone}")
        return {"status": "success", "message": f"تم إرسال رمز استعادة كلمة المرور إلى الرقم {phone}"}

if __name__ == '__main__':
    api = ClinicApi()
    # فتح نافذة سطح مكتب عبر pywebview تعرض واجهة الـ HTML
    window = webview.create_window(
        'نظام إدارة العيادة الطبية', 
        'frontend/index.html', 
        js_api=api, 
        width=950, 
        height=650
    )
    webview.start()
import re
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

# Load biến môi trường từ .env
load_dotenv()

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# =============================
# 1. ĐĂNG KÝ TÀI KHOẢN
# =============================
def register_user(email, password, full_name):
    try:
        # Kiểm tra định dạng email
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            return False, "❌ Email không hợp lệ."

        # Kiểm tra email đã tồn tại chưa
        user_list = supabase.auth.admin.list_users(email=email)
        if user_list.users:
            return False, "⚠️ Email này đã được đăng ký. Vui lòng đăng nhập hoặc sử dụng email khác."

        # Đăng ký tài khoản
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if not res.user:
            return False, "⚠️ Không thể đăng ký tài khoản, vui lòng thử lại."

        return True, f"✅ Đăng ký thành công! Vui lòng xác minh email: {email}"

    except Exception as e:
        return False, f"❌ Lỗi đăng ký: {str(e)}"


# =============================
# 2. ĐĂNG NHẬP
# =============================
def login_user(email, password):
    try:
        result = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = result.user
        session = result.session

        if not session:
            return False, "❌ Sai email hoặc mật khẩu."

        if user.email_confirmed_at is None:
            return False, "📩 Vui lòng xác minh email trước khi đăng nhập."

        # Lưu thông tin user vào session
        st.session_state["user"] = {
            "id": user.id,
            "email": user.email
        }

        # =============================
        # TẠO user_profiles nếu chưa có
        # =============================
        profile_check = supabase.table("user_profiles").select("id").eq("id", user.id).execute()
        if not profile_check.data:
            supabase.table("user_profiles").insert({
                "id": user.id,
                "full_name": user.email.split("@")[0],
                "role": "client"
            }).execute()

        return True, f"🎉 Đăng nhập thành công, xin chào {user.email}!"

    except Exception as e:
        return False, f"❌ Lỗi đăng nhập: {e}"


# =============================
# 3. RESET PASSWORD
# =============================
def reset_password(email):
    try:
        supabase.auth.reset_password_for_email(email)
        return True, "📬 Đã gửi email đặt lại mật khẩu."
    except Exception as e:
        return False, f"❌ Lỗi khi gửi email: {e}"


# =============================
# 4. LƯU BÀI HÁT
# =============================
def save_song(user_id, title, lyrics, genre, audio_url, style, instruments, is_public=False):
    try:
        supabase.table("songs").insert({
            "user_id": user_id,
            "title": title,
            "lyrics": lyrics,
            "genre": genre,
            "audio_url": audio_url,
            "style": style,
            "instruments": instruments,
            "is_public": is_public
        }).execute()
        return True
    except Exception as e:
        print("Lỗi lưu bài hát:", e)
        return False

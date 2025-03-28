
# auth.py

import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

# Kết nối Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# 1. HÀM ĐĂNG KÝ NGƯỜI DÙNG (Sign Up)
# ============================================
import re  # Thêm trên đầu file nếu chưa có

def register_user(email, password, full_name):
    try:
        # Kiểm tra định dạng email bằng regex
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            return False, "❌ Email không hợp lệ. Vui lòng kiểm tra lại."

        # Gửi yêu cầu đăng ký
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        # Nếu không có user được trả về
        if not res.user:
            return False, "⚠️ Email này đã được đăng ký. Vui lòng đăng nhập hoặc sử dụng email khác."

        return True, f"✅ Đăng ký thành công! Mã xác minh đã được gửi đến {email}."

    except Exception as e:
        error_message = str(e)

        # Bắt lỗi phổ biến
        if "User already registered" in error_message or "duplicate key" in error_message or "Email rate limit" in error_message:
            return False, "⚠️ Email đã tồn tại. Vui lòng đăng nhập hoặc dùng email khác."

        print("Đăng ký lỗi:", error_message)
        return False, f"❌ Lỗi đăng ký: {error_message}"



# ============================================
# 2. HÀM ĐĂNG NHẬP (Sign In)
# ============================================
def login_user(email, password):
    try:
        # Gửi yêu cầu đăng nhập
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

        # Lưu vào session_state của Streamlit
        st.session_state["user"] = {
            "id": user.id,
            "email": user.email
        }

        # ============================================
        # TẠO PROFILE VÀ VÍ CREDITS nếu chưa tồn tại
        # ============================================
        # Kiểm tra user_profiles
        profile_check = supabase.table("user_profiles").select("id").eq("id", user.id).execute()
        if not profile_check.data:
            supabase.table("user_profiles").insert({
                "id": user.id,
                "full_name": user.email.split("@")[0],
                "role": "client"
            }).execute()

            supabase.table("credits_wallet").insert({
                "user_id": user.id,
                "credit": 10000000
            }).execute()

        return True, f"🎉 Xin chào {user.email}!"

    except Exception as e:
        return False, f"❌ Lỗi đăng nhập: {e}"

# ============================================
# 3. EXPORT LẠI SUPABASE ĐỂ DÙNG RESET PASSWORD
# ============================================
# Trong app.py sẽ gọi: from auth import supabase


    return True, "✅ Đã trừ credit"
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
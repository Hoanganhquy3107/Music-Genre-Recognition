
# auth.py

import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import re  # Thêm trên đầu file nếu chưa có
# Load biến môi trường
load_dotenv()

# Kết nối Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# 1. HÀM ĐĂNG KÝ NGƯỜI DÙNG (Sign Up)
# ============================================

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
       
        # Đăng ký thành công, lưu vào session_state
        st.session_state["user"] = {
            "id": res.user.id,
            "email": res.user.email,
        }

        # Cập nhật user vào bảng user_profiles (không có access_token ở đây)
        supabase.table("user_profiles").upsert({
            "id": res.user.id,
            "full_name": full_name,
            "role": "client"
        }).execute()

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
            "password": password,
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
            "email": user.email,
        }

        # Lưu access token vào session_state
        st.session_state["access_token"] = session.access_token  # Lưu token vào session_state

        # Kiểm tra xem user có trong bảng user_profiles chưa
        profile_check = supabase.table("user_profiles").select("id").eq("id", user.id).execute()

        if not profile_check.data:
            # Nếu chưa có thì insert vào bảng user_profiles
            supabase.table("user_profiles").insert({
                "id": user.id,
                "full_name": user.email.split("@")[0],
                "role": "client"
            }).execute()

        # Cập nhật hoặc chèn access_token vào bảng user_profiles
        supabase.table("user_profiles").upsert({
            "id": user.id,
            "access_token": session.access_token  # Lưu access_token vào bảng user_profiles
        }).execute()

        return True, f"🎉 Xin chào {user.email}!"

    except Exception as e:
        return False, f"❌ Lỗi đăng nhập: {e}"








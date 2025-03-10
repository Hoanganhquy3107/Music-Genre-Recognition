import numpy as np
import streamlit as st
import base64
import pytube
import os
import subprocess 
import librosa
import tempfile 
from pydub import AudioSegmentimport os
import sqlite3
import sqlite3
import bcrypt
import re  # Thêm thư viện kiểm tra email hợp lệ
from openai import OpenAI
import numpy as np
import streamlit as st
import base64
import pytube
import os
import subprocess 
import librosa
import tempfile 
from pydub import AudioSegment
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import tensorflow as tf
from statistics import mode
from tensorflow import keras
from keras import regularizers
from keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (Conv2D, MaxPooling2D, Flatten, Dropout, Dense, Activation)
from streamlit_option_menu import option_menu
import time
from dotenv import load_dotenv
from supabase import create_client, Client

st.set_page_config(page_title="Music AI Website", layout="wide")
# Load API key từ file .env
load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_lyrics(prompt):
    """Gửi prompt đến OpenAI API để tạo lời bài hát"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Hoặc "gpt-3.5-turbo" nếu tài khoản không có quyền truy cập GPT-4
            messages=[
                {"role": "system", "content": "Bạn là một nhạc sĩ sáng tác lời bài hát chuyên nghiệp."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=900
        )

        # ✅ Lấy nội dung phản hồi đúng cách
        return response.choices[0].message.content  

    except Exception as e:
        return f"⚠️ Lỗi khi tạo lời bài hát: {str(e)}"

# Test thử hàm
#prompt = "Viết lời bài hát về tình yêu mùa thu"
#lyrics = generate_lyrics(prompt)
#print(lyrics)

st.markdown(
    """
    <style>
        /* Đặt hình nền chung cho toàn bộ trang */
        body, .stApp {
            background: url("https://i.pinimg.com/originals/c3/aa/cd/c3aacdb10d1c0d550b7fa08b6d0bddb1.jpg") no-repeat center center fixed;
            background-size: cover;
        }

        /* Sidebar trong suốt, giữ nền đồng nhất */
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(5px);
            border-right: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* Làm mờ nhẹ phần nội dung chính để nổi bật hơn */
        .stApp > div:nth-child(1) {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
        }

        /* Chỉnh màu chữ để dễ đọc trên nền */
        h1, h2, h3, p {
            color: white !important;
        }

        /* Tùy chỉnh nút bấm */
        .stButton>button {
            background: linear-gradient(to right, #ff758c, #ff7eb3);
            color: white;
            font-size: 16px;
            border: none;
            padding: 10px;
            border-radius: 8px;
            transition: 0.3s;
        }

        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(to right, #ff5f6d, #ffc371);
        }

        /* Ô nhập liệu trong suốt */
        .stTextInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.2) !important;
            border-radius: 5px;
            border: 1px solid rgba(255, 255, 255, 0.5) !important;
            padding: 10px !important;
            font-size: 14px !important;
            color: white !important;
        }

    </style>
    """,
    unsafe_allow_html=True
)





# Tạo menu Sidebar có icon
with st.sidebar:
    st.image("https://media.giphy.com/media/xThtapIXXGuYEnqNgU/giphy.gif", use_container_width=True)

    menu = option_menu(
        menu_title="Navigation",
        options=["Home", "Create Lyrics", "Feel The Beat", "Classify", "Explore", "Library", "Search"],
        icons=["house", "music-note-list", "soundwave", "graph-up", "globe", "book", "search"],
        menu_icon="menu-button-wide",
        default_index=0,
        styles={
            "container": {"background-color": "rgba(0,0,0,0.8)", "padding": "5px"},
            "icon": {"color": "#feb47b", "font-size": "20px"},
            "nav-link": {"font-size": "18px", "color": "#ffffff", "text-align": "left", "margin": "5px"},
            "nav-link-selected": {"background-color": "#ff7e5f"},
        }
    )




# Nếu chọn "Classify", hiển thị nội dung này
if menu == "Classify":
    st.markdown("<h1 style='text-align: center; color: white;'>Music Genre Recognition</h1>", unsafe_allow_html=True)

    # Upload file mp3
    st.write("## Upload an MP3 file to classify:")
    mp3_file = st.file_uploader("Upload an audio file", type=["mp3"], label_visibility="collapsed")    
    
    if mp3_file is not None:
        st.write("**Play the song below:**")
        st.audio(mp3_file, "audio/mp3")

        # Hàm chuyển đổi MP3 sang WAV
        def convert_mp3_to_wav(music_file):  
            sound = AudioSegment.from_mp3(music_file)
            sound.export("music_file.wav", format="wav")

        # Hàm tạo Mel Spectrogram
        def create_melspectrogram(wav_file):  
            y, sr = librosa.load(wav_file)  
            mel_spec = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr))    
            plt.figure(figsize=(10, 5))
            plt.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
            librosa.display.specshow(mel_spec, x_axis="time", y_axis='mel', sr=sr)
            plt.margins(0)
            plt.savefig('melspectrogram.png')

        # Xây dựng mô hình CNN
        def GenreModel(input_shape=(100,200,4), classes=10):
            classifier = Sequential()
            classifier.add(Conv2D(8, (3, 3), input_shape=input_shape, activation='relu'))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Conv2D(16, (3, 3), activation='relu'))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Conv2D(32, (3, 3), activation='relu'))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Conv2D(64, (3, 3), activation='relu'))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Conv2D(128, (3, 3), activation='relu'))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Flatten())
            classifier.add(Dropout(0.5))
            classifier.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.0001)))
            classifier.add(Dropout(0.25))
            classifier.add(Dense(10, activation='softmax'))
            classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            return classifier

        # Dự đoán thể loại nhạc
        def predict(image_data, model):   
            image = img_to_array(image_data)   
            image = np.reshape(image, (1, 100, 200, 4))   
            prediction = model.predict(image / 255)   
            prediction = prediction.reshape((10,))     
            class_label = np.argmax(prediction)     
            return class_label, prediction

        # Nhãn của các thể loại nhạc
        class_labels = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

        # Load mô hình
        model = GenreModel(input_shape=(100, 200, 4), classes=10)
        model.load_weights("music_genre_recog_model.h5")

        # Hiệu ứng loading
        with st.spinner("🔍 Analyzing music genre..."):
            time.sleep(2)

        # Chuyển đổi file và tạo spectrogram
        convert_mp3_to_wav(mp3_file)
        audio_full = AudioSegment.from_wav('music_file.wav')

        class_labels_total = []
        predictions_total = []
        for w in range(int(round(len(audio_full) / 3000, 0))):
            audio_3sec = audio_full[3 * (w) * 1000: 3 * (w + 1) * 1000]
            audio_3sec.export(out_f="audio_3sec.wav", format="wav")
            create_melspectrogram("audio_3sec.wav")
            image_data = load_img('melspectrogram.png', color_mode='rgba', target_size=(100, 200))   
            class_label, prediction = predict(image_data, model)
            class_labels_total.append(class_label)
            predictions_total.append(prediction)

        # Lấy thể loại có dự đoán cao nhất
        class_label_final = mode(class_labels_total)
        predictions_final = np.mean(predictions_total, axis=0)

        # Hiển thị kết quả
        st.success(f"✅ The genre of your song is: **{class_labels[class_label_final]}**")
        # Hiển thị biểu đồ xác suất dự đoán
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(class_labels, predictions_final, color=cm.viridis(np.linspace(0, 1, len(class_labels))))
        ax.set_xlabel("Music Genre")
        ax.set_ylabel("Prediction Probability")
        ax.set_title("Genre Prediction Probability Distribution")
        ax.set_xticklabels(class_labels, rotation=45)
        # Hiển thị biểu đồ trong Streamlit
        st.pyplot(fig)



import requests
# =================== GIAO DIỆN CHO CREATE LYRICS ===================
if menu == "Create Lyrics":
    st.markdown("<h1>🎶 AI Lyric Generator 🎵</h1>", unsafe_allow_html=True)

    # Người dùng nhập thể loại nhạc và chủ đề
    genre = st.selectbox("🎼 Chọn thể loại nhạc:", ["Pop", "Rock", "Hip-Hop", "Jazz", "Ballad", "EDM"])
    theme = st.text_input("✍️ Nhập chủ đề bài hát (VD: Tình yêu, Mùa thu, Tuổi trẻ, ...)")
    mood = st.radio("🎭 Chọn cảm xúc:", ["Vui vẻ", "Buồn", "Hào hứng", "Thư giãn", "Kịch tính"])

    if st.button("🎤 Sáng tác ngay!"):
        if theme.strip():
            with st.spinner("🎶 AI đang sáng tác lời bài hát cho bạn..."):
                prompt = f"Hãy viết lời bài hát thể loại {genre} về chủ đề '{theme}', với cảm xúc {mood}."
                lyrics = generate_lyrics(prompt)
                print(lyrics)
                st.text_area("🎼 Lời bài hát AI tạo:", lyrics, height=300)
        else:
            st.warning("⚠️ Vui lòng nhập chủ đề bài hát trước khi tạo!")
       

if menu == "Feel The Beat":
    st.title("🎵 Feel The Beat - Tạo Nhạc AI")

    # Nhập API Token
    api_token = st.text_input("🔑 Nhập API Token:", type="password")

    # Nhập mô tả nhạc cần tạo
    prompt = st.text_area("💡 Nhập mô tả bản nhạc bạn muốn tạo:", 
                          placeholder="Một bản nhạc piano thư giãn với giai điệu nhẹ nhàng...")

    # Các tùy chọn nhạc
    style = st.selectbox("🎼 Chọn phong cách nhạc:", ["Classical", "Jazz", "Lo-fi", "Ambient", "Rock"])
    title = st.text_input("🎶 Đặt tên bản nhạc:", "My AI Music")
    instrumental = st.checkbox("🎻 Nhạc không lời?", value=False)

    # Xử lý khi bấm nút
    if st.button("🎧 Feel The Beat"):
        if not api_token or not prompt:
            st.warning("⚠️ Vui lòng nhập API Token và mô tả nhạc!")
        else:
            # Gửi yêu cầu API tạo nhạc
            api_url = "https://apibox.erweima.ai/api/v1/generate"
            headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
            data = {
                "prompt": prompt,
                "style": style,
                "title": title,
                "customMode": True,
                "instrumental": instrumental,
                "model": "V3_5",
                "callBackUrl": "https://api.example.com/callback"
            }

            with st.spinner("🎼 Đang tạo nhạc..."):
                response = requests.post(api_url, json=data, headers=headers)

            # Xử lý kết quả
            if response.status_code == 200:
                task_id = response.json().get("data", {}).get("taskId", None)
                st.write("📌 Task ID:", task_id)  # Debug Task ID

                if not task_id:
                    st.error("🚨 API không trả về Task ID!")
                else:
                    check_url = f"https://apibox.erweima.ai/api/v1/generate/record-info?taskId={task_id}"
                    headers = {
                        "Authorization": f"Bearer {api_token}",
                        "Accept": "application/json"
                    }

                    st.info("⏳ Đang chờ nhạc... (tối đa 5 phút)")
                    audio_url = None

                    for _ in range(60):  # Lặp tối đa 60 lần (5 phút)
                        check_response = requests.get(check_url, headers=headers)

                        if check_response.status_code == 200:
                            try:
                                music_info = check_response.json()
                                data = music_info.get("data", {})
                                status = data.get("status", "PENDING")  # Kiểm tra trạng thái

                                if status == "SUCCESS":
                                    response_data = data.get("response", {})
                                    suno_data = response_data.get("sunoData", [])

                                    if suno_data and isinstance(suno_data, list):
                                        audio_url = suno_data[0].get("audioUrl")

                                if audio_url:
                                    break  # Dừng vòng lặp nếu đã có nhạc

                            except Exception as e:
                                st.error(f"🚨 Lỗi khi xử lý JSON từ API: {e}")
                                st.write("📄 Nội dung API trả về:", check_response.text)
                                break  # Nếu lỗi, dừng luôn
                        time.sleep(5)  # Chờ 5 giây trước khi kiểm tra lại

                    # Kiểm tra kết quả sau vòng lặp
                    if audio_url:
                        st.success(f"🎵 Nhạc đã sẵn sàng: [{title}]({audio_url})")
                        st.audio(audio_url, format="audio/mp3")
                    else:
                        st.warning("⏳ Nhạc chưa sẵn sàng sau 5 phút, hãy thử lại sau!")
            else:
                st.error(f"🚨 Lỗi API: {response.json().get('error', 'Không rõ lỗi!')}")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import tensorflow as tf
from statistics import mode
from tensorflow import keras
from keras import regularizers
from keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (Conv2D, MaxPooling2D, Flatten, Dropout, Dense, Activation)
from streamlit_option_menu import option_menu
import time
from openai import OpenAI  
import openai  

# Cấu hình trang
st.set_page_config(page_title="Music AI Website", layout="wide")

# Tùy chỉnh CSS cho Sidebar
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-image: url("https://cdn.pixabay.com/photo/2024/02/26/14/13/sky-8598072_1280.jpg");
            background-size: cover;
        }
        .css-1d391kg {
            background-color: rgba(0,0,0,0.8) !important;
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            color: white;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            transition: 0.3s;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Tạo menu Sidebar có icon
with st.sidebar:
    st.markdown(
        '<img src="https://media.giphy.com/media/xThtapIXXGuYEnqNgU/giphy.gif" width="100%">',
        unsafe_allow_html=True
    )
    menu = option_menu(
        menu_title="Navigation",
        options=["Home", "Create Lyric", "Feel The Beat", "Classify", "Explore", "Library", "Search"],
        icons=["house", "music-note-list", "soundwave", "graph-up", "globe", "book", "search"],
        menu_icon="menu-button-wide",
        default_index=0,
        styles={
            "container": {"background-color": "rgba(0,0,0,0.8)", "padding": "5px"},
            "icon": {"color": "#feb47b", "font-size": "20px"},
            "nav-link": {"font-size": "18px", "color": "#ffffff", "text-align": "left", "margin": "5px"},
            "nav-link-selected": {"background-color": "#ff7e5f"},
        }
    )
    




# --- Tạo Lời Bài Hát Bằng AI ---
if menu == "Create Lyric":
    st.title("🎼 Tạo Lời Bài Hát Bằng AI")

    # Nhập API Key
    api_key = st.text_input("🔑 Nhập API Key của bạn:", type="password")

    # Nhập ý tưởng bài hát
    song_idea = st.text_area("💡 Nhập ý tưởng cho bài hát:", placeholder="Viết về tình yêu, mùa thu, hoặc bất kỳ điều gì bạn muốn...")

    # Xử lý khi người dùng nhấn nút tạo lời bài hát
    if st.button("✨ Tạo Lời Bài Hát"):
        if not api_key:
            st.warning("⚠️ Vui lòng nhập API Key!")
        elif not song_idea:
            st.warning("⚠️ Vui lòng nhập ý tưởng bài hát!")
        else:
            try:
                # Gửi yêu cầu đến OpenAI GPT
                openai.api_key = api_key  # Truyền API Key đúng cách
                
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": f"Viết lời bài hát theo phong cách chuyên nghiệp dựa trên ý tưởng: {song_idea}"}],
                    max_tokens=300
                )

                # Lấy nội dung trả về từ API
                lyrics = response["choices"][0]["message"]["content"].strip()

                # Hiển thị kết quả
                st.subheader("🎶 Lời Bài Hát Của Bạn:")
                st.text_area("📜", lyrics, height=300)

            except openai.error.OpenAIError as e:
                st.error(f"🚨 Lỗi từ OpenAI: {e}")
            except Exception as e:
                st.error(f"🚨 Lỗi hệ thống: {e}")

# Nếu chọn "Classify", hiển thị nội dung này
if menu == "Classify":
    st.markdown("<h1 style='text-align: center; color: white;'>Music Genre Recognition</h1>", unsafe_allow_html=True)

    # Upload file mp3
    st.write("## Upload an MP3 file to classify:")
    mp3_file = st.file_uploader("Upload an audio file", type=["mp3"], label_visibility="collapsed")    
    
    if mp3_file is not None:
        st.write("**Play the song below:**")
        st.audio(mp3_file, "audio/mp3")

        # Hàm chuyển đổi MP3 sang WAV
        def convert_mp3_to_wav(music_file):  
            sound = AudioSegment.from_mp3(music_file)
            sound.export("music_file.wav", format="wav")

        # Hàm tạo Mel Spectrogram
        def create_melspectrogram(wav_file):  
            y, sr = librosa.load(wav_file)  
            mel_spec = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr))    
            plt.figure(figsize=(10, 5))
            plt.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
            librosa.display.specshow(mel_spec, x_axis="time", y_axis='mel', sr=sr)
            plt.margins(0)
            plt.savefig('melspectrogram.png')

        # Xây dựng mô hình CNN
        def GenreModel(input_shape=(100,200,4), classes=10):
            classifier = Sequential()
            classifier.add(Conv2D(8, (3, 3), input_shape=input_shape, activation='relu'))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Conv2D(16, (3, 3), activation='relu'))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Conv2D(32, (3, 3), activation='relu'))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Conv2D(64, (3, 3), activation='relu'))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Conv2D(128, (3, 3), activation='relu'))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Flatten())
            classifier.add(Dropout(0.5))
            classifier.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.0001)))
            classifier.add(Dropout(0.25))
            classifier.add(Dense(10, activation='softmax'))
            classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            return classifier

        # Dự đoán thể loại nhạc
        def predict(image_data, model):   
            image = img_to_array(image_data)   
            image = np.reshape(image, (1, 100, 200, 4))   
            prediction = model.predict(image / 255)   
            prediction = prediction.reshape((10,))     
            class_label = np.argmax(prediction)     
            return class_label, prediction

        # Nhãn của các thể loại nhạc
        class_labels = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

        # Load mô hình
        model = GenreModel(input_shape=(100, 200, 4), classes=10)
        model.load_weights("music_genre_recog_model.h5")

        # Hiệu ứng loading
        with st.spinner("🔍 Analyzing music genre..."):
            time.sleep(2)

        # Chuyển đổi file và tạo spectrogram
        convert_mp3_to_wav(mp3_file)
        audio_full = AudioSegment.from_wav('music_file.wav')

        class_labels_total = []
        predictions_total = []
        for w in range(int(round(len(audio_full) / 3000, 0))):
            audio_3sec = audio_full[3 * (w) * 1000: 3 * (w + 1) * 1000]
            audio_3sec.export(out_f="audio_3sec.wav", format="wav")
            create_melspectrogram("audio_3sec.wav")
            image_data = load_img('melspectrogram.png', color_mode='rgba', target_size=(100, 200))   
            class_label, prediction = predict(image_data, model)
            class_labels_total.append(class_label)
            predictions_total.append(prediction)

        # Lấy thể loại có dự đoán cao nhất
        class_label_final = mode(class_labels_total)
        predictions_final = np.mean(predictions_total, axis=0)

        # Hiển thị kết quả
        st.success(f"✅ The genre of your song is: **{class_labels[class_label_final]}**")
        # Hiển thị biểu đồ xác suất dự đoán
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(class_labels, predictions_final, color=cm.viridis(np.linspace(0, 1, len(class_labels))))
        ax.set_xlabel("Music Genre")
        ax.set_ylabel("Prediction Probability")
        ax.set_title("Genre Prediction Probability Distribution")
        ax.set_xticklabels(class_labels, rotation=45)
        # Hiển thị biểu đồ trong Streamlit
        st.pyplot(fig)


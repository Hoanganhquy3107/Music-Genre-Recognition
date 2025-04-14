import streamlit as st

# Dữ liệu các câu hỏi và câu trả lời
faq_data = {
    "Custom Mode là gì?": "Custom Mode là chế độ cho phép bạn tạo nhạc với phong cách và cảm xúc cá nhân hóa. Bạn có thể chọn thể loại nhạc, tên bài hát và yêu cầu nhạc không lời (instrumental). Tính năng này giúp bạn tạo ra những bản nhạc độc đáo theo sở thích riêng của mình.",
    "Create Lyrics là gì?": "Create Lyrics là tính năng cho phép bạn yêu cầu AI sáng tác lời bài hát dựa trên thể loại nhạc, cảm xúc và chủ đề mà bạn muốn. Bạn có thể nhập vào chủ đề như tình yêu, mùa thu, tuổi trẻ, v.v., và AI sẽ tự động tạo ra lời bài hát cho bạn.",
    "Feel The Beat là gì?": "Feel The Beat là tính năng cho phép bạn tạo nhạc AI theo phong cách và cảm xúc bạn chọn. Bạn có thể lựa chọn các thể loại nhạc khác nhau (như Classical, Jazz, Lo-fi, v.v.) và mô tả cảm xúc hoặc ý tưởng của bạn để AI tạo ra những bản nhạc phù hợp.",
    "Classify là gì?": "Classify là tính năng giúp phân loại thể loại nhạc từ một file âm thanh MP3 mà bạn tải lên. Sau khi tải lên file, ứng dụng sẽ tự động phân tích và đưa ra thể loại nhạc của bài hát (như Pop, Rock, Hip-hop, v.v.).",
    "Library là gì?": "Library là nơi bạn có thể quản lý các bài hát mà bạn đã tạo hoặc tải lên. Bạn có thể xem các bài hát đã tạo, điều chỉnh thông tin bài hát, và chọn chia sẻ chúng với cộng đồng hoặc giữ chúng riêng tư. Ngoài ra, bạn cũng có thể xóa hoặc thay đổi trạng thái công khai của bài hát trong thư viện.",
    "Tại sao tôi không thể tạo nhạc mới?": "Để sử dụng tính năng tạo nhạc, bạn cần có đủ tín dụng trong tài khoản. Nếu bạn không đủ tín dụng, bạn sẽ không thể sử dụng tính năng này. Bạn có thể kiểm tra số dư tín dụng và nạp thêm nếu cần.",
    "Tôi cần làm gì khi không thấy bài hát của mình trong thư viện?": "Nếu bạn không thấy bài hát của mình trong thư viện, hãy kiểm tra lại trạng thái bài hát có được lưu thành công hay không. Bạn cũng có thể thử làm mới trang hoặc kiểm tra lại tài khoản người dùng.",
    "Làm thế nào để tạo một bài hát không lời (Instrumental)?": "Khi tạo bài hát mới, bạn có thể chọn tùy chọn Instrumental để yêu cầu AI tạo nhạc không lời. Điều này sẽ giúp bạn có được một bản nhạc mà không có lời hát.",
    "Làm thế nào để chia sẻ bài hát của tôi với cộng đồng?": "Trong thư viện của bạn, mỗi bài hát có một tùy chọn Public/Private. Bạn có thể thay đổi trạng thái của bài hát từ Private sang Public để chia sẻ bài hát với cộng đồng và những người dùng khác có thể nghe và đánh giá bài hát của bạn.",
    "Tại sao tôi không thể đăng nhập?": "Nếu bạn gặp vấn đề khi đăng nhập, hãy chắc chắn rằng bạn đã nhập đúng email và mật khẩu. Nếu quên mật khẩu, bạn có thể sử dụng tính năng Quên mật khẩu để đặt lại mật khẩu mới. Nếu vấn đề vẫn tiếp tục, hãy liên hệ với đội ngũ hỗ trợ kỹ thuật của chúng tôi.",
    "Làm thế nào để đổi mật khẩu hoặc cập nhật thông tin tài khoản?": "Bạn có thể cập nhật thông tin tài khoản của mình trong phần Cài đặt tài khoản hoặc sử dụng tính năng Quên mật khẩu để đặt lại mật khẩu nếu cần thiết.",
    "Nhạc của tôi không thể tải lên hoặc không thể chơi được, làm sao để khắc phục?": "Nếu bạn gặp vấn đề khi tải lên hoặc phát nhạc, hãy kiểm tra lại định dạng file và đảm bảo rằng file bạn tải lên là MP3 hoặc WAV. Ngoài ra, nếu bạn gặp phải sự cố kỹ thuật, hãy thử tải lại trang hoặc liên hệ với bộ phận hỗ trợ.",
    "Tại sao tôi thấy thông báo 'Không đủ tín dụng'?": "Để tạo bài hát mới, bạn cần có tín dụng trong tài khoản của mình. Mỗi bài hát yêu cầu một số tín dụng nhất định (ví dụ: 25 tín dụng mỗi bài hát). Bạn có thể nạp thêm tín dụng trong phần Thanh toán."
}

# Hàm chatbot để trả lời câu hỏi của người dùng
def chat_with_bot(user_message):
    if user_message in faq_data:
        return faq_data[user_message]
    else:
        return "⚠️ Xin lỗi, tôi không hiểu câu hỏi của bạn. Vui lòng thử lại hoặc hỏi về các tính năng của ứng dụng."

# Phần giao diện chatbot
def display_chatbot():
    st.markdown("### 💬 Trợ Lý Ảo - Hướng Dẫn Sử Dụng Ứng Dụng")

    # Hướng dẫn người dùng sử dụng chatbot
    st.markdown("""
        Bạn có thể hỏi tôi về các tính năng của ứng dụng này. Ví dụ:
        - "Tạo lời bài hát là gì?"
        - "Cách phân loại thể loại nhạc như thế nào?"
        - "Cách thanh toán tín dụng?"
    """, unsafe_allow_html=True)

    # Input của người dùng
    user_message = st.text_input("Nhập câu hỏi của bạn", "")

    # Xử lý câu hỏi của người dùng
    if user_message:
        bot_response = chat_with_bot(user_message)
        st.markdown(f"**Trợ lý ảo:** {bot_response}")

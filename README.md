# VietVoice-TTS

Dự án này sử dụng [Modal](https://modal.com/) để chạy mô hình chuyển văn bản thành giọng nói (Text-to-Speech) tiếng Việt.

## Giới thiệu

Đây là một ứng dụng cho phép bạn chuyển đổi văn bản tiếng Việt thành file âm thanh. Ứng dụng được xây dựng để chạy trên nền tảng Modal, giúp tận dụng sức mạnh của GPU để xử lý nhanh chóng mà không cần cài đặt phức tạp trên máy tính cá nhân.

## Yêu cầu

*   Cài đặt Modal: `pip install modal`
*   Tài khoản Modal (đăng ký tại [modal.com](https://modal.com/))

## Cách sử dụng

1.  **Clone repository này:**
    ```bash
    git clone https://github.com/your-username/VietVoice-TTS.git
    cd VietVoice-TTS
    ```

2.  **Chạy ứng dụng:**

    Sử dụng lệnh `modal run` để thực thi. Bạn cần cung cấp văn bản muốn chuyển đổi.

    ```bash
    modal run modal_app.py --text "Xin chào Việt Nam"
    ```

    File âm thanh sẽ được lưu với tên `output.wav` trong cùng thư mục.

3.  **Tùy chỉnh đầu ra:**

    Bạn có thể thay đổi tên file đầu ra:

    ```bash
    modal run modal_app.py --text "Xin chào Việt Nam" --output-file "chao.wav"
    ```

4.  **Tùy chọn giọng nói:**

    Hàm `synthesize` cho phép tùy chỉnh các tham số sau:
    *   `gender`: Giới tính (`female` hoặc `male`). Mặc định là `female`.
    *   `area`: Vùng miền (`northern`, `central`, `southern`). Mặc định là `northern`.
    *   `emotion`: Cảm xúc (`neutral`, `happy`, `sad`, `angry`). Mặc định là `neutral`.
    *   `group`: Nhóm giọng đọc (`story`, `news`, `dialog`). Mặc định là `story`.

    Ví dụ sử dụng giọng nam miền Nam:
    ```bash
    # (Lưu ý: Cần sửa đổi file modal_app.py để truyền các tham số này từ CLI)
    # Ví dụ về cách gọi hàm synthesize trực tiếp trong code:
    # synthesize.remote("Xin chào", gender="male", area="southern")
    ```

## Cấu trúc dự án

*   `modal_app.py`: File chính của ứng dụng Modal, định nghĩa môi trường, các hàm xử lý và điểm vào.
*   `requirements.txt`: Chứa các thư viện Python cần thiết.
*   `vietvoicetts/`: Thư mục chứa mã nguồn của thư viện `vietvoicetts`.

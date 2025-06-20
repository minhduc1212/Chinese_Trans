import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLabel, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QFont, QColor

class HighlightDictionaryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Dữ liệu từ điển
        # Đây là nơi bạn có thể thay đổi hoặc thêm các từ của riêng mình
        self.dictionary = {
            "đức": "1. Phẩm chất tốt đẹp, phù hợp với đạo lý.",
            "đức hạnh": "2. Phẩm chất đạo đức tốt đẹp nói chung của con người.",
            "đức tính": "3. Tính tốt thuộc về đạo đức.",
            "Người": "Một cá nhân thuộc loài người.",
            "quan trọng": "Có tác dụng hoặc giá trị lớn."
        }
        
        # Cấu hình cửa sổ chính
        self.setWindowTitle("Highlight to Define")
        self.setGeometry(200, 200, 600, 400)

        # Khởi tạo giao diện người dùng
        self.init_ui()

    def init_ui(self):
        # Tạo widget trung tâm và layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 2. Tạo các thành phần giao diện
        
        # Nhãn hướng dẫn
        instruction_label = QLabel("Hãy bôi đen (highlight) một từ trong ô văn bản bên dưới:")
        instruction_label.setFont(QFont("Arial", 12))

        # Ô văn bản chính
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Arial", 14))
        # Đoạn văn bản mẫu để thử nghiệm
        sample_text = "Người có đức hạnh thì sẽ có đức tính tốt. Chữ đức rất quan trọng."
        self.text_edit.setPlainText(sample_text)
        
        # Nhãn để hiển thị kết quả
        self.result_label = QLabel("Bôi đen một từ để xem định nghĩa.")
        self.result_label.setFont(QFont("Arial", 12))
        self.result_label.setStyleSheet("color: blue; font-weight: bold; padding: 10px; border: 1px solid #ccc; background-color: #f0f8ff;")
        self.result_label.setWordWrap(True) # Cho phép xuống dòng nếu định nghĩa quá dài
        
        # Thêm các widget vào layout
        layout.addWidget(instruction_label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.result_label)
        
        # 3. Kết nối tín hiệu (Signal) với hành động (Slot)
        # Đây là phần quan trọng nhất:
        # Khi vùng chọn trong text_edit thay đổi, nó sẽ gọi hàm self.on_selection_changed
        self.text_edit.selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        """
        Hàm này được gọi mỗi khi người dùng thay đổi vùng bôi đen.
        """
        # Lấy con trỏ văn bản hiện tại
        cursor = self.text_edit.textCursor()
        
        # Lấy đoạn văn bản đã được bôi đen
        selected_text = cursor.selectedText()
        
        # Loại bỏ các khoảng trắng thừa ở đầu và cuối
        cleaned_text = selected_text.strip()
        
        # Nếu có văn bản được chọn
        if cleaned_text:
            # Tra cứu trong từ điển (sử dụng .get() để tránh lỗi nếu không tìm thấy)
            definition = self.dictionary.get(cleaned_text)
            
            if definition:
                # Nếu tìm thấy, hiển thị định nghĩa
                self.result_label.setText(f"'{cleaned_text}': {definition}")
            else:
                # Nếu không tìm thấy, thông báo
                self.result_label.setText(f"Không tìm thấy định nghĩa cho '{cleaned_text}'.")
        else:
            # Nếu không có gì được bôi đen, reset nhãn kết quả
            self.result_label.setText("Bôi đen một từ để xem định nghĩa.")


# --- Phần chạy ứng dụng ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = HighlightDictionaryApp()
    main_win.show()
    sys.exit(app.exec_())
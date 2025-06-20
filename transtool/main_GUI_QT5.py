import sys
import os
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget,
    QAction, QFileDialog, QMenu, QInputDialog, QMessageBox,
    QSizePolicy, QPushButton, QLabel, QHBoxLayout, QFrame,
    QDialog, QLineEdit, QDialogButtonBox  # Thêm các import thiếu
)
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt, QPoint, QThread, QObject, pyqtSignal

from collections import namedtuple

# --- Cấu hình Files ---
MAIN_NAMES_FILE = 'main_names.txt'
SUB_NAMES_FILE = 'sub_names.txt'
VIETPHRASE_FILE = 'Vietphrase_new.txt'


# --- Cấu trúc dữ liệu Trie ---
class TrieNode:
    __slots__ = ('children', 'translations')
    def __init__(self):
        self.children = {}
        self.translations = None

class DictionaryTrie:
    def __init__(self, all_dictionaries):
        self.root = TrieNode()
        self.all_dictionaries = all_dictionaries
        self._build_trie(all_dictionaries)
    def _build_trie(self, all_dictionaries):
        print("Đang xây dựng Trie từ điển...")
        for file_type, data_dict in all_dictionaries.items():
            for chinese_key, full_viet_value in data_dict.items():
                if chinese_key: self._insert(chinese_key, file_type, full_viet_value)
        print("Đã xây dựng Trie xong.")
    def _insert(self, chinese_key, file_type, full_viet_value):
        node = self.root
        for char in chinese_key:
            if char not in node.children: node.children[char] = TrieNode()
            node = node.children[char]
        if node.translations is None: node.translations = {}
        node.translations[file_type] = full_viet_value
    def find_longest_match(self, text, start_index):
        node, longest_match_key, longest_match_node, match_length = self.root, None, None, 0
        last_match_node, last_match_length, current_index = None, 0, start_index
        while current_index < len(text):
            char = text[current_index]
            if char in node.children:
                node = node.children[char]; current_index += 1
                if node.translations is not None:
                    last_match_length = current_index - start_index; last_match_node = node
            else: break
        if last_match_node:
            match_length = last_match_length; longest_match_node = last_match_node
            longest_match_key = text[start_index : start_index + match_length]
        return longest_match_key, longest_match_node, match_length

# --- Cấu trúc dữ liệu cho Segment ---
TranslationSegment = namedtuple("TranslationSegment", ['original_chinese', 'translated_viet', 'output_start', 'output_end', 'full_viet_meaning', 'file_type_matched'])

# --- Hàm xử lý Data File ---
def _load_dictionary(filepath):
    dict_data = {}
    if not os.path.exists(filepath): return dict_data
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '=' not in line: continue
                try:
                    ch_phrase, vi_translation = line.split('=', 1)
                    if ch_phrase.strip(): dict_data[ch_phrase.strip()] = vi_translation.strip()
                except ValueError: print(f"Cảnh báo: Dòng không đúng định dạng: '{line}'")
    except Exception as e: print(f"Lỗi đọc file '{filepath}': {e}")
    return dict_data

def save_dictionary_file(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for original in sorted(data.keys(), key=len, reverse=True): f.write(f"{original}={data[original]}\n")
    except Exception as e: print(f"Lỗi ghi file {filepath}: {e}")

def load_all_dictionaries():
    return { 'main_names': _load_dictionary(MAIN_NAMES_FILE), 'sub_names': _load_dictionary(SUB_NAMES_FILE), 'vietphrase': _load_dictionary(VIETPHRASE_FILE) }

def save_all_dictionaries(all_data):
    save_dictionary_file(MAIN_NAMES_FILE, all_data['main_names'])
    save_dictionary_file(SUB_NAMES_FILE, all_data['sub_names'])
    save_dictionary_file(VIETPHRASE_FILE, all_data['vietphrase'])

# --- Hàm xử lý chuỗi ---
def capitalize_after_punctuation(string_input):
    if not string_input: return ""
    processed_string = string_input[0].upper() + string_input[1:]
    pattern = r'(?<=[.!?"])\s*(\w)'
    return re.sub(pattern, lambda m: m.group(0)[:-1] + m.group(1).upper(), processed_string)

PUNCTUATION_NO_SPACE_BEFORE_REGEX = re.compile(r'[,.!?。？！:;()"\'‘’“”…]')

# --- Hàm Dịch ---
# --- Hàm Dịch (PHIÊN BẢN MỚI) ---
# --- Hàm Dịch (PHIÊN BẢN CẢI TIẾN) ---
def translate_chinese_string_with_trie(input_str, dictionary_trie):
    """
    Dịch chuỗi tiếng Trung bằng cách lặp và tìm chuỗi con dài nhất.
    Gộp các ký tự liên tiếp không có trong từ điển thành một cụm.
    """
    # Lấy các dict từ điển ra từ đối tượng Trie
    all_dictionaries = dictionary_trie.all_dictionaries
    main_name_dict = all_dictionaries.get('main_names', {})
    sub_name_dict = all_dictionaries.get('sub_names', {})
    phrase_dict = all_dictionaries.get('vietphrase', {})
    
    # 1. Kiểm tra đầu vào và chuẩn hóa dấu câu
    if not input_str: return "", []
    
    processed_str = input_str.replace('，', ',').replace('。', '.').replace('！', '!').replace('？', '?')
    processed_str = processed_str.replace('：', ':').replace('；', ';').replace('（', '(').replace('）', ')')
    processed_str = processed_str.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'").replace('…', '...')
    
    # 2. Phân đoạn (Segmentation) chuỗi - CẢI TIẾN LOGIC
    segmented_chinese_phrases = []
    i = 0
    n = len(processed_str)

    while i < n:
        # Tìm cụm từ dài nhất có trong từ điển bắt đầu từ vị trí 'i'
        longest_match_len = 0
        for length in range(n - i, 0, -1): # Duyệt từ dài nhất đến ngắn nhất
            sub_string = processed_str[i : i + length]
            if sub_string in main_name_dict or \
               sub_string in sub_name_dict or \
               sub_string in phrase_dict:
                longest_match_len = length
                break # Đã tìm thấy cụm dài nhất, thoát vòng lặp
        
        # Trường hợp 1: TÌM THẤY một cụm từ trong từ điển
        if longest_match_len > 0:
            match = processed_str[i : i + longest_match_len]
            segmented_chinese_phrases.append(match)
            i += longest_match_len # Nhảy con trỏ qua cụm từ đã tìm thấy
        
        # Trường hợp 2: KHÔNG TÌM THẤY cụm nào
        else:
            # Bắt đầu tìm một chuỗi các ký tự không xác định
            start_of_unknown = i
            # Di chuyển con trỏ 'i' cho đến khi gặp một ký tự CÓ THỂ bắt đầu một cụm từ trong từ điển
            # hoặc đến cuối chuỗi.
            i += 1
            while i < n:
                # Kiểm tra xem có cụm nào bắt đầu từ vị trí 'i' mới không
                is_start_of_known_word = False
                # Chỉ cần kiểm tra ký tự đơn lẻ là đủ để biết có nên dừng lại không
                char_at_i = processed_str[i]
                if char_at_i in main_name_dict or \
                   char_at_i in sub_name_dict or \
                   char_at_i in phrase_dict:
                    # Tối ưu hơn: có thể kiểm tra sâu hơn, nhưng kiểm tra ký tự đơn là một heuristic tốt
                    is_start_of_known_word = True
                
                if is_start_of_known_word:
                    break # Dừng lại vì đã đến đầu của một từ đã biết
                
                i += 1 # Tiếp tục gộp chuỗi không xác định
            
            # Thêm toàn bộ chuỗi không xác định vừa tìm được vào danh sách
            unknown_phrase = processed_str[start_of_unknown : i]
            segmented_chinese_phrases.append(unknown_phrase)
            
    # 3. Dịch các mảnh đã phân đoạn (Giữ nguyên)
    intermediate_segments = []
    priority_order = ['main_names', 'sub_names', 'vietphrase']

    for chinese_key in segmented_chinese_phrases:
        full_viet_meaning, translated_viet, file_type_matched = chinese_key, chinese_key, None
        
        if chinese_key in main_name_dict:
            full_viet_meaning, file_type_matched = main_name_dict[chinese_key], 'main_names'
        elif chinese_key in sub_name_dict:
            full_viet_meaning, file_type_matched = sub_name_dict[chinese_key], 'sub_names'
        elif chinese_key in phrase_dict:
            full_viet_meaning, file_type_matched = phrase_dict[chinese_key], 'vietphrase'

        parts = full_viet_meaning.split('/')
        translated_viet = parts[0].strip() or (parts[1].strip() if len(parts) > 1 else full_viet_meaning.strip())
        
        intermediate_segments.append((chinese_key, translated_viet, full_viet_meaning, file_type_matched))

    # 4. Ghép nối và tạo bản đồ vị trí (Giữ nguyên)
    final_result_builder, translation_segments_map, current_output_index = [], [], 0
    for segment_data in intermediate_segments:
        original_chinese, translated_viet, full_viet_meaning, file_type_matched = segment_data
        
        if current_output_index > 0:
            last_char = final_result_builder[-1] if final_result_builder else ''
            current_starts_punct = translated_viet and PUNCTUATION_NO_SPACE_BEFORE_REGEX.match(translated_viet[0])
            if last_char != ' ' and not current_starts_punct and translated_viet.strip():
                final_result_builder.append(' '); current_output_index += 1
        
        segment_output_start = current_output_index
        final_result_builder.append(translated_viet)
        current_output_index += len(translated_viet)
        segment_output_end = current_output_index
        
        translation_segments_map.append(TranslationSegment(
            original_chinese, translated_viet, segment_output_start, segment_output_end, 
            full_viet_meaning, file_type_matched
        ))

    # 5. Hoàn thiện và trả về kết quả (Giữ nguyên)
    final_result_string = "".join(final_result_builder).strip()
    result = capitalize_after_punctuation(final_result_string)
    
    return result, translation_segments_map
# --- Worker Thread Class ---
class TranslatorWorker(QObject):
    finished = pyqtSignal(str, list, str)

    def __init__(self, input_text, dictionary_trie): # Vẫn nhận vào đối tượng Trie
        super().__init__()
        self._input_text = input_text
        self._dictionary_trie = dictionary_trie # Lưu lại

    def run(self):
        try:
            # Gọi hàm đã được viết lại. 
            # Hàm này sẽ tự truy cập vào self._dictionary_trie.all_dictionaries
            translated_text, segments_map = translate_chinese_string_with_trie(
                self._input_text, 
                self._dictionary_trie # Truyền cả đối tượng Trie vào
            )
            self.finished.emit(translated_text, segments_map, None)
        except Exception as e:
            self.finished.emit("", [], f"Lỗi trong quá trình dịch: {e}")


class UpdateDictionaryDialog(QDialog):
    entry_updated = pyqtSignal(str, str, str, str)
    def __init__(self, chinese_key, file_type, current_full_meaning, entries_count, parent=None, suggested_vietnamese_meaning=None):
        super().__init__(parent)
        self.chinese_key, self.file_type, self.current_full_meaning = chinese_key, file_type, current_full_meaning
        self.entries_count, self.suggested_vietnamese_meaning = entries_count, suggested_vietnamese_meaning
        self.setWindowTitle(f"Cập nhật từ điển ({self.file_type})"); self.setMinimumWidth(400)
        self._setup_ui(); self._load_entry_data()
    def _setup_ui(self):
        layout = QVBoxLayout(); header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Entries:")); self.entries_label = QLabel(str(self.entries_count)); header_layout.addWidget(self.entries_label)
        header_layout.addStretch(1); layout.addLayout(header_layout)
        fields_layout = QVBoxLayout(); fields_layout.setSpacing(10)
        chinese_layout = QHBoxLayout(); chinese_layout.addWidget(QLabel("Chinese:")); self.chinese_lineedit = QLineEdit(self.chinese_key)
        self.chinese_lineedit.setReadOnly(True); self.chinese_lineedit.setStyleSheet("background-color: #f0f0f0;"); chinese_layout.addWidget(self.chinese_lineedit)
        fields_layout.addLayout(chinese_layout)
        hanviet_layout = QHBoxLayout(); hanviet_layout.addWidget(QLabel("Hán Việt:")); self.hanviet_lineedit = QLineEdit(); hanviet_layout.addWidget(self.hanviet_lineedit)
        fields_layout.addLayout(hanviet_layout)
        name_layout = QHBoxLayout(); name_label = QLabel("Name:"); name_label.setMinimumWidth(QLabel("Hán Việt:").sizeHint().width())
        name_layout.addWidget(name_label); self.name_lineedit = QLineEdit(); name_layout.addWidget(self.name_lineedit)
        fields_layout.addLayout(name_layout);
        quick_edit_frame = QFrame(self); quick_edit_layout = QVBoxLayout(quick_edit_frame)
        quick_edit_layout.addWidget(QLabel("<b>Edit nhanh:</b>")); cap_buttons_layout = QVBoxLayout(); cap_buttons_layout.setSpacing(2)
        actions = [("Việt hoa 1 từ đơn đầu", 1), ("Việt hoa 2 từ đơn đầu", 2),("Việt hoa 3 từ đơn đầu", 3), ("Việt hoa tất cả", 0)]
        for text, num in actions:
            action = QAction(text, self); action.triggered.connect(lambda _, n=num: self._capitalize_name_field(n)); self._add_action_as_link(cap_buttons_layout, action)
        quick_edit_layout.addLayout(cap_buttons_layout); quick_edit_frame.setFrameShape(QFrame.StyledPanel)
        main_fields_quick_layout = QHBoxLayout(); main_fields_quick_layout.addLayout(fields_layout, 2); main_fields_quick_layout.addWidget(quick_edit_frame, 1)
        layout.addLayout(main_fields_quick_layout)
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel); delete_button = QPushButton("Delete")
        button_box.addButton(delete_button, QDialogButtonBox.DestructiveRole); button_box.button(QDialogButtonBox.Save).setText("Add")
        button_box.accepted.connect(self._on_save); delete_button.clicked.connect(self._on_delete); button_box.rejected.connect(self.reject)
        layout.addWidget(button_box); self.setLayout(layout)
    def _add_action_as_link(self, layout, action):
        button = QPushButton(action.text()); button.setStyleSheet("QPushButton { text-decoration: underline; color: blue; border: none; background: none; } QPushButton:hover { color: darkblue; }")
        button.clicked.connect(action.trigger); button.setCursor(Qt.PointingHandCursor); layout.addWidget(button, alignment=Qt.AlignLeft)
    def _load_entry_data(self):
        if self.current_full_meaning:
            parts = self.current_full_meaning.split('/'); self._other_meanings = [p.strip() for p in parts[2:]]
            self.hanviet_lineedit.setText(parts[0].strip())
            if len(parts) > 1: self.name_lineedit.setText(parts[1].strip())
        elif self.suggested_vietnamese_meaning: self.name_lineedit.setText(self.suggested_vietnamese_meaning); self._other_meanings = []
        else: self._other_meanings = []
    def _reconstruct_full_meaning(self):
        return "/".join([self.hanviet_lineedit.text().strip(), self.name_lineedit.text().strip()] + self._other_meanings)
    def _capitalize_name_field(self, num_words):
        words = self.name_lineedit.text().strip().split()
        if not words: return
        if num_words == 0: capitalized = [w.capitalize() for w in words]
        else: capitalized = [w.capitalize() for w in words[:num_words]] + words[num_words:]
        self.name_lineedit.setText(" ".join(capitalized))
    def _on_save(self):
        new_meaning = self._reconstruct_full_meaning()
        if not new_meaning.replace('/', '').strip():
            if QMessageBox.question(self, "Cảnh báo", f"Nghĩa trống. Xóa mục '{self.chinese_key}'?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                self.entry_updated.emit(self.chinese_key, self.file_type, None, 'delete'); self.accept()
        else: self.entry_updated.emit(self.chinese_key, self.file_type, new_meaning, 'save'); self.accept()
    def _on_delete(self):
        if QMessageBox.question(self, "Xác nhận", f"Xóa mục '{self.chinese_key}' trong '{self.file_type}'?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            self.entry_updated.emit(self.chinese_key, self.file_type, None, 'delete'); self.accept()

# --- Lớp Ứng dụng Chính ---
class StoryReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Story Translator")
        self.setGeometry(100, 100, 900, 700)
        self.all_dictionaries, self.dictionary_trie = {}, None
        self._translation_thread, self._translator_worker = None, None
        self.translation_segments_map = []
        self._setup_ui(); self._create_actions(); self._create_menus()
        self.reload_dictionaries(); QApplication.setStyle("Fusion")

    def _setup_ui(self):
        font = QFont("Arial", 12); central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        # Input Area
        input_layout = QVBoxLayout(); input_layout.addWidget(QLabel("Văn bản Tiếng Trung:"))
        self.input_text_edit = QTextEdit(self); self.input_text_edit.setFont(font)
        self.input_text_edit.setPlaceholderText("Nhập văn bản tiếng Trung ở đây..."); input_layout.addWidget(self.input_text_edit)
        # Translate Button
        button_layout = QHBoxLayout(); self.translate_button = QPushButton("Dịch", self); self.translate_button.setFont(font)
        self.translate_button.clicked.connect(self.start_translation_thread)
        button_layout.addStretch(1); button_layout.addWidget(self.translate_button); button_layout.addStretch(1)
        # Output Area
        output_layout = QVBoxLayout(); output_layout.addWidget(QLabel("Kết quả Dịch:"))
        self.output_text_edit = QTextEdit(self); self.output_text_edit.setFont(font)
        self.output_text_edit.setReadOnly(False); self.output_text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.output_text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.output_text_edit.customContextMenuRequested.connect(self.show_context_menu_output)
        self.output_text_edit.selectionChanged.connect(self.on_output_selection_changed)
        output_layout.addWidget(self.output_text_edit)
        main_layout.addLayout(input_layout, 2); main_layout.addLayout(button_layout); main_layout.addLayout(output_layout, 3)
        # Info Box
        self.info_label = QLabel("Bôi đen một từ trong kết quả dịch để xem chi tiết.")
        self.info_label.setFont(QFont("Arial", 11))
        self.info_label.setStyleSheet("color: #155724; background-color: #d4edda; border: 1px solid #c3e6cb; padding: 8px; border-radius: 4px;")
        self.info_label.setWordWrap(True); self.info_label.setMinimumHeight(50)
        main_layout.addWidget(self.info_label)
        self.setCentralWidget(central_widget)

    def on_output_selection_changed(self):
        cursor = self.output_text_edit.textCursor()
        
        if not cursor.hasSelection():
            self.info_label.setText("Bôi đen một từ trong kết quả dịch để xem chi tiết.")
            return

        start, end = cursor.selectionStart(), cursor.selectionEnd()

        overlapping_segments = [
            s for s in self.translation_segments_map 
            if max(s.output_start, start) < min(s.output_end, end)
        ]

        if not overlapping_segments:
            self.info_label.setText("Không có thông tin cho vùng chọn này.")
            return
        
        if len(overlapping_segments) == 1:
            segment = overlapping_segments[0]
            info_text = (
                f"<b>Từ gốc:</b> {segment.original_chinese}<br>"
                f"<b>Nghĩa đầy đủ:</b> {segment.full_viet_meaning}<br>"
                f"<b>Nguồn:</b> {segment.file_type_matched or 'Không xác định'}"
            )
            self.info_label.setText(info_text)
        else: 
            # *** SỬA LỖI Ở ĐÂY ***
            # 1. Tính toán phần phức tạp và gán vào một biến
            combined_chinese_text = "".join([s.original_chinese for s in overlapping_segments])
            
            # 2. Sử dụng biến đó trong f-string một cách an toàn
            info_text = (
                f"<b>Vùng chọn:</b> '{cursor.selectedText()}'<br>"
                f"<b>Tương ứng gốc:</b> {combined_chinese_text}"
            )
            self.info_label.setText(info_text)
    def _create_actions(self):
        self.open_action = QAction("&Mở File Trung...", self, shortcut="Ctrl+O", triggered=self.open_file)
        self.exit_action = QAction("&Thoát", self, shortcut="Ctrl+Q", triggered=self.close)
        self.reload_dict_action = QAction("&Tải lại Từ điển", self, shortcut="Ctrl+R", triggered=self.reload_dictionaries)

    def _create_menus(self):
        menu_bar = self.menuBar(); file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.open_action); file_menu.addSeparator(); file_menu.addAction(self.exit_action)
        dict_menu = menu_bar.addMenu("&Từ điển"); dict_menu.addAction(self.reload_dict_action)

    def open_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Mở File", "", "Text Files (*.txt);;All Files (*)")
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f: self.input_text_edit.setPlainText(f.read())
                self.start_translation_thread()
            except Exception as e: QMessageBox.critical(self, "Lỗi", f"Không thể đọc file:\n{e}")

    def reload_dictionaries(self):
        self.all_dictionaries = load_all_dictionaries()
        self.dictionary_trie = DictionaryTrie(self.all_dictionaries)
        QMessageBox.information(self, "Thông báo", "Đã tải lại từ điển!")
        if self.input_text_edit.toPlainText().strip(): self.start_translation_thread()

    def start_translation_thread(self):
        input_text = self.input_text_edit.toPlainText()
        if not input_text.strip() or self.dictionary_trie is None: return
        if self._translation_thread and self._translation_thread.isRunning(): return
        self.translate_button.setEnabled(False); self.output_text_edit.setPlainText("Đang dịch..."); self.translation_segments_map = []
        self._translation_thread = QThread(); self._translator_worker = TranslatorWorker(input_text, self.dictionary_trie)
        self._translator_worker.moveToThread(self._translation_thread)
        self._translation_thread.started.connect(self._translator_worker.run); self._translator_worker.finished.connect(self.handle_translation_result)
        self._translator_worker.finished.connect(self._translation_thread.quit); self._translator_worker.finished.connect(self._translator_worker.deleteLater)
        self._translation_thread.finished.connect(self._translation_thread.deleteLater); self._translation_thread.finished.connect(self._cleanup_translation_vars)
        self._translation_thread.start()

    def handle_translation_result(self, text, segments_map, error):
        if error:
            self.output_text_edit.setPlainText(f"Lỗi: {error}"); QMessageBox.critical(self, "Lỗi Dịch", f"Đã xảy ra lỗi:\n{error}")
        else: self.output_text_edit.setPlainText(text); self.translation_segments_map = segments_map
        self.translate_button.setEnabled(True)

    def _cleanup_translation_vars(self):
         self.translate_button.setEnabled(True); self._translation_thread, self._translator_worker = None, None

    def show_context_menu_output(self, pos: QPoint):
        cursor = self.output_text_edit.textCursor(); start, end = cursor.selectionStart(), cursor.selectionEnd()
        if start == end: end = start + 1
        overlapping_segments = sorted([s for s in self.translation_segments_map if max(s.output_start, start) < min(s.output_end, end)], key=lambda s: s.output_start)
        context_menu = QMenu(self)
        if not overlapping_segments: context_menu.addAction(QAction("Không tìm thấy mục liên quan", self, enabled=False))
        elif len(overlapping_segments) == 1 and not cursor.hasSelection():
            segment = overlapping_segments[0]
            if segment.original_chinese.strip():
                action_text = f"Sửa '{segment.original_chinese}' ('{segment.translated_viet}')..."
                update_action = QAction(action_text, self, triggered=lambda _, k=segment.original_chinese: self.show_update_dialog_for_chinese_key(k))
                context_menu.addAction(update_action)
        else:
            context_menu.addAction(QAction("Các mục trong vùng chọn:", self, enabled=False))
            for seg in overlapping_segments:
                if seg.original_chinese.strip():
                    update_action = QAction(f"  Sửa '{seg.original_chinese}' ('{seg.translated_viet}')", self, triggered=lambda _, k=seg.original_chinese: self.show_update_dialog_for_chinese_key(k))
                    context_menu.addAction(update_action)
            combined_chinese = "".join([s.original_chinese for s in overlapping_segments])
            if cursor.hasSelection() and combined_chinese.strip():
                context_menu.addSeparator(); combine_action = QAction(f"Tạo mục mới cho '{cursor.selectedText()}'...", self)
                font = combine_action.font(); font.setBold(True); combine_action.setFont(font)
                combine_action.triggered.connect(lambda _, g=combined_chinese, v=cursor.selectedText(): self.prompt_for_manual_combination(g, v))
                context_menu.addAction(combine_action)
        context_menu.addSeparator()
        copy_action = QAction("Copy vùng chọn (Ctrl+C)", self, shortcut="Ctrl+C", triggered=self.output_text_edit.copy)
        manual_add_action = QAction("Thêm mục mới (thủ công)...", self, triggered=self.prompt_for_chinese_key_and_update_manual)
        context_menu.addAction(copy_action); context_menu.addAction(manual_add_action)
        context_menu.exec_(self.output_text_edit.mapToGlobal(pos))
    
    def prompt_for_manual_combination(self, chinese_guess, vietnamese_selection):
        chinese_key, ok = QInputDialog.getText(self, "Xác nhận Cụm Tiếng Trung", f"Xác nhận/sửa lại gốc Trung cho nghĩa: '{vietnamese_selection}'", QLineEdit.Normal, chinese_guess)
        if ok and chinese_key.strip(): self.show_update_dialog_for_chinese_key(chinese_key.strip(), suggested_vietnamese_meaning=vietnamese_selection)
        elif ok: QMessageBox.warning(self, "Lỗi", "Cụm Tiếng Trung không được để trống.")

    def prompt_for_chinese_key_and_update_manual(self):
        chinese_key, ok = QInputDialog.getText(self, "Thêm mục mới", "Nhập cụm Tiếng Trung gốc:")
        if ok and chinese_key.strip(): self.show_update_dialog_for_chinese_key(chinese_key.strip())
        elif ok: QMessageBox.warning(self, "Lỗi", "Cụm Tiếng Trung không được để trống.")
    
    def show_update_dialog_for_chinese_key(self, chinese_key, suggested_vietnamese_meaning=None):
        file_type = 'vietphrase'
        if chinese_key in self.all_dictionaries.get('main_names', {}): file_type = 'main_names'
        elif chinese_key in self.all_dictionaries.get('sub_names', {}): file_type = 'sub_names'
        current_meaning = self.all_dictionaries.get(file_type, {}).get(chinese_key, "")
        total_entries = sum(len(d) for d in self.all_dictionaries.values())
        dialog = UpdateDictionaryDialog(chinese_key, file_type, current_meaning, total_entries, self, suggested_vietnamese_meaning)
        dialog.entry_updated.connect(self.handle_dictionary_update_from_dialog)
        dialog.exec_()

    def handle_dictionary_update_from_dialog(self, chinese_key, file_type, new_meaning, action):
        if file_type not in self.all_dictionaries or not chinese_key.strip(): return
        if action == 'save':
            if not new_meaning or not new_meaning.replace('/', '').strip(): action = 'delete'
            else:
                self.all_dictionaries[file_type][chinese_key] = new_meaning.strip()
                print(f"Đã cập nhật/thêm: '{chinese_key}'='{new_meaning.strip()}' trong {file_type}")
        if action == 'delete':
            if chinese_key in self.all_dictionaries[file_type]:
                 del self.all_dictionaries[file_type][chinese_key]; print(f"Đã xóa: '{chinese_key}' từ {file_type}")
        save_all_dictionaries(self.all_dictionaries); self.dictionary_trie = DictionaryTrie(self.all_dictionaries)
        if self.input_text_edit.toPlainText().strip(): self.start_translation_thread()

# --- Chạy ứng dụng ---
if __name__ == '__main__':
    for f in [MAIN_NAMES_FILE, SUB_NAMES_FILE, VIETPHRASE_FILE]:
        if not os.path.exists(f):
            try: open(f, 'w', encoding='utf-8').close(); print(f"Đã tạo file data rỗng: {f}")
            except Exception as e: print(f"Không thể tạo file {f}: {e}")
    app = QApplication(sys.argv)
    main_win = StoryReaderApp()
    main_win.show()
    sys.exit(app.exec_())
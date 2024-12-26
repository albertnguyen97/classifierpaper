import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox, QGroupBox
from textblob import TextBlob
import spacy
from spacy.tokens import Doc
from googletrans import Translator

# Tải mô hình ngôn ngữ tiếng Anh
nlp = spacy.load("en_core_web_sm")

# Đăng ký thuộc tính mở rộng 'polarity'
Doc.set_extension("polarity", getter=lambda doc: doc._.sentiment.polarity if hasattr(doc._, 'sentiment') else 0)

# Danh sách các từ stop words tùy chỉnh
custom_stop_words = {"tôi", "tao", "tớ", "bạn"}

# Danh sách từ khóa cho các chủ đề
topic_keywords = {
"công nghệ": [
    "công nghệ", "technology", "kỹ thuật", "engineering", "phần mềm", "software", 
    "ứng dụng", "application", "internet", "AI", "trí tuệ nhân tạo", "artificial intelligence", 
    "robot", "machine learning", "học máy", "blockchain", "máy tính", "computer", 
    "khoa học dữ liệu", "data science", "điện toán đám mây", "cloud computing", "ứng dụng di động",
    "cybersecurity", "bảo mật mạng", "network security", "big data", "dữ liệu lớn", "IoT", "internet of things",
    "cảm biến", "sensor", "smartphone", "điện thoại thông minh", "coding", "lập trình", "quantum computing", 
    "điện toán lượng tử", "automation", "tự động hóa", "startup", "khởi nghiệp", "virtual reality", "thực tế ảo",
    "augmented reality", "thực tế tăng cường", "dữ liệu", "data", "AI ethics", "đạo đức AI", "deep learning", 
    "học sâu", "chatbot", "bot", "web", "trang web", "URL", "ứng dụng web", "machine", "hệ thống nhúng",
    "embedded systems", "trí tuệ nhân tạo", "AR", "VR", "robotics", "hardware", "phần cứng", "điện tử", 
    "electronic", "sensor", "camera", "cloud", "đám mây", "hosting", "server", "mạng", "network", "cơ sở dữ liệu",
    "database", "phi tập trung", "decentralized", "token", "crypto", "block", "thiết kế giao diện", "UI design",
    "UX", "user experience", "phân tích dữ liệu", "data analysis", "tăng trưởng", "growth hacking", "meta data",
    "Google", "Apple", "Microsoft", "Amazon", "Meta", "Facebook", "IBM", "Intel", "Samsung", "Tesla", 
    "Sony", "NVIDIA", "Oracle", "Cisco", "Qualcomm", "Salesforce", "Adobe", "Dell", "HP", "Lenovo", 
    "Alibaba", "Tencent", "Baidu", "TikTok", "Bytedance", "Zoom", "Slack", "Twitter", "Spotify", 
    "Netflix", "Uber", "Lyft", "Airbnb", "SpaceX", "PayPal", "Stripe", "Square", "Snapchat", 
    "Huawei", "Xiaomi", "ASUS", "Acer", "LG", "Ericsson", "ARM", "Foxconn", "Broadcom", "Seagate",
    "Western Digital", "AMD", "VMware", "Red Hat", "Epic Games", "Unity", "Cloudflare", "Akamai", 
    "Shopify", "GitHub", "GitLab", "DigitalOcean", "Alibaba Cloud", "Huawei Cloud", "Tencent Cloud", 
    "OpenAI", "DeepMind", "Darktrace", "Palantir", "Raspberry Pi", "Boston Dynamics", "ZoomInfo", 
    "Nokia", "Yandex", "Kaspersky", "Atlassian", "Splunk", "Figma", "Canva", "Wix", "Weebly", 
    "Zynga", "EA", "Activision Blizzard", "Unity Technologies", "Spotify Technology", "Twitch",
    "Epic Systems", "Roku", "Vizio", "Sonos", "Ring", "Nest", "Zebra Technologies", "Logitech"
    ],

"chính trị": [
    "chính trị", "politics", "bầu cử", "election", "đảng", "party", 
    "quốc hội", "parliament", "chính phủ", "government", "tổng thống", "president", 
    "thủ tướng", "prime minister", "ngoại giao", "diplomacy", "đối ngoại", "foreign policy", 
    "nhân quyền", "human rights", "luật pháp", "law", "bạo động", "protest", "chiến tranh", "war",
    "lập pháp", "legislation", "chính sách", "policy", "hòa bình", "peace", "tranh cử", "campaign", 
    "cấm vận", "sanctions", "liên minh", "alliance", "quân sự", "military", "hiệp ước", "treaty",
    "nội chiến", "civil war", "lãnh thổ", "territory", "chủ quyền", "sovereignty", "quốc gia", "nation", 
    "cộng hòa", "republic", "dân chủ", "democracy", "độc tài", "dictatorship", "thượng viện", "senate",
    "hạ viện", "house of representatives", "quyền lực", "power", "thống đốc", "governor", "đạo luật", 
    "act", "tòa án", "court", "xung đột", "conflict", "liên hiệp quốc", "united nations", "nội bộ", 
    "domestic", "đàm phán", "negotiation", "biểu tình", "strike", "bảo hộ", "protectionism",
    "Việt Nam", "Vietnam", "Hoa Kỳ", "United States", "Mỹ", "Nga", "Russia", "Trung Quốc", "China", 
    "Ấn Độ", "India", "Nhật Bản", "Japan", "Hàn Quốc", "South Korea", "Đức", "Germany", "Pháp", "France", 
    "Anh", "United Kingdom", "Ý", "Italy", "Canada", "Úc", "Australia", "Brazil", "Mexico", "Argentina", 
    "Tây Ban Nha", "Spain", "Bồ Đào Nha", "Portugal", "Thổ Nhĩ Kỳ", "Turkey", "Iran", "Iraq", 
    "Afghanistan", "Pakistan", "Ai Cập", "Egypt", "Nam Phi", "South Africa", "Saudi Arabia", "Israel", 
    "Palestine", "Syria", "Ukraine", "Ba Lan", "Poland", "Hungary", "Thụy Điển", "Sweden", 
    "Na Uy", "Norway", "Đan Mạch", "Denmark", "Phần Lan", "Finland", "Hà Lan", "Netherlands", 
    "Bỉ", "Belgium", "Thụy Sĩ", "Switzerland", "Hy Lạp", "Greece", "Áo", "Austria", "Singapore", 
    "Malaysia", "Thái Lan", "Myanmar", "Campuchia", "Lào", "Indonesia", "Philippines", "Bangladesh", 
    "Sri Lanka", "New Zealand", "Chile", "Colombia", "Venezuela", "Peru", "Cuba", "Triều Tiên", "North Korea", 
    "Mông Cổ", "Mongolia", "Kazakhstan", "Uzbekistan", "Kyrgyzstan", "Tajikistan", "Turkmenistan", 
    "Georgia", "Azerbaijan", "Armenia", "Qatar", "UAE", "United Arab Emirates", "Kuwait", "Bahrain", 
    "Oman", "Jordan", "Lebanon", "Yemen", "Sudan", "Ethiopia", "Kenya", "Nigeria", "Ghana", "Senegal", 
    "Morocco", "Algeria", "Tunisia", "Libya", "Zimbabwe", "Zambia", "Mozambique", "Angola", "Botswana", 
    "Ivory Coast", "Cameroon", "Congo", "Madagascar", "Malawi", "Rwanda", "Burundi", "Tanzania"
],

    "văn hóa": [
        "văn hóa", "culture", "nghệ thuật", "art", "truyền thống", "tradition", 
        "lễ hội", "festival", "âm nhạc", "music", "văn học", "literature", 
        "kịch", "theater", "điện ảnh", "cinema", "phong tục", "custom", 
        "di sản", "heritage", "ẩm thực", "cuisine", "hội họa", "painting", 
        "kiến trúc", "architecture", "nghệ sĩ", "artist", "tác phẩm", "work of art", 
        "nhiếp ảnh", "photography", "biểu diễn", "performance", "sân khấu", "stage",
        "hài kịch", "comedy", "bi kịch", "tragedy", "bảo tàng", "museum", "triển lãm", "exhibition",
        "văn hóa dân gian", "folklore", "thời trang", "fashion", "ngôn ngữ", "language", "tiếng nói", 
        "diễn xuất", "acting", "hội họa", "drawing", "thiết kế", "design", "sáng tạo", "creativity",
        "ca sĩ", "singer", "nhạc sĩ", "composer", "ban nhạc", "band", "đàn guitar", "guitar", "thơ ca", 
        "poetry", "điêu khắc", "sculpture", "múa", "dance", "hòa nhạc", "concert", "kiệt tác", "masterpiece",
        "giải thưởng", "award", "đạo diễn", "director", "diễn viên", "actor", "kịch bản", "script"
    ],
    "xã hội": [
        "xã hội", "society", "cộng đồng", "community", "tình nguyện", "volunteer", 
        "phúc lợi", "welfare", "giáo dục", "education", "y tế", "healthcare", 
        "bình đẳng", "equality", "phát triển", "development", "việc làm", "employment", 
        "nghèo đói", "poverty", "dân số", "population", "môi trường", "environment", 
        "quyền lợi", "rights", "thanh niên", "youth", "người già", "elderly", "nhập cư", "immigration",
        "bảo hiểm", "insurance", "xã hội học", "sociology", "đời sống", "life", "phụ nữ", "women", 
        "trẻ em", "children", "công lý", "justice", "an sinh", "security", "người khuyết tật", 
        "disabled", "hòa nhập", "inclusion", "đô thị", "urban", "nông thôn", "rural", "vấn đề xã hội",
        "social issues", "phân biệt đối xử", "discrimination", "hỗ trợ", "support", "nạn đói", "famine",
        "mạng xã hội", "social media", "nghiện", "addiction", "bạo lực", "violence", "hội nhập", "integration",
        "đoàn kết", "solidarity", "tiến bộ", "progress", "bảo vệ trẻ em", "child protection", "già hóa dân số",
        "aging population"
    ],
    "thể thao": [
        "thể thao", "sports", "bóng đá", "football", "soccer", "bóng rổ", "basketball", 
        "bóng chuyền", "volleyball", "quần vợt", "tennis", "cầu lông", "badminton", 
        "điền kinh", "athletics", "bơi lội", "swimming", "đua xe", "racing", "xe đạp", "cycling", 
        "đấm bốc", "boxing", "võ thuật", "martial arts", "karate", "judo", "taekwondo", 
        "bóng chày", "baseball", "cricket", "rugby", "khúc côn cầu", "hockey", 
        "trượt băng", "ice skating", "trượt tuyết", "skiing", "lướt ván", "surfing", 
        "leo núi", "climbing", "bắn cung", "archery", "golf", "đua thuyền", "rowing", 
        "cờ vua", "chess", "cờ tướng", "chinese chess", "thể hình", "bodybuilding", 
        "thể dục", "gymnastics", "vũ đạo", "dance sport", "futsal", "đấu vật", "wrestling", 
        "đi bộ", "walking", "chạy bộ", "running", "marathon", "bóng bàn", "table tennis", 
        "bi-a", "billiards", "snooker", "trượt patin", "roller skating", "esports", "thể thao điện tử", 
        "game thủ", "gamer", "cuộc thi", "competition", "giải đấu", "tournament", "thế vận hội", "olympics", 
        "huy chương", "medal", "vận động viên", "athlete", "huấn luyện viên", "coach", "đội bóng", "team", 
        "sân vận động", "stadium", "cổ động viên", "fan", "kỷ lục", "record", "bàn thắng", "goal", 
        "trọng tài", "referee", "thể chất", "fitness", "chấn thương", "injury", "phục hồi", "recovery", 
        "tập luyện", "training", "cúp", "cup", "đối kháng", "match", "sự kiện thể thao", "sports event", 
        "đồng đội", "teammate", "thủ môn", "goalkeeper", "tiền đạo", "striker", "hậu vệ", "defender", 
        "trung vệ", "center back", "tiền vệ", "midfielder", "đội tuyển quốc gia", "national team", 
        "điểm số", "score", "chiến thắng", "victory", "thua cuộc", "defeat", "kỹ năng", "skills", 
        "chiến thuật", "tactics", "hòa", "draw", "trận đấu", "game", "thi đấu", "compete", "phong độ", "form"
    ],
    "kinh tế": [
    "kinh tế", "economy", "tài chính", "finance", "doanh nghiệp", "business", "công ty", "company", 
    "đầu tư", "investment", "chứng khoán", "stock", "thị trường", "market", "thương mại", "trade", 
    "xuất khẩu", "export", "nhập khẩu", "import", "GDP", "gross domestic product", "lạm phát", "inflation", 
    "ngân hàng", "bank", "tín dụng", "credit", "lãi suất", "interest rate", "bảo hiểm", "insurance", 
    "thuế", "tax", "vốn", "capital", "doanh thu", "revenue", "lợi nhuận", "profit", "khấu hao", "depreciation", 
    "thâm hụt", "deficit", "cán cân thương mại", "trade balance", "ngân sách", "budget", "chi phí", "cost", 
    "xu hướng kinh tế", "economic trend", "công nghiệp", "industry", "dịch vụ", "service", "thị trường lao động", 
    "labor market", "khởi nghiệp", "startup", "thương hiệu", "brand", "cạnh tranh", "competition", "hợp đồng", "contract", 
    "chiến lược", "strategy", "xu hướng", "trend", "kinh doanh", "business operation", "sản phẩm", "product", 
    "hàng hóa", "goods", "phân phối", "distribution", "thương mại điện tử", "e-commerce", "Amazon", "Alibaba", 
    "eBay", "Shopee", "Lazada", "Tiki", "truyền thông", "media", "quảng cáo", "advertising", "tiếp thị", "marketing", 
    "chiến dịch", "campaign", "vận tải", "transportation", "logistics", "chuỗi cung ứng", "supply chain", 
    "kinh tế học", "economics", "vi mô", "microeconomics", "vĩ mô", "macroeconomics", "tổ chức quốc tế", 
    "international organization", "IMF", "World Bank", "WTO", "OECD", "EU", "ASEAN", "hiệp định thương mại", 
    "trade agreement", "FTAs", "RCEP", "thương mại toàn cầu", "global trade", "xuất khẩu nông sản", "agricultural export", 
    "thương mại kỹ thuật số", "digital trade", "công nghiệp 4.0", "industry 4.0", "tự động hóa", "automation", 
    "quản lý tài sản", "asset management", "tài sản cố định", "fixed assets", "thị trường bất động sản", "real estate market"
    ],
    "giải trí": [
    "giải trí", "entertainment", "phim", "movie", "điện ảnh", "cinema", "ca nhạc", "music", "nhạc", "song", 
    "diễn viên", "actor", "actress", "ca sĩ", "singer", "ban nhạc", "band", "thể thao", "sports", 
    "trò chơi", "game", "video game", "trò chơi điện tử", "kịch", "theater", "hài kịch", "comedy", 
    "chương trình truyền hình", "TV show", "truyền hình", "television", "vở nhạc kịch", "musical", 
    "nghệ thuật", "art", "triển lãm", "exhibition", "kỷ niệm", "celebration", "sự kiện", "event", 
    "lễ hội", "festival", "phim tài liệu", "documentary", "thời trang", "fashion", "chụp ảnh", "photography", 
    "mạng xã hội", "social media", "YouTube", "TikTok", "Instagram", "Facebook", "livestream", 
    "diễn đàn", "forum", "podcast", "âm nhạc điện tử", "EDM", "rap", "hip-hop", "nhạc cổ điển", "classical music", 
    "hòa nhạc", "concert", "giải thưởng", "award", "trò chơi di động", "mobile game", "show thực tế", "reality show",
    "Netflix", "Disney", "Marvel", "DC Comics", "HBO", "Warner Bros", "Pixar", "Sony Pictures", 
    "Paramount", "Universal Studios", "Nintendo", "PlayStation", "Xbox", "Ubisoft", "EA Sports", 
    "Square Enix", "Capcom", "Bandai Namco", "Blizzard", "Spotify", "Apple Music", "SoundCloud", 
    "VNG", "Garena", "Tencent Games", "PUBG", "Free Fire", "K-pop", "J-pop", "Bollywood", "Hollywood", 
    "Broadway", "karaoke", "streaming", "vũ đạo", "dancing", "TikTok dance", "fanclub", "fan hâm mộ", 
    "manga", "anime", "cosplay", "kịch bản", "script", "đạo diễn", "director", "sân khấu", "stage", 
    "ảo thuật", "magic", "ảo thuật gia", "magician", "nhà sản xuất", "producer", "trò chơi nhập vai", "RPG", 
    "FPS", "game bắn súng", "thể loại nhạc", "music genre", "nhạc phim", "soundtrack", "thể thao điện tử", "eSports"
]
}

class TextClassifier(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.translator = Translator()  # Khởi tạo bộ dịch
        self.current_language = 'vi'  # Ngôn ngữ mặc định là tiếng Việt
        self.dark_mode = False  # Chế độ sáng mặc định

    def initUI(self):
        self.setWindowTitle('Phân loại văn bản')
        layout = QVBoxLayout()

        # Nhóm nhập văn bản
        input_group = QGroupBox("Phân tích văn bản")
        input_layout = QVBoxLayout()
        self.label = QLabel('Nhập văn bản:')
        self.textEdit = QTextEdit()
        input_layout.addWidget(self.label)
        input_layout.addWidget(self.textEdit)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Nhóm nút chức năng
        button_group = QGroupBox("Chức năng")
        button_layout = QHBoxLayout()
        self.classifyButton = QPushButton('Phân loại')
        self.classifyButton.clicked.connect(self.classify_text)
        self.translateButton = QPushButton('Dịch')
        self.translateButton.clicked.connect(self.translate_text)
        self.toggleLanguageButton = QPushButton('Chuyển ngôn ngữ')
        self.toggleLanguageButton.clicked.connect(self.toggle_language)
        self.toggleModeButton = QPushButton('Chuyển chế độ')
        self.toggleModeButton.clicked.connect(self.toggle_mode)
        button_layout.addWidget(self.classifyButton)
        button_layout.addWidget(self.translateButton)
        button_layout.addWidget(self.toggleLanguageButton)
        button_layout.addWidget(self.toggleModeButton)
        button_group.setLayout(button_layout)
        layout.addWidget(button_group)

        self.setLayout(layout)

    def classify_text(self):
        text = self.textEdit.toPlainText()
        if not text:
            QMessageBox.warning(self, 'Cảnh báo', 'Vui lòng nhập văn bản!')
            return

        # Chuyển đổi văn bản thành chữ thường
        text_lower = text.lower()

        if self.is_vietnamese(text):
            sentiment, sentiment_label = self.analyze_sentiment_vietnamese(text)
            topic = self.analyze_topic_vietnamese(text_lower)  # Phân tích chủ đề cho tiếng Việt
        else:
            cleaned_text = self.remove_stop_words(text)  # Loại bỏ stop words
            sentiment, sentiment_label = self.analyze_sentiment_english(cleaned_text)
            topic = self.analyze_topic_english(cleaned_text)  # Phân tích chủ đề cho tiếng Anh

        # Dịch kết quả phân tích sang tiếng Việt
        translated_result = f"Cảm xúc: {sentiment_label} (Độ chính xác: {sentiment})\nChủ đề: {topic}"
        translated = self.translator.translate(translated_result, dest='vi')
        translated_topic = self.translator.translate(topic, dest='vi')  # Dịch chủ đề sang tiếng Việt
        QMessageBox.information(self, 'Kết quả', f'Tiếng Việt: {translated.text}\nChủ đề: {translated_topic.text}')

    def translate_text(self):
        text = self.textEdit.toPlainText()
        if not text:
            QMessageBox.warning(self, 'Cảnh báo', 'Vui lòng nhập văn bản để dịch!')
            return

        dest_lang = 'vi' if self.current_language == 'en' else 'en'
        translated = self.translator.translate(text, dest=dest_lang)
        QMessageBox.information(self, 'Kết quả dịch', f'Tiếng {dest_lang}: {translated.text}')

    def toggle_language(self):
        self.current_language = 'en' if self.current_language == 'vi' else 'vi'
        if self.current_language == 'en':
            self.label.setText('Enter text:')
            self.classifyButton.setText('Classify')
            self.translateButton.setText('Translate')
            self.toggleLanguageButton.setText('Switch to Vietnamese')
            self.toggleModeButton.setText('Switch Mode')
        else:
            self.label.setText('Nhập văn bản:')
            self.classifyButton.setText('Phân loại')
            self.translateButton.setText('Dịch')
            self.toggleLanguageButton.setText('Chuyển ngôn ngữ')
            self.toggleModeButton.setText('Chuyển chế độ')

    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet("background-color: black; color: white;")
        else:
            self.setStyleSheet("background-color: white; color: black;")

    def is_vietnamese(self, text):
        return any('\u0102' <= char <= '\u1EF9' for char in text)

    def analyze_sentiment_vietnamese(self, text):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        sentiment_label = self.get_sentiment_label(sentiment)
        return sentiment, sentiment_label

    def analyze_topic_vietnamese(self, text):
        # Kiểm tra các từ trong topic_keywords
        found_topics = {}
        total_words = len(text.split())

        for topic, keywords in topic_keywords.items():
            count = sum(text.count(keyword) for keyword in keywords)
            if count > 0:
                found_topics[topic] = count

        # Tính tỷ lệ phần trăm cho mỗi chủ đề
        if found_topics:
            topic_percentages = {topic: (count / total_words) * 100 for topic, count in found_topics.items()}
            return ', '.join([f"{topic} ({percentage:.2f}%)" for topic, percentage in topic_percentages.items()])
        else:
            return "Chủ đề chưa được xác định"

    def analyze_sentiment_english(self, text):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity  # Sử dụng TextBlob để phân tích cảm xúc
        sentiment_label = self.get_sentiment_label(sentiment)
        return sentiment, sentiment_label

    def analyze_topic_english(self, text):
        doc = nlp(text)
        topics = [chunk.text for chunk in doc.noun_chunks]  # Lấy các cụm danh từ làm chủ đề
        return ', '.join(topics) if topics else "Chủ đề chưa được xác định"

    def remove_stop_words(self, text):
        doc = nlp(text)
        # Lọc ra các từ không phải là stop words
        cleaned_tokens = [token.text for token in doc if not token.is_stop]
        return ' '.join(cleaned_tokens)

    def get_sentiment_label(self, sentiment):
        if sentiment > 0.5:
            return "Yêu thương"
        elif sentiment > 0:
            return "Tích cực"
        elif sentiment == 0:
            return "Trung lập"
        elif sentiment > -0.5:
            return "Tiêu cực"
        else:
            return "Thù ghét"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    classifier = TextClassifier()
    classifier.show()
    sys.exit(app.exec_())
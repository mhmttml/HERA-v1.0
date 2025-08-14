from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect, QTextEdit, QWidget
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class KulupTanimlaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kulüp Tanımla")
        self.setFixedSize(600, 500)
        self.setStyleSheet("background-color: #EBF2FA;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Başlık
        title = QLabel("Kulüp Tanımla")
        title.setFont(QFont("Sora DemiBold", 24, QFont.Weight.DemiBold))
        title.setStyleSheet("color: #427AA2;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(30)

        # Kulüp Adı
        kulup_adi_section = QWidget()
        kulup_adi_layout = QHBoxLayout(kulup_adi_section)
        kulup_adi_layout.setContentsMargins(0, 0, 0, 0)
        kulup_adi_layout.setSpacing(15)

        kulup_adi_label = QLabel("Kulüp Adı:")
        kulup_adi_label.setFont(QFont("Sora", 14))
        kulup_adi_label.setStyleSheet("color: #427AA2;")
        kulup_adi_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        kulup_adi_label.setFixedWidth(120)
        kulup_adi_layout.addWidget(kulup_adi_label)

        self.kulup_adi_edit = QLineEdit()
        self.kulup_adi_edit.setFont(QFont("Sora", 14))
        self.kulup_adi_edit.setFixedHeight(50)
        self.kulup_adi_edit.setFixedWidth(350)
        self.kulup_adi_edit.setStyleSheet("""
            QLineEdit {
                background: white;
                border-radius: 12px;
                border: 1.5px solid #e0e0e0;
                padding: 0px 15px;
                color: #222;
            }
            QLineEdit:hover, QLineEdit:focus {
                border: 1.5px solid #227199;
                background: #F0F6FB;
            }
        """)
        kulup_adi_layout.addWidget(self.kulup_adi_edit)

        kulup_adi_layout.addStretch(1)
        layout.addWidget(kulup_adi_section)
        layout.addSpacing(20)

        # Kulüp Açıklaması
        kulup_aciklama_section = QWidget()
        kulup_aciklama_layout = QHBoxLayout(kulup_aciklama_section)
        kulup_aciklama_layout.setContentsMargins(0, 0, 0, 0)
        kulup_aciklama_layout.setSpacing(15)

        kulup_aciklama_label = QLabel("Açıklama:")
        kulup_aciklama_label.setFont(QFont("Sora", 14))
        kulup_aciklama_label.setStyleSheet("color: #427AA2;")
        kulup_aciklama_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        kulup_aciklama_label.setFixedWidth(120)
        kulup_aciklama_layout.addWidget(kulup_aciklama_label)

        self.kulup_aciklama_edit = QLineEdit()
        self.kulup_aciklama_edit.setFont(QFont("Sora", 14))
        self.kulup_aciklama_edit.setFixedHeight(50)
        self.kulup_aciklama_edit.setFixedWidth(350)
        self.kulup_aciklama_edit.setStyleSheet("""
            QLineEdit {
                background: white;
                border-radius: 12px;
                border: 1.5px solid #e0e0e0;
                padding: 0px 15px;
                color: #222;
            }
            QLineEdit:hover, QLineEdit:focus {
                border: 1.5px solid #227199;
                background: #F0F6FB;
            }
        """)
        kulup_aciklama_layout.addWidget(self.kulup_aciklama_edit)

        kulup_aciklama_layout.addStretch(1)
        layout.addWidget(kulup_aciklama_section)
        layout.addSpacing(40)

        # Alt butonlar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Kaydet butonu
        self.save_btn = QPushButton("Kaydet")
        self.save_btn.setFont(QFont("Sora ExtraBold", 16, QFont.Weight.DemiBold))
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #A5BE00;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #C6E400;
                color: #427AA2;
            }
            QPushButton:pressed {
                background-color: #A5BE00;
            }
        """)
        save_shadow = QGraphicsDropShadowEffect()
        save_shadow.setBlurRadius(16)
        save_shadow.setOffset(0, 4)
        save_shadow.setColor(QColor(66, 122, 162, 60))
        self.save_btn.setGraphicsEffect(save_shadow)
        self.save_btn.setFixedSize(150, 50)
        self.save_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.save_btn)

        # İptal butonu
        self.cancel_btn = QPushButton("İptal")
        self.cancel_btn.setFont(QFont("Sora ExtraBold", 16, QFont.Weight.DemiBold))
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #A9C5DB;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #8FB7D6;
                color: #427AA2;
            }
            QPushButton:pressed {
                background-color: #A9C5DB;
            }
        """)
        cancel_shadow = QGraphicsDropShadowEffect()
        cancel_shadow.setBlurRadius(16)
        cancel_shadow.setOffset(0, 4)
        cancel_shadow.setColor(QColor(66, 122, 162, 60))
        self.cancel_btn.setGraphicsEffect(cancel_shadow)
        self.cancel_btn.setFixedSize(150, 50)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

    def get_kulup_data(self):
        """Kulüp verilerini döndür"""
        return {
            'kulup_adi': self.kulup_adi_edit.text(),
            'kulup_aciklama': self.kulup_aciklama_edit.text()
        }

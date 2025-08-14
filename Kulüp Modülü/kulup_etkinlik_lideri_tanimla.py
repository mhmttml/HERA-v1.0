from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QHBoxLayout, QGraphicsDropShadowEffect, QWidget)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class EtkinlikLideriTanimlaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Etkinlik Lideri Tanımla")
        self.setFixedSize(600, 600)
        self.setStyleSheet("background-color: #EBF2FA;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Başlık
        title = QLabel("Etkinlik Lideri Tanımla")
        title.setFont(QFont("Sora DemiBold", 24, QFont.Weight.DemiBold))
        title.setStyleSheet("color: #427AA2;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(30)

        # Etkinlik Lideri Adı-Soyadı
        ad_soyad_section = QWidget()
        ad_soyad_layout = QHBoxLayout(ad_soyad_section)
        ad_soyad_layout.setContentsMargins(0, 0, 0, 0)
        ad_soyad_layout.setSpacing(15)

        ad_soyad_label = QLabel("Ad-Soyad:")
        ad_soyad_label.setFont(QFont("Sora", 14))
        ad_soyad_label.setStyleSheet("color: #427AA2;")
        ad_soyad_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        ad_soyad_label.setFixedWidth(120)
        ad_soyad_layout.addWidget(ad_soyad_label)

        self.ad_soyad_edit = QLineEdit()
        self.ad_soyad_edit.setFont(QFont("Sora", 14))
        self.ad_soyad_edit.setFixedHeight(50)
        self.ad_soyad_edit.setFixedWidth(350)
        self.ad_soyad_edit.setStyleSheet("""
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
        ad_soyad_layout.addWidget(self.ad_soyad_edit)

        ad_soyad_layout.addStretch(1)
        layout.addWidget(ad_soyad_section)
        layout.addSpacing(20)

        # Etkinlik Lideri Telefon Numarası
        telefon_section = QWidget()
        telefon_layout = QHBoxLayout(telefon_section)
        telefon_layout.setContentsMargins(0, 0, 0, 0)
        telefon_layout.setSpacing(15)

        telefon_label = QLabel("Telefon:")
        telefon_label.setFont(QFont("Sora", 14))
        telefon_label.setStyleSheet("color: #427AA2;")
        telefon_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        telefon_label.setFixedWidth(120)
        telefon_layout.addWidget(telefon_label)

        self.telefon_edit = QLineEdit()
        self.telefon_edit.setFont(QFont("Sora", 14))
        self.telefon_edit.setFixedHeight(50)
        self.telefon_edit.setFixedWidth(350)
        self.telefon_edit.setStyleSheet("""
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
        telefon_layout.addWidget(self.telefon_edit)

        telefon_layout.addStretch(1)
        layout.addWidget(telefon_section)
        layout.addSpacing(20)

        # Etkinlik Lideri Mail Adresi
        mail_section = QWidget()
        mail_layout = QHBoxLayout(mail_section)
        mail_layout.setContentsMargins(0, 0, 0, 0)
        mail_layout.setSpacing(15)

        mail_label = QLabel("E-mail:")
        mail_label.setFont(QFont("Sora", 14))
        mail_label.setStyleSheet("color: #427AA2;")
        mail_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        mail_label.setFixedWidth(120)
        mail_layout.addWidget(mail_label)

        self.mail_edit = QLineEdit()
        self.mail_edit.setFont(QFont("Sora", 14))
        self.mail_edit.setFixedHeight(50)
        self.mail_edit.setFixedWidth(350)
        self.mail_edit.setStyleSheet("""
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
        mail_layout.addWidget(self.mail_edit)

        mail_layout.addStretch(1)
        layout.addWidget(mail_section)
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

    def get_etkinlik_lideri_data(self):
        """Etkinlik lideri tanımlama verilerini döndür"""
        return {
            'ad_soyad': self.ad_soyad_edit.text(),
            'telefon': self.telefon_edit.text(),
            'mail': self.mail_edit.text()
        }

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect, QDateEdit, QCalendarWidget, QWidget, QComboBox, QGridLayout
from PyQt6.QtGui import QFont, QColor, QIntValidator, QIcon
from PyQt6.QtCore import Qt, QLocale
QLocale.setDefault(QLocale(QLocale.Language.Turkish, QLocale.Country.Turkey))

class GeziEkleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gezi Ekle")
        self.setFixedSize(1000, 800)
        self.setStyleSheet("background-color: #EBF2FA;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Başlık
        title = QLabel("Gezi Ekle")
        title.setFont(QFont("Arial", 22, QFont.Weight.DemiBold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(18)

        # İki sütunlu grid layout
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        # Sol Sütun
        # Gezi ID
        gezi_id_label = QLabel("Gezi ID:")
        gezi_id_label.setFont(QFont("Arial", 14))
        gezi_id_label.setStyleSheet("color: #427AA2;")
        gezi_id_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.gezi_id_edit = QLineEdit()
        self.gezi_id_edit.setFont(QFont("Arial", 14))
        self.gezi_id_edit.setFixedHeight(50)
        self.gezi_id_edit.setStyleSheet("""
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
        self.gezi_id_edit.setReadOnly(True)
        self.gezi_id_edit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        grid_layout.addWidget(gezi_id_label, 0, 0)
        grid_layout.addWidget(self.gezi_id_edit, 0, 1)

        # Gezi Adı
        gezi_adi_label = QLabel("Gezi Adı:")
        gezi_adi_label.setFont(QFont("Arial", 14))
        gezi_adi_label.setStyleSheet("color: #427AA2;")
        gezi_adi_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.gezi_adi_edit = QLineEdit()
        self.gezi_adi_edit.setFont(QFont("Arial", 14))
        self.gezi_adi_edit.setFixedHeight(50)
        self.gezi_adi_edit.setStyleSheet("""
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
        grid_layout.addWidget(gezi_adi_label, 1, 0)
        grid_layout.addWidget(self.gezi_adi_edit, 1, 1)

        # Gezi Başlangıç tarihi
        baslangic_label = QLabel("Gezi Başlangıç Tarihi:")
        baslangic_label.setFont(QFont("Arial", 14))
        baslangic_label.setStyleSheet("color: #427AA2;")
        baslangic_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.baslangic_edit = QLineEdit()
        self.baslangic_edit.setFont(QFont("Arial", 14))
        self.baslangic_edit.setFixedHeight(50)
        self.baslangic_edit.setStyleSheet("""
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
        self.baslangic_edit.setReadOnly(True)
        grid_layout.addWidget(baslangic_label, 2, 0)
        grid_layout.addWidget(self.baslangic_edit, 2, 1)

        # Gezi bitiş tarihi
        bitis_label = QLabel("Gezi Bitiş Tarihi:")
        bitis_label.setFont(QFont("Arial", 14))
        bitis_label.setStyleSheet("color: #427AA2;")
        bitis_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.bitis_edit = QLineEdit()
        self.bitis_edit.setFont(QFont("Arial", 14))
        self.bitis_edit.setFixedHeight(50)
        self.bitis_edit.setStyleSheet("""
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
        self.bitis_edit.setReadOnly(True)
        grid_layout.addWidget(bitis_label, 3, 0)
        grid_layout.addWidget(self.bitis_edit, 3, 1)

        # Gezi ücreti
        ucret_label = QLabel("Gezi Ücreti:")
        ucret_label.setFont(QFont("Arial", 14))
        ucret_label.setStyleSheet("color: #427AA2;")
        ucret_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.ucret_edit = QLineEdit()
        self.ucret_edit.setFont(QFont("Arial", 14))
        self.ucret_edit.setFixedHeight(50)
        self.ucret_edit.setStyleSheet("""
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
        grid_layout.addWidget(ucret_label, 4, 0)
        grid_layout.addWidget(self.ucret_edit, 4, 1)

        # Minimum katılımcı sayısı (gezi ücreti alanının altında)
        min_participant_label = QLabel("Minimum Katılımcı Sayısı:")
        min_participant_label.setFont(QFont("Arial", 14))
        min_participant_label.setStyleSheet("color: #427AA2;")
        min_participant_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.min_participant_edit = QLineEdit()
        self.min_participant_edit.setFont(QFont("Arial", 14))
        self.min_participant_edit.setFixedHeight(50)
        self.min_participant_edit.setStyleSheet("""
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
        self.min_participant_edit.setValidator(QIntValidator(1, 1000))
        grid_layout.addWidget(min_participant_label, 5, 0)
        grid_layout.addWidget(self.min_participant_edit, 5, 1)

        # Maksimum katılımcı sayısı (minimum katılımcı alanının altında)
        max_participant_label = QLabel("Maksimum Katılımcı Sayısı:")
        max_participant_label.setFont(QFont("Arial", 14))
        max_participant_label.setStyleSheet("color: #427AA2;")
        max_participant_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.max_participant_edit = QLineEdit()
        self.max_participant_edit.setFont(QFont("Arial", 14))
        self.max_participant_edit.setFixedHeight(50)
        self.max_participant_edit.setStyleSheet("""
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
        self.max_participant_edit.setValidator(QIntValidator(1, 1000))
        grid_layout.addWidget(max_participant_label, 6, 0)
        grid_layout.addWidget(self.max_participant_edit, 6, 1)

        # Sağ Sütun
        # Gezi Lideri (ComboBox)
        lider_label = QLabel("Gezi Lideri:")
        lider_label.setFont(QFont("Arial", 14))
        lider_label.setStyleSheet("color: #427AA2;")
        lider_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.lider_combo = QComboBox()
        self.lider_combo.setFont(QFont("Arial", 14))
        self.lider_combo.setFixedHeight(50)
        self.lider_combo.addItems(["Lider Seçin", "özgür", "ahmet", "fatma", "mehmet"])
        self.lider_combo.setStyleSheet("""
            QComboBox {
                background: white;
                border-radius: 12px;
                border: 1.5px solid #e0e0e0;
                padding: 0px 15px;
                color: #222;
            }
            QComboBox:hover, QComboBox:focus {
                border: 1.5px solid #227199;
                background: #F0F6FB;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(ucgen.png);
                width: 20px;
                height: 20px;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                selection-background-color: #F0F6FB;
            }
        """)
        grid_layout.addWidget(lider_label, 0, 2)
        grid_layout.addWidget(self.lider_combo, 0, 3)

        # Gezi Durumu (ComboBox)
        durum_label = QLabel("Gezi Durumu:")
        durum_label.setFont(QFont("Arial", 14))
        durum_label.setStyleSheet("color: #427AA2;")
        durum_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.durum_combo = QComboBox()
        self.durum_combo.setFont(QFont("Arial", 14))
        self.durum_combo.setFixedHeight(50)
        self.durum_combo.addItems(["Durum Seçin", "Planlandı", "Aktif", "Tamamlandı", "İptal Edildi"])
        self.durum_combo.setStyleSheet("""
            QComboBox {
                background: white;
                border-radius: 12px;
                border: 1.5px solid #e0e0e0;
                padding: 0px 15px;
                color: #222;
            }
            QComboBox:hover, QComboBox:focus {
                border: 1.5px solid #227199;
                background: #F0F6FB;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(ucgen.png);
                width: 20px;
                height: 20px;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                selection-background-color: #F0F6FB;
            }
        """)
        grid_layout.addWidget(durum_label, 1, 2)
        grid_layout.addWidget(self.durum_combo, 1, 3)

        # Gezi Adresi
        adres_label = QLabel("Gezi Adresi:")
        adres_label.setFont(QFont("Arial", 14))
        adres_label.setStyleSheet("color: #427AA2;")
        adres_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.adres_edit = QLineEdit()
        self.adres_edit.setFont(QFont("Arial", 14))
        self.adres_edit.setFixedHeight(50)
        self.adres_edit.setStyleSheet("""
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
        grid_layout.addWidget(adres_label, 2, 2)
        grid_layout.addWidget(self.adres_edit, 2, 3)

        # Gezi açıklaması
        aciklama_label = QLabel("Gezi Açıklaması:")
        aciklama_label.setFont(QFont("Arial", 14))
        aciklama_label.setStyleSheet("color: #427AA2;")
        aciklama_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.aciklama_edit = QLineEdit()
        self.aciklama_edit.setFont(QFont("Arial", 14))
        self.aciklama_edit.setFixedHeight(50)
        self.aciklama_edit.setStyleSheet("""
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
        grid_layout.addWidget(aciklama_label, 3, 2)
        grid_layout.addWidget(self.aciklama_edit, 3, 3)

        # Organizatör bilgisi
        organizator_label = QLabel("Organizatör Bilgisi:")
        organizator_label.setFont(QFont("Arial", 14))
        organizator_label.setStyleSheet("color: #427AA2;")
        organizator_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.organizator_edit = QLineEdit()
        self.organizator_edit.setFont(QFont("Arial", 14))
        self.organizator_edit.setFixedHeight(50)
        self.organizator_edit.setStyleSheet("""
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
        grid_layout.addWidget(organizator_label, 4, 2)
        grid_layout.addWidget(self.organizator_edit, 4, 3)

        # Araç plakası
        plaka_label = QLabel("Araç Plakası:")
        plaka_label.setFont(QFont("Arial", 14))
        plaka_label.setStyleSheet("color: #427AA2;")
        plaka_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.plaka_edit = QLineEdit()
        self.plaka_edit.setFont(QFont("Arial", 14))
        self.plaka_edit.setFixedHeight(50)
        self.plaka_edit.setStyleSheet("""
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
        grid_layout.addWidget(plaka_label, 5, 2)
        grid_layout.addWidget(self.plaka_edit, 5, 3)

        layout.addLayout(grid_layout)
        layout.addSpacing(40)

        # Alt butonlar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Kaydet butonu
        self.save_btn = QPushButton("Kaydet")
        self.save_btn.setFont(QFont("Arial", 16, QFont.Weight.DemiBold))
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
        self.save_btn.setFixedSize(180, 55)
        self.save_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.save_btn)

        # İptal butonu
        self.cancel_btn = QPushButton("İptal")
        self.cancel_btn.setFont(QFont("Arial", 16, QFont.Weight.DemiBold))
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
        self.cancel_btn.setFixedSize(180, 55)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

        # Takvim widget'ları (gizli)
        self.baslangic_calendar = QCalendarWidget()
        self.baslangic_calendar.setWindowFlags(Qt.WindowType.Popup)
        self.baslangic_calendar.setGridVisible(True)
        self.baslangic_calendar.setStyleSheet("font-family: Arial; font-size: 14px;")
        self.baslangic_calendar.hide()

        self.bitis_calendar = QCalendarWidget()
        self.bitis_calendar.setWindowFlags(Qt.WindowType.Popup)
        self.bitis_calendar.setGridVisible(True)
        self.bitis_calendar.setStyleSheet("font-family: Arial; font-size: 14px;")
        self.bitis_calendar.hide()

        # Takvim fonksiyonları
        def show_baslangic_calendar(event=None):
            pos = self.baslangic_edit.mapToGlobal(self.baslangic_edit.rect().bottomRight())
            self.baslangic_calendar.move(pos.x() - self.baslangic_calendar.width(), pos.y())
            self.baslangic_calendar.show()
        self.baslangic_edit.mousePressEvent = show_baslangic_calendar

        def show_bitis_calendar(event=None):
            pos = self.bitis_edit.mapToGlobal(self.bitis_edit.rect().bottomRight())
            self.bitis_calendar.move(pos.x() - self.bitis_calendar.width(), pos.y())
            self.bitis_calendar.show()
        self.bitis_edit.mousePressEvent = show_bitis_calendar

        def set_baslangic_date(date):
            tarih_str = date.toString("dd MMMM yyyy")
            aylar = {
                "January": "Ocak", "February": "Şubat", "March": "Mart", "April": "Nisan",
                "May": "Mayıs", "June": "Haziran", "July": "Temmuz", "August": "Ağustos",
                "September": "Eylül", "October": "Ekim", "November": "Kasım", "December": "Aralık"
            }
            for en, tr in aylar.items():
                tarih_str = tarih_str.replace(en, tr)
            self.baslangic_edit.setText(tarih_str)
            self.baslangic_calendar.hide()
        self.baslangic_calendar.clicked.connect(set_baslangic_date)

        def set_bitis_date(date):
            tarih_str = date.toString("dd MMMM yyyy")
            aylar = {
                "January": "Ocak", "February": "Şubat", "March": "Mart", "April": "Nisan",
                "May": "Mayıs", "June": "Haziran", "July": "Temmuz", "August": "Ağustos",
                "September": "Eylül", "October": "Ekim", "November": "Kasım", "December": "Aralık"
            }
            for en, tr in aylar.items():
                tarih_str = tarih_str.replace(en, tr)
            self.bitis_edit.setText(tarih_str)
            self.bitis_calendar.hide()
        self.bitis_calendar.clicked.connect(set_bitis_date)

    def get_gezi_data(self):
        """Gezi verilerini döndür"""
        return {
            'gezi_id': self.gezi_id_edit.text(),
            'gezi_adi': self.gezi_adi_edit.text(),
            'baslangic_tarihi': self.baslangic_edit.text(),
            'bitis_tarihi': self.bitis_edit.text(),
            'ucret': self.ucret_edit.text(),
            'lider': self.lider_combo.currentText(),
            'durum': self.durum_combo.currentText(),
            'adres': self.adres_edit.text(),
            'aciklama': self.aciklama_edit.text(),
            'organizator': self.organizator_edit.text(),
            'plaka': self.plaka_edit.text(),
            'min_katilimci': self.min_participant_edit.text(),
            'max_katilimci': self.max_participant_edit.text()
        } 
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect, QDateEdit, QCalendarWidget, QWidget, QComboBox, QGridLayout, QTextEdit, QMessageBox
from PyQt6.QtGui import QFont, QColor, QIntValidator, QIcon
from PyQt6.QtCore import Qt, QLocale
from kulup_tanimla import KulupTanimlaDialog
from kulup_etkinlik_lideri_tanimla import EtkinlikLideriTanimlaDialog
QLocale.setDefault(QLocale(QLocale.Language.Turkish, QLocale.Country.Turkey))

class EtkinlikEkleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Etkinlik Ekle")
        self.setFixedSize(600,800)
        self.setStyleSheet("background-color: #EBF2FA;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Başlık
        title = QLabel("Etkinlik Ekle")
        title.setFont(QFont("Arial", 22, QFont.Weight.DemiBold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(18)

        # İki sütunlu grid layout
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        # Sol Sütun
        # Etkinlik ID
        etkinlik_id_label = QLabel("Etkinlik ID:")
        etkinlik_id_label.setFont(QFont("Arial", 14))
        etkinlik_id_label.setStyleSheet("color: #427AA2;")
        etkinlik_id_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.etkinlik_id_edit = QLineEdit()
        self.etkinlik_id_edit.setFont(QFont("Arial", 14))
        self.etkinlik_id_edit.setFixedHeight(50)
        self.etkinlik_id_edit.setStyleSheet("""
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
        self.etkinlik_id_edit.setReadOnly(True)
        self.etkinlik_id_edit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        grid_layout.addWidget(etkinlik_id_label, 0, 0)
        grid_layout.addWidget(self.etkinlik_id_edit, 0, 1)

        # Etkinlik Adı
        etkinlik_adi_label = QLabel("Etkinlik Adı:")
        etkinlik_adi_label.setFont(QFont("Arial", 14))
        etkinlik_adi_label.setStyleSheet("color: #427AA2;")
        etkinlik_adi_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.etkinlik_adi_edit = QLineEdit()
        self.etkinlik_adi_edit.setFont(QFont("Arial", 14))
        self.etkinlik_adi_edit.setFixedHeight(50)
        self.etkinlik_adi_edit.setStyleSheet("""
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
        grid_layout.addWidget(etkinlik_adi_label, 1, 0)
        grid_layout.addWidget(self.etkinlik_adi_edit, 1, 1)

        # Kulüp
        kulup_label = QLabel("Kulüp:")
        kulup_label.setFont(QFont("Arial", 14))
        kulup_label.setStyleSheet("color: #427AA2;")
        kulup_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # Kulüp seçimi için horizontal layout
        kulup_layout = QHBoxLayout()
        self.kulup_combo = QComboBox()
        self.kulup_combo.setFont(QFont("Arial", 14))
        self.kulup_combo.setFixedHeight(50)
        self.kulup_combo.setStyleSheet("""
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
        """)
        self.kulup_combo.addItems(["Spor Kulübü", "Müzik Kulübü", "Kitap Kulübü", "Sanat Kulübü", "Bilim Kulübü"])
        
        # Kulüp ekleme butonu
        self.kulup_ekle_btn = QPushButton("+")
        self.kulup_ekle_btn.setFont(QFont("Arial", 20, QFont.Weight.DemiBold))
        self.kulup_ekle_btn.setFixedSize(50, 50)
        self.kulup_ekle_btn.setStyleSheet("""
            QPushButton {
                background: white;
                border-radius: 12px;
                border: 1.5px solid #e0e0e0;
                color: #427AA2;
            }
            QPushButton:hover {
                border: 1.5px solid #227199;
                background: #F0F6FB;
            }
        """)
        # Gölge efekti ekle
        kulup_shadow = QGraphicsDropShadowEffect()
        kulup_shadow.setBlurRadius(8)
        kulup_shadow.setOffset(0, 2)
        kulup_shadow.setColor(QColor(0, 0, 0, 25))
        self.kulup_ekle_btn.setGraphicsEffect(kulup_shadow)
        
        # Kulüp ekleme butonuna tıklama olayını bağla
        self.kulup_ekle_btn.clicked.connect(self.show_kulup_tanimla_popup)
        
        kulup_layout.addWidget(self.kulup_combo)
        kulup_layout.addWidget(self.kulup_ekle_btn)
        grid_layout.addWidget(kulup_label, 2, 0)
        grid_layout.addLayout(kulup_layout, 2, 1)

        # Etkinlik Durumu
        durum_label = QLabel("Etkinlik Durumu:")
        durum_label.setFont(QFont("Arial", 14))
        durum_label.setStyleSheet("color: #427AA2;")
        durum_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.durum_combo = QComboBox()
        self.durum_combo.setFont(QFont("Arial", 14))
        self.durum_combo.setFixedHeight(50)
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
        """)
        self.durum_combo.addItems(["Planlandı", "Aktif", "Tamamlandı", "İptal Edildi"])
        grid_layout.addWidget(durum_label, 3, 0)
        grid_layout.addWidget(self.durum_combo, 3, 1)

        # Etkinlik Lideri
        lider_label = QLabel("Etkinlik Lideri:")
        lider_label.setFont(QFont("Arial", 14))
        lider_label.setStyleSheet("color: #427AA2;")
        lider_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # Lider seçimi için horizontal layout
        lider_layout = QHBoxLayout()
        self.lider_combo = QComboBox()
        self.lider_combo.setFont(QFont("Arial", 14))
        self.lider_combo.setFixedHeight(50)
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
        """)
        self.lider_combo.addItems(["Ahmet Yılmaz", "Ayşe Demir", "Mehmet Kaya", "Fatma Şahin", "Ali Özkan"])
        
        # Lider ekleme butonu
        self.lider_ekle_btn = QPushButton("+")
        self.lider_ekle_btn.setFont(QFont("Arial", 20, QFont.Weight.DemiBold))
        self.lider_ekle_btn.setFixedSize(50, 50)
        self.lider_ekle_btn.setStyleSheet("""
            QPushButton {
                background: white;
                border-radius: 12px;
                border: 1.5px solid #e0e0e0;
                color: #427AA2;
            }
            QPushButton:hover {
                border: 1.5px solid #227199;
                background: #F0F6FB;
            }
        """)
        # Gölge efekti ekle
        lider_shadow = QGraphicsDropShadowEffect()
        lider_shadow.setBlurRadius(8)
        lider_shadow.setOffset(0, 2)
        lider_shadow.setColor(QColor(0, 0, 0, 25))
        self.lider_ekle_btn.setGraphicsEffect(lider_shadow)
        
        # Lider ekleme butonuna tıklama olayını bağla
        self.lider_ekle_btn.clicked.connect(self.show_etkinlik_lideri_tanimla_popup)
        
        lider_layout.addWidget(self.lider_combo)
        lider_layout.addWidget(self.lider_ekle_btn)
        grid_layout.addWidget(lider_label, 4, 0)
        grid_layout.addLayout(lider_layout, 4, 1)

        # Etkinlik Açıklaması
        aciklama_label = QLabel("Etkinlik Açıklaması:")
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
        grid_layout.addWidget(aciklama_label, 5, 0)
        grid_layout.addWidget(self.aciklama_edit, 5, 1)

        # Minimum katılımcı sayısı
        min_katilimci_label = QLabel("Minimum Katılımcı Sayısı:")
        min_katilimci_label.setFont(QFont("Arial", 14))
        min_katilimci_label.setStyleSheet("color: #427AA2;")
        min_katilimci_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.min_katilimci_edit = QLineEdit()
        self.min_katilimci_edit.setFont(QFont("Arial", 14))
        self.min_katilimci_edit.setFixedHeight(50)
        self.min_katilimci_edit.setStyleSheet("""
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
        self.min_katilimci_edit.setValidator(QIntValidator(1, 1000))
        grid_layout.addWidget(min_katilimci_label, 6, 0)
        grid_layout.addWidget(self.min_katilimci_edit, 6, 1)

        # Maksimum katılımcı sayısı
        max_katilimci_label = QLabel("Maksimum Katılımcı Sayısı:")
        max_katilimci_label.setFont(QFont("Arial", 14))
        max_katilimci_label.setStyleSheet("color: #427AA2;")
        max_katilimci_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.max_katilimci_edit = QLineEdit()
        self.max_katilimci_edit.setFont(QFont("Arial", 14))
        self.max_katilimci_edit.setFixedHeight(50)
        self.max_katilimci_edit.setStyleSheet("""
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
        self.max_katilimci_edit.setValidator(QIntValidator(1, 1000))
        grid_layout.addWidget(max_katilimci_label, 7, 0)
        grid_layout.addWidget(self.max_katilimci_edit, 7, 1)

        # Etkinlik Başlangıç Tarihi
        baslangic_label = QLabel("Etkinlik Başlangıç Tarihi:")
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
        grid_layout.addWidget(baslangic_label, 8, 0)
        grid_layout.addWidget(self.baslangic_edit, 8, 1)

        # Etkinlik Bitiş Tarihi
        bitis_label = QLabel("Etkinlik Bitiş Tarihi:")
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
        grid_layout.addWidget(bitis_label, 9, 0)
        grid_layout.addWidget(self.bitis_edit, 9, 1)

        # Grid layout'u ana layout'a ekle
        layout.addLayout(grid_layout)
        layout.addStretch(1)

        # Buton layout'u
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

        # Etkinlik ID'yi otomatik olarak ata
        self.generate_etkinlik_id()

    def show_kulup_tanimla_popup(self):
        """Kulüp tanımla ekranını aç"""
        dialog = KulupTanimlaDialog(self)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            # Kulüp verilerini al
            kulup_data = dialog.get_kulup_data()
            
            # Yeni kulübü ComboBox'a ekle
            self.kulup_combo.addItem(kulup_data['kulup_adi'])
            
            # Yeni eklenen kulübü seç
            self.kulup_combo.setCurrentText(kulup_data['kulup_adi'])
            
            QMessageBox.information(self, "Başarılı", f"Kulüp '{kulup_data['kulup_adi']}' başarıyla eklendi!")
        else:
            print("Kulüp ekleme işlemi iptal edildi.")

    def show_etkinlik_lideri_tanimla_popup(self):
        """Etkinlik lideri tanımla ekranını aç"""
        dialog = EtkinlikLideriTanimlaDialog(self)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            # Etkinlik lideri verilerini al
            lider_data = dialog.get_etkinlik_lideri_data()
            
            # Yeni lideri ComboBox'a ekle
            self.lider_combo.addItem(lider_data['ad_soyad'])
            
            # Yeni eklenen lideri seç
            self.lider_combo.setCurrentText(lider_data['ad_soyad'])
            
            QMessageBox.information(self, "Başarılı", f"Etkinlik Lideri '{lider_data['ad_soyad']}' başarıyla eklendi!")
        else:
            print("Etkinlik lideri ekleme işlemi iptal edildi.")

    def generate_etkinlik_id(self, current_count=0):
        """Yeni etkinlik için otomatik ID oluştur"""
        # Mevcut etkinlik sayısına göre yeni ID oluştur
        new_id = f"ET{current_count + 1:03d}"
        self.etkinlik_id_edit.setText(new_id)

    def get_etkinlik_data(self):
        """Etkinlik verilerini döndür"""
        return {
            'etkinlik_id': self.etkinlik_id_edit.text(),
            'etkinlik_adi': self.etkinlik_adi_edit.text(),
            'kulup': self.kulup_combo.currentText(),
            'durum': self.durum_combo.currentText(),
            'lider': self.lider_combo.currentText(),
            'aciklama': self.aciklama_edit.text(),
            'min_katilimci': self.min_katilimci_edit.text(),
            'max_katilimci': self.max_katilimci_edit.text(),
            'baslangic_tarihi': self.baslangic_edit.text(),
            'bitis_tarihi': self.bitis_edit.text()
        }

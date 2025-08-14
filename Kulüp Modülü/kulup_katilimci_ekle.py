from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, 
                             QGraphicsDropShadowEffect, QWidget, QTableWidget, QTableWidgetItem,
                             QHeaderView, QScrollBar, QAbstractScrollArea, QAbstractItemView,
                             QRadioButton, QButtonGroup, QMessageBox, QSizePolicy)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class KulupKatilimciEkleDialog(QDialog):
    def __init__(self, parent=None, kulup_adi="", etkinlik_adi=""):
        super().__init__(parent)
        self.setWindowTitle("Katılımcı Ekle")
        self.kulup_adi = kulup_adi
        self.etkinlik_adi = etkinlik_adi
        
        # Responsive boyut hesaplama (sağlık değer gir ekranındaki gibi)
        base_width, base_height = 1920, 1080
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        self.scroll_scale = min(screen_width / base_width, screen_height / base_height)
        
        # Dialog boyutları - normal boyut
        dialog_width = int(900 * self.scroll_scale)
        dialog_height = int(700 * self.scroll_scale)
        self.setFixedSize(dialog_width, dialog_height)
        
        self.setStyleSheet("background-color: #EBF2FA;")
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Responsive margins ve spacing
        margin = int(30 * self.scroll_scale)
        spacing = int(15 * self.scroll_scale)
        
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(spacing)

        # Başlık
        title = QLabel("Katılımcı Ekle")
        title_font_size = int(22 * self.scroll_scale)
        title.setFont(QFont("Arial", title_font_size, QFont.Weight.DemiBold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(int(18 * self.scroll_scale))
        
        # Kulüp ve Etkinlik Bilgisi
        if self.kulup_adi and self.etkinlik_adi:
            kulup_etkinlik_label = QLabel(f"{self.kulup_adi} - {self.etkinlik_adi}")
            kulup_etkinlik_font_size = int(18 * self.scroll_scale)
            kulup_etkinlik_label.setFont(QFont("Arial", kulup_etkinlik_font_size, QFont.Weight.Medium))
            kulup_etkinlik_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            kulup_etkinlik_label.setStyleSheet("color: #427AA2; margin-bottom: 10px;")
            layout.addWidget(kulup_etkinlik_label)
            layout.addSpacing(int(15 * self.scroll_scale))



        # Tablo container (sağlık değer gir ekranındaki gibi)
        table_container = QWidget()
        table_container.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 15px;
                border: none;
            }
        """)
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(int(12 * self.scroll_scale), int(12 * self.scroll_scale), int(12 * self.scroll_scale), int(12 * self.scroll_scale))

        # Tablo
        self.katilimci_table = QTableWidget()
        self.katilimci_table.setColumnCount(4)
        self.katilimci_table.setHorizontalHeaderLabels([
            "İsim", "Soyisim", "Sınıf", "Katılım Sağlanıyor mu?"
        ])
        
        # Tablo stilini ayarla (sağlık değer gir ekranındaki gibi)
        self.katilimci_table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 2px solid #427AA2;
                border-top-left-radius: 13px;
                border-top-right-radius: 13px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                gridline-color: #f0f0f0;
                selection-background-color: #E8F4FD;
                selection-color: #427AA2;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
                border-bottom: 2px solid #f0f0f0;
                border-right: 2px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #E8F4FD;
                color: #427AA2;
            }
            QHeaderView::section {
                background-color: #427AA2;
                color: white;
                padding: 12px 8px;
                border: none;
                border-right: 1px solid #FFFFFF;
                font-weight: bold;
                font-size: 14px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 13px;
                border-right: none;
            }
        """)
        
        # Sütun genişliklerini ayarla
        header = self.katilimci_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # İsim
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # Soyisim
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # Sınıf
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Katılım
        
        # Dikey başlığı gizle (satır numaraları)
        vertical_header = self.katilimci_table.verticalHeader()
        vertical_header.setVisible(False)
        
        # Tablo scroll bar'larını gizle
        self.katilimci_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.katilimci_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.katilimci_table.verticalScrollBar().setStyleSheet("QScrollBar { width: 0px; }")
        self.katilimci_table.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0px; }")
        
        # Sütun genişliklerini ayarla (responsive) - tablo border içinde kalabilsin
        self.katilimci_table.setColumnWidth(0, int(190 * self.scroll_scale))  # İsim
        self.katilimci_table.setColumnWidth(1, int(190 * self.scroll_scale))  # Soyisim
        self.katilimci_table.setColumnWidth(2, int(170 * self.scroll_scale))  # Sınıf
        self.katilimci_table.setColumnWidth(3, int(220 * self.scroll_scale))  # Katılım
        
        # Tablo boyutunu sınırla
        self.katilimci_table.setFixedHeight(int(400 * self.scroll_scale))
        self.katilimci_table.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        # Özel scroll bar konteynerleri oluştur (sağlık değer gir ekranındaki gibi)
        # Dikey scroll bar konteyneri
        scroll_container = QWidget()
        scroll_container.setFixedWidth(int(30 * self.scroll_scale))
        scroll_container.setStyleSheet("background-color: #A9C5DB; border-radius: 15px;")
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)
        
        # Dikey scroll bar
        self.scrollbar = QScrollBar(Qt.Orientation.Vertical)
        self.scrollbar.setStyleSheet(f"""
            QScrollBar:vertical {{
                background: rgba(66,122,162,0.5);
                border-radius: 10px;
                width: {int(30 * self.scroll_scale)}px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: white;
                border-radius: 10px;
                min-width: {int(20 * self.scroll_scale)}px;
                min-height: {int(90 * self.scroll_scale)}px;
                max-width: {int(20 * self.scroll_scale)}px;
                max-height: {int(90 * self.scroll_scale)}px;
                width: {int(20 * self.scroll_scale)}px;
                height: {int(90 * self.scroll_scale)}px;
                margin-left: {int(5 * self.scroll_scale)}px;
                margin-right: {int(5 * self.scroll_scale)}px;
                margin-top: {int(6 * self.scroll_scale)}px;
                margin-bottom: {int(6 * self.scroll_scale)}px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
                subcontrol-origin: margin;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)
        scroll_layout.addWidget(self.scrollbar)
        
        # Scroll bar ile tabloyu senkronize et
        def update_scrollbar():
            try:
                self.scrollbar.setMinimum(self.katilimci_table.verticalScrollBar().minimum())
                self.scrollbar.setMaximum(self.katilimci_table.verticalScrollBar().maximum())
                self.scrollbar.setPageStep(self.katilimci_table.verticalScrollBar().pageStep())
                self.scrollbar.setSingleStep(self.katilimci_table.verticalScrollBar().singleStep())
                self.scrollbar.setValue(self.katilimci_table.verticalScrollBar().value())
            except:
                pass
        
        def update_table_scrollbar():
            try:
                self.katilimci_table.verticalScrollBar().setValue(self.scrollbar.value())
            except:
                pass
        
        # Başlangıç değerlerini ayarla
        update_scrollbar()
        
        # Senkronizasyon bağlantıları
        self.scrollbar.valueChanged.connect(update_table_scrollbar)
        self.katilimci_table.verticalScrollBar().valueChanged.connect(lambda: self.scrollbar.setValue(self.katilimci_table.verticalScrollBar().value()) if hasattr(self, 'scrollbar') else None)
        self.katilimci_table.verticalScrollBar().rangeChanged.connect(update_scrollbar)
        
        # Tablo ve scroll bar'ı yan yana yerleştir
        self.table_and_scroll_layout = QHBoxLayout()
        self.table_and_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.table_and_scroll_layout.setSpacing(int(15 * self.scroll_scale))
        self.table_and_scroll_layout.addWidget(self.katilimci_table)
        self.table_and_scroll_layout.addWidget(scroll_container)
        
        table_layout.addLayout(self.table_and_scroll_layout)
        layout.addWidget(table_container)
        layout.addSpacing(int(20 * self.scroll_scale))

        # Alt butonlar - görseldeki gibi daha iyi spacing
        button_layout = QHBoxLayout()
        button_layout.setSpacing(int(20 * self.scroll_scale))  # Butonlar arası spacing artırıldı
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Responsive button boyutları (sağlık değer gir ekranındaki gibi)
        button_width = int(170 * self.scroll_scale)  # Dışarı aktar için genişletildi
        button_height = int(50 * self.scroll_scale)
        button_font_size = int(14 * self.scroll_scale)
        button_radius = int(8 * self.scroll_scale)
        button_padding = int(12 * self.scroll_scale)

        # Dışarı Aktar butonu
        self.disari_aktar_btn = QPushButton("Dışarı Aktar")
        self.disari_aktar_btn.setFont(QFont("Sora ExtraBold", button_font_size, QFont.Weight.DemiBold))
        self.disari_aktar_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #A9C5DB;
                color: #FFFFFF;
                border: none;
                border-radius: {button_radius}px;
                padding: {button_padding}px {button_padding * 2}px;
            }}
            QPushButton:hover {{
                background-color: #8FB7D6;
                color: #427AA2;
            }}
            QPushButton:pressed {{
                background-color: #A9C5DB;
            }}
        """)
        disari_aktar_shadow = QGraphicsDropShadowEffect()
        disari_aktar_shadow.setBlurRadius(int(16 * self.scroll_scale))
        disari_aktar_shadow.setOffset(0, int(4 * self.scroll_scale))
        disari_aktar_shadow.setColor(QColor(66, 122, 162, 60))
        self.disari_aktar_btn.setGraphicsEffect(disari_aktar_shadow)
        self.disari_aktar_btn.setFixedSize(button_width, button_height)
        self.disari_aktar_btn.clicked.connect(self.disari_aktar)
        button_layout.addWidget(self.disari_aktar_btn)

        # Kaydet butonu
        self.save_btn = QPushButton("Kaydet")
        self.save_btn.setFont(QFont("Sora ExtraBold", button_font_size, QFont.Weight.DemiBold))
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #A5BE00;
                color: #FFFFFF;
                border: none;
                border-radius: {button_radius}px;
                padding: {button_padding}px {button_padding * 2}px;
            }}
            QPushButton:hover {{
                background-color: #C6E400;
                color: #427AA2;
            }}
            QPushButton:pressed {{
                background-color: #A5BE00;
            }}
        """)
        save_shadow = QGraphicsDropShadowEffect()
        save_shadow.setBlurRadius(int(16 * self.scroll_scale))
        save_shadow.setOffset(0, int(4 * self.scroll_scale))
        save_shadow.setColor(QColor(66, 122, 162, 60))
        self.save_btn.setGraphicsEffect(save_shadow)
        self.save_btn.setFixedSize(button_width, button_height)
        self.save_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.save_btn)

        # İptal butonu
        self.cancel_btn = QPushButton("İptal")
        self.cancel_btn.setFont(QFont("Sora ExtraBold", button_font_size, QFont.Weight.DemiBold))
        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #A9C5DB;
                color: #FFFFFF;
                border: none;
                border-radius: {button_radius}px;
                padding: {button_padding}px {button_padding * 2}px;
            }}
            QPushButton:hover {{
                background-color: #8FB7D6;
                color: #427AA2;
            }}
            QPushButton:pressed {{
                background-color: #A9C5DB;
            }}
        """)
        cancel_shadow = QGraphicsDropShadowEffect()
        cancel_shadow.setBlurRadius(int(16 * self.scroll_scale))
        cancel_shadow.setOffset(0, int(4 * self.scroll_scale))
        cancel_shadow.setColor(QColor(66, 122, 162, 60))
        self.cancel_btn.setGraphicsEffect(cancel_shadow)
        self.cancel_btn.setFixedSize(button_width, button_height)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

    def load_sample_data(self):
        """Örnek katılımcı verilerini yükle"""
        # Ön kayıt, Misafir, 1,2,3,4, Mezun öğrencileri sırasıyla
        sample_data = [
            # Ön kayıt
            ("Ahmet", "Yılmaz", "Ön Kayıt"),
            ("Ayşe", "Demir", "Ön Kayıt"),
            ("Mehmet", "Kaya", "Ön Kayıt"),
            
            # Misafir
            ("Fatma", "Şahin", "Misafir"),
            ("Ali", "Özkan", "Misafir"),
            ("Zeynep", "Arslan", "Misafir"),
            
            # 1. Sınıf
            ("Can", "Yıldız", "1"),
            ("Elif", "Çelik", "1"),
            ("Burak", "Kurt", "1"),
            ("Selin", "Özkan", "1"),
            
            # 2. Sınıf
            ("Deniz", "Arslan", "2"),
            ("Gizem", "Yılmaz", "2"),
            ("Emre", "Demir", "2"),
            ("Merve", "Kaya", "2"),
            
            # 3. Sınıf
            ("Kaan", "Şahin", "3"),
            ("İrem", "Özkan", "3"),
            ("Tolga", "Yıldız", "3"),
            ("Esra", "Çelik", "3"),
            
            # 4. Sınıf
            ("Ozan", "Kurt", "4"),
            ("Seda", "Arslan", "4"),
            ("Berk", "Yılmaz", "4"),
            ("Derya", "Demir", "4"),
            
            # Mezun
            ("Cem", "Kaya", "Mezun"),
            ("Büşra", "Şahin", "Mezun"),
            ("Serkan", "Özkan", "Mezun"),
            ("Hande", "Yıldız", "Mezun")
        ]

        # Tabloyu doldur
        self.katilimci_table.setRowCount(len(sample_data))
        
        for row, (isim, soyisim, sinif) in enumerate(sample_data):
            # İsim
            isim_item = QTableWidgetItem(isim)
            isim_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.katilimci_table.setItem(row, 0, isim_item)
            
            # Soyisim
            soyisim_item = QTableWidgetItem(soyisim)
            soyisim_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.katilimci_table.setItem(row, 1, soyisim_item)
            
            # Sınıf
            sinif_item = QTableWidgetItem(sinif)
            sinif_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.katilimci_table.setItem(row, 2, sinif_item)
            
            # Katılım radio button'ları
            katilim_widget = QWidget()
            katilim_layout = QHBoxLayout(katilim_widget)
            katilim_layout.setContentsMargins(0, 0, 0, 0)
            katilim_layout.setSpacing(10)
            katilim_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Radio button grubu
            if not hasattr(self, 'radio_groups'):
                self.radio_groups = {}
            
            self.radio_groups[row] = QButtonGroup()
            
            # Evet radio button
            evet_radio = QRadioButton("Evet")
            evet_radio.setStyleSheet("""
                QRadioButton {
                    font-family: Sora DemiBold;
                    font-size: 12px;
                    color: #427AA2;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
                QRadioButton::indicator:unchecked {
                    border: 2px solid #A9C5DB;
                    border-radius: 8px;
                    background: white;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #A5BE00;
                    border-radius: 8px;
                    background: #A5BE00;
                }
            """)
            
            # Hayır radio button (varsayılan seçili)
            hayir_radio = QRadioButton("Hayır")
            hayir_radio.setChecked(True)  # Varsayılan olarak seçili
            hayir_radio.setStyleSheet("""
                QRadioButton {
                    font-family: Sora DemiBold;
                    font-size: 12px;
                    color: #427AA2;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
                QRadioButton::indicator:unchecked {
                    border: 2px solid #A9C5DB;
                    border-radius: 8px;
                    background: white;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #A5BE00;
                    border-radius: 8px;
                    background: #A5BE00;
                }
            """)
            
            # Radio button'ları gruba ekle
            self.radio_groups[row].addButton(evet_radio)
            self.radio_groups[row].addButton(hayir_radio)
            
            # Layout'a ekle
            katilim_layout.addWidget(evet_radio)
            katilim_layout.addWidget(hayir_radio)
            
            # Widget'ı tabloya ekle
            self.katilimci_table.setCellWidget(row, 3, katilim_widget)

        # Tablo boyutunu ayarla
        self.katilimci_table.resizeRowsToContents()
        
        # Scroll bar'ı güncelle (sağlık değer gir ekranındaki gibi)
        if hasattr(self, 'scrollbar'):
            try:
                self.scrollbar.setMinimum(self.katilimci_table.verticalScrollBar().minimum())
                self.scrollbar.setMaximum(self.katilimci_table.verticalScrollBar().maximum())
                self.scrollbar.setPageStep(self.katilimci_table.verticalScrollBar().pageStep())
            except:
                pass

    def disari_aktar(self):
        """Dışarı aktar işlemi"""
        QMessageBox.information(self, "Bilgi", "Dışarı aktar işlemi başlatıldı!")

    def get_katilimci_data(self):
        """Katılımcı verilerini döndür"""
        katilimci_list = []
        
        for row in range(self.katilimci_table.rowCount()):
            isim = self.katilimci_table.item(row, 0).text()
            soyisim = self.katilimci_table.item(row, 1).text()
            sinif = self.katilimci_table.item(row, 2).text()
            
            # Radio button durumunu kontrol et
            katilim_widget = self.katilimci_table.cellWidget(row, 3)
            if katilim_widget:
                radio_group = self.radio_groups.get(row)
                if radio_group:
                    checked_button = radio_group.checkedButton()
                    katilim = "Evet" if checked_button and checked_button.text() == "Evet" else "Hayır"
                else:
                    katilim = "Hayır"
            else:
                katilim = "Hayır"
            
            katilimci_list.append({
                'isim': isim,
                'soyisim': soyisim,
                'sinif': sinif,
                'katilim': katilim
            })
        
        return katilimci_list

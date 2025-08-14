import os
import sys
try:
    from PyQt6.QtCore import QLibraryInfo
    plugin_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
except Exception as e:
    print("Qt plugin path ayarlanamadı:", e, file=sys.stderr)

from PyQt6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QAbstractItemView, QWidget, QMessageBox,
                             QGraphicsDropShadowEffect, QSizePolicy, QScrollBar)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from gezi_katilimci_detayi import GeziKatilimciDetayiDialog

class GeziKatilimciEkleDialog(QDialog):
    def __init__(self, parent=None, gezi_data=None):
        super().__init__(parent)
        self.gezi_data = gezi_data or {}
        self.setWindowTitle("Gezi Katılımcı Ekle")
        
        # Responsive boyut hesaplama (sağlık modülündeki gibi)
        base_width, base_height = 1920, 1080
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        self.scroll_scale = min(screen_width / base_width, screen_height / base_height)

        # Dialog boyutları - responsive (sağlık modülündeki gibi)
        dialog_width = int(1200 * self.scroll_scale)
        dialog_height = int(1000 * self.scroll_scale)
        self.setFixedSize(dialog_width, dialog_height)
        
        self.setStyleSheet("background-color: #EBF2FA;")
        
        # Gezi ücreti (varsayılan değer, gerçek uygulamada gezi_data'dan gelecek)
        self.gezi_ucreti = self.gezi_data.get('ucret', 500)  # TL cinsinden
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Responsive margins ve spacing (sağlık modülündeki gibi)
        margin = int(40 * self.scroll_scale)
        spacing = int(20 * self.scroll_scale)
        
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(spacing)

        # Başlık
        title = QLabel(f"Katılımcı Ekle - {self.gezi_data.get('adi', 'Seçili Gezi')}")
        title_font_size = int(22 * self.scroll_scale)
        title.setFont(QFont("Arial", title_font_size, QFont.Weight.DemiBold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(int(18 * self.scroll_scale))

        # Üst kontroller container - ortalanmış (sağlık modülündeki gibi)
        controls_wrapper = QWidget()
        controls_wrapper_layout = QHBoxLayout(controls_wrapper)
        controls_wrapper_layout.setContentsMargins(int(20 * self.scroll_scale), int(20 * self.scroll_scale), int(20 * self.scroll_scale), int(20 * self.scroll_scale))
        
        controls_container = QWidget()
        controls_container.setMaximumWidth(int(900 * self.scroll_scale))
        controls_layout = QHBoxLayout(controls_container)
        controls_layout.setSpacing(int(30 * self.scroll_scale))
        controls_layout.setContentsMargins(int(10 * self.scroll_scale), 0, int(10 * self.scroll_scale), 0)
        
        # Kontrolleri wrapper'a ekle ve ortala (sağlık modülündeki gibi)
        controls_wrapper_layout.addStretch()
        controls_wrapper_layout.addWidget(controls_container)
        controls_wrapper_layout.addStretch()
        
        layout.addWidget(controls_wrapper)
        layout.addSpacing(int(10 * self.scroll_scale))

        # Tablo adı (sağlık modülündeki gibi)
        self.table_title = QLabel("Katılımcı Listesi")
        self.table_title.setFont(QFont("Arial", int(18 * self.scroll_scale), QFont.Weight.Bold))
        self.table_title.setStyleSheet("color: #427AA2; background: transparent; margin-bottom: 2px;")
        self.table_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.table_title)

        # Tablo container (sağlık modülündeki gibi)
        table_container = QWidget()
        table_container.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 15px;
                border: none;
            }
        """)
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(int(15 * self.scroll_scale), int(15 * self.scroll_scale), int(15 * self.scroll_scale), int(15 * self.scroll_scale))

        # Tablo
        self.katilimci_table = QTableWidget()
        self.setup_table()
        
        # Başlangıçta tüm katılımcıları göster
        self.load_all_katilimcilar()
        
        table_layout.addLayout(self.table_and_scroll_layout)
        layout.addWidget(table_container)
        
        layout.addSpacing(int(20 * self.scroll_scale))

        # Alt butonlar (sağlık modülündeki gibi)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(int(15 * self.scroll_scale))
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Responsive button boyutları (sağlık modülündeki gibi)
        button_width = int(170 * self.scroll_scale)
        button_height = int(50 * self.scroll_scale)
        button_font_size = int(14 * self.scroll_scale)
        button_radius = int(8 * self.scroll_scale)
        button_padding = int(12 * self.scroll_scale)

        # Dışarı Aktar butonu
        self.export_btn = QPushButton("Dışarı Aktar")
        self.export_btn.setFont(QFont("Sora ExtraBold", button_font_size, QFont.Weight.DemiBold))
        self.export_btn.setStyleSheet(f"""
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
        export_shadow = QGraphicsDropShadowEffect()
        export_shadow.setBlurRadius(int(16 * self.scroll_scale))
        export_shadow.setOffset(0, int(4 * self.scroll_scale))
        export_shadow.setColor(QColor(66, 122, 162, 60))
        self.export_btn.setGraphicsEffect(export_shadow)
        self.export_btn.setFixedSize(button_width, button_height)
        self.export_btn.clicked.connect(self.export_data)
        button_layout.addWidget(self.export_btn)

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
        self.save_btn.clicked.connect(self.save_data)
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

    def setup_table(self):
        """Tabloyu başlangıç durumuna ayarlar (sağlık modülündeki gibi)"""
        # Tablo sütunları
        self.katilimci_table.setColumnCount(7)
        self.katilimci_table.setHorizontalHeaderLabels([
            "İsim", "Soyisim", "Sınıf", "Katılım Bilgisi", "Katılımcı Sayısı", "Toplam Ücret", "Ödeme Durumu"
        ])
        
        # Tablo styling (dinamik font boyutları)
        header_font_size = int(14 * self.scroll_scale)
        cell_font_size = int(13 * self.scroll_scale)
        
        self.katilimci_table.setFont(QFont("Arial", cell_font_size))
        
        # Tablo stilini ayarla (sağlık modülündeki gibi)
        self.katilimci_table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 2px solid #427AA2;
                border-top-left-radius: 13px;
                border-top-right-radius: 18px;
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
                border-top-right-radius: 15px;
                border-right: none;
            }
        """)
        
        # Sütun genişliklerini dinamik olarak ayarla
        header = self.katilimci_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)  # İsim
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)  # Soyisim
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)  # Sınıf
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)  # Katılım Bilgisi
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)  # Katılımcı Sayısı
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Interactive)  # Toplam Ücret
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)      # Ödeme Durumu (genişletilebilir)
        
        # Dikey başlığı gizle (satır numaraları)
        vertical_header = self.katilimci_table.verticalHeader()
        vertical_header.setVisible(False)
        
        # Tablo scroll bar'larını gizle
        self.katilimci_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.katilimci_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.katilimci_table.verticalScrollBar().setStyleSheet("QScrollBar { width: 0px; }")
        self.katilimci_table.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0px; }")
        
        # Başlangıç sütun genişliklerini ayarla (responsive)
        self.katilimci_table.setColumnWidth(0, int(150 * self.scroll_scale))  # İsim
        self.katilimci_table.setColumnWidth(1, int(150 * self.scroll_scale))  # Soyisim
        self.katilimci_table.setColumnWidth(2, int(120 * self.scroll_scale))  # Sınıf
        self.katilimci_table.setColumnWidth(3, int(150 * self.scroll_scale))  # Katılım Bilgisi
        self.katilimci_table.setColumnWidth(4, int(150 * self.scroll_scale))  # Katılımcı Sayısı
        self.katilimci_table.setColumnWidth(5, int(150 * self.scroll_scale))  # Toplam Ücret
        self.katilimci_table.setColumnWidth(6, int(200 * self.scroll_scale))  # Ödeme Durumu
        
        # Tablo yüksekliğini dinamik yap
        self.katilimci_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Özel scroll bar konteynerleri oluştur (sağlık modülündeki gibi)
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
        
        # Scroll bar ile tabloyu senkronize et (sağlık modülündeki gibi)
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
        
        # Tablo verileri değiştiğinde scroll bar'ı güncelle
        self.katilimci_table.verticalScrollBar().rangeChanged.connect(update_scrollbar)
        
        # Tablo ve scroll bar'ı yan yana yerleştir
        self.table_and_scroll_layout = QHBoxLayout()
        self.table_and_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.table_and_scroll_layout.setSpacing(int(15 * self.scroll_scale))
        self.table_and_scroll_layout.addWidget(self.katilimci_table)
        self.table_and_scroll_layout.addWidget(scroll_container)
        
        # Başlangıçta boş tablo
        self.katilimci_table.setRowCount(0)
        
        # Corner widget'ını kaldır
        self.katilimci_table.setCornerWidget(None)

        # Çift tık fonksiyonunu ekle
        self.katilimci_table.cellDoubleClicked.connect(self.show_katilimci_detay)

        # Tablo ayarları
        self.katilimci_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.katilimci_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.katilimci_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    def load_all_katilimcilar(self):
        """Başlangıçta tüm katılımcıları gösterir"""
        # Örnek katılımcı verileri (sınıf sıralamasına göre)
        katilimcilar = [
            # Ön kayıt öğrencileri
            ("Ahmet", "Yılmaz", "Ön Kayıt", "Aktif", 1, "Ödendi"),
            ("Fatma", "Demir", "Ön Kayıt", "Aktif", 1, "Ödendi"),
            ("Mehmet", "Kaya", "Ön Kayıt", "Pasif", 1, "Bekliyor"),
            
            # Misafir öğrenciler
            ("Ayşe", "Çelik", "Misafir", "Aktif", 1, "Ödendi"),
            ("Ali", "Özkan", "Misafir", "Aktif", 2, "Ödendi"),
            ("Zeynep", "Arslan", "Misafir", "Pasif", 1, "Bekliyor"),
            
            # 1. sınıf öğrencileri
            ("Can", "Yıldız", "1", "Aktif", 1, "Ödendi"),
            ("Deniz", "Korkmaz", "1", "Aktif", 1, "Ödendi"),
            ("Elif", "Şahin", "1", "Aktif", 2, "Ödendi"),
            ("Furkan", "Aydın", "1", "Pasif", 1, "Bekliyor"),
            
            # 2. sınıf öğrencileri
            ("Gizem", "Öztürk", "2", "Aktif", 1, "Ödendi"),
            ("Hakan", "Koç", "2", "Aktif", 1, "Ödendi"),
            ("İrem", "Kurt", "2", "Aktif", 3, "Ödendi"),
            ("Jale", "Özkan", "2", "Pasif", 1, "Bekliyor"),
            
            # 3. sınıf öğrencileri
            ("Kaan", "Erdoğan", "3", "Aktif", 1, "Ödendi"),
            ("Leyla", "Yılmaz", "3", "Aktif", 1, "Ödendi"),
            ("Mert", "Demir", "3", "Aktif", 2, "Ödendi"),
            ("Nur", "Kaya", "3", "Pasif", 1, "Bekliyor"),
            
            # 4. sınıf öğrencileri
            ("Ozan", "Çelik", "4", "Aktif", 1, "Ödendi"),
            ("Pınar", "Özkan", "4", "Aktif", 1, "Ödendi"),
            ("Rıza", "Arslan", "4", "Aktif", 4, "Ödendi"),
            ("Selin", "Yıldız", "4", "Pasif", 1, "Bekliyor"),
            
            # Mezun öğrenciler
            ("Taha", "Korkmaz", "Mezun", "Aktif", 1, "Ödendi"),
            ("Ufuk", "Şahin", "Mezun", "Aktif", 1, "Ödendi"),
            ("Vildan", "Aydın", "Mezun", "Aktif", 2, "Ödendi"),
            ("Yasin", "Öztürk", "Mezun", "Pasif", 1, "Bekliyor"),
        ]

        # Tabloyu doldur
        self.katilimci_table.setRowCount(len(katilimcilar))
        for row, katilimci in enumerate(katilimcilar):
            # Veri yapısı: (isim, soyisim, sinif, katilim_bilgisi, katilimci_sayisi, odeme_durumu)
            isim, soyisim, sinif, katilim_bilgisi, katilimci_sayisi, odeme_durumu = katilimci
            
            # Toplam ücret hesapla (katılımcı sayısı * gezi ücreti)
            toplam_ucret = katilimci_sayisi * self.gezi_ucreti
            
            # Yeni veri yapısı: (isim, soyisim, sinif, katilim_bilgisi, katilimci_sayisi, toplam_ucret, odeme_durumu)
            row_data = [isim, soyisim, sinif, katilim_bilgisi, str(katilimci_sayisi), f"{toplam_ucret} TL", odeme_durumu]
            
            for col, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Katılım bilgisine göre arka plan rengi
                if col == 3:  # Katılım Bilgisi sütunu
                    if val == "Aktif":
                        item.setBackground(QColor("#E8F5E8"))  # Açık yeşil
                    else:
                        item.setBackground(QColor("#FFE8E8"))  # Açık kırmızı
                # Ödeme durumuna göre arka plan rengi
                elif col == 6:  # Ödeme Durumu sütunu
                    if val == "Ödendi":
                        item.setBackground(QColor("#E8F5E8"))  # Açık yeşil
                    else:
                        item.setBackground(QColor("#FFF3CD"))  # Açık sarı (bekliyor)
                else:
                    item.setBackground(Qt.GlobalColor.white)
                
                self.katilimci_table.setItem(row, col, item)
            
            # Alternatif satır renklerini ayarla (sağlık modülündeki gibi)
            if row % 2 == 0:
                for col in range(7):  # 7 sütun
                    item = self.katilimci_table.item(row, col)
                    if item:
                        item.setBackground(QColor("#fafafa"))
            
            # Satır yüksekliğini dinamik ayarla
            self.katilimci_table.setRowHeight(row, int(50 * self.scroll_scale))
        
        # Scroll bar'ı güncelle
        if hasattr(self, 'scrollbar'):
            try:
                self.scrollbar.setMinimum(self.katilimci_table.verticalScrollBar().minimum())
                self.scrollbar.setMaximum(self.katilimci_table.verticalScrollBar().maximum())
                self.scrollbar.setPageStep(self.katilimci_table.verticalScrollBar().pageStep())
            except:
                pass

    def show_katilimci_detay(self, row, column):
        """Katılımcı detay ekranını aç"""
        # Seçili satırdan katılımcı verilerini al
        katilimci_data = {
            'isim': self.katilimci_table.item(row, 0).text(),
            'soyisim': self.katilimci_table.item(row, 1).text(),
            'sinif': self.katilimci_table.item(row, 2).text(),
            'katilim_bilgisi': self.katilimci_table.item(row, 3).text(),
            'katilimci_sayisi': self.katilimci_table.item(row, 4).text(),
            'toplam_ucret': self.katilimci_table.item(row, 5).text(),
            'odeme_durumu': self.katilimci_table.item(row, 6).text()
        }
        
        # Katılımcı detay dialog'unu aç
        dialog = GeziKatilimciDetayiDialog(self, katilimci_data, self.gezi_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Kaydet butonuna basıldıysa verileri al
            detay_data = dialog.get_katilimci_detay_data()
            print(f"Katılımcı detay verileri: {detay_data}")

    def export_data(self):
        """Katılımcı verilerini dışarı aktar"""
        QMessageBox.information(self, "Bilgi", "Katılımcı verileri dışarı aktarıldı!")

    def save_data(self):
        """Katılımcı verilerini kaydet"""
        # Aktif katılımcı sayısını ve toplam ücreti hesapla
        active_count = 0
        total_revenue = 0
        pending_payments = 0
        
        for row in range(self.katilimci_table.rowCount()):
            katilim_item = self.katilimci_table.item(row, 3)  # Katılım Bilgisi sütunu
            if katilim_item and katilim_item.text() == "Aktif":
                katilimci_sayisi_item = self.katilimci_table.item(row, 4)  # Katılımcı Sayısı sütunu
                odeme_durumu_item = self.katilimci_table.item(row, 6)  # Ödeme Durumu sütunu
                
                if katilimci_sayisi_item:
                    try:
                        katilimci_sayisi = int(katilimci_sayisi_item.text())
                        active_count += katilimci_sayisi
                        
                        # Toplam ücret hesapla
                        toplam_ucret = katilimci_sayisi * self.gezi_ucreti
                        
                        # Ödeme durumuna göre gelir hesapla
                        if odeme_durumu_item and odeme_durumu_item.text() == "Ödendi":
                            total_revenue += toplam_ucret
                        else:
                            pending_payments += toplam_ucret
                            
                    except ValueError:
                        active_count += 1

        message = f"Katılımcı verileri kaydedildi!\n\n"
        message += f"Toplam aktif katılımcı sayısı: {active_count}\n"
        message += f"Toplam gelir (ödendi): {total_revenue} TL\n"
        message += f"Bekleyen ödemeler: {pending_payments} TL"
        
        QMessageBox.information(self, "Başarılı", message)
        self.accept()

    def get_katilimci_data(self):
        """Katılımcı verilerini döndür"""
        active_count = 0
        total_revenue = 0
        pending_payments = 0
        
        for row in range(self.katilimci_table.rowCount()):
            katilim_item = self.katilimci_table.item(row, 3)
            if katilim_item and katilim_item.text() == "Aktif":
                katilimci_sayisi_item = self.katilimci_table.item(row, 4)
                odeme_durumu_item = self.katilimci_table.item(row, 6)
                
                if katilimci_sayisi_item:
                    try:
                        katilimci_sayisi = int(katilimci_sayisi_item.text())
                        active_count += katilimci_sayisi
                        
                        # Toplam ücret hesapla
                        toplam_ucret = katilimci_sayisi * self.gezi_ucreti
                        
                        # Ödeme durumuna göre gelir hesapla
                        if odeme_durumu_item and odeme_durumu_item.text() == "Ödendi":
                            total_revenue += toplam_ucret
                        else:
                            pending_payments += toplam_ucret
                            
                    except ValueError:
                        active_count += 1
        
        return {
            'gezi_id': self.gezi_data.get('id', ''),
            'gezi_adi': self.gezi_data.get('adi', ''),
            'toplam_katilimci': str(active_count),
            'toplam_gelir': str(total_revenue),
            'bekleyen_odemeler': str(pending_payments),
            'gezi_ucreti': str(self.gezi_ucreti)
        } 
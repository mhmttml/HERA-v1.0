import os
import sys
try:
    from PyQt6.QtCore import QLibraryInfo
    plugin_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
except Exception as e:
    print("Qt plugin path ayarlanamadı:", e, file=sys.stderr)
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QScrollBar, QAbstractScrollArea, QAbstractItemView, QSizePolicy, QDialog, QComboBox
from PyQt6.QtGui import QFont, QPixmap, QColor, QPainter
from PyQt6.QtCore import Qt, QDateTime, QTimer
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from gunce_ekle import GunceEkleDialog

class ShadowLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.shadow_offset = (3, 3, 5)
        self.shadow_color = QColor(0, 0, 0, 80)
        self.text_color = QColor("#EBF2FA")
        self.setFont(QFont("Arial", 20, QFont.Weight.DemiBold))
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font())
        # Draw shadow
        painter.setPen(self.shadow_color)
        painter.drawText(
            self.shadow_offset[0], self.shadow_offset[1] + self.fontMetrics().ascent(),
            self.text()
        )
        # Draw main text
        painter.setPen(self.text_color)
        painter.drawText(
            0, self.fontMetrics().ascent(),
            self.text()
        )

class GunceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Günce Modülü")
        self.setStyleSheet("background-color: #EBF2FA;")
        self.setMinimumSize(1000, 700)  # Minimum pencere boyutu
        
        # Responsive scaling için screen boyutunu hesapla
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        base_width = 1920
        base_height = 1080
        self.scroll_scale = min(screen_width / base_width, screen_height / base_height)
        self.scroll_scale = max(0.7, min(1.5, self.scroll_scale))
        
        self.init_ui()
        self.showMaximized()

    def update_table_column_widths(self):
        if not hasattr(self, 'gunce_table') or not hasattr(self, 'right_content'):
            return
        right_panel_width = max(1200, self.right_content.width())
        column_ratios = [0.08, 0.13, 0.13, 0.10, 0.13, 0.13, 0.13, 0.09, 0.08]
        header_labels = [
            "Günce ID", "İsim", "Soyisim", "Sınıf", "Günce Grubu",
            "Günce Tipi", "Açıklama", "Belge Durumu", "İşlem Tarihi"
        ]
        fm = self.gunce_table.fontMetrics()
        for col, ratio in enumerate(column_ratios):
            min_width = fm.horizontalAdvance(header_labels[col]) + 40
            proportional_width = int(right_panel_width * ratio)
            final_width = max(min_width, proportional_width)
            self.gunce_table.setColumnWidth(col, final_width)

    def resizeEvent(self, event):
        self.update_table_column_widths()
        super().resizeEvent(event)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar
        top_bar_widget = self._create_top_bar()
        main_layout.addWidget(top_bar_widget)

        # Alt kısım: yatayda sol panel ve sağ içerik
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(2)

        # Sol panel (butonlar) - sabit genişlik, spacing 30px, üstte spacing 80px
        left_panel = QWidget()
        left_panel.setFixedWidth(300)
        left_panel.setStyleSheet("background-color: #EBF2FA;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(30)
        left_layout.addSpacing(60)
        # 1. Ana Sayfa
        btn_anasayfa = QPushButton("Ana Sayfa")
        btn_anasayfa.setFixedSize(260, 50)
        btn_anasayfa.setFont(QFont("Arial", 15, QFont.Weight.DemiBold))
        btn_anasayfa.setStyleSheet("""
            QPushButton {
                background-color: #A9C5DB;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #8FB7D6;
                color: #427AA2;
            }
            QPushButton:pressed {
                background-color: #A9C5DB;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(66, 122, 162, 60))
        btn_anasayfa.setGraphicsEffect(shadow)
        btn_anasayfa.clicked.connect(lambda: print("Ana Sayfa butonuna tıklandı."))
        left_layout.addWidget(btn_anasayfa)
        # 2. Öğrenim Durumu Seç ComboBox
        self.ogrenim_durumu_combo = QComboBox()
        self.ogrenim_durumu_combo.addItem("Öğrenim Durumu")
        self.ogrenim_durumu_combo.addItem("Ön Kayıt")
        self.ogrenim_durumu_combo.addItem("Misafir")
        self.ogrenim_durumu_combo.addItem("1. Sınıf")
        self.ogrenim_durumu_combo.addItem("2. Sınıf")
        self.ogrenim_durumu_combo.addItem("3. Sınıf")
        self.ogrenim_durumu_combo.addItem("4. Sınıf")
        self.ogrenim_durumu_combo.addItem("Dondurulmuş")
        self.ogrenim_durumu_combo.addItem("Mezun")
        self.ogrenim_durumu_combo.addItem("Vefat")
        self.ogrenim_durumu_combo.setCurrentText("Öğrenim Durumu Seç")
        self.ogrenim_durumu_combo.setStyleSheet('''
            QComboBox {
                background-color: #A9C5DB;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 0px 15px;
                text-align: center;
            }
            QComboBox:hover {
                background-color: #8FB7D6;
                color: #427AA2;
            }
            QComboBox:focus {
                background-color: #8FB7D6;
                color: #427AA2;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(ucgen.png);
                width: 30px;
                height: 30px;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #A9C5DB;
                border: none;
                border-radius: 8px;
                selection-background-color: #8FB7D6;
                selection-color: #427AA2;
                text-align: center;
            }
        ''')
        self.ogrenim_durumu_combo.setMinimumSize(200, 50)
        self.ogrenim_durumu_combo.setMaximumSize(300, 50)
        self.ogrenim_durumu_combo.setFont(QFont("Arial", 15, QFont.Weight.DemiBold))
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(16)
        shadow2.setOffset(0, 4)
        shadow2.setColor(QColor(66, 122, 162, 60))
        self.ogrenim_durumu_combo.setGraphicsEffect(shadow2)
        left_layout.addWidget(self.ogrenim_durumu_combo)
        # 3. Öğrenci Seç ComboBox
        self.ogrenci_combo = QComboBox()
        self.ogrenci_combo.addItem("Öğrenci Seç")
        self.ogrenci_combo.setCurrentText("Öğrenci Seç")
        self.ogrenci_combo.setStyleSheet('''
            QComboBox {
                background-color: #A9C5DB;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 0px 15px;
                text-align: center;
            }
            QComboBox:hover {
                background-color: #8FB7D6;
                color: #427AA2;
            }
            QComboBox:focus {
                background-color: #8FB7D6;
                color: #427AA2;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(ucgen.png);
                width: 30px;
                height: 30px;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #A9C5DB;
                border: none;
                border-radius: 8px;
                selection-background-color: #8FB7D6;
                selection-color: #427AA2;
                text-align: center;
            }
        ''')
        self.ogrenci_combo.setMinimumSize(200, 50)
        self.ogrenci_combo.setMaximumSize(300, 50)
        self.ogrenci_combo.setFont(QFont("Arial", 15, QFont.Weight.DemiBold))
        shadow3 = QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(16)
        shadow3.setOffset(0, 4)
        shadow3.setColor(QColor(66, 122, 162, 60))
        self.ogrenci_combo.setGraphicsEffect(shadow3)
        left_layout.addWidget(self.ogrenci_combo)
        self.ogrenim_durumu_combo.currentTextChanged.connect(self.update_ogrenci_list)
        # 4. Günceyi Getir
        btn_getir = QPushButton("Günceyi Getir")
        btn_getir.setFixedSize(260, 50)
        btn_getir.setFont(QFont("Arial", 15, QFont.Weight.DemiBold))
        btn_getir.setStyleSheet(btn_anasayfa.styleSheet())
        shadow4 = QGraphicsDropShadowEffect()
        shadow4.setBlurRadius(16)
        shadow4.setOffset(0, 4)
        shadow4.setColor(QColor(66, 122, 162, 60))
        btn_getir.setGraphicsEffect(shadow4)
        btn_getir.clicked.connect(self.get_ogrenci_gunce)
        left_layout.addWidget(btn_getir)
        # 5. Günce (Ekle)
        btn_ekle = QPushButton("Günce")
        btn_ekle.setFixedSize(260, 50)
        btn_ekle.setFont(QFont("Arial", 15, QFont.Weight.DemiBold))
        btn_ekle.setStyleSheet(btn_anasayfa.styleSheet())
        shadow5 = QGraphicsDropShadowEffect()
        shadow5.setBlurRadius(16)
        shadow5.setOffset(0, 4)
        shadow5.setColor(QColor(66, 122, 162, 60))
        btn_ekle.setGraphicsEffect(shadow5)
        btn_ekle.clicked.connect(self.show_gunce_ekle)
        left_layout.addWidget(btn_ekle)
        # 6. Tüm Liste
        btn_tum = QPushButton("Tüm Liste")
        btn_tum.setFixedSize(260, 50)
        btn_tum.setFont(QFont("Arial", 15, QFont.Weight.DemiBold))
        btn_tum.setStyleSheet(btn_anasayfa.styleSheet())
        shadow6 = QGraphicsDropShadowEffect()
        shadow6.setBlurRadius(16)
        shadow6.setOffset(0, 4)
        shadow6.setColor(QColor(66, 122, 162, 60))
        btn_tum.setGraphicsEffect(shadow6)
        btn_tum.clicked.connect(self.show_tum_liste)
        left_layout.addWidget(btn_tum)
        # 7. Rapor Seç (ComboBox)
        rapor_combo = QComboBox()
        rapor_combo.setMinimumSize(200, 50)
        rapor_combo.setMaximumSize(300, 50)
        rapor_combo.setFont(QFont("Arial", 15, QFont.Weight.DemiBold))
        rapor_combo.addItems(["Rapor Seç", "Aylık Rapor", "Öğrenci Raporu", "Genel Rapor"])
        rapor_combo.setStyleSheet('''
            QComboBox {
                background-color: #A9C5DB;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 0px 15px;
                text-align: center;
            }
            QComboBox:focus, QComboBox:hover {
                background-color: #8FB7D6;
                color: #427AA2;
            }
            QComboBox::down-arrow {
                image: url(ucgen.png);
                width: 40px;
                height: 40px;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
                width: 40px;
            }
            QComboBox QAbstractItemView {
                text-align: center;
            }
        ''')
        shadow7 = QGraphicsDropShadowEffect()
        shadow7.setBlurRadius(16)
        shadow7.setOffset(0, 4)
        shadow7.setColor(QColor(66, 122, 162, 60))
        rapor_combo.setGraphicsEffect(shadow7)
        left_layout.addWidget(rapor_combo)
        # 8. Rapor Getir
        btn_rapor = QPushButton("Rapor Getir")
        btn_rapor.setFixedSize(260, 50)
        btn_rapor.setFont(QFont("Arial", 15, QFont.Weight.DemiBold))
        btn_rapor.setStyleSheet(btn_anasayfa.styleSheet())
        shadow8 = QGraphicsDropShadowEffect()
        shadow8.setBlurRadius(16)
        shadow8.setOffset(0, 4)
        shadow8.setColor(QColor(66, 122, 162, 60))
        btn_rapor.setGraphicsEffect(shadow8)
        btn_rapor.clicked.connect(lambda: print("Rapor Getir butonuna tıklandı."))
        left_layout.addWidget(btn_rapor)
        # 9. Dışarı Aktar
        btn_disari = QPushButton("Dışarı Aktar")
        btn_disari.setFixedSize(260, 50)
        btn_disari.setFont(QFont("Arial", 15, QFont.Weight.DemiBold))
        btn_disari.setStyleSheet(btn_anasayfa.styleSheet())
        shadow9 = QGraphicsDropShadowEffect()
        shadow9.setBlurRadius(16)
        shadow9.setOffset(0, 4)
        shadow9.setColor(QColor(66, 122, 162, 60))
        btn_disari.setGraphicsEffect(shadow9)
        btn_disari.clicked.connect(lambda: print("Dışarı Aktar butonuna tıklandı."))
        left_layout.addWidget(btn_disari)
        left_layout.addStretch(1)

        # Sağ içerik (veri tablosu) - responsive
        self.right_content = QWidget()
        self.right_content.setStyleSheet("background-color: #EBF2FA;")
        self.right_content.setMinimumWidth(1200)
        right_layout = QVBoxLayout(self.right_content)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(0)
        # addSpacing(80) kaldırıldı, başlık ve tablo doğrudan üstten başlıyor
        self.table_title_label = QLabel("Günce Listesi")
        self.table_title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.table_title_label.setStyleSheet("""
            QLabel {
                color: #427AA2;
                background-color: #EBF2FA;
                padding: 15px;
                border: none;
                margin: 0px;
            }
        """)
        self.table_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.table_title_label)

        # Günce veri tablosu - belirtilen sütunlarla
        self.gunce_table = QTableWidget()
        self.gunce_table.setColumnCount(9)
        self.gunce_table.setHorizontalHeaderLabels([
            "Günce ID", "İsim", "Soyisim", "Sınıf", "Günce Grubu", 
            "Günce Tipi", "Açıklama", "Belge Durumu", "İşlem Tarihi"
        ])
        
        # Örnek veri - görseldeki verilere benzer şekilde
        gunce_veriler = [
            ("1", "Naciye", "Görür", "1. Sınıf", "Genel", "Resmi Evrak", "500tl", "Belge Mevcut", "19 Nis 2025"),
            ("2", "Zafer", "Yetişir", "2. Sınıf", "Sağlık", "Genel Bilgi", "kızı doğum yaptı", "Belge Bulunmuyor", "21 Mar 2025"),
            ("3", "Tahir", "Sabuncuoğlu", "3. Sınıf", "Eğitim", "Sağlık Belgesi", "500tl", "Belge Bulunmuyor", ""),
            ("4", "Necla", "Demir", "1. Sınıf", "Genel", "Genel Bilgi", "", "Belge Bulunmuyor", ""),
            ("5", "Ayşe", "Temiz", "2. Sınıf", "Sağlık", "Resmi Evrak", "", "Belge Bulunmuyor", ""),
            ("6", "Kazım", "Al", "3. Sınıf", "Eğitim", "Sağlık Belgesi", "", "Belge Bulunmuyor", ""),
            ("7", "Hatice", "Dur", "1. Sınıf", "Genel", "Genel Bilgi", "", "Belge Bulunmuyor", ""),
            ("8", "Hasan", "Keskin", "2. Sınıf", "Sağlık", "Resmi Evrak", "", "Belge Bulunmuyor", ""),
            ("9", "Durmuş", "Duran", "3. Sınıf", "Eğitim", "Sağlık Belgesi", "", "Belge Bulunmuyor", ""),
            ("10", "Fatih", "Kel", "1. Sınıf", "Genel", "Genel Bilgi", "", "Belge Bulunmuyor", ""),
            ("11", "Kamuran", "Akgün", "2. Sınıf", "Sağlık", "Resmi Evrak", "", "Belge Bulunmuyor", ""),
            ("12", "Ahmet", "Baklavacı", "3. Sınıf", "Eğitim", "Sağlık Belgesi", "", "Belge Bulunmuyor", ""),
        ]
        
        # Tabloyu doldur
        self.gunce_table.setRowCount(len(gunce_veriler))
        for row, veri in enumerate(gunce_veriler):
            for col, val in enumerate(veri):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Satır renklendirme (alternatif satırlar)
                if row % 2 == 0:
                    item.setBackground(QColor("#F8F9FA"))  # Açık gri
                else:
                    item.setBackground(Qt.GlobalColor.white)
                
                item.setForeground(Qt.GlobalColor.black)
                self.gunce_table.setItem(row, col, item)
        
        # Tablo ayarları
        self.gunce_table.resizeColumnsToContents()
        self.gunce_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.gunce_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Hücre düzenlemeyi devre dışı bırak
        self.gunce_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Satır seçimini etkinleştir (çift tıklama için)
        self.gunce_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.gunce_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # Çift tıklama olayını bağla
        self.gunce_table.cellDoubleClicked.connect(self.show_gunce_detay)
        
        # Sütun genişliklerini ayarla
        header_labels = [
            "Günce ID", "İsim", "Soyisim", "Sınıf", "Günce Grubu", 
            "Günce Tipi", "Açıklama", "Belge Durumu", "İşlem Tarihi"
        ]
        fm = self.gunce_table.fontMetrics()
        for col, label in enumerate(header_labels):
            max_width = fm.horizontalAdvance(label)
            for row in range(self.gunce_table.rowCount()):
                item = self.gunce_table.item(row, col)
                if item:
                    content_width = fm.horizontalAdvance(item.text())
                    if content_width > max_width:
                        max_width = content_width
            self.gunce_table.setColumnWidth(col, max_width + 60)
        
        # Tablo scroll bar'larını gizle
        self.gunce_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.gunce_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.gunce_table.verticalScrollBar().setStyleSheet("QScrollBar { width: 0px; }")
        self.gunce_table.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0px; }")
        
        # Tablo border ve header stilini güncelle
        self.gunce_table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #427AA2;
                border-radius: 8px;
                background-color: white;
            }
        """)
        self.gunce_table.horizontalHeader().setStyleSheet('''
            QHeaderView::section {
                background-color: #427AA2;
                color: #EBF2FA;
                font-weight: bold;
                font-size: 15px;
                border: none;
                border-right: 1px solid #EBF2FA;
                height: 36px;
            }
        ''')
        self.gunce_table.verticalHeader().setVisible(False)
        
        # Responsive scroll bar boyutları
        scroll_width = int(30 * self.scroll_scale)
        scroll_radius = int(10 * self.scroll_scale)
        handle_radius = int(10 * self.scroll_scale)
        handle_min_height = int(90 * self.scroll_scale)
        handle_margin = int(5 * self.scroll_scale)
        
        # Dikey scroll bar konteyneri
        gunce_scroll_container = QWidget()
        gunce_scroll_container.setFixedWidth(scroll_width)
        gunce_scroll_container.setFixedHeight(self.gunce_table.height())
        gunce_scroll_layout = QVBoxLayout(gunce_scroll_container)
        gunce_scroll_layout.setContentsMargins(0, 0, 0, 0)
        gunce_scroll_layout.setSpacing(0)
        gunce_scrollbar = QScrollBar(Qt.Orientation.Vertical)
        gunce_scrollbar.setStyleSheet(f'''
            QScrollBar:vertical {{
                background: rgba(66,122,162,0.5);
                border-radius: {scroll_radius}px;
                width: {scroll_width}px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: white;
                border-radius: {handle_radius}px;
                min-width: {int(20 * self.scroll_scale)}px;
                min-height: {handle_min_height}px;
                max-width: {int(20 * self.scroll_scale)}px;
                max-height: {handle_min_height}px;
                width: {int(20 * self.scroll_scale)}px;
                height: {handle_min_height}px;
                margin-left: {handle_margin}px;
                margin-right: {handle_margin}px;
                margin-top: 6px;
                margin-bottom: 6px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
                subcontrol-origin: margin;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        ''')
        gunce_scroll_layout.addWidget(gunce_scrollbar)
        def update_scroll_container_height():
            gunce_scroll_container.setFixedHeight(self.gunce_table.height())
        self.gunce_table.resizeEvent = lambda event: update_scroll_container_height()
        gunce_scrollbar.setMinimum(self.gunce_table.verticalScrollBar().minimum())
        gunce_scrollbar.setMaximum(self.gunce_table.verticalScrollBar().maximum())
        gunce_scrollbar.setPageStep(self.gunce_table.verticalScrollBar().pageStep())
        gunce_scrollbar.setSingleStep(self.gunce_table.verticalScrollBar().singleStep())
        gunce_scrollbar.setValue(self.gunce_table.verticalScrollBar().value())
        gunce_scrollbar.valueChanged.connect(self.gunce_table.verticalScrollBar().setValue)
        self.gunce_table.verticalScrollBar().valueChanged.connect(gunce_scrollbar.setValue)

        # Yatay scroll bar
        hscroll_height = int(30 * self.scroll_scale)
        hscroll_radius = int(15 * self.scroll_scale)
        hhandle_radius = int(10 * self.scroll_scale)
        hhandle_min_width = int(90 * self.scroll_scale)
        hhandle_height = int(20 * self.scroll_scale)
        hhandle_margin = int(5 * self.scroll_scale)
        gunce_hscroll_container = QWidget()
        gunce_hscroll_container.setFixedHeight(hscroll_height)
        gunce_hscroll_layout = QHBoxLayout(gunce_hscroll_container)
        gunce_hscroll_layout.setContentsMargins(0, 0, 0, 0)
        gunce_hscroll_layout.setSpacing(0)
        gunce_hscrollbar = QScrollBar(Qt.Orientation.Horizontal)
        gunce_hscrollbar.setStyleSheet(f'''
            QScrollBar:horizontal {{
                background: rgba(66,122,162,0.5);
                border-radius: {hscroll_radius}px;
                height: {hscroll_height}px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: white;
                border-radius: {hhandle_radius}px;
                min-height: {hhandle_height}px;
                min-width: {hhandle_min_width}px;
                max-height: {hhandle_height}px;
                max-width: {hhandle_min_width}px;
                height: {hhandle_height}px;
                width: {hhandle_min_width}px;
                margin-top: {hhandle_margin}px;
                margin-bottom: {hhandle_margin}px;
                margin-left: 6px;
                margin-right: 6px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
                subcontrol-origin: margin;
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
        ''')
        gunce_hscroll_layout.addWidget(gunce_hscrollbar)
        gunce_hscrollbar.setMinimum(self.gunce_table.horizontalScrollBar().minimum())
        gunce_hscrollbar.setMaximum(self.gunce_table.horizontalScrollBar().maximum())
        gunce_hscrollbar.setPageStep(self.gunce_table.horizontalScrollBar().pageStep())
        gunce_hscrollbar.setSingleStep(self.gunce_table.horizontalScrollBar().singleStep())
        gunce_hscrollbar.setValue(self.gunce_table.horizontalScrollBar().value())
        gunce_hscrollbar.valueChanged.connect(self.gunce_table.horizontalScrollBar().setValue)
        self.gunce_table.horizontalScrollBar().valueChanged.connect(gunce_hscrollbar.setValue)
        def update_hscrollbar_range(minimum, maximum):
            gunce_hscrollbar.setMinimum(minimum)
            gunce_hscrollbar.setMaximum(maximum)
            gunce_hscrollbar.setPageStep(self.gunce_table.horizontalScrollBar().pageStep())
            gunce_hscrollbar.setSingleStep(self.gunce_table.horizontalScrollBar().singleStep())
        self.gunce_table.horizontalScrollBar().rangeChanged.connect(update_hscrollbar_range)

        # Tablo ve scroll barları yerleştir
        gunce_table_and_scroll = QWidget()
        gunce_table_and_scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        gunce_table_and_scroll_layout = QVBoxLayout(gunce_table_and_scroll)
        gunce_table_and_scroll_layout.setContentsMargins(0, 0, 0, 0)
        gunce_table_and_scroll_layout.setSpacing(0)
        gunce_table_and_scroll_layout.addWidget(self.gunce_table)
        gunce_table_and_scroll_layout.addSpacing(20)
        gunce_table_and_scroll_layout.addWidget(gunce_hscroll_container)

        # Tablo için margin widget
        table_margin_widget = QWidget()
        table_margin_widget.setStyleSheet("background-color: #EBF2FA;")
        table_margin_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table_margin_layout = QHBoxLayout(table_margin_widget)
        table_margin_layout.setContentsMargins(0, 0, 0, 0)  # Tüm marginleri kaldır
        table_margin_layout.addWidget(gunce_table_and_scroll, 1)
        table_margin_layout.addSpacing(10)
        table_margin_layout.addWidget(gunce_scroll_container, 0, Qt.AlignmentFlag.AlignTop)
        right_layout.addWidget(table_margin_widget)

        # Layout'ları birleştir
        bottom_layout.addWidget(left_panel)
        bottom_layout.addWidget(self.right_content)
        main_layout.addLayout(bottom_layout)

        # Dinamik minimum pencere boyutu: sol panel sabit genişlik + sağ içerik minimumu
        try:
            left_panel_min_w = 300
            right_min_w = self.right_content.minimumWidth() if self.right_content.minimumWidth() > 0 else 1200
            total_min_w = left_panel_min_w + bottom_layout.spacing() + right_min_w
            top_h = 80
            right_content_min_h = max(self.gunce_table.minimumHeight() + 160, self.right_content.sizeHint().height())
            total_min_h = top_h + right_content_min_h
            self.setMinimumSize(total_min_w, total_min_h)
        except Exception:
            pass

    def _create_top_bar(self):
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_bar.setSpacing(0)
        top_widget = QWidget()
        top_widget.setStyleSheet("background-color: #427AA2;")
        top_widget.setFixedHeight(80)
        top_widget.setLayout(top_bar)

        # Logo
        logo = QLabel()
        logo.setFixedSize(64, 64)
        logo.setStyleSheet("""
            background: white;
            border-radius: 32px;
            border: 2px solid #427AA2;
        """)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setContentsMargins(0, 0, 0, 0)
        import os
        if os.path.exists("2.png"):
            logo.setPixmap(QPixmap("2.png").scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        # Başlık
        title = ShadowLabel("HEALTHY ELDERS' RECORDS ASSISTANT - GÜNCE MODÜLÜ")
        title.setStyleSheet("letter-spacing: 1px; vertical-align: middle; background: transparent;")

        # Kullanıcı kutusu
        user_container = QWidget()
        user_container_layout = QHBoxLayout(user_container)
        user_container_layout.setContentsMargins(0, 0, 0, 0)
        user_container_layout.setSpacing(0)
        user_container.setStyleSheet(
            "background: rgba(235,242,250,0.5);"
            "border-top-right-radius: 14px;"
            "border-bottom-right-radius: 14px;"
            "border-top-left-radius: 14px;"
            "border-bottom-left-radius: 14px;"
        )
        icon_bg = QLabel()
        icon_bg.setFixedSize(48, 48)
        icon_bg.setStyleSheet(
            "background: rgba(66,122,162,0.18);"
            "border-radius: 0px;"
        )
        user_icon = QLabel(icon_bg)
        user_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_icon.setGeometry(0, 0, 48, 48)
        user_label = QLabel("")
        user_label.setStyleSheet(
            "color: #EBF2FA;"
            "font-weight: bold;"
            "font-size: 20px;"
            "background: transparent;"
            "padding: 0 32px;"
            "min-width: 130px;"
            "min-height: 48px;"
        )
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_container_layout.addWidget(icon_bg)
        user_container_layout.addWidget(user_label)

        # Top bar hizalama
        top_bar.addSpacing(32)
        top_bar.addWidget(logo, alignment=Qt.AlignmentFlag.AlignVCenter)
        top_bar.addSpacing(32)
        top_bar.addWidget(title, alignment=Qt.AlignmentFlag.AlignVCenter)
        top_bar.addStretch(1)
        top_bar.addSpacing(80)
        top_bar.addWidget(user_container, alignment=Qt.AlignmentFlag.AlignVCenter)
        top_bar.addSpacing(30)

        return top_widget

    def update_ogrenci_list(self):
        """Öğrenim durumu değiştiğinde öğrenci listesini günceller"""
        selected_durum = self.ogrenim_durumu_combo.currentText()
        self.ogrenci_combo.clear()
        self.ogrenci_combo.addItem("Öğrenci Seç")
        
        if selected_durum == "Öğrenim Durumu Seç":
            return
            
        # Öğrenim durumuna göre öğrenci listesi
        ogrenci_verileri = {
            "Ön Kayıt": [
                ("ÖN001", "Ahmet", "Yılmaz"),
                ("ÖN002", "Fatma", "Demir"),
                ("ÖN003", "Mehmet", "Kaya"),
            ],
            "Misafir": [
                ("M001", "Zeynep", "Çelik"),
                ("M002", "Ali", "Şahin"),
                ("M003", "Hatice", "Özkan"),
            ],
            "1. Sınıf": [
                ("101", "Naciye", "Görür"),
                ("102", "Zafer", "Yetişir"),
                ("103", "Tahir", "Sabuncuoğlu"),
                ("104", "Necla", "Demir"),
            ],
            "2. Sınıf": [
                ("201", "Ayşe", "Temiz"),
                ("202", "Kazım", "Al"),
                ("203", "Hatice", "Dur"),
                ("204", "Hasan", "Keskin"),
            ],
            "3. Sınıf": [
                ("301", "Durmuş", "Duran"),
                ("302", "Fatih", "Kel"),
                ("303", "Kamuran", "Akgün"),
                ("304", "Ahmet", "Baklavacı"),
            ],
            "4. Sınıf": [
                ("401", "Elif", "Arslan"),
                ("402", "Mustafa", "Koç"),
                ("403", "Zehra", "Yıldız"),
            ],
            "Dondurulmuş": [
                ("D001", "Kemal", "Özkan"),
                ("D002", "Sultan", "Demir"),
            ],
            "Mezun": [
                ("MZ001", "Hüseyin", "Kaya"),
                ("MZ002", "Meryem", "Çelik"),
                ("MZ003", "Osman", "Şahin"),
            ],
            "Vefat": [
                ("V001", "Hasan", "Yılmaz"),
                ("V002", "Fatma", "Demir"),
            ]
        }
        
        if selected_durum in ogrenci_verileri:
            for ogrenci_id, isim, soyisim in ogrenci_verileri[selected_durum]:
                self.ogrenci_combo.addItem(f"{isim} {soyisim} ({ogrenci_id})")

    def get_ogrenci_gunce(self):
        """Seçili öğrencinin günce geçmişini getirir"""
        selected_ogrenci = self.ogrenci_combo.currentText()
        
        if selected_ogrenci == "Öğrenci Seç":
            return
            
        # Öğrenci bilgilerini parçala
        ogrenci_parts = selected_ogrenci.split(" (")
        if len(ogrenci_parts) < 2:
            return
            
        isim_soyisim = ogrenci_parts[0]
        ogrenci_id = ogrenci_parts[1].rstrip(")")
        
        # Örnek günce verileri - gerçek uygulamada veritabanından gelecek
        gunce_verileri = {
            "101": [  # Naciye Görür
                ("Genel", "Resmi Evrak", "500tl", "Belge Mevcut", "19 Nis 2025"),
                ("Sağlık", "Sağlık Belgesi", "Kontrol randevusu", "Belge Bulunmuyor", "15 Nis 2025"),
                ("Eğitim", "Genel Bilgi", "Sınıf değişikliği", "Belge Bulunmuyor", "10 Nis 2025"),
            ],
            "102": [  # Zafer Yetişir
                ("Sağlık", "Genel Bilgi", "kızı doğum yaptı", "Belge Bulunmuyor", "21 Mar 2025"),
                ("Genel", "Resmi Evrak", "Adres değişikliği", "Belge Mevcut", "18 Mar 2025"),
                ("Eğitim", "Genel Bilgi", "Devamsızlık bildirimi", "Belge Bulunmuyor", "15 Mar 2025"),
            ],
            "103": [  # Tahir Sabuncuoğlu
                ("Eğitim", "Sağlık Belgesi", "500tl", "Belge Bulunmuyor", "25 Mar 2025"),
                ("Genel", "Resmi Evrak", "İletişim bilgisi güncelleme", "Belge Bulunmuyor", "20 Mar 2025"),
            ],
            "201": [  # Ayşe Temiz
                ("Sağlık", "Resmi Evrak", "Sağlık raporu", "Belge Mevcut", "22 Mar 2025"),
                ("Genel", "Genel Bilgi", "Telefon numarası değişikliği", "Belge Bulunmuyor", "18 Mar 2025"),
            ],
            "202": [  # Kazım Al
                ("Eğitim", "Sağlık Belgesi", "Doktor raporu", "Belge Bulunmuyor", "24 Mar 2025"),
                ("Genel", "Resmi Evrak", "Kimlik fotokopisi", "Belge Mevcut", "20 Mar 2025"),
            ],
            "301": [  # Durmuş Duran
                ("Genel", "Resmi Evrak", "Adres belgesi", "Belge Mevcut", "23 Mar 2025"),
                ("Sağlık", "Genel Bilgi", "İlaç değişikliği", "Belge Bulunmuyor", "19 Mar 2025"),
            ],
        }
        
        # Tabloyu temizle ve yeni verileri yükle
        self.gunce_table.setRowCount(0)
        
        if ogrenci_id in gunce_verileri:
            gunce_listesi = gunce_verileri[ogrenci_id]
            self.gunce_table.setRowCount(len(gunce_listesi))
            
            for row, (gunce_grubu, gunce_tipi, aciklama, belge_durumu, islem_tarihi) in enumerate(gunce_listesi):
                # Günce ID
                item_id = QTableWidgetItem(str(row + 1))
                item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.gunce_table.setItem(row, 0, item_id)
                
                # İsim ve Soyisim
                isim_parts = isim_soyisim.split()
                if len(isim_parts) >= 2:
                    item_isim = QTableWidgetItem(isim_parts[0])
                    item_soyisim = QTableWidgetItem(isim_parts[1])
                else:
                    item_isim = QTableWidgetItem(isim_soyisim)
                    item_soyisim = QTableWidgetItem("")
                
                item_isim.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item_soyisim.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.gunce_table.setItem(row, 1, item_isim)
                self.gunce_table.setItem(row, 2, item_soyisim)
                
                # Sınıf bilgisi
                selected_durum = self.ogrenim_durumu_combo.currentText()
                item_sinif = QTableWidgetItem(selected_durum)
                item_sinif.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.gunce_table.setItem(row, 3, item_sinif)
                
                # Günce bilgileri
                item_grubu = QTableWidgetItem(gunce_grubu)
                item_tipi = QTableWidgetItem(gunce_tipi)
                item_aciklama = QTableWidgetItem(aciklama)
                item_belge = QTableWidgetItem(belge_durumu)
                item_tarih = QTableWidgetItem(islem_tarihi)
                
                for item in [item_grubu, item_tipi, item_aciklama, item_belge, item_tarih]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                self.gunce_table.setItem(row, 4, item_grubu)
                self.gunce_table.setItem(row, 5, item_tipi)
                self.gunce_table.setItem(row, 6, item_aciklama)
                self.gunce_table.setItem(row, 7, item_belge)
                self.gunce_table.setItem(row, 8, item_tarih)
                
                # Satır renklendirme
                if row % 2 == 0:
                    for col in range(9):
                        self.gunce_table.item(row, col).setBackground(QColor("#F8F9FA"))
                else:
                    for col in range(9):
                        self.gunce_table.item(row, col).setBackground(Qt.GlobalColor.white)
                
                for col in range(9):
                    self.gunce_table.item(row, col).setForeground(Qt.GlobalColor.black)
        else:
            # Öğrenci için günce verisi yoksa boş tablo göster
            pass

    def show_gunce_detay(self, row, column):
        """Seçili günce satırının detaylarını gösterir"""
        # Satırdaki verileri al
        gunce_id = self.gunce_table.item(row, 0).text()
        isim = self.gunce_table.item(row, 1).text()
        soyisim = self.gunce_table.item(row, 2).text()
        sinif = self.gunce_table.item(row, 3).text()
        gunce_grubu = self.gunce_table.item(row, 4).text()
        gunce_tipi = self.gunce_table.item(row, 5).text()
        aciklama = self.gunce_table.item(row, 6).text()
        belge_durumu = self.gunce_table.item(row, 7).text()
        islem_tarihi = self.gunce_table.item(row, 8).text()
        
        # Öğrenci adını birleştir
        ogrenci_adi = f"{isim} {soyisim}"
        
        # Günce verilerini hazırla
        gunce_data = {
            'id': gunce_id,
            'grup': gunce_grubu,
            'tip': gunce_tipi,
            'aciklama': aciklama,
            'belge_durumu': belge_durumu,
            'islem_tarihi': islem_tarihi,
            'ogrenci': ogrenci_adi
        }
        
        # Günce detay ekranını aç (görüntüleme modu)
        dialog = GunceEkleDialog(self, ogrenci_adi, view_mode=True, gunce_data=gunce_data)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            print("Günce detayları görüntülendi.")
        else:
            print("Günce detayları kapatıldı.")

    def show_gunce_ekle(self):
        """Günce Ekleme ekranını açar"""
        selected_student = self.ogrenci_combo.currentText()
        
        if selected_student == "Öğrenci Seç":
            # Öğrenci seçilmemişse uyarı göster
            print("Lütfen önce bir öğrenci seçin!")
            return
        
        dialog = GunceEkleDialog(self, selected_student)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            print("Günce başarıyla eklendi!")
            # Günce eklendikten sonra tabloyu güncelle
            self.get_ogrenci_gunce()
        else:
            print("Günce ekleme iptal edildi.")

    def show_tum_liste(self):
        """Tüm günce listesini gösterir - ilk görünen genel tablo"""
        # İlk görünen genel tablo verileri
        tum_gunce_veriler = [
            ("1", "Naciye", "Görür", "1. Sınıf", "Genel", "Resmi Evrak", "500tl", "Belge Mevcut", "19 Nis 2025"),
            ("2", "Zafer", "Yetişir", "2. Sınıf", "Sağlık", "Genel Bilgi", "kızı doğum yaptı", "Belge Bulunmuyor", "21 Mar 2025"),
            ("3", "Tahir", "Sabuncuoğlu", "3. Sınıf", "Eğitim", "Sağlık Belgesi", "500tl", "Belge Bulunmuyor", ""),
            ("4", "Necla", "Demir", "1. Sınıf", "Genel", "Genel Bilgi", "", "Belge Bulunmuyor", ""),
            ("5", "Ayşe", "Temiz", "2. Sınıf", "Sağlık", "Resmi Evrak", "", "Belge Bulunmuyor", ""),
            ("6", "Kazım", "Al", "3. Sınıf", "Eğitim", "Sağlık Belgesi", "", "Belge Bulunmuyor", ""),
            ("7", "Hatice", "Dur", "1. Sınıf", "Genel", "Genel Bilgi", "", "Belge Bulunmuyor", ""),
            ("8", "Hasan", "Keskin", "2. Sınıf", "Sağlık", "Resmi Evrak", "", "Belge Bulunmuyor", ""),
            ("9", "Durmuş", "Duran", "3. Sınıf", "Eğitim", "Sağlık Belgesi", "", "Belge Bulunmuyor", ""),
            ("10", "Fatih", "Kel", "1. Sınıf", "Genel", "Genel Bilgi", "", "Belge Bulunmuyor", ""),
            ("11", "Kamuran", "Akgün", "2. Sınıf", "Sağlık", "Resmi Evrak", "", "Belge Bulunmuyor", ""),
            ("12", "Ahmet", "Baklavacı", "3. Sınıf", "Eğitim", "Sağlık Belgesi", "", "Belge Bulunmuyor", ""),
        ]
        
        # Tabloyu temizle ve genel verileri yükle
        self.gunce_table.setRowCount(0)
        self.gunce_table.setRowCount(len(tum_gunce_veriler))
        
        for row, veri in enumerate(tum_gunce_veriler):
            for col, val in enumerate(veri):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Satır renklendirme (alternatif satırlar)
                if row % 2 == 0:
                    item.setBackground(QColor("#F8F9FA"))  # Açık gri
                else:
                    item.setBackground(Qt.GlobalColor.white)
                
                item.setForeground(Qt.GlobalColor.black)
                self.gunce_table.setItem(row, col, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GunceWindow()
    sys.exit(app.exec())

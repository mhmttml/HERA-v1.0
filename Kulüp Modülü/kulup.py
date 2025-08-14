import os
import sys
try:
    from PyQt6.QtCore import QLibraryInfo
    plugin_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
except Exception as e:
    print("Qt plugin path ayarlanamadı:", e, file=sys.stderr)
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QStackedWidget, QHeaderView, QScrollBar, QAbstractScrollArea, QAbstractItemView, QComboBox, QSizePolicy, QDialog, QMessageBox
from PyQt6.QtGui import QFont, QPixmap, QColor, QPainter
from PyQt6.QtCore import Qt, QDateTime, QTimer
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QButtonGroup
from kulup_etkinlik_ekle import EtkinlikEkleDialog
from kulup_etkinlik_guncelle import KulupEtkinlikGuncelleDialog
from kulup_katilimci_ekle import KulupKatilimciEkleDialog

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

class KulupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HERA - Kulüp Modülü")
        self.setStyleSheet("background-color: #EBF2FA;")
        # Başlangıç minimumu; gerçek minimum, UI kurulduktan sonra dinamik ayarlanır
        self.setMinimumSize(800, 600)
        
        # Scroll bar'lar için ekran boyutuna göre ölçeklendirme faktörü hesapla
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        # 1920x1080 baz alınarak ölçeklendirme faktörü
        base_width = 1920
        base_height = 1080
        self.scroll_scale = min(screen_width / base_width, screen_height / base_height)
        # Minimum ölçek 0.7, maksimum 1.5 olsun
        self.scroll_scale = max(0.7, min(1.5, self.scroll_scale))
        
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar (tam genişlik)
        top_bar_widget = self._create_top_bar()
        main_layout.addWidget(top_bar_widget)

        # Alt kısım: yatayda sol panel ve sağ içerik
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(2)  # Sol panel ile sağ panel arası boşluk azaltıldı

        # Sol panel (butonlar) - sabit genişlik
        left_panel = QWidget()
        left_panel.setFixedWidth(300)  # Sabit genişlik
        left_panel.setStyleSheet("background-color: #EBF2FA;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(30)
        
        # Sol panelin üst kısmına boşluk ekle - butonları yukarı taşımak için
        left_layout.addSpacing(80)

        # Sol panel butonları (kulüp modülü için)
        left_buttons = [
            ("Ana Sayfa", "#A9C5DB", "#FFFFFF"),
            ("Etkinlik Ekle", "#A9C5DB", "#FFFFFF"),
            ("Etkinlik Güncelle", "#A9C5DB", "#FFFFFF"),
            ("Katılımcı Ekle", "#A9C5DB", "#FFFFFF"),
            ("Tüm Liste", "#A9C5DB", "#FFFFFF"),
            ("Rapor Seç", "#A9C5DB", "#FFFFFF"),
            ("Rapor Getir", "#A9C5DB", "#FFFFFF"),
            ("Dışarı Aktar", "#A9C5DB", "#FFFFFF"),
        ]
        
        for text, bg, fg in left_buttons:
            if text == "Rapor Seç":
                combo = QComboBox()
                combo.setMinimumSize(200, 50)
                combo.setMaximumSize(300, 50)
                combo.setFont(QFont("Arial", 15, QFont.Weight.DemiBold))
                combo.addItems(["Rapor Seç", "Aylık Rapor", "Yıllık Rapor", "Katılımcı Raporu", "Kulüp Performans Raporu"])
                combo.setStyleSheet('''
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
                
                # Shadow efekti ekle
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(16)
                shadow.setOffset(0, 4)
                shadow.setColor(QColor(66, 122, 162, 60))
                combo.setGraphicsEffect(shadow)
                
                left_layout.addWidget(combo)
                continue
                
            btn = QPushButton(text)
            # Ortak özellikler
            btn.setFixedSize(260, 50)  # Sabit boyut
            btn.setFont(QFont("Arial", 15, QFont.Weight.DemiBold))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg};
                    color: {fg};
                    border: none;
                    border-radius: 8px;
                    padding: 0px 15px;
                }}
                QPushButton:hover {{
                    background-color: #8FB7D6;
                    color: #427AA2;
                }}
                QPushButton:pressed {{
                    background-color: #A9C5DB;
                }}
            """)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(16)
            shadow.setOffset(0, 4)
            shadow.setColor(QColor(66, 122, 162, 60))
            btn.setGraphicsEffect(shadow)
            left_layout.addWidget(btn)
            
            # Buton tıklama olaylarını bağla
            if text == "Etkinlik Ekle":
                btn.clicked.connect(self.show_etkinlik_ekle_popup)
            elif text == "Etkinlik Güncelle":
                btn.clicked.connect(self.show_etkinlik_guncelle_popup)
            elif text == "Katılımcı Ekle":
                btn.clicked.connect(self.show_katilimci_ekle_popup)

        left_layout.addStretch(1)

        # Sağ içerik (veri tablosu) - responsive
        right_content = QWidget()
        right_content.setStyleSheet("background-color: #EBF2FA;")
        right_content.setMinimumWidth(1200)  # Minimum genişlik artırıldı
        right_layout = QVBoxLayout(right_content)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(0)
        
        # Tablo başlığı label'ı - sağ panel içinde tablonun üzerinde
        self.table_title_label = QLabel("Kulüp Etkinlik Listesi")
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
        
        # Tablo başlığı label'ını sağ panel içine ekle
        right_layout.addWidget(self.table_title_label)
        
        # Kulüp etkinlik veri tablosu
        self.etkinlik_table = QTableWidget()
        self.etkinlik_table.setColumnCount(9)
        self.etkinlik_table.setHorizontalHeaderLabels([
            "Etkinlik ID", "Kulüp", "Etkinlik", "Etkinlik Açıklaması", "Etkinlik Lideri", 
            "Etkinlik Durumu", "Katılımcı Sayısı", "Etkinlik Başlangıç Tarihi", 
            "Etkinlik Bitiş Tarihi"
        ])
        
        # Örnek veriler
        etkinlikler = [
            ("ET001", "Spor Kulübü", "Futbol Turnuvası", "Hafta sonu futbol turnuvası", "Ahmet Yılmaz", "Aktif", "25", "15 Mar 2025", "16 Mar 2025"),
            ("ET002", "Müzik Kulübü", "Konser", "Bahar konseri", "Ayşe Demir", "Planlandı", "0", "20 Nis 2025", "20 Nis 2025"),
            ("ET003", "Kitap Kulübü", "Kitap Tartışması", "Aylık kitap tartışması", "Mehmet Kaya", "Tamamlandı", "15", "10 Mar 2025", "10 Mar 2025"),
        ]
        
        # Tabloyu doldur
        self.etkinlik_table.setRowCount(len(etkinlikler))
        for row, etkinlik in enumerate(etkinlikler):
            for col, val in enumerate(etkinlik):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Etkinlik durumuna göre renklendirme
                if col == 5:  # Etkinlik Durumu sütunu
                    if val == "Aktif":
                        item.setBackground(QColor("#E8F5E8"))  # Açık yeşil
                        item.setForeground(QColor("#2E7D32"))  # Koyu yeşil
                    elif val == "Planlandı":
                        item.setBackground(QColor("#FFF3E0"))  # Açık turuncu
                        item.setForeground(QColor("#E65100"))  # Koyu turuncu
                    elif val == "Tamamlandı":
                        item.setBackground(QColor("#E3F2FD"))  # Açık mavi
                        item.setForeground(QColor("#1565C0"))  # Koyu mavi
                    else:
                        item.setBackground(Qt.GlobalColor.white)
                        item.setForeground(Qt.GlobalColor.black)
                else:
                    item.setBackground(Qt.GlobalColor.white)
                    item.setForeground(Qt.GlobalColor.black)
                
                self.etkinlik_table.setItem(row, col, item)
        
        # Tablo ayarları
        self.etkinlik_table.resizeColumnsToContents()
        self.etkinlik_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.etkinlik_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.etkinlik_table.setMinimumHeight(600)
        
        # Hücre düzenlemeyi devre dışı bırak
        self.etkinlik_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Hücre seçimini tek satır seçimi olarak ayarla
        self.etkinlik_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.etkinlik_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        # Kolon genişliklerini elle düzenlemeyi devre dışı bırak
        self.etkinlik_table.horizontalHeader().setStretchLastSection(False)
        self.etkinlik_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        # Sütun genişliklerini ayarla
        header_labels = [
            "Etkinlik ID", "Kulüp", "Etkinlik", "Etkinlik Açıklaması", "Etkinlik Lideri", 
            "Etkinlik Durumu", "Katılımcı Sayısı", "Etkinlik Başlangıç Tarihi", 
            "Etkinlik Bitiş Tarihi"
        ]
        fm = self.etkinlik_table.fontMetrics()
        for col, label in enumerate(header_labels):
            max_width = fm.horizontalAdvance(label)
            for row in range(self.etkinlik_table.rowCount()):
                item = self.etkinlik_table.item(row, col)
                if item:
                    content_width = fm.horizontalAdvance(item.text())
                    if content_width > max_width:
                        max_width = content_width
            self.etkinlik_table.setColumnWidth(col, max_width + 100)
        
        # Tablo scroll bar'larını gizle
        self.etkinlik_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.etkinlik_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.etkinlik_table.verticalScrollBar().setStyleSheet("QScrollBar { width: 0px; }")
        self.etkinlik_table.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0px; }")
        
        # Tablo border'ını ayarla
        self.etkinlik_table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #427AA2;
                border-radius: 8px;
                background-color: white;
            }
        """)
        
        # Tablo header stilini ayarla
        self.etkinlik_table.horizontalHeader().setStyleSheet('''
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
        self.etkinlik_table.verticalHeader().setVisible(False)
        
        # Responsive scroll bar boyutları
        scroll_width = int(30 * self.scroll_scale)
        scroll_radius = int(10 * self.scroll_scale)
        handle_radius = int(10 * self.scroll_scale)
        handle_min_height = int(90 * self.scroll_scale)
        handle_margin = int(5 * self.scroll_scale)
        
        # Dikey scroll bar konteyneri
        etkinlik_scroll_container = QWidget()
        etkinlik_scroll_container.setFixedWidth(scroll_width)
        # Dikey scroll container yüksekliğini tablo container ile aynı yap
        etkinlik_scroll_container.setFixedHeight(self.etkinlik_table.height())
        etkinlik_scroll_layout = QVBoxLayout(etkinlik_scroll_container)
        etkinlik_scroll_layout.setContentsMargins(0, 0, 0, 0)
        etkinlik_scroll_layout.setSpacing(0)
        etkinlik_scrollbar = QScrollBar(Qt.Orientation.Vertical)
        etkinlik_scrollbar.setStyleSheet(f'''
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
        etkinlik_scroll_layout.addWidget(etkinlik_scrollbar)
        
        # Tablo boyutu değiştiğinde scroll container'ı da güncelle
        def update_scroll_container_height():
            etkinlik_scroll_container.setFixedHeight(self.etkinlik_table.height())
        
        # Tablo resize event'ini yakala
        self.etkinlik_table.resizeEvent = lambda event: update_scroll_container_height()
        
        # Scroll bar ile tabloyu senkronize et
        etkinlik_scrollbar.setMinimum(self.etkinlik_table.verticalScrollBar().minimum())
        etkinlik_scrollbar.setMaximum(self.etkinlik_table.verticalScrollBar().maximum())
        etkinlik_scrollbar.setPageStep(self.etkinlik_table.verticalScrollBar().pageStep())
        etkinlik_scrollbar.setSingleStep(self.etkinlik_table.verticalScrollBar().singleStep())
        etkinlik_scrollbar.setValue(self.etkinlik_table.verticalScrollBar().value())
        etkinlik_scrollbar.valueChanged.connect(self.etkinlik_table.verticalScrollBar().setValue)
        self.etkinlik_table.verticalScrollBar().valueChanged.connect(etkinlik_scrollbar.setValue)

        # Responsive yatay scroll bar boyutları
        hscroll_height = int(30 * self.scroll_scale)
        hscroll_radius = int(15 * self.scroll_scale)
        hhandle_radius = int(10 * self.scroll_scale)
        hhandle_min_width = int(40 * self.scroll_scale)
        hhandle_height = int(20 * self.scroll_scale)
        hhandle_margin = int(4 * self.scroll_scale)
        
        # Yatay scroll bar konteyneri
        etkinlik_hscroll_container = QWidget()
        etkinlik_hscroll_container.setFixedHeight(hscroll_height)
        etkinlik_hscroll_layout = QHBoxLayout(etkinlik_hscroll_container)
        etkinlik_hscroll_layout.setContentsMargins(0, 0, 0, 0)
        etkinlik_hscroll_layout.setSpacing(0)
        etkinlik_hscrollbar = QScrollBar(Qt.Orientation.Horizontal)
        etkinlik_hscrollbar.setStyleSheet(f'''
            QScrollBar:horizontal {{
                background: rgba(66,122,162,0.5);
                border-radius: {hscroll_radius}px;
                height: {hscroll_height}px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: white;
                border-radius: {hhandle_radius}px;
                min-height: {int(20 * self.scroll_scale)}px;
                min-width: {hhandle_min_width}px;
                max-height: {int(20 * self.scroll_scale)}px;
                max-width: {hhandle_min_width}px;
                height: {int(20 * self.scroll_scale)}px;
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
        etkinlik_hscroll_layout.addWidget(etkinlik_hscrollbar)
        
        # Yatay scroll bar ile tabloyu senkronize et
        etkinlik_hscrollbar.setMinimum(self.etkinlik_table.horizontalScrollBar().minimum())
        etkinlik_hscrollbar.setMaximum(self.etkinlik_table.horizontalScrollBar().maximum())
        etkinlik_hscrollbar.setPageStep(self.etkinlik_table.horizontalScrollBar().pageStep())
        etkinlik_hscrollbar.setSingleStep(self.etkinlik_table.horizontalScrollBar().singleStep())
        etkinlik_hscrollbar.setValue(self.etkinlik_table.horizontalScrollBar().value())
        etkinlik_hscrollbar.valueChanged.connect(self.etkinlik_table.horizontalScrollBar().setValue)
        self.etkinlik_table.horizontalScrollBar().valueChanged.connect(etkinlik_hscrollbar.setValue)
        
        # Scroll bar parametrelerini dinamik güncelle
        def update_hscrollbar_range(minimum, maximum):
            etkinlik_hscrollbar.setMinimum(minimum)
            etkinlik_hscrollbar.setMaximum(maximum)
            etkinlik_hscrollbar.setPageStep(self.etkinlik_table.horizontalScrollBar().pageStep())
            etkinlik_hscrollbar.setSingleStep(self.etkinlik_table.horizontalScrollBar().singleStep())
        self.etkinlik_table.horizontalScrollBar().rangeChanged.connect(update_hscrollbar_range)
        
        # Tablo ve scroll barlarını yerleştir
        etkinlik_table_and_scroll = QWidget()
        etkinlik_table_and_scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        etkinlik_table_and_scroll_layout = QVBoxLayout(etkinlik_table_and_scroll)
        etkinlik_table_and_scroll_layout.setContentsMargins(0, 0, 0, 0)
        etkinlik_table_and_scroll_layout.setSpacing(0)
        etkinlik_table_and_scroll_layout.addWidget(self.etkinlik_table)
        etkinlik_table_and_scroll_layout.addSpacing(20)
        etkinlik_table_and_scroll_layout.addWidget(etkinlik_hscroll_container)
        
        # Tablo için margin widget
        table_margin_widget = QWidget()
        table_margin_widget.setStyleSheet("background-color: #EBF2FA;")
        table_margin_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table_margin_layout = QHBoxLayout(table_margin_widget)
        # Scroll container'ı yukarı taşımak için üst margin'i azalt
        table_margin_layout.setContentsMargins(20, 0, 20, 20)
        table_margin_layout.addWidget(etkinlik_table_and_scroll, 1)  # Stretch factor 1 ekle
        table_margin_layout.addSpacing(10)
        # Scroll container'ı yukarı taşımak için üst margin ekle
        table_margin_layout.addWidget(etkinlik_scroll_container, 0, Qt.AlignmentFlag.AlignTop)
        
        right_layout.addWidget(table_margin_widget)

        # Layout'ları birleştir
        bottom_layout.addWidget(left_panel)
        bottom_layout.addWidget(right_content)

        # Ana layouta ekle
        main_layout.addLayout(bottom_layout)

        # Dinamik minimum pencere boyutu: sol panel sabit genişlik + sağ içerik minimumu
        try:
            left_panel_min_w = 300  # sol panel sabit
            right_min_w = right_content.minimumWidth() if right_content.minimumWidth() > 0 else 1200
            total_min_w = left_panel_min_w + bottom_layout.spacing() + right_min_w

            # Yükseklik: top bar + sağ içerik yaklaşık minimumu
            top_h = 80  # top bar fixed
            right_content_min_h = max(self.etkinlik_table.minimumHeight() + 160, right_content.sizeHint().height())
            total_min_h = top_h + right_content_min_h

            self.setMinimumSize(total_min_w, total_min_h)
        except Exception:
            # Her ihtimale karşı, önceki minimumlarla devam et
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
        try:
            logo.setPixmap(QPixmap("2.png").scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        except:
            # Logo yüklenemezse boş bırak
            pass

        # Başlık
        title = ShadowLabel("HEALTHY ELDERS' RECORDS ASSISTANT - KULÜP MODÜLÜ")
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

    def show_etkinlik_ekle_popup(self):
        """Etkinlik ekle ekranını aç"""
        # Mevcut etkinlik sayısını al
        current_count = self.etkinlik_table.rowCount()
        
        dialog = EtkinlikEkleDialog(self)
        # Etkinlik ID'yi otomatik olarak ata
        dialog.generate_etkinlik_id(current_count)
        
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            # Etkinlik verilerini al
            etkinlik_data = dialog.get_etkinlik_data()
            
            # Yeni satır ekle
            self.add_etkinlik_to_table(etkinlik_data)
            
            QMessageBox.information(self, "Başarılı", "Etkinlik başarıyla eklendi!")
        else:
            print("İşlem iptal edildi.")

    def add_etkinlik_to_table(self, etkinlik_data):
        """Yeni etkinlik verilerini tabloya ekle"""
        # Yeni satır ekle
        row = self.etkinlik_table.rowCount()
        self.etkinlik_table.insertRow(row)
        
        # Etkinlik ID'yi otomatik oluştur (ET001, ET002, ...)
        etkinlik_id = f"ET{row + 1:03d}"
        
        # Verileri tabloya ekle
        self.etkinlik_table.setItem(row, 0, QTableWidgetItem(etkinlik_id))  # Etkinlik ID
        self.etkinlik_table.setItem(row, 1, QTableWidgetItem(etkinlik_data['kulup']))  # Kulüp
        self.etkinlik_table.setItem(row, 2, QTableWidgetItem(etkinlik_data['etkinlik_adi']))  # Etkinlik
        self.etkinlik_table.setItem(row, 3, QTableWidgetItem(etkinlik_data['aciklama']))  # Etkinlik Açıklaması
        self.etkinlik_table.setItem(row, 4, QTableWidgetItem(etkinlik_data['lider']))  # Etkinlik Lideri
        self.etkinlik_table.setItem(row, 5, QTableWidgetItem(etkinlik_data['durum']))  # Etkinlik Durumu
        self.etkinlik_table.setItem(row, 6, QTableWidgetItem("0"))  # Katılımcı Sayısı (başlangıçta 0)
        self.etkinlik_table.setItem(row, 7, QTableWidgetItem(etkinlik_data['baslangic_tarihi']))  # Başlangıç Tarihi
        self.etkinlik_table.setItem(row, 8, QTableWidgetItem(etkinlik_data['bitis_tarihi']))  # Bitiş Tarihi
        
        # Tüm hücreleri ortala ve renklendir
        for col in range(9):
            item = self.etkinlik_table.item(row, col)
            if item:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Etkinlik durumuna göre renklendirme
                if col == 5:  # Etkinlik Durumu sütunu
                    if item.text() == "Aktif":
                        item.setBackground(QColor("#E8F5E8"))  # Açık yeşil
                        item.setForeground(QColor("#2E7D32"))  # Koyu yeşil
                    elif item.text() == "Planlandı":
                        item.setBackground(QColor("#FFF3E0"))  # Açık turuncu
                        item.setForeground(QColor("#E65100"))  # Koyu turuncu
                    elif item.text() == "Tamamlandı":
                        item.setBackground(QColor("#E3F2FD"))  # Açık mavi
                        item.setForeground(QColor("#1565C0"))  # Koyu mavi
                    else:
                        item.setBackground(Qt.GlobalColor.white)
                        item.setForeground(Qt.GlobalColor.black)
                else:
                    item.setBackground(Qt.GlobalColor.white)
                    item.setForeground(Qt.GlobalColor.black)

    def show_etkinlik_guncelle_popup(self):
        """Etkinlik güncelleme ekranını aç"""
        # Seçili satırı kontrol et
        current_selection = self.etkinlik_table.selectionModel().selectedRows()
        if not current_selection:
            QMessageBox.warning(self, "Uyarı", "Lütfen güncellenecek etkinliği seçin!")
            return
        
        selected_row = current_selection[0].row()
        
        # Seçili satırdan etkinlik verilerini al
        etkinlik_data = {
            'etkinlik_id': self.etkinlik_table.item(selected_row, 0).text(),
            'kulup': self.etkinlik_table.item(selected_row, 1).text(),
            'etkinlik_adi': self.etkinlik_table.item(selected_row, 2).text(),
            'etkinlik_aciklamasi': self.etkinlik_table.item(selected_row, 3).text(),
            'etkinlik_lideri': self.etkinlik_table.item(selected_row, 4).text(),
            'etkinlik_durumu': self.etkinlik_table.item(selected_row, 5).text(),
            'katilimci_sayisi': self.etkinlik_table.item(selected_row, 6).text(),
            'baslangic_tarihi': self.etkinlik_table.item(selected_row, 7).text(),
            'bitis_tarihi': self.etkinlik_table.item(selected_row, 8).text(),
            'min_katilimci': '10',  # Varsayılan değer
            'max_katilimci': '50'   # Varsayılan değer
        }
        
        # Güncelleme ekranını aç
        dialog = KulupEtkinlikGuncelleDialog(etkinlik_data, self)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            # Güncellenmiş verileri al
            updated_data = dialog.get_updated_etkinlik_data()
            
            # Tabloyu güncelle
            self.update_etkinlik_in_table(selected_row, updated_data)
            
            QMessageBox.information(self, "Başarılı", "Etkinlik başarıyla güncellendi!")
        else:
            print("Etkinlik güncelleme işlemi iptal edildi.")

    def update_etkinlik_in_table(self, row, updated_data):
        """Tablodaki etkinlik verilerini güncelle"""
        # Etkinlik ID değiştirilemez
        self.etkinlik_table.item(row, 0).setText(updated_data['etkinlik_id'])
        
        # Diğer alanları güncelle
        self.etkinlik_table.item(row, 1).setText(updated_data['kulup'])
        self.etkinlik_table.item(row, 2).setText(updated_data['etkinlik_adi'])
        self.etkinlik_table.item(row, 3).setText(updated_data['etkinlik_aciklamasi'])
        self.etkinlik_table.item(row, 4).setText(updated_data['etkinlik_lideri'])
        self.etkinlik_table.item(row, 5).setText(updated_data['etkinlik_durumu'])
        
        # Katılımcı sayısı (değişmez, sadece görüntüleme)
        # self.etkinlik_table.item(row, 6).setText(updated_data['katilimci_sayisi'])
        
        self.etkinlik_table.item(row, 7).setText(updated_data['baslangic_tarihi'])
        self.etkinlik_table.item(row, 8).setText(updated_data['bitis_tarihi'])
        
        # Etkinlik durumuna göre renklendirme
        self.color_table_cell(row, 5, updated_data['etkinlik_durumu'])

    def color_table_cell(self, row, col, value):
        """Tablo hücresini değere göre renklendir"""
        item = self.etkinlik_table.item(row, col)
        if item:
            if value == "Aktif":
                item.setBackground(QColor("#E8F5E8"))  # Açık yeşil
                item.setForeground(QColor("#2E7D32"))  # Koyu yeşil
            elif value == "Planlandı":
                item.setBackground(QColor("#FFF3E0"))  # Açık turuncu
                item.setForeground(QColor("#E65100"))  # Koyu turuncu
            elif value == "Tamamlandı":
                item.setBackground(QColor("#E3F2FD"))  # Açık mavi
                item.setForeground(QColor("#1565C0"))  # Koyu mavi
            else:
                item.setBackground(Qt.GlobalColor.white)
                item.setForeground(Qt.GlobalColor.black)

    def show_katilimci_ekle_popup(self):
        """Katılımcı ekleme ekranını aç"""
        # Seçili satırı kontrol et
        current_selection = self.etkinlik_table.selectionModel().selectedRows()
        if not current_selection:
            QMessageBox.warning(self, "Uyarı", "Lütfen katılımcı eklenecek etkinliği seçin!")
            return
        
        selected_row = current_selection[0].row()
        selected_kulup = self.etkinlik_table.item(selected_row, 1).text()  # Kulüp adı
        selected_etkinlik = self.etkinlik_table.item(selected_row, 2).text()  # Etkinlik adı
        
        # Katılımcı ekleme ekranını aç - kulüp ve etkinlik bilgilerini geçir
        dialog = KulupKatilimciEkleDialog(self, selected_kulup, selected_etkinlik)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            # Katılımcı verilerini al
            katilimci_data = dialog.get_katilimci_data()
            
            # Katılımcı sayısını güncelle
            katilimci_sayisi = sum(1 for k in katilimci_data if k['katilim'] == 'Evet')
            self.etkinlik_table.item(selected_row, 6).setText(str(katilimci_sayisi))
            
            QMessageBox.information(self, "Başarılı", f"'{selected_etkinlik}' etkinliği için {katilimci_sayisi} katılımcı başarıyla eklendi!")
        else:
            print("Katılımcı ekleme işlemi iptal edildi.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KulupWindow()
    sys.exit(app.exec())

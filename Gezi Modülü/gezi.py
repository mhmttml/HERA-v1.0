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
from gezi_ekle import GeziEkleDialog
from gezi_guncelle import GeziGuncelleDialog
from gezi_katilimci_ekle import GeziKatilimciEkleDialog

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

class GeziWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HERA - Gezi Modülü")
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

        # Sol panel (butonlar) - responsive
        left_panel = QWidget()
        left_panel.setFixedWidth(300)  # Sabit genişlik
        left_panel.setStyleSheet("background-color: #EBF2FA;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(30)
        
        # Sol panelin üst kısmına boşluk ekle - butonları yukarı taşımak için
        left_layout.addSpacing(80)

        # Sol panel butonları (görseldeki gibi)
        left_buttons = [
            ("Ana Sayfa", "#A9C5DB", "#FFFFFF"),
            ("Gezi Ekle", "#A9C5DB", "#FFFFFF"),
            ("Gezi Güncelle", "#A9C5DB", "#FFFFFF"),
            ("Katılımcı Ekle", "#A9C5DB", "#FFFFFF"),
            ("Rapor Seç", "#A9C5DB", "#FFFFFF"),
            ("Rapor Getir", "#A9C5DB", "#FFFFFF"),
            ("Tüm Liste", "#A9C5DB", "#FFFFFF"),
            ("Dışarı Aktar", "#A9C5DB", "#FFFFFF"),
        ]
        
        for text, bg, fg in left_buttons:
            if text == "Rapor Seç":
                combo = QComboBox()
                combo.setMinimumSize(200, 50)
                combo.setMaximumSize(300, 50)
                combo.setFont(QFont("Arial", 15, QFont.Weight.DemiBold))
                combo.addItems(["Rapor Seç", "Aylık Rapor", "Yıllık Rapor", "Katılımcı Raporu"])
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
            # Gezi Ekle butonuna tıklanınca pop-up aç
            if text == "Gezi Ekle":
                btn.clicked.connect(self.show_gezi_ekle_popup)
            # Gezi Güncelle butonuna tıklanınca pop-up aç
            elif text == "Gezi Güncelle":
                btn.clicked.connect(self.show_gezi_guncelle_popup)
            # Katılımcı Ekle butonuna tıklanınca pop-up aç
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
        self.table_title_label = QLabel("Gezi Listesi")
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
        
        # Gezi veri tablosu
        self.gezi_table = QTableWidget()
        self.gezi_table.setColumnCount(9)
        self.gezi_table.setHorizontalHeaderLabels([
            "Gezi ID", "Gezi Adı", "Gezi Başlangıç Tarihi", "Gezi Bitiş Tarihi", 
            "Toplam Katılımcı Sayısı", "Gezi Durumu", "Gezi Ücreti", "Gezi Lideri", "Gezi Açıklaması"
        ])
        
        # Görseldeki veriler
        geziler = [
            ("GZ001", "antalya turu", "15 Mar 2025", "18 Mar 2025", "", "Planlandı", "500 tl", "özgür", ""),
            ("GZ002", "mersin gezisi", "18 Haz 2025", "20 Haz 2025", "", "Aktif", "650 tl", "ahmet", ""),
        ]
        
        # Tabloyu doldur
        self.gezi_table.setRowCount(len(geziler))
        for row, gezi in enumerate(geziler):
            for col, val in enumerate(gezi):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setBackground(Qt.GlobalColor.white)
                self.gezi_table.setItem(row, col, item)
        
        # Tablo ayarları
        self.gezi_table.resizeColumnsToContents()
        self.gezi_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.gezi_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.gezi_table.setMinimumHeight(600)
        
        # Hücre düzenlemeyi devre dışı bırak
        self.gezi_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Hücre seçimini tek satır seçimi olarak ayarla
        self.gezi_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.gezi_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        # Kolon genişliklerini elle düzenlemeyi devre dışı bırak
        self.gezi_table.horizontalHeader().setStretchLastSection(False)
        self.gezi_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        # Sütun genişliklerini ayarla
        header_labels = [
            "Gezi ID", "Gezi Adı", "Gezi Başlangıç Tarihi", "Gezi Bitiş Tarihi", 
            "Toplam Katılımcı Sayısı", "Gezi Durumu", "Gezi Ücreti", "Gezi Lideri", "Gezi Açıklaması"
        ]
        fm = self.gezi_table.fontMetrics()
        for col, label in enumerate(header_labels):
            max_width = fm.horizontalAdvance(label)
            for row in range(self.gezi_table.rowCount()):
                item = self.gezi_table.item(row, col)
                if item:
                    content_width = fm.horizontalAdvance(item.text())
                    if content_width > max_width:
                        max_width = content_width
            self.gezi_table.setColumnWidth(col, max_width + 100)
        
        # Tablo scroll bar'larını gizle
        self.gezi_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.gezi_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.gezi_table.verticalScrollBar().setStyleSheet("QScrollBar { width: 0px; }")
        self.gezi_table.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0px; }")
        
        # Tablo border'ını ayarla
        self.gezi_table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #427AA2;
                border-radius: 8px;
                background-color: white;
            }
        """)
        
        # Tablo header stilini ayarla
        self.gezi_table.horizontalHeader().setStyleSheet('''
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
        self.gezi_table.verticalHeader().setVisible(False)
        
        # Responsive dikey scroll bar boyutları (sağlık modülü stilinde)
        scroll_width = int(30 * self.scroll_scale)
        scroll_radius = int(10 * self.scroll_scale)
        handle_radius = int(10 * self.scroll_scale)
        handle_min_height = int(90 * self.scroll_scale)
        handle_margin = int(5 * self.scroll_scale)
        
        # Dikey scroll bar konteyneri
        gezi_scroll_container = QWidget()
        gezi_scroll_container.setFixedWidth(scroll_width)
        # Dikey scroll container yüksekliğini artır
        # Tablo header yüksekliği 36px, bu yüzden toplam yükseklikten çıkar ve ekstra yükseklik ekle
        gezi_scroll_container.setFixedHeight(self.gezi_table.height() - 36 + 36)
        gezi_scroll_layout = QVBoxLayout(gezi_scroll_container)
        gezi_scroll_layout.setContentsMargins(0, 0, 0, 0)
        gezi_scroll_layout.setSpacing(0)
        gezi_scrollbar = QScrollBar(Qt.Orientation.Vertical)
        gezi_scrollbar.setStyleSheet(f'''
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
        gezi_scroll_layout.addWidget(gezi_scrollbar)
        
        # Tablo boyutu değiştiğinde scroll container'ı da güncelle
        def update_scroll_container_height():
            gezi_scroll_container.setFixedHeight(self.gezi_table.height() - 36 + 36)
        
        # Tablo resize event'ini yakala
        self.gezi_table.resizeEvent = lambda event: update_scroll_container_height()
        
        # Scroll bar ile tabloyu senkronize et
        gezi_scrollbar.setMinimum(self.gezi_table.verticalScrollBar().minimum())
        gezi_scrollbar.setMaximum(self.gezi_table.verticalScrollBar().maximum())
        gezi_scrollbar.setPageStep(self.gezi_table.verticalScrollBar().pageStep())
        gezi_scrollbar.setSingleStep(self.gezi_table.verticalScrollBar().singleStep())
        gezi_scrollbar.setValue(self.gezi_table.verticalScrollBar().value())
        gezi_scrollbar.valueChanged.connect(self.gezi_table.verticalScrollBar().setValue)
        self.gezi_table.verticalScrollBar().valueChanged.connect(gezi_scrollbar.setValue)

        # Gezi tablosunun yatay scroll barını gizle ve alanını kaldır
        self.gezi_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # Yatay scroll bar alanını tamamen kaldır
        self.gezi_table.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0px; }")
        
        # Responsive yatay scroll bar boyutları (sağlık modülü stilinde)
        hscroll_height = int(30 * self.scroll_scale)
        hscroll_radius = int(15 * self.scroll_scale)
        hhandle_radius = int(10 * self.scroll_scale)
        hhandle_min_width = int(90 * self.scroll_scale)
        hhandle_height = int(20 * self.scroll_scale)
        hhandle_margin = int(5 * self.scroll_scale)
        
        # Yatay scroll bar konteyneri
        gezi_hscroll_container = QWidget()
        gezi_hscroll_container.setFixedHeight(hscroll_height)
        gezi_hscroll_layout = QHBoxLayout(gezi_hscroll_container)
        gezi_hscroll_layout.setContentsMargins(0, 0, 0, 0)
        gezi_hscroll_layout.setSpacing(0)
        gezi_hscrollbar = QScrollBar(Qt.Orientation.Horizontal)
        gezi_hscrollbar.setStyleSheet(f'''
            QScrollBar:horizontal {{
                background: rgba(66,122,162,0.5);
                border-top-left-radius: {hscroll_radius}px;
                border-top-right-radius: {hscroll_radius}px;
                border-bottom-left-radius: {hscroll_radius}px;
                border-bottom-right-radius: {hscroll_radius}px;
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
        gezi_hscroll_layout.addWidget(gezi_hscrollbar)
        
        # Scroll bar ile tabloyu senkronize et
        gezi_hscrollbar.setMinimum(self.gezi_table.horizontalScrollBar().minimum())
        gezi_hscrollbar.setMaximum(self.gezi_table.horizontalScrollBar().maximum())
        gezi_hscrollbar.setPageStep(self.gezi_table.horizontalScrollBar().pageStep())
        gezi_hscrollbar.setSingleStep(self.gezi_table.horizontalScrollBar().singleStep())
        gezi_hscrollbar.setValue(self.gezi_table.horizontalScrollBar().value())
        gezi_hscrollbar.valueChanged.connect(self.gezi_table.horizontalScrollBar().setValue)
        self.gezi_table.horizontalScrollBar().valueChanged.connect(gezi_hscrollbar.setValue)

        # --- YENİ: Scroll bar parametrelerini dinamik güncelle ---
        def update_hscrollbar_range(minimum, maximum):
            gezi_hscrollbar.setMinimum(minimum)
            gezi_hscrollbar.setMaximum(maximum)
            gezi_hscrollbar.setPageStep(self.gezi_table.horizontalScrollBar().pageStep())
            gezi_hscrollbar.setSingleStep(self.gezi_table.horizontalScrollBar().singleStep())
        self.gezi_table.horizontalScrollBar().rangeChanged.connect(update_hscrollbar_range)
        # ---

        # Tablo ve scroll barlarını yerleştir
        gezi_table_and_scroll = QWidget()
        gezi_table_and_scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        gezi_table_and_scroll_layout = QVBoxLayout(gezi_table_and_scroll)
        gezi_table_and_scroll_layout.setContentsMargins(0, 0, 0, 0)
        gezi_table_and_scroll_layout.setSpacing(0)
        gezi_table_and_scroll_layout.addWidget(self.gezi_table)
        gezi_table_and_scroll_layout.addSpacing(20)
        gezi_table_and_scroll_layout.addWidget(gezi_hscroll_container)
        
        # Tablo için margin widget
        table_margin_widget = QWidget()
        table_margin_widget.setStyleSheet("background-color: #EBF2FA;")
        table_margin_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table_margin_layout = QHBoxLayout(table_margin_widget)
        # Scroll container'ı yukarı taşımak için üst margin'i azalt
        table_margin_layout.setContentsMargins(20, 0, 20, 20)
        table_margin_layout.addWidget(gezi_table_and_scroll, 1)  # Stretch factor 1 ekle
        table_margin_layout.addSpacing(10)
        # Scroll container'ı yukarı taşımak için üst margin ekle
        table_margin_layout.addWidget(gezi_scroll_container, 0, Qt.AlignmentFlag.AlignTop)
        
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
            right_content_min_h = max(self.gezi_table.minimumHeight() + 160, right_content.sizeHint().height())
            total_min_h = top_h + right_content_min_h

            self.setMinimumSize(total_min_w, total_min_h)
        except Exception:
            # Her ihtimale karşı, önceki minimumlarla devam et
            pass
        
        # Pencere boyutu değiştiğinde tablo sütun genişliklerini güncelle
        self.resizeEvent = self.on_resize



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
        title = ShadowLabel("HEALTHY ELDERS' RECORDS ASSISTANT - GEZİ MODÜLÜ")
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
        # user_icon.setPixmap(QPixmap('kullanici1.png').scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
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

    def show_gezi_ekle_popup(self):
        dialog = GeziEkleDialog(self)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            # Gezi verilerini al
            gezi_data = dialog.get_gezi_data()
            
            # Yeni satır ekle
            self.add_gezi_to_table(gezi_data)
            
            QMessageBox.information(self, "Başarılı", "Gezi başarıyla eklendi!")
        else:
            print("İşlem iptal edildi.")

    def add_gezi_to_table(self, gezi_data):
        """Yeni gezi verilerini tabloya ekle"""
        # Yeni satır ekle
        row = self.gezi_table.rowCount()
        self.gezi_table.insertRow(row)
        
        # Gezi ID'yi otomatik oluştur (GZ001, GZ002, ...)
        gezi_id = f"GZ{row + 1:03d}"
        
        # Verileri tabloya ekle
        self.gezi_table.setItem(row, 0, QTableWidgetItem(gezi_id))  # Gezi ID
        self.gezi_table.setItem(row, 1, QTableWidgetItem(gezi_data['gezi_adi']))  # Gezi Adı
        self.gezi_table.setItem(row, 2, QTableWidgetItem(gezi_data['baslangic_tarihi']))  # Başlangıç Tarihi
        self.gezi_table.setItem(row, 3, QTableWidgetItem(gezi_data['bitis_tarihi']))  # Bitiş Tarihi
        self.gezi_table.setItem(row, 4, QTableWidgetItem(""))  # Toplam Katılımcı Sayısı (Katılımcı Ekle ekranından gelecek)
        self.gezi_table.setItem(row, 5, QTableWidgetItem(gezi_data['durum']))  # Gezi Durumu
        self.gezi_table.setItem(row, 6, QTableWidgetItem(gezi_data['ucret']))  # Gezi Ücreti
        self.gezi_table.setItem(row, 7, QTableWidgetItem(gezi_data['lider']))  # Gezi Lideri
        self.gezi_table.setItem(row, 8, QTableWidgetItem(gezi_data['aciklama']))  # Gezi Açıklaması
        
        # Tüm hücreleri ortala ve beyaz arka plan ver
        for col in range(9):
            item = self.gezi_table.item(row, col)
            if item:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setBackground(Qt.GlobalColor.white)

    def show_gezi_guncelle_popup(self):
        # Seçili satırı kontrol et
        selected_rows = self.gezi_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Uyarı", "Lütfen güncellenecek geziyi seçin!")
            return
        
        # Seçili gezi verilerini al
        row = selected_rows[0].row()
        gezi_data = {
            'id': self.gezi_table.item(row, 0).text(),
            'adi': self.gezi_table.item(row, 1).text(),
            'baslangic': self.gezi_table.item(row, 2).text(),
            'bitis': self.gezi_table.item(row, 3).text(),
            'katilimci': self.gezi_table.item(row, 4).text(),
            'durum': self.gezi_table.item(row, 5).text(),
            'ucret': self.gezi_table.item(row, 6).text(),
            'lider': self.gezi_table.item(row, 7).text(),
            'aciklama': self.gezi_table.item(row, 8).text(),
            # Gezi ekle ekranından gelen veriler (şimdilik örnek veriler)
            'organizator': 'Örnek Organizatör',  # Gezi ekle verilerinden gelecek
            'plaka': '34 ABC 123',  # Gezi ekle verilerinden gelecek
            'max_katilimci': '50',  # Gezi ekle verilerinden gelecek
            'adres': 'Örnek Adres',  # Gezi ekle verilerinden gelecek
        }
        
        dialog = GeziGuncelleDialog(self, gezi_data)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            # Güncellenmiş veriyi al ve tabloyu güncelle
            updated_data = dialog.get_gezi_data()
            self.update_table_row(row, updated_data)
            QMessageBox.information(self, "Başarılı", "Gezi bilgileri başarıyla güncellendi!")
        else:
            print("Gezi güncelleme işlemi iptal edildi.")

    def update_table_row(self, row, updated_data):
        """Tablodaki belirtilen satırı güncelle"""
        # Gezi ID değiştirilmez (sistem tarafından atanır)
        self.gezi_table.item(row, 1).setText(updated_data['gezi_adi'])
        self.gezi_table.item(row, 2).setText(updated_data['baslangic_tarihi'])
        self.gezi_table.item(row, 3).setText(updated_data['bitis_tarihi'])
        # Toplam Katılımcı Sayısı değiştirilmez (Katılımcı Ekle ekranından gelecek)
        self.gezi_table.item(row, 5).setText(updated_data['durum'])
        self.gezi_table.item(row, 6).setText(updated_data['ucret'])
        self.gezi_table.item(row, 7).setText(updated_data['lider'])
        self.gezi_table.item(row, 8).setText(updated_data['aciklama'])
        
        # Tüm güncellenen hücreleri ortala ve beyaz arka plan ver
        for col in [1, 2, 3, 5, 6, 7, 8]:
            item = self.gezi_table.item(row, col)
            if item:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setBackground(Qt.GlobalColor.white)

    def show_katilimci_ekle_popup(self):
        """Katılımcı ekle ekranını aç"""
        # Seçili satırı kontrol et
        selected_rows = self.gezi_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Uyarı", "Lütfen katılımcı eklenecek geziyi seçin!")
            return
        
        # Seçili gezi verilerini al
        row = selected_rows[0].row()
        gezi_data = {
            'id': self.gezi_table.item(row, 0).text(),
            'adi': self.gezi_table.item(row, 1).text(),
            'baslangic': self.gezi_table.item(row, 2).text(),
            'bitis': self.gezi_table.item(row, 3).text(),
            'katilimci': self.gezi_table.item(row, 4).text(),
            'durum': self.gezi_table.item(row, 5).text(),
            'ucret': self.gezi_table.item(row, 6).text(),
            'lider': self.gezi_table.item(row, 7).text(),
            'aciklama': self.gezi_table.item(row, 8).text(),
        }
        
        dialog = GeziKatilimciEkleDialog(self, gezi_data)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            # Katılımcı verilerini al ve ana tabloyu güncelle
            katilimci_data = dialog.get_katilimci_data()
            self.update_katilimci_count(row, katilimci_data['toplam_katilimci'])
            QMessageBox.information(self, "Başarılı", "Katılımcı verileri başarıyla kaydedildi!")
        else:
            print("Katılımcı ekleme işlemi iptal edildi.")

    def update_katilimci_count(self, row, total_count):
        """Ana tablodaki toplam katılımcı sayısını güncelle"""
        self.gezi_table.item(row, 4).setText(total_count)
        item = self.gezi_table.item(row, 4)
        if item:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setBackground(Qt.GlobalColor.white)

    def on_resize(self, event):
        """Pencere boyutu değiştiğinde tablo sütun genişliklerini güncelle"""
        super().resizeEvent(event)
        
        # Sağ panel genişliğini hesapla
        right_panel_width = max(1200, self.width() - 300)
        
        # Sütun genişliklerini orantılı olarak güncelle
        column_ratios = [0.06, 0.15, 0.12, 0.12, 0.15, 0.08, 0.08, 0.10, 0.10]
        
        for col, ratio in enumerate(column_ratios):
            # Minimum genişlik hesapla
            header_labels = [
                "Gezi ID", "Gezi Adı", "Gezi Başlangıç Tarihi", "Gezi Bitiş Tarihi", 
                "Toplam Katılımcı Sayısı", "Gezi Durumu", "Gezi Ücreti", "Gezi Lideri", "Gezi Açıklaması"
            ]
            fm = self.gezi_table.fontMetrics()
            min_width = fm.horizontalAdvance(header_labels[col]) + 40
            
            # Orantılı genişlik hesapla
            proportional_width = int(right_panel_width * ratio)
            
            # Daha büyük olanı kullan
            final_width = max(min_width, proportional_width)
            self.gezi_table.setColumnWidth(col, final_width)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeziWindow()
    sys.exit(app.exec()) 
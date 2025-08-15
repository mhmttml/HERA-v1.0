import os
import sys
try:
    from PyQt6.QtCore import QLibraryInfo
    plugin_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
except Exception as e:
    print("Qt plugin path ayarlanamadı:", e, file=sys.stderr)
from PyQt6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QTextEdit, QPushButton, QWidget, 
                             QFileDialog, QScrollArea, QFrame, QSizePolicy, QCheckBox)
from PyQt6.QtGui import QFont, QPixmap, QColor, QPainter
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

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

class GunceEkleDialog(QDialog):
    def __init__(self, parent=None, selected_student="", view_mode=False, gunce_data=None):
        super().__init__(parent)
        self.selected_student = selected_student
        self.view_mode = view_mode
        self.gunce_data = gunce_data
        self.belge_yolu = ""
        
        if view_mode and gunce_data:
            self.gunce_id = gunce_data.get('id', '')
        else:
            self.gunce_id = self.generate_gunce_id()
        
        self.setWindowTitle("Günce Ekle")
        self.setStyleSheet("background-color: #EBF2FA;")
        self.setMinimumSize(1200, 800)
        
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
        # Responsive pencere boyutlandırma (yatayda max 1200px)
        max_width = 1200
        w = min(int(screen_width * 0.8), max_width)
        h = int(screen_height * 0.9)  # Dikeyde %90
        self.resize(w, h)
        self.setMinimumSize(900, 600)
        self.setMaximumSize(max_width, screen_height)
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def generate_gunce_id(self):
        """Otomatik Günce ID oluşturur"""
        import random
        return f"G{random.randint(1000, 9999)}"

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # Başlık
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)
        
        if self.view_mode:
            title = QLabel("Günce Detayları")
        else:
            title = QLabel("Günce Ekle")
        
        title.setFont(QFont("Arial", 22, QFont.Weight.DemiBold))
        title.setStyleSheet("color: #427AA2; background: transparent;")
        
        if self.selected_student:
            student_label = QLabel(f"- {self.selected_student}")
            student_label.setFont(QFont("Arial", 18, QFont.Weight.Normal))
            student_label.setStyleSheet("color: #427AA2; background: transparent;")
            title_layout.addWidget(title)
            title_layout.addWidget(student_label)
        else:
            title_layout.addWidget(title)
        
        title_layout.addStretch(1)
        main_layout.addLayout(title_layout)
        main_layout.addSpacing(18)

        # Ana içerik alanı
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(30)

        # Sol panel - Form alanları
        left_panel = self.create_left_panel()
        content_layout.addWidget(left_panel)

        # Sağ panel - Önizleme alanı
        right_panel = self.create_right_panel()
        content_layout.addWidget(right_panel)

        main_layout.addLayout(content_layout)

        # Alt butonlar
        bottom_buttons = self.create_bottom_buttons()
        main_layout.addWidget(bottom_buttons)

    def create_left_panel(self):
        """Sol panel - Form alanları"""
        panel = QWidget()
        panel.setMinimumWidth(400)
        panel.setMaximumWidth(500)
        panel.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
        """)
        
        # Gölge efekti
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 30))
        panel.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Günce ID
        id_layout = QVBoxLayout()
        id_label = QLabel("Günce ID:")
        id_label.setFont(QFont("Arial", 14))
        id_label.setStyleSheet("color: #427AA2; background: transparent;")
        id_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        self.id_input = QLineEdit(self.gunce_id)
        self.id_input.setReadOnly(True)
        self.id_input.setStyleSheet("""
            QLineEdit {
                background-color: #F8F9FA;
                border: 2px solid #E9ECEF;
                border-radius: 10px;
                padding: 12px 15px;
                font-size: 14px;
                color: #6C757D;
            }
            QLineEdit:focus {
                border-color: #427AA2;
            }
        """)
        self.id_input.setMinimumHeight(50)
        
        # Görüntüleme modunda verileri doldur
        if self.view_mode and self.gunce_data:
            self.id_input.setText(self.gunce_data.get('id', ''))
        
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_input)
        layout.addLayout(id_layout)

        # Günce Grubu
        grup_layout = QVBoxLayout()
        grup_label = QLabel("Günce Grubu:")
        grup_label.setFont(QFont("Arial", 14))
        grup_label.setStyleSheet("color: #427AA2; background: transparent;")
        grup_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        self.grup_combo = QComboBox()
        self.grup_combo.addItem("Günce Grubu")
        self.grup_combo.addItem("Genel")
        self.grup_combo.addItem("Sağlık")
        self.grup_combo.addItem("Eğitim")
        self.grup_combo.addItem("Sosyal")
        self.grup_combo.addItem("Ekonomik")
        self.grup_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #E9ECEF;
                border-radius: 10px;
                padding: 12px 15px;
                font-size: 14px;
                color: #2C3E50;
            }
            QComboBox:hover {
                border-color: #427AA2;
            }
            QComboBox:focus {
                border-color: #427AA2;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(ucgen.png);
                width: 20px;
                height: 20px;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #E9ECEF;
                border-radius: 10px;
                selection-background-color: #427AA2;
                selection-color: white;
            }
        """)
        self.grup_combo.setMinimumHeight(50)
        
        # Görüntüleme modunda verileri doldur ve devre dışı bırak
        if self.view_mode and self.gunce_data:
            self.grup_combo.setCurrentText(self.gunce_data.get('grup', ''))
            self.grup_combo.setEnabled(False)
        
        grup_layout.addWidget(grup_label)
        grup_layout.addWidget(self.grup_combo)
        layout.addLayout(grup_layout)

        # Günce Tipi
        tip_layout = QVBoxLayout()
        tip_label = QLabel("Günce Tipi:")
        tip_label.setFont(QFont("Arial", 14))
        tip_label.setStyleSheet("color: #427AA2; background: transparent;")
        tip_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        self.tip_combo = QComboBox()
        self.tip_combo.addItem("Günce Tipi")
        self.tip_combo.addItem("Resmi Evrak")
        self.tip_combo.addItem("Genel Bilgi")
        self.tip_combo.addItem("Sağlık Belgesi")
        self.tip_combo.addItem("Eğitim Raporu")
        self.tip_combo.addItem("Sosyal Aktivite")
        self.tip_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #E9ECEF;
                border-radius: 10px;
                padding: 12px 15px;
                font-size: 14px;
                color: #2C3E50;
            }
            QComboBox:hover {
                border-color: #427AA2;
            }
            QComboBox:focus {
                border-color: #427AA2;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(ucgen.png);
                width: 20px;
                height: 20px;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #E9ECEF;
                border-radius: 10px;
                selection-background-color: #427AA2;
                selection-color: white;
            }
        """)
        self.tip_combo.setMinimumHeight(50)
        
        # Görüntüleme modunda verileri doldur ve devre dışı bırak
        if self.view_mode and self.gunce_data:
            self.tip_combo.setCurrentText(self.gunce_data.get('tip', ''))
            self.tip_combo.setEnabled(False)
        
        tip_layout.addWidget(tip_label)
        tip_layout.addWidget(self.tip_combo)
        layout.addLayout(tip_layout)

        # Açıklama
        aciklama_layout = QVBoxLayout()
        aciklama_label = QLabel("Açıklama:")
        aciklama_label.setFont(QFont("Arial", 14))
        aciklama_label.setStyleSheet("color: #427AA2; background: transparent;")
        aciklama_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        self.aciklama_text = QTextEdit()
        self.aciklama_text.setPlaceholderText("Açıklama")
        self.aciklama_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid #E9ECEF;
                border-radius: 10px;
                padding: 12px 15px;
                font-size: 14px;
                color: #2C3E50;
            }
            QTextEdit:focus {
                border-color: #427AA2;
            }
        """)
        self.aciklama_text.setMinimumHeight(120)
        
        # Görüntüleme modunda verileri doldur ve devre dışı bırak
        if self.view_mode and self.gunce_data:
            self.aciklama_text.setPlainText(self.gunce_data.get('aciklama', ''))
            self.aciklama_text.setReadOnly(True)
        
        aciklama_layout.addWidget(aciklama_label)
        aciklama_layout.addWidget(self.aciklama_text)
        layout.addLayout(aciklama_layout)



        # Belge Ekle butonu (sadece ekleme modunda göster)
        if not self.view_mode:
            self.belge_btn = QPushButton("Belge Ekle")
            self.belge_btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 2px solid #E9ECEF;
                    border-radius: 10px;
                    padding: 12px 15px;
                    font-size: 14px;
                    font-weight: bold;
                    color: #2C3E50;
                }
                QPushButton:hover {
                    border-color: #427AA2;
                    background-color: #F8F9FA;
                }
                QPushButton:pressed {
                    background-color: #E9ECEF;
                }
            """)
            self.belge_btn.setMinimumHeight(50)
            self.belge_btn.clicked.connect(self.belge_ekle)
            layout.addWidget(self.belge_btn)

        layout.addStretch(1)
        return panel

    def create_right_panel(self):
        """Sağ panel - Önizleme alanı"""
        panel = QWidget()
        panel.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 30))
        panel.setGraphicsEffect(shadow)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        # Önizleme başlığı
        preview_label = QLabel("Belge Önizlemesi:")
        preview_label.setFont(QFont("Arial", 14))
        preview_label.setStyleSheet("color: #427AA2; background: transparent;")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(preview_label)
        # Önizleme alanı (yüksekliği azaltıldı)
        self.preview_area = QLabel("Henüz belge eklenmedi")
        self.preview_area.setStyleSheet("""
            QLabel {
                background-color: #F8F9FA;
                border: 2px dashed #E9ECEF;
                border-radius: 10px;
                color: #6C757D;
                font-size: 14px;
            }
        """)
        self.preview_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_area.setMinimumHeight(580)
        self.preview_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.preview_area, 20)
        # Navigasyon butonları (panelin en altında, ortalanmış)
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(10)
        left_btn = QPushButton("<")
        left_btn.setFixedSize(40, 40)
        left_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #E9ECEF;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                color: #2C3E50;
            }
            QPushButton:hover {
                border-color: #427AA2;
                background-color: #F8F9FA;
            }
        """)
        right_btn = QPushButton(">")
        right_btn.setFixedSize(40, 40)
        right_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #E9ECEF;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                color: #2C3E50;
            }
            QPushButton:hover {
                border-color: #427AA2;
                background-color: #F8F9FA;
            }
        """)
        nav_layout.addStretch(1)
        nav_layout.addWidget(left_btn)
        nav_layout.addWidget(right_btn)
        nav_layout.addStretch(1)
        layout.addLayout(nav_layout, 1)
        layout.addStretch(1)
        return panel

    def create_bottom_buttons(self):
        """Alt butonlar"""
        button_widget = QWidget()
        button_widget.setStyleSheet("background: transparent;")
        
        layout = QHBoxLayout(button_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Dışarı Aktar butonu
        export_btn = QPushButton("Dışarı Aktar")
        export_btn.setFont(QFont("Arial", 16, QFont.Weight.DemiBold))
        export_btn.setStyleSheet("""
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
        export_shadow = QGraphicsDropShadowEffect()
        export_shadow.setBlurRadius(16)
        export_shadow.setOffset(0, 4)
        export_shadow.setColor(QColor(66, 122, 162, 60))
        export_btn.setGraphicsEffect(export_shadow)
        export_btn.setFixedSize(180, 55)

        # Kaydet butonu
        save_btn = QPushButton("Kaydet")
        save_btn.setFont(QFont("Arial", 16, QFont.Weight.DemiBold))
        save_btn.setStyleSheet("""
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
        save_btn.setGraphicsEffect(save_shadow)
        save_btn.setFixedSize(180, 55)
        save_btn.clicked.connect(self.kaydet)

        # İptal butonu
        cancel_btn = QPushButton("İptal")
        cancel_btn.setFont(QFont("Arial", 16, QFont.Weight.DemiBold))
        cancel_btn.setStyleSheet("""
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
        cancel_btn.setGraphicsEffect(cancel_shadow)
        cancel_btn.setFixedSize(180, 55)
        cancel_btn.clicked.connect(self.reject)

        layout.addStretch(1)
        if not self.view_mode:
            # Ekleme modu: Kaydet ve İptal
            layout.addWidget(save_btn)
            layout.addWidget(cancel_btn)
        else:
            # Görüntüleme modu: Dışarı Aktar ve İptal
            layout.addWidget(export_btn)
            layout.addWidget(cancel_btn)
        layout.addStretch(1)
        
        return button_widget

    def disari_aktar(self):
        """Günce verilerini dışarı aktarma işlevi"""
        if not self.gunce_data:
            return
            
        # Dosya kaydetme dialog'u
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self,
            "Günce Verilerini Kaydet",
            f"gunce_{self.gunce_data.get('id', 'detay')}.txt",
            "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("GÜNCE DETAYLARI\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Günce ID: {self.gunce_data.get('id', '')}\n")
                    f.write(f"Öğrenci: {self.gunce_data.get('ogrenci', '')}\n")
                    f.write(f"Günce Grubu: {self.gunce_data.get('grup', '')}\n")
                    f.write(f"Günce Tipi: {self.gunce_data.get('tip', '')}\n")
                    f.write(f"Açıklama: {self.gunce_data.get('aciklama', '')}\n")
                    f.write(f"Belge Durumu: {self.gunce_data.get('belge_durumu', '')}\n")
                    f.write(f"Belge Yolu: {self.gunce_data.get('belge', '')}\n")
                    f.write(f"İşlem Tarihi: {self.gunce_data.get('tarih', '')}\n")
                
                print(f"Günce verileri başarıyla kaydedildi: {file_path}")
            except Exception as e:
                print(f"Dosya kaydetme hatası: {e}")

    def belge_ekle(self):
        """Belge ekleme işlevi"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, 
            "Belge Seç", 
            "", 
            "Tüm Dosyalar (*);;Resim Dosyaları (*.png *.jpg *.jpeg);;PDF Dosyaları (*.pdf)"
        )
        
        if file_path:
            self.belge_yolu = file_path
            # Dosya adını göster
            import os
            file_name = os.path.basename(file_path)
            self.preview_area.setText(f"Seçilen Belge:\n{file_name}")
            self.preview_area.setStyleSheet("""
                QLabel {
                    background-color: #E8F5E8;
                    border: 2px solid #28A745;
                    border-radius: 10px;
                    color: #155724;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)

    def kaydet(self):
        """Günce kaydetme işlevi"""
        # Validasyon
        if self.grup_combo.currentText() == "Günce Grubu":
            # Hata mesajı göster
            return
        
        # Belge durumunu kontrol et
        belge_durumu = "Belge Mevcut" if self.belge_yolu else "Belge Bulunmuyor"
        
        # Günce verilerini topla
        gunce_data = {
            'id': self.gunce_id,
            'grup': self.grup_combo.currentText(),
            'tip': self.tip_combo.currentText(),
            'aciklama': self.aciklama_text.toPlainText(),
            'belge': self.belge_yolu,
            'belge_durumu': belge_durumu,
            'ogrenci': self.selected_student
        }
        
        # Burada veritabanına kaydetme işlemi yapılacak
        print("Günce kaydedildi:", gunce_data)
        
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = GunceEkleDialog(selected_student="Naciye Görür (101)")
    result = dialog.exec()
    if result == QDialog.DialogCode.Accepted:
        print("Günce başarıyla eklendi!")
    else:
        print("İşlem iptal edildi.")
    sys.exit(app.exec())

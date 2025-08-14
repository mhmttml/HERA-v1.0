import os
import sys
try:
    from PyQt6.QtCore import QLibraryInfo
    plugin_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
except Exception as e:
    print("Qt plugin path ayarlanamadı:", e, file=sys.stderr)

from PyQt6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QSlider, QButtonGroup, QRadioButton,
                             QWidget, QMessageBox, QFrame)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

class GeziKatilimciDetayiDialog(QDialog):
    def __init__(self, parent=None, katilimci_data=None, gezi_data=None):
        super().__init__(parent)
        self.katilimci_data = katilimci_data or {}
        self.gezi_data = gezi_data or {}
        self.setWindowTitle("Katılımcı Detayı")
        self.setFixedSize(600, 650)
        self.setStyleSheet("background-color: #EBF2FA;")
        self.init_ui()

    def init_ui(self):
        # Ana layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(8)

        # Başlık
        title = QLabel(f"{self.katilimci_data.get('isim', '')} {self.katilimci_data.get('soyisim', '')}")
        title.setFont(QFont("Arial", 24, QFont.Weight.DemiBold))
        title.setStyleSheet("color: #427AA2; text-align: center;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 1. Katılım Onayı Bölümü
        participation_label = QLabel("Geziye katılım sağlanacak mı?")
        participation_label.setFont(QFont("Arial", 16, QFont.Weight.Medium))
        participation_label.setStyleSheet("color: #427AA2;")
        participation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(participation_label)
        layout.addSpacing(-10)  # Soru ile butonlar arası mesafeyi azalt

        # Radio butonları
        radio_layout = QHBoxLayout()
        radio_layout.setSpacing(30)
        radio_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.participation_group = QButtonGroup()
        
        self.yes_radio = QRadioButton("Evet")
        self.yes_radio.setFont(QFont("Arial", 16, QFont.Weight.Medium))
        self.yes_radio.setStyleSheet("""
            QRadioButton {
                font-family: Arial;
                font-size: 20px;
                color: #427AA2;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #A9C5DB;
                border-radius: 9px;
                background: white;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #A5BE00;
                border-radius: 9px;
                background: #A5BE00;
            }
        """)
        self.yes_radio.setChecked(True)
        self.participation_group.addButton(self.yes_radio)
        self.yes_radio.toggled.connect(self.on_participation_changed)
        radio_layout.addWidget(self.yes_radio)

        self.no_radio = QRadioButton("Hayır")
        self.no_radio.setFont(QFont("Arial", 16, QFont.Weight.Medium))
        self.no_radio.setStyleSheet("""
            QRadioButton {
                font-family: Arial;
                font-size: 20px;
                color: #427AA2;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #A9C5DB;
                border-radius: 9px;
                background: white;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #A5BE00;
                border-radius: 9px;
                background: #A5BE00;
            }
        """)
        self.participation_group.addButton(self.no_radio)
        self.no_radio.toggled.connect(self.on_participation_changed)
        radio_layout.addWidget(self.no_radio)

        layout.addLayout(radio_layout)
        layout.addSpacing(0)

        # Katılım onayı bölümü sonu çizgi
        participation_line = QFrame()
        participation_line.setFrameShape(QFrame.Shape.HLine)
        participation_line.setStyleSheet("background-color: #427AA2; border: none; height: 0.5px;")
        layout.addWidget(participation_line)

        # 2. Katılımcı Sayısı Bölümü
        count_label = QLabel("Toplam Katılan Sayısı:")
        count_label.setFont(QFont("Arial", 16, QFont.Weight.Medium))
        count_label.setStyleSheet("color: #427AA2;")
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(count_label)

        # Slider ve değer gösterimi
        slider_layout = QHBoxLayout()
        slider_layout.setSpacing(20)
        slider_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Slider
        self.participant_slider = QSlider(Qt.Orientation.Horizontal)
        self.participant_slider.setMinimum(1)
        self.participant_slider.setMaximum(10)
        self.participant_slider.setValue(1)
        self.participant_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #A9C5DB;
                height: 8px;
                background: #F0F6FB;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #427AA2;
                border: 2px solid #427AA2;
                width: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #A5BE00;
                border: 2px solid #A5BE00;
            }
            QSlider::sub-page:horizontal {
                background: #A5BE00;
                border-radius: 4px;
            }
        """)
        self.participant_slider.valueChanged.connect(self.update_participant_count)
        slider_layout.addWidget(self.participant_slider)

        # Değer gösterimi
        self.count_display = QLabel("1")
        self.count_display.setFont(QFont("Arial", 16, QFont.Weight.Medium))
        self.count_display.setStyleSheet("background-color: #F0F6FB; border: 2px solid #A9C5DB; border-radius: 8px; padding: 8px 16px; color: #427AA2; min-width: 40px; text-align: center;")
        self.count_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider_layout.addWidget(self.count_display)

        layout.addLayout(slider_layout)
        layout.addSpacing(0)

        # Katılımcı sayısı bölümü sonu çizgi
        count_line = QFrame()
        count_line.setFrameShape(QFrame.Shape.HLine)
        count_line.setStyleSheet("background-color: #427AA2; border: none; height: 0.5px;")
        layout.addWidget(count_line)

        # 3. Ödeme Durumu Bölümü
        self.payment_question = QLabel(f"{self.count_display.text()} kişi için ... tl tutarında {self.gezi_data.get('adi', 'Gezi')} ücreti ödendi mi?")
        self.payment_question.setFont(QFont("Arial", 16, QFont.Weight.Medium))
        self.payment_question.setStyleSheet("color: #427AA2;")
        self.payment_question.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.payment_question.setWordWrap(True)
        layout.addWidget(self.payment_question)

        # Radio butonları
        payment_radio_layout = QHBoxLayout()
        payment_radio_layout.setSpacing(30)
        payment_radio_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.payment_group = QButtonGroup()
        
        self.paid_radio = QRadioButton("Ödendi")
        self.paid_radio.setFont(QFont("Arial", 16, QFont.Weight.Medium))
        self.paid_radio.setStyleSheet("""
            QRadioButton {
                font-family: Arial;
                font-size: 20px;
                color: #427AA2;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #A9C5DB;
                border-radius: 9px;
                background: white;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #A5BE00;
                border-radius: 9px;
                background: #A5BE00;
            }
        """)
        self.paid_radio.setChecked(True)
        self.payment_group.addButton(self.paid_radio)
        self.paid_radio.toggled.connect(self.on_payment_changed)
        payment_radio_layout.addWidget(self.paid_radio)

        self.not_paid_radio = QRadioButton("Ödenmedi")
        self.not_paid_radio.setFont(QFont("Arial", 16, QFont.Weight.Medium))
        self.not_paid_radio.setStyleSheet("""
            QRadioButton {
                font-family: Arial;
                font-size: 20px;
                color: #427AA2;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #A9C5DB;
                border-radius: 9px;
                background: white;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #A5BE00;
                border-radius: 9px;
                background: #A5BE00;
            }
        """)
        self.payment_group.addButton(self.not_paid_radio)
        self.not_paid_radio.toggled.connect(self.on_payment_changed)
        payment_radio_layout.addWidget(self.not_paid_radio)

        layout.addLayout(payment_radio_layout)

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

    def on_participation_changed(self):
        """Katılım onayı değiştiğinde dinamik alanları güncelle"""
        if self.yes_radio.isChecked():
            # Evet seçildiğinde dinamik alanları aktif et
            self.participant_slider.setEnabled(True)
            self.count_display.setEnabled(True)
            self.paid_radio.setEnabled(True)
            self.not_paid_radio.setEnabled(True)
            
            # Aktif stil
            self.participant_slider.setStyleSheet("""
                QSlider::groove:horizontal {
                    border: 1px solid #A9C5DB;
                    height: 8px;
                    background: #F0F6FB;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #427AA2;
                    border: 2px solid #427AA2;
                    width: 20px;
                    margin: -6px 0;
                    border-radius: 10px;
                }
                QSlider::handle:horizontal:hover {
                    background: #A5BE00;
                    border: 2px solid #A5BE00;
                }
                QSlider::sub-page:horizontal {
                    background: #A5BE00;
                    border-radius: 4px;
                }
            """)
            
            self.count_display.setStyleSheet("background-color: #F0F6FB; border: 2px solid #A9C5DB; border-radius: 8px; padding: 8px 16px; color: #427AA2; min-width: 40px; text-align: center;")
            
            # Ödeme durumu radio butonlarını da normal stil yap
            self.paid_radio.setStyleSheet("""
                QRadioButton {
                    font-family: Arial;
                    font-size: 20px;
                    color: #427AA2;
                }
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                }
                QRadioButton::indicator:unchecked {
                    border: 2px solid #A9C5DB;
                    border-radius: 9px;
                    background: white;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #A5BE00;
                    border-radius: 9px;
                    background: #A5BE00;
                }
            """)
            
            self.not_paid_radio.setStyleSheet("""
                QRadioButton {
                    font-family: Arial;
                    font-size: 20px;
                    color: #427AA2;
                }
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                }
                QRadioButton::indicator:unchecked {
                    border: 2px solid #A9C5DB;
                    border-radius: 9px;
                    background: white;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #A5BE00;
                    border-radius: 9px;
                    background: #A5BE00;
                }
            """)
            
        else:
            # Hayır seçildiğinde dinamik alanları pasif et
            self.participant_slider.setEnabled(False)
            self.count_display.setEnabled(False)
            self.paid_radio.setEnabled(False)
            self.not_paid_radio.setEnabled(False)
            
            # Pasif stil
            self.participant_slider.setStyleSheet("""
                QSlider::groove:horizontal {
                    border: 1px solid #CCCCCC;
                    height: 8px;
                    background: #F5F5F5;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #CCCCCC;
                    border: 2px solid #CCCCCC;
                    width: 20px;
                    margin: -6px 0;
                    border-radius: 10px;
                }
                QSlider::sub-page:horizontal {
                    background: #CCCCCC;
                    border-radius: 4px;
                }
            """)
            
            self.count_display.setStyleSheet("background-color: #F5F5F5; border: 2px solid #CCCCCC; border-radius: 8px; padding: 8px 16px; color: #999999; min-width: 40px; text-align: center;")
            
            # Ödeme durumu radio butonlarını da pasif stil yap
            self.paid_radio.setStyleSheet("""
                QRadioButton {
                    font-family: Arial;
                    font-size: 20px;
                    color: #999999;
                }
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                }
                QRadioButton::indicator:unchecked {
                    border: 2px solid #CCCCCC;
                    border-radius: 9px;
                    background: white;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #CCCCCC;
                    border-radius: 9px;
                    background: #CCCCCC;
                }
            """)
            
            self.not_paid_radio.setStyleSheet("""
                QRadioButton {
                    font-family: Arial;
                    font-size: 20px;
                    color: #999999;
                }
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                }
                QRadioButton::indicator:unchecked {
                    border: 2px solid #CCCCCC;
                    border-radius: 9px;
                    background: white;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #CCCCCC;
                    border-radius: 9px;
                    background: #CCCCCC;
                }
            """)

    def on_payment_changed(self):
        """Ödeme durumu değiştiğinde dinamik alanları güncelle"""
        if self.paid_radio.isChecked():
            # Ödendi seçildiğinde ödeme sorusunu güncelle
            katilimci_sayisi = self.participant_slider.value()
            self.payment_question.setText(f"{katilimci_sayisi} kişi için ... tl tutarında {self.gezi_data.get('adi', 'Gezi')} ücreti ödendi mi?")
        else:
            # Ödenmedi seçildiğinde ödeme sorusunu güncelle
            katilimci_sayisi = self.participant_slider.value()
            self.payment_question.setText(f"{katilimci_sayisi} kişi için ... tl tutarında {self.gezi_data.get('adi', 'Gezi')} ücreti ödendi mi?")

    def update_participant_count(self, value):
        """Slider değeri değiştiğinde katılımcı sayısını güncelle"""
        self.count_display.setText(str(value))
        
        # Ödeme sorusunu da güncelle
        self.payment_question.setText(f"{value} kişi için ... tl tutarında {self.gezi_data.get('adi', 'Gezi')} ücreti ödendi mi?")

    def get_katilimci_detay_data(self):
        """Katılımcı detay verilerini döndür"""
        katilim_onay = 'Evet' if self.yes_radio.isChecked() else 'Hayır'
        
        if katilim_onay == 'Evet':
            return {
                'katilim_onay': katilim_onay,
                'katilimci_sayisi': self.participant_slider.value(),
                'odeme_durumu': 'Ödendi' if self.paid_radio.isChecked() else 'Ödenmedi'
            }
        else:
            return {
                'katilim_onay': katilim_onay,
                'katilimci_sayisi': 0,
                'odeme_durumu': 'Geçersiz'
            } 
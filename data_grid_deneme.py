import customtkinter
from tkinter import ttk

# Filtreleme seçenekleri için açılacak olan diyalog penceresi sınıfı
class FilterDialog(customtkinter.CTkToplevel):
    def __init__(self, parent, column_id, column_name, x, y):
        super().__init__(parent)
        self.transient(parent) # Ana pencerenin üzerinde kalmasını sağlar
        self.grab_set() # Bu pencere açıkken ana pencereye tıklamayı engeller
        self.title(f"{column_name} Seçenekleri")
        
        self.parent_app = parent
        self.column_id = column_id
        self.column_name = column_name

        # --- Sıralama Bölümü ---
        sort_frame = customtkinter.CTkFrame(self)
        sort_frame.pack(pady=10, padx=10, fill="x")
        customtkinter.CTkLabel(sort_frame, text="Sıralama", font=("Arial", 12, "bold")).pack()
        
        customtkinter.CTkButton(sort_frame, text="Artan Sırala (A-Z, 1-9)", command=self.sort_ascending).pack(fill="x", pady=5)
        customtkinter.CTkButton(sort_frame, text="Azalan Sırala (Z-A, 9-1)", command=self.sort_descending).pack(fill="x", pady=5)

        # --- Filtreleme Bölümü ---
        filter_frame = customtkinter.CTkFrame(self)
        filter_frame.pack(pady=10, padx=10, fill="x")
        customtkinter.CTkLabel(filter_frame, text="Filtreleme", font=("Arial", 12, "bold")).pack()

        self.operator_var = customtkinter.StringVar()
        self.value_entry = None
        self.value_combo = None

        # Sütun tipine göre farklı filtreleme arayüzü oluştur
        if self.column_id in ["isim", "şehir"]:
            customtkinter.CTkLabel(filter_frame, text=f"{column_name} içeren:").pack(anchor="w")
            self.value_entry = customtkinter.CTkEntry(filter_frame)
            self.value_entry.pack(fill="x", pady=5)
            self.operator_var.set("contains")
        elif self.column_id == "ülke":
            customtkinter.CTkLabel(filter_frame, text=f"Ülke seçin:").pack(anchor="w")
            self.value_combo = customtkinter.CTkComboBox(filter_frame, values=["Türkiye", "Almanya"])
            self.value_combo.pack(fill="x", pady=5)
            self.operator_var.set("equals")
        elif self.column_id == "yaş":
            customtkinter.CTkLabel(filter_frame, text="Operatör:").pack(anchor="w")
            self.operator_combo = customtkinter.CTkComboBox(filter_frame, values=["=", ">", "<", ">=", "<="])
            self.operator_combo.pack(fill="x", pady=5)
            self.operator_combo.set("=")
            customtkinter.CTkLabel(filter_frame, text="Değer:").pack(anchor="w")
            self.value_entry = customtkinter.CTkEntry(filter_frame)
            self.value_entry.pack(fill="x", pady=5)

        # --- Kontrol Butonları ---
        action_frame = customtkinter.CTkFrame(self)
        action_frame.pack(pady=10, padx=10, fill="x")

        customtkinter.CTkButton(action_frame, text="Filtreyi Uygula", command=self.apply_filter).pack(side="left", expand=True, padx=5)
        customtkinter.CTkButton(action_frame, text="Filtreyi Temizle", command=self.clear_filter).pack(side="left", expand=True, padx=5)
        
        # Pencereyi konumlandır
        self.geometry(f"+{x}+{y}")
        self.value_entry.focus_set() if self.value_entry else (self.value_combo.focus_set() if self.value_combo else None)


    def sort_ascending(self):
        self.parent_app.sort_data(self.column_id, reverse=False)
        self.destroy()

    def sort_descending(self):
        self.parent_app.sort_data(self.column_id, reverse=True)
        self.destroy()

    def apply_filter(self):
        operator = self.operator_var.get()
        if self.column_id == 'yaş':
             operator = self.operator_combo.get()

        value = ""
        if self.value_entry:
            value = self.value_entry.get()
        elif self.value_combo:
            value = self.value_combo.get()
            
        if value:
            self.parent_app.update_filter(self.column_id, operator, value)
            self.destroy()

    def clear_filter(self):
        self.parent_app.clear_filter(self.column_id)
        self.destroy()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gelişmiş Veri Tablosu")
        self.geometry("800x500")

        # --- Veri ve Durum Yönetimi ---
        self.orijinal_veri = [
            {"isim": "Ahmet Yılmaz", "yaş": 34, "ülke": "Türkiye", "şehir": "İstanbul"},
            {"isim": "Hans Müller", "yaş": 45, "ülke": "Almanya", "şehir": "Berlin"},
            {"isim": "Ayşe Kaya", "yaş": 28, "ülke": "Türkiye", "şehir": "Ankara"},
            {"isim": "Klaus Weber", "yaş": 52, "ülke": "Almanya", "şehir": "Münih"},
            {"isim": "Mehmet Öztürk", "yaş": 41, "ülke": "Türkiye", "şehir": "İzmir"},
            {"isim": "Fatma Demir", "yaş": 25, "ülke": "Türkiye", "şehir": "Bursa"},
            {"isim": "Anna Schmidt", "yaş": 31, "ülke": "Almanya", "şehir": "Hamburg"},
             {"isim": "Mustafa Can", "yaş": 34, "ülke": "Türkiye", "şehir": "Ankara"},
        ]
        
        self.active_filters = {} # Aktif filtreleri tutan sözlük. Örn: {'ülke': ('equals', 'Türkiye')}
        self.sort_info = {"column": None, "reverse": False}

        # --- Arayüz ---
        main_frame = customtkinter.CTkFrame(self)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        customtkinter.CTkButton(main_frame, text="Tüm Filtreleri ve Sıralamayı Sıfırla", command=self.reset_all).pack(pady=10)

        self.sutun_idler = ("isim", "yaş", "ülke", "şehir")
        self.sutun_basliklari = ("İsim Soyisim", "Yaş", "Ülke", "Şehir")

        self.tree = ttk.Treeview(main_frame, columns=self.sutun_idler, show="headings")
        
        for col_id, col_text in zip(self.sutun_idler, self.sutun_basliklari):
            self.tree.heading(col_id, text=col_text)
            self.tree.column(col_id, width=150)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        # Sütun başlığına tıklama olayını bağlama
        self.tree.bind("<Button-1>", self.on_header_click)

        self.apply_filters_and_sort()

    def on_header_click(self, event):
        """Sütun başlığına tıklandığında menüyü açar."""
        if self.tree.identify_region(event.x, event.y) == "heading":
            col_id_num = self.tree.identify_column(event.x)
            column_id = self.tree.column(col_id_num, "id")
            column_name = self.tree.heading(col_id_num, "text")
            FilterDialog(self, column_id, column_name, event.x_root, event.y_root)

    def populate_tree(self, data):
        """Treeview'i verilen veriyle doldurur."""
        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert("", "end", values=[row[col] for col in self.sutun_idler])

    def apply_filters_and_sort(self):
        """Tüm aktif filtreleri ve sıralamayı verilere uygular."""
        filtered_data = self.orijinal_veri[:]

        # Filtreleri uygula
        for col, (op, val) in self.active_filters.items():
            temp_data = []
            for row in filtered_data:
                row_val = row[col]
                if col == 'yaş':
                    try:
                        row_val, val = int(row_val), int(val)
                        if (op == '=' and row_val == val) or \
                           (op == '>' and row_val > val) or \
                           (op == '<' and row_val < val) or \
                           (op == '>=' and row_val >= val) or \
                           (op == '<=' and row_val <= val):
                            temp_data.append(row)
                    except ValueError:
                        continue
                else: # Metin filtreleri
                    row_val, val = str(row_val).lower(), str(val).lower()
                    if (op == 'equals' and row_val == val) or \
                       (op == 'contains' and val in row_val):
                        temp_data.append(row)
            filtered_data = temp_data

        # Sıralamayı uygula
        if self.sort_info["column"]:
            col = self.sort_info["column"]
            is_numeric = col == 'yaş'
            filtered_data.sort(
                key=lambda x: int(x[col]) if is_numeric else str(x[col]).lower(),
                reverse=self.sort_info["reverse"]
            )
        
        self.populate_tree(filtered_data)

    def update_filter(self, column, operator, value):
        """Yeni bir filtre ekler veya günceller."""
        self.active_filters[column] = (operator, value)
        self.apply_filters_and_sort()
    
    def clear_filter(self, column):
        """Belirli bir sütunun filtresini kaldırır."""
        if column in self.active_filters:
            del self.active_filters[column]
            self.apply_filters_and_sort()

    def sort_data(self, column, reverse):
        """Sıralama bilgisini günceller."""
        self.sort_info = {"column": column, "reverse": reverse}
        self.apply_filters_and_sort()

    def reset_all(self):
        """Tüm filtreleri ve sıralamayı sıfırlar."""
        self.active_filters.clear()
        self.sort_info = {"column": None, "reverse": False}
        self.apply_filters_and_sort()


if __name__ == "__main__":
    app = App()
    app.mainloop()
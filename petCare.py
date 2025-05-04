import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from collections import deque
import json 
import os

# Inisialisasi tampilan GUI
ctk.set_appearance_mode("light")  # set ke mode light bisa juga "dark"
ctk.set_default_color_theme("dark-blue")  # Tema warna biru

# Struktur data antrian dan riwayat menggunakan deque dan list
queue = deque()  # Antrian pasien
riwayat = []  # Riwayat pasien yang sudah selesai

# Nama file untuk menyimpan data antrian
FILE_QUEUE = "queue.json"

# Fungsi untuk menyimpan antrian ke file JSON
#-Fungsi ini akan menyimpan isi antrian (queue) ke dalam file queue.json
# Jika file belum ada, maka akan dibuat otomatis
# Format penyimpanan adalah JSON

def simpan_queue():
  with open(FILE_QUEUE, "w") as file_antrian:  # Membuka (atau membuat) file JSON untuk ditulis
    data = list(queue)  # Mengubah deque menjadi list biasa agar bisa disimpan ke JSON ([]) -> ()
    json.dump(data, file_antrian)  # Menyimpan data ke file dalam format JSON

# Fungsi untuk memuat antrian dari file JSON saat program dijalankan
# Jika file queue.json ada, maka isinya dibaca dan dimasukkan ke queue

def muat_queue():
  if os.path.exists(FILE_QUEUE):  # Mengecek apakah file antrian sudah ada di komputer (os)
    with open(FILE_QUEUE, "r") as file_antrian:  # Membuka file JSON dalam mode baca
      data = json.load(file_antrian)  # Membaca isi file dan mengubahnya menjadi list Python
      for pasien in data:  # Menambahkan tiap pasien dari file ke dalam queue
        queue.append(pasien)

# Fungsi untuk memperbarui tampilan daftar antrian di textbox GUI
def update_tampilan_antrian():
  antrian_textbox.configure(state="normal")  # Mengaktifkan textbox supaya bisa diubah
  antrian_textbox.delete("1.0", "end")  # Menghapus seluruh isi dari textbox dari 1 hingga akhir
  if queue:  # Jika queue ada isinya jalankan for
    for i, pasien in enumerate(queue, 1):  # Loop setiap pasien dengan nomor urut mulai dari 1
      estimasi = i * 5  # Estimasi waktu tunggu 5 menit per pasien
      antrian_textbox.insert("end", f"{i}. {pasien['nama']} 🐾 {pasien['jenis']} - {pasien['keluhan']} | ⏳ {estimasi} menit\n")
  else:
    antrian_textbox.insert("end", "Belum ada pasien dalam antrean.")  # Jika kosong
  antrian_textbox.configure(state="disabled")  # Mengunci kembali textbox agar tidak bisa diketik

# Fungsi untuk memperbarui tampilan riwayat pasien
def update_tampilan_riwayat():
  riwayat_textbox.configure(state="normal")
  riwayat_textbox.delete("1.0", "end")
  if riwayat:
    for i, pasien in enumerate(riwayat, 1):
      riwayat_textbox.insert("end", f"{i}. {pasien['nama']} 🐾 {pasien['jenis']} - Selesai\n")  # Menampilkan pasien selesai
  else:
    riwayat_textbox.insert("end", "Belum ada pasien yang selesai.")
  riwayat_textbox.configure(state="disabled")

# Fungsi untuk menambahkan pasien baru ke antrian
def tambah_pasien():
  nama = input_nama.get().strip()  # Ambil input nama dan hapus spasi di ujung
  jenis = pilihan_jenis.get()  # Ambil jenis hewan dari combo box
  keluhan = input_keluhan.get().strip()  # Ambil input keluhan

  if not nama or not jenis or not keluhan:  # Validasi: input gaboleh kosong harus isi nama,jenis,keluhan
    CTkMessagebox(title="Error", message="Semua data harus diisi!", icon="cancel")
    return

  pasien = {"nama": nama, "jenis": jenis, "keluhan": keluhan}  # Buat data pasien dalam dictionary
  queue.append(pasien)  # Tambah pasien ke antrian
  simpan_queue()  # Simpan ke file

  input_nama.delete(0, "end")  # Kosongkan form input nama
  input_keluhan.delete(0, "end")  # Kosongkan form input keluhan
  pilihan_jenis.set("")  # Reset pilihan jenis

  update_tampilan_antrian()  # Update tampilan daftar antrian

# Fungsi untuk memanggil pasien pertama dalam antrian

def panggil_pasien():
  if queue:
    pasien = queue.popleft()  # Ambil pasien pertama dari antrian
    riwayat.append(pasien)  # Masukkan ke riwayat
    simpan_queue()  # Simpan data antrian
    update_tampilan_antrian()  # Update tampilan antrian
    update_tampilan_riwayat()  # Update tampilan riwayat
    CTkMessagebox(title="Panggilan", message=f"📣 Giliran {pasien['nama']} untuk konsultasi!", icon="info")  # Munculkan notifikasi
  else:
    CTkMessagebox(title="Info", message="Tidak ada pasien dalam antrean.", icon="info")  # Jika tidak ada pasien

'''
↓
↓
↓
'''

# Membuat window utama
app = ctk.CTk()
app.title("PetCare - Klinik Hewan")
app.geometry("720x480")
app.resizable(False, False)# Ukuran tidak bisa diubah
# - HEADER
judul = ctk.CTkLabel(app, text="🐾 PetCare - Sistem Antrean Klinik Hewan", font=ctk.CTkFont(size=20, weight="bold"))
judul.pack(pady=(20, 10))

# TabView
tabs = ctk.CTkTabview(app, height=530, width=700)
tabs.pack(pady=10)
tab_input = tabs.add("📝 DAFTAR")
tab_antrian = tabs.add("📋 ANTRIAN")
tab_riwayat = tabs.add("✅ RIWAYAT")

'''--------------------------
  Form Input di Tab "Daftar"
  --------------------------'''
form_frame = ctk.CTkFrame(tab_input)
form_frame.pack(pady=20)

# Input Nama
label_nama = ctk.CTkLabel(form_frame, text="Nama Pemilik:", font=ctk.CTkFont(family="Consolas",size=14, weight="bold"))
label_nama.grid(row=0, column=0, sticky="w", padx=10, pady=5)
input_nama = ctk.CTkEntry(form_frame, width=300, height=35, border_width=0,)
input_nama.grid(row=0, column=1, pady=5)


# Input Jenis Hewan
label_jenis = ctk.CTkLabel(form_frame, text="Jenis Hewan:", font=ctk.CTkFont(family="Consolas",size=14, weight="bold"))
label_jenis.grid(row=1, column=0, sticky="w", padx=10, pady=5)
pilihan_jenis = ctk.CTkComboBox(form_frame, values=["Kucing", "Anjing", "Kelinci", "Burung", "Lainnya"], width=300,  height=35, border_width=0,)
pilihan_jenis.grid(row=1, column=1, pady=5)

# Input Keluhan
label_keluhan = ctk.CTkLabel(form_frame, text="Keluhan:", font=ctk.CTkFont(family="Consolas",size=14, weight="bold"))
label_keluhan.grid(row=2, column=0, sticky="w", padx=10, pady=5)
input_keluhan = ctk.CTkEntry(form_frame, width=300, height=35, border_width=0,)
input_keluhan.grid(row=2, column=1, pady=5)

# Tombol Tambah Pasien
tombol_tambah = ctk.CTkButton(form_frame, text="➕ Tambah ke Antrian →", command=tambah_pasien)
tombol_tambah.grid(row=3, columnspan=2, pady=10)

'''--------------------------
        Tab "Antrian"
  --------------------------'''
antrian_textbox = ctk.CTkTextbox(tab_antrian, width=640, height=260, font=("Consolas", 16))
antrian_textbox.pack(pady=10)
antrian_textbox.insert("end", "Antrean akan muncul di sini...")
antrian_textbox.configure(state="disabled")

tombol_panggil = ctk.CTkButton(tab_antrian, text="📢 Panggil Pasien", command=panggil_pasien) 
tombol_panggil.pack(pady=5)

'''--------------------------
        Tab "Riwayat"
  --------------------------'''
riwayat_textbox = ctk.CTkTextbox(tab_riwayat, width=640, height=300, font=("Consolas", 16))
riwayat_textbox.pack(pady=10)
riwayat_textbox.insert("end", "Riwayat pasien akan tampil di sini...")
riwayat_textbox.configure(state="disabled")

# Muat antrean dari file saat program mulai dijalankan
muat_queue()
update_tampilan_antrian()
update_tampilan_riwayat()

# Menjalankan aplikasi
app.mainloop()

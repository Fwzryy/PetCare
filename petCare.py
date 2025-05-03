import customtkinter as ctk
from CTkMessagebox import ctkmessagebox
from collections import deque
import json 
import os

# Inisialisasi GUI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Struktur data antrian dan riwayat
queue = deque()
riwayat = []

# File penyimpanan
FILE_QUEUE = "queue.json"
#-Fungsi untuk menyimpan antrian ke file JSON
def simpan_queue():
  with open(FILE_QUEUE, "w") as file_antrian:
    data = list(queue) #mengubah objek queue menjadi bentuk list biasa
    json.dump(data, file_antrian) #proses menyimpan data ke dalam file dalam format JSON, json.dump akan menulis data langsung ke dalam file file_antrian, 

#Fungsi untuk memuat antrean file dari JSON
def muat_queue():
  if os.path.exists(FILE_QUEUE):
    with open(FILE_QUEUE, "r") as file_antrian:
      data = json.load(file_antrian)
      for pasien in data:
        queue.append(pasien)
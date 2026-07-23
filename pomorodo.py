import tkinter as tk
import winsound
import json
from datetime import datetime

KAYIT_DOSYASI = "pomodoro.json"

def kayitlari_oku():
    try:
        with open(KAYIT_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def kayit_et(kayitlar):
    with open(KAYIT_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(kayitlar, f, ensure_ascii=False, indent=2)

bugun = datetime.now().strftime("%Y-%m-%d")
kayitlar = kayitlari_oku()
tur = kayitlar.get(bugun, 0)          # bugünkü sayıyı al, yoksa 0

pencere = tk.Tk()
pencere.title("POMORODO")
pencere.attributes("-fullscreen", True)
pencere.configure(bg="#E63946")

merkez = tk.Frame(pencere, bg="#E63946")
merkez.place(relx=0.5, rely=0.5, anchor="center")

hello = tk.Label(merkez, text="HELLO", font=("Impact", 90),
                 fg="#7DD3FC", bg="#E63946")
hello.pack(pady=(0, 10))

sayac_label = tk.Label(merkez, text="25:00", font=("Verdana", 150, "bold"),
                       fg="#FFFFFF", bg="#E63946")
sayac_label.pack()

durum_label = tk.Label(merkez, text="hazır", font=("Segoe UI", 22),
                       fg="#FFD9DC", bg="#E63946")
durum_label.pack(pady=(10, 6))

tur_label = tk.Label(merkez, text=f"bugün: {tur} pomodoro", font=("Segoe UI", 16),
                     fg="#FFD9DC", bg="#E63946")
tur_label.pack(pady=(0, 34))

buton_cerceve = tk.Frame(merkez, bg="#E63946")
buton_cerceve.pack()

kalan_saniye = 25 * 60
calisiyor = False
mola_modu = False

def renk_ayarla(renk):
    pencere.configure(bg=renk)
    merkez.config(bg=renk)
    hello.config(bg=renk)
    sayac_label.config(bg=renk)
    durum_label.config(bg=renk)
    tur_label.config(bg=renk)
    buton_cerceve.config(bg=renk)

def guncelle():
    global kalan_saniye, calisiyor, mola_modu, tur
    if calisiyor and kalan_saniye > 0:
        dk = kalan_saniye // 60
        sn = kalan_saniye % 60
        sayac_label.config(text=f"{dk:02d}:{sn:02d}")
        kalan_saniye -= 1
        pencere.after(1000, guncelle)
    elif kalan_saniye == 0:
        winsound.Beep(1000, 500)
        calisiyor = False
        if mola_modu:                      # mola bitti → odağa dön
            mola_modu = False
            kalan_saniye = 25 * 60
            sayac_label.config(text="25:00")
            durum_label.config(text="bitti — odağa dön")
            hello.config(text="HELLO")
            renk_ayarla("#E63946")
        else:                              # odak bitti → 1 pomodoro tamam!
            tur += 1
            tur_label.config(text=f"bugün: {tur} pomodoro")
            kayitlar[bugun] = tur
            kayit_et(kayitlar)
            mola_modu = True
            kalan_saniye = 5 * 60
            sayac_label.config(text="05:00")
            durum_label.config(text="bitti — mola ver")
            hello.config(text="MOLA")
            renk_ayarla("#2E7D32")

def basla():
    global calisiyor
    if calisiyor:
        return
    calisiyor = True
    if mola_modu:
        durum_label.config(text="mola")
    else:
        durum_label.config(text="odaklanma")
    guncelle()

def duraklat():
    global calisiyor
    calisiyor = False
    durum_label.config(text="duraklatıldı")

def sifirla():
    global kalan_saniye, calisiyor, mola_modu
    calisiyor = False
    mola_modu = False
    kalan_saniye = 25 * 60
    sayac_label.config(text="25:00")
    durum_label.config(text="hazır")
    hello.config(text="HELLO")
    renk_ayarla("#E63946")

tk.Button(buton_cerceve, text="başlat", font=("Segoe UI", 16),
          bg="#7DD3FC", fg="#1A1D20", width=11, relief="flat",
          borderwidth=0, cursor="hand2", command=basla).pack(side="left", padx=10)

tk.Button(buton_cerceve, text="duraklat", font=("Segoe UI", 16),
          bg="#FFFFFF", fg="#1A1D20", width=11, relief="flat",
          borderwidth=0, cursor="hand2", command=duraklat).pack(side="left", padx=10)

tk.Button(buton_cerceve, text="sıfırla", font=("Segoe UI", 16),
          bg="#FFFFFF", fg="#1A1D20", width=11, relief="flat",
          borderwidth=0, cursor="hand2", command=sifirla).pack(side="left", padx=10)

def cik(event=None):
    pencere.destroy()

pencere.bind("<Escape>", cik)

pencere.mainloop()
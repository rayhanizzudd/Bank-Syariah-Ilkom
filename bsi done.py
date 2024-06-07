# import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, simpledialog, Tk,ttk
from libb import *
# from PIL import Image, ImageTk
from libb import cek_no_rek as cnr 
from libb import TransferUang as tfu
from datetime import datetime
from tkinter import *
import locale
from PIL import ImageTk, Image


locale.setlocale(locale.LC_TIME, 'id_ID')
class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BSI App")
        self.saldo = None
        self.i = 0

        #background
       

        self.image = Image.open("E:\\PINDAHAN E\\RANDOM FILE KULIAH\\SEMESTER 3\\FUNCTIONAL PROGRAMING\\NEW PROJEK\\PROJEK PROGRES 1_F3\\bsi.png")
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background_label = Label(self.root, image=self.background_image, bg="black")
        self.background_label.pack()

        # Widgets user
        self.label = Label(self.root, text="Welcome to BANK SYARIAH ILKOM ")
        self.label.place(relx=0.5, rely=0.3, anchor="center")
        self.username_label = Label(self.root, text="Masukkan ID:")
        self.username_label.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry = Entry(self.root)
        self.username_entry.place(relx=0.5, rely=0.45, anchor="center")
        self.password_label = Label(self.root, text="Password:")
        self.password_label.place(relx=0.5, rely=0.5, anchor="center")
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.login_button = Button(self.root, text="Login", command=self.menu_login)
        self.login_button.place(relx=0.5, rely=0.6, anchor="center")



        self.childview_label = Label(self.root, text="", width=69, height=18, bg="white") 

        self.sort_button = Button(self.root, text="Sort ID",width= 10, bg="grey", command=lambda:self.urutkan(0))
        self.sort2_button = Button(self.root, text="Sort Name",width= 10, bg="grey", command=lambda:self.urutkan(1))
        self.sort3_button = Button(self.root, text="Sort Saldo",width= 10, bg="grey", command=lambda:self.urutkan(2))

        # self.footer = Label(self.root, text="", width=69, height= 2,bg="blue" )
        self.sidebar = Label(self.root, text="", width=20, height= 100, font=("Courier", 10), bg="gray", fg = "white")
        self.atasbar = Label(self.root, text="", width=100, height= 2, font=("Courier", 10), bg="gray", fg = "white")
        self.childhome_label = Label(self.root, text="HALOO, ADMIN",font=("Helvetica", 24)) 
        self.greeting_label = Label(self.root, text=f"SELAMAT DATANG DI BANK BSI", bg="gray")
        self.admin_label = Label(self.root, text=f"ADMINISTRATOR", bg="gray")
        self.home_button = Button(self.root, text=" Home Page", width=20, command=self.homepageadmin)
        self.view_button = Button(self.root, text="View Data", width= 20, command=self.viewadmin)
        # self.search_button = Button(self.root, text="Searching Data", width= 20, command=self.search)
        self.exit_button = Button(self.root, text="Exit", width= 20, command=self.root.destroy)
        self.table_frame = Frame(self.childview_label)

        

        

        #scrollbar
        self.table_scroll = Scrollbar(self.table_frame)
        self.table_scroll.pack(side=RIGHT, fill=Y)

        self.table_scroll = Scrollbar(self.table_frame,orient='horizontal')
        self.table_scroll.pack(side= BOTTOM,fill=X)
        self.tables = ttk.Treeview(self.table_frame,yscrollcommand=self.table_scroll.set, xscrollcommand =self.table_scroll.set)
        self.table_scroll.config(command=self.tables.yview)
        self.table_scroll.config(command=self.tables.xview)
        self.tables.bind("<Double-1>", self.double_click_seleksi) 

    def menu_login(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()
        admin_only = 9
        admin_pass = 99
        
        if int(entered_username) == admin_only and int(entered_password) == admin_pass:
            return self.homepageadmin()

        try:
            idd,pin=int(entered_username),(int(entered_password))
        except:
            return messagebox.showinfo("Peringatan", "Pastikan Inputan berupa angka")

        self.login = login(idd,pin)

        # if True:
        if self.login.status():
            print(self.login.namauser())
            self.saldo = saldo(idd)
            self.show_main_menu()

            # print("log berhasil")

        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


    def show_main_menu(self):
        # Clear login widgets
        self.label.place_forget()
        self.username_label.place_forget()
        self.username_entry.place_forget()
        self.password_label.place_forget()
        self.password_entry.place_forget()
        self.login_button.place_forget()

  # Widgets for main menu
        self.saldo_label = Label(self.root, text=f"SELAMAT DATANG DI BANK BSI\n {self.login.namauser()}", fg="white",bg="black", font=("arial",14))
        self.saldo_label.place(x=220,y=20)
        self.view_button = Button(self.root, text="Lihat Saldo", command=self.view_balance)
        self.view_button.place(x=10,y=220)
        self.transfer_button = Button(self.root, text="Tranfer uang", command=self.tamptransfer)
        self.transfer_button.place(x=10,y=270)
        self.exit_button = Button(self.root, text="Exit", command=self.root.destroy)
        self.exit_button.place(x=10,y=320)
        self.tambah_button = Button(self.root, text="Tambah Uang", command=self.deposit)
        self.tambah_button.place(x=605,y=270)
        self.ambil_button = Button(self.root, text="Ambil Uang", command=self.withdraw)
        self.ambil_button.place(x=615,y=220)
        self.warisan_button = Button(self.root, text="Pembagian warisan", command=self.mainwarisan)
        self.warisan_button.place(x=575,y=320)


    def double_click_seleksi(self, event):
        # Mendapatkan item yang dipilih pada double-click
        item_terpilih = self.tables.selection()
        print(item_terpilih)


    def view_balance(self):
        messagebox.showinfo("Saldo", f"Saldo Anda: {self.saldo.view()}")

    def deposit(self):
        amount = simpledialog.askinteger("Jumlah", "Masukkan jumlah uang:")
        # a = self.saldo.tambahsaldo(float(simpledialog.askstring("Jumlah", "Masukkan jumlah uang:")))
        if amount is not None:
            print("saldo bertambah", amount)
            # self.view_balance()
            self.saldo.tambahsaldo(amount)
            if messagebox.askquestion("TRANSAKSI BERHASIL", f"{self.saldo.view()}\nLANJUT TRANSAKSI??") == "yes":
                #hapus button
                self.ambil_button.place_forget()
                self.tambah_button.place_forget()
                self.warisan_button.place_forget()
                self.view_button.place_forget()
                self.transfer_button.place_forget()
                #tampil lagi
                self.pm()
            else : 
                self.root.destroy()

    def pm(self):
        self.saldo_label.pack_forget()
        self.exit_button.place_forget()
        self.show_main_menu()

    def withdraw(self):
        # menghapus button sebelumnya
        self.ambil_button.place_forget()
        self.tambah_button.place_forget()
        self.warisan_button.place_forget()
        self.view_button.place_forget()
        self.transfer_button.place_forget()

        #mengganti dengan nominal
        piluang = ("50.000", "100.000", "150.000","200.000") #immutable
        self.uang1_button = Button(self.root, text=f"Rp {piluang[0]}", command=lambda : self.ambil(50000))
        self.uang1_button.place(x=10,y=220)
        self.uang2_button = Button(self.root, text=f"Rp {piluang[1]}", command=lambda : self.ambil(100000))
        self.uang2_button.place(x=10,y=270)
        self.uang3_button = Button(self.root, text=f"Rp {piluang[2]}", command=lambda : self.ambil(150000))
        self.uang3_button.place(x=615,y=220)
        self.uang4_button = Button(self.root, text=f"Rp {piluang[3]}", command=lambda : self.ambil(200000))
        self.uang4_button.place(x=615,y=270)
        self.uang7_button = Button(self.root, text="Jumlah Lainnya", command=self.ambil)
        self.uang7_button.place(x=590,y=320)


    def ambil(self,amount=""): 
        if amount == "":
            amount = simpledialog.askinteger("Jumlah", "Masukkan jumlah uang:") #muncul dialog ketika ambil uang tidak ada dipilihan
        # print(amount)
        # print(type(amount))
        if amount != 0 and amount <= self.saldo.duit():
            print("saldo berkurang", amount)
            self.saldo.kurangsaldo(amount)
            # self.view_balance()
            if messagebox.askquestion("TRANSAKSI BERHASIL", "LANJUT TRANSAKSI??") == "yes":

                # megnhilangkan button pada tampilan ambil uang
                self.saldo_label.pack_forget()
                self.uang1_button.place_forget()
                self.uang2_button.place_forget()
                self.uang3_button.place_forget()
                self.uang4_button.place_forget()
                self.uang7_button.place_forget()
                self.exit_button.place_forget()
                #kembali ke menu utama
                # self.show_main_menu()
                self.pm()
            else:
                self.root.destroy()

        else:
            messagebox.showerror("Error", "Jumlah penarikan tidak valid atau melebihi saldo.")
    
    def mainwarisan(self):
        self.ambil_button.place_forget()
        self.tambah_button.place_forget()
        self.warisan_button.place_forget()
        self.view_button.place_forget()
        self.transfer_button.place_forget()
        
        # mengganti dengan Warisan
        self.warisan_label = Label(self.root,text="Perhitungan Harta Warisan (Trial)")
        self.warisan_label.place(relx=0.5, rely=0.15, anchor="center")
        self.warisan_yatim_button = Button(self.root,text="Jika Yatim",command=self.inputwarisyatim)
        self.warisan_yatim_button.place(relx=0.5, rely=0.3, anchor="center")
        self.warisan_piatu_button = Button(self.root,text="Jika Piatu",command=self.inputwarispiatu)
        self.warisan_piatu_button.place(relx=0.5, rely=0.4, anchor="center")
        self.warisan_yatimpiatu_button = Button(self.root,text="Jika Yatim Piatu",command=self.inputwarisyatimpiatu)
        self.warisan_yatimpiatu_button.place(relx=0.5, rely=0.5, anchor="center")
        # Tombol Tombol warisan sesuai dengan ketentuan
        
        #menampilkan
    def inputwarisyatim(self):
        self.ambil_button.place_forget()
        self.tambah_button.place_forget()
        self.warisan_button.place_forget()
        self.view_button.place_forget()
        self.transfer_button.place_forget()
        self.warisan_yatimpiatu_button.place_forget()
        self.warisan_piatu_button.place_forget()
        self.warisan_yatim_button.place_forget()
        self.warisan_label.place_forget()
    
        
        self.inputyatim_label = Label(self.root,text="Perhitungan Harta Warisan Yatim")
        self.inputyatim_label.place(relx=0.5, rely=0.15, anchor="center")
        self.input_anaklaki1_label = Label(self.root,text="Masukkan Jumlah Anak Laki Laki")
        self.input_anaklaki1_label.place(relx=0.5, rely=0.2, anchor="center")
        self.input_anakpr1_label = Label(self.root,text="Masukkan Jumlah Anak Perempuan")
        self.input_anakpr1_label.place(relx=0.5, rely=0.3, anchor="center")
        self.next_warisyatim_button = Button(self.root,text="Next",command=self.warisyatim)
        self.next_warisyatim_button.place(x=590,y=320)
        self.input_anaklaki1_entry = Entry(self.root)
        self.input_anaklaki1_entry.place(relx=0.5, rely=0.25, anchor="center")
        self.input_anakpr1_entry = Entry(self.root)
        self.input_anakpr1_entry.place(relx=0.5, rely=0.35, anchor="center") 
        
        
        
    def inputwarispiatu(self):
        self.ambil_button.place_forget()
        self.tambah_button.place_forget()
        self.warisan_button.place_forget()
        self.view_button.place_forget()
        self.transfer_button.place_forget()
        self.warisan_yatimpiatu_button.place_forget()
        self.warisan_piatu_button.place_forget()
        self.warisan_yatim_button.place_forget()
        self.warisan_label.place_forget()
        
        self.inputpiatu_label = Label(self.root,text="Perhitungan Harta Warisan Piatu")
        self.inputpiatu_label.place(relx=0.5, rely=0.15, anchor="center")
        self.input_anaklaki2_label = Label(self.root,text="Masukkan Jumlah Anak Laki Laki")
        self.input_anaklaki2_label.place(relx=0.5, rely=0.2, anchor="center")
        self.input_anakpr2_label = Label(self.root,text="Masukkan Jumlah Anak Perempuan")
        self.input_anakpr2_label.place(relx=0.5, rely=0.3, anchor="center")
        self.next_warispiatu_button = Button(self.root,text="Next",command=self.warispiatu)
        self.next_warispiatu_button.place(x=590,y=320)
        self.input_anaklaki2_entry = Entry(self.root)
        self.input_anaklaki2_entry.place(relx=0.5, rely=0.25, anchor="center")
        self.input_anakpr2_entry = Entry(self.root)
        self.input_anakpr2_entry.place(relx=0.5, rely=0.35, anchor="center") 
        
    def inputwarisyatimpiatu(self):
        self.ambil_button.place_forget()
        self.tambah_button.place_forget()
        self.warisan_button.place_forget()
        self.view_button.place_forget()
        self.transfer_button.place_forget()
        self.warisan_yatimpiatu_button.place_forget()
        self.warisan_piatu_button.place_forget()
        self.warisan_yatim_button.place_forget()
        self.warisan_label.place_forget()
        
        self.inputyatimpiatu_label = Label(self.root,text="Perhitungan Harta Warisan Yatim Piatu")
        self.inputyatimpiatu_label.place(relx=0.5, rely=0.15, anchor="center")
        self.input_anaklaki3_label = Label(self.root,text="Masukkan Jumlah Anak Laki Laki")
        self.input_anaklaki3_label.place(relx=0.5, rely=0.2, anchor="center")
        self.input_anakpr3_label = Label(self.root,text="Masukkan Jumlah Anak Perempuan")
        self.input_anakpr3_label.place(relx=0.5, rely=0.3, anchor="center")
        self.next_warisyatimpiatu_button = Button(self.root,text="Next",command=self.warisyatimpiatu)
        self.next_warisyatimpiatu_button.place(x=590,y=320)

        self.input_anaklaki3_entry = Entry(self.root)
        self.input_anaklaki3_entry.place(relx=0.5, rely=0.25, anchor="center")
        self.input_anakpr3_entry = Entry(self.root)
        self.input_anakpr3_entry.place(relx=0.5, rely=0.35, anchor="center") 

        
    def warisyatim(self):
        self.ambil_button.place_forget()
        self.tambah_button.place_forget()
        self.warisan_button.place_forget()
        self.view_button.place_forget()
        self.transfer_button.place_forget()
        self.warisan_yatimpiatu_button.place_forget()
        self.warisan_piatu_button.place_forget()
        self.warisan_yatim_button.place_forget()
        self.warisan_label.place_forget()
        self.next_warisyatim_button.place_forget()

        hasil = self.saldo.pembagian_harta_suami(int(self.input_anaklaki1_entry.get()), int(self.input_anakpr1_entry.get()))
        print(hasil)

        
        self.warisan_yatim_label = Label(self.root,text="Pembagian Harta Warisan Yatim")
        self.warisan_yatim_label.place(relx=0.5, rely=0.15, anchor="center")
        self.hasil_ibu_label = Label(self.root,text="Hasil Pembagian Harta Waris untuk Ibu")
        self.hasil_ibu_label.place(relx=0.5, rely=0.2, anchor="center")
        self.hasil_anaklaki1_label = Label(self.root,text="Hasil Pembagian Harta Waris untuk Masing Masing Anak Laki Laki")
        self.hasil_anaklaki1_label.place(relx=0.5, rely=0.3, anchor="center")
        self.hasil_anakpr1_label = Label(self.root,text="Hasil Pembagian Harta Waris untuk Masing Masing Anak Perempuan")
        self.hasil_anakpr1_label.place(relx=0.5, rely=0.4, anchor="center")
        self.hasil_saudaradekat1_label = Label(self.root,text="Hasil Pembagian Harta Waris untuk Saudara Terdekat")
        self.hasil_saudaradekat1_label.place(relx=0.5, rely=0.5, anchor="center")
        self.hasil_ibu_entry = Entry(self.root)
        self.hasil_ibu_entry.insert(0, hasil[2])
        self.hasil_ibu_entry.place(relx=0.5, rely=0.25, anchor="center")
        self.hasil_ibu_entry.config(state="readonly")
        self.hasil_anaklaki1_entry = Entry(self.root)
        self.hasil_anaklaki1_entry.insert(0, hasil[0])
        self.hasil_anaklaki1_entry.place(relx=0.5, rely=0.35, anchor="center")
        self.hasil_anaklaki1_entry.config(state="readonly")
        self.hasil_anakpr1_entry = Entry(self.root)
        self.hasil_anakpr1_entry.insert(0, hasil[1])
        self.hasil_anakpr1_entry.place(relx=0.5, rely=0.45, anchor="center")
        self.hasil_anakpr1_entry.config(state="readonly")
        self.hasil_saudaradekat1_entry = Entry(self.root)
        self.hasil_saudaradekat1_entry.insert(0, hasil[3])
        self.hasil_saudaradekat1_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.hasil_saudaradekat1_entry.config(state="readonly")
        
    def warispiatu(self):
        self.ambil_button.place_forget()
        self.tambah_button.place_forget()
        self.warisan_button.place_forget()
        self.view_button.place_forget()
        self.transfer_button.place_forget()
        self.warisan_yatimpiatu_button.place_forget()
        self.warisan_piatu_button.place_forget()
        self.warisan_yatim_button.place_forget()
        self.inputpiatu_label.place_forget()
        self.next_warispiatu_button.place_forget()
        self.warisan_label.place_forget()
        

        hasil2 = self.saldo.pembagian_harta_istri(int(self.input_anaklaki2_entry.get()), int(self.input_anakpr2_entry.get()))
        print(hasil2)

        self.warisan_piatu_label = Label(self.root,text="Pembagian Harta Warisan Piatu")
        self.warisan_piatu_label.place(relx=0.5, rely=0.15, anchor="center")
        self.hasil_ayah_label = Label(self.root,text="Hasil Pembagian Harta Waris untuk Ayah")
        self.hasil_ayah_label.place(relx=0.5, rely=0.2, anchor="center")
        self.hasil_anaklaki2_label = Label(self.root,text="Hasil Pembagian Harta Waris untuk Masing Masing Anak Laki Laki")
        self.hasil_anaklaki2_label.place(relx=0.5, rely=0.3, anchor="center")
        self.hasil_anakpr2_label = Label(self.root,text="Hasil Pembagian Harta Waris untuk Masing Masing Anak Perempuan")
        self.hasil_anakpr2_label.place(relx=0.5, rely=0.4, anchor="center")
        self.hasil_saudaradekat2_label = Label(self.root,text="Hasil Pembagian Harta Waris untuk Saudara Terdekat")
        self.hasil_saudaradekat2_label.place(relx=0.5, rely=0.5, anchor="center")

        self.hasil_ayah_entry = Entry(self.root)
        self.hasil_ayah_entry.place(relx=0.5, rely=0.25, anchor="center")
        self.hasil_ayah_entry.insert(0, hasil2[2])
        self.hasil_ayah_entry.config(state="readonly")
        self.hasil_anaklaki2_entry = Entry(self.root)
        self.hasil_anaklaki2_entry.place(relx=0.5, rely=0.35, anchor="center")
        self.hasil_anaklaki2_entry.insert(0, hasil2[0])
        self.hasil_anaklaki2_entry.config(state="readonly")
        self.hasil_anakpr2_entry = Entry(self.root)
        self.hasil_anakpr2_entry.place(relx=0.5, rely=0.45, anchor="center")
        self.hasil_anakpr2_entry.insert(0, hasil2[1])
        self.hasil_anakpr2_entry.config(state="readonly")
        self.hasil_saudaradekat2_entry = Entry(self.root)
        self.hasil_saudaradekat2_entry.insert(0, hasil2[3])
        self.hasil_saudaradekat2_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.hasil_saudaradekat2_entry.config(state="readonly")
  
        
    def warisyatimpiatu(self):
        #hapus
        self.ambil_button.place_forget()
        self.tambah_button.place_forget()
        self.warisan_button.place_forget()
        self.view_button.place_forget()
        self.transfer_button.place_forget()
        self.warisan_yatimpiatu_button.place_forget()
        self.warisan_piatu_button.place_forget()
        self.warisan_yatim_button.place_forget()
        self.next_warisyatimpiatu_button.place_forget()
        self.inputyatimpiatu_label.place_forget()
        self.warisan_label.place_forget()

        #tampill

        hasil3 = self.saldo.pembagian_harta_anak(int(self.input_anaklaki3_entry.get()), int(self.input_anakpr3_entry.get()))
        print(hasil3)

        self.warisan_yatimpiatu_label = Label(self.root,text="Pembagian Harta Warisan Yatim Piatu")
        self.warisan_yatimpiatu_label.place(relx=0.5, rely=0.15, anchor="center")
        self.hasil_anaklaki3_label = Label(self.root,text="Hasil Pembagian Harta Waris untuk Masing Masing Anak Laki Laki")
        self.hasil_anaklaki3_label.place(relx=0.5, rely=0.2, anchor="center")
        self.hasil_anakpr3_label = Label(self.root,text="Hasil Pembagian Harta Waris untuk Masing Masing Anak Perempuan")
        self.hasil_anakpr3_label.place(relx=0.5, rely=0.3, anchor="center")
        self.hasil_saudaradekat3_label = Label(self.root,text="Hasil Pembagian Harta Waris untuk Saudara Terdekat  ")
        self.hasil_saudaradekat3_label.place(relx=0.5, rely=0.4, anchor="center")
        # self.hasil_ayah_entry = Entry(self.root)
        self.hasil_anaklaki3_entry = Entry(self.root)
        self.hasil_anaklaki3_entry.place(relx=0.5, rely=0.25, anchor="center")
        self.hasil_anaklaki3_entry.insert(0, hasil3[0])
        self.hasil_anaklaki3_entry.config(state="readonly")
        self.hasil_anakpr3_entry = Entry(self.root)
        self.hasil_anakpr3_entry.place(relx=0.5, rely=0.35, anchor="center") 
        self.hasil_anakpr3_entry.insert(0, hasil3[1])
        self.hasil_anakpr3_entry.config(state="readonly")
        self.hasil_saudaradekat3_entry = Entry(self.root)
        self.hasil_saudaradekat3_entry.place(relx=0.5, rely=0.45, anchor="center")
        self.hasil_saudaradekat3_entry.insert(0, hasil3[2])
        self.hasil_saudaradekat3_entry.config(state="readonly")
 
    def tamptransfer(self):
        self.ambil_button.place_forget()
        self.tambah_button.place_forget()
        self.warisan_button.place_forget()
        self.view_button.place_forget()
        self.transfer_button.place_forget()
         #mengganti dengan tf
        self.rek_label = Label(self.root, text="Masukkan rekening")
        self.rek_entry = Entry(self.root)
        self.next_button1 = Button(self.root, text="Nexttt", command=self.show2)


        self.nominal_label = Label(self.root, text="Masukkan nominal")
        self.nominal_entry = Entry(self.root)
        # self.next_button22 = Button(self.root, text="Next", command=lambda:tfu(int(self.username_entry.get()), cnr(int(self.rek_entry.get()))[0][0], int(self.nominal_entry.get())))
        self.next_button22 = Button(self.root, text="Next", command=self.transfer)
        self.hapus_button = Button(self.root, text="Back", command=self.backTF)
        self.exit_button = Button(self.root, text="Exit", command=self.root.destroy)


        self.rek_label.place(relx=0.5, rely=0.4, anchor="center")
        self.rek_entry.place(relx=0.5, rely=0.45, anchor="center")
        self.next_button1.place(relx=0.5, rely=0.52, anchor="center")
        self.exit_button.place(x=10,y=320)
    
    def backTF(self):
        self.label.place_forget()
        self.next_button1.place_forget()
        self.rek_label.place_forget()
        self.rek_entry.place_forget()
        self.rek_entry.place_forget()
        self.inforek_label.place_forget()
        self.nominal_label.place_forget()
        self.nominal_entry.place_forget()
        self.hapus_button.place_forget()
        self.next_button22.place_forget()
        # self.show_main_menu()

    def show2(self):
        if self.username_entry.get() == self.rek_entry.get():
            messagebox.showwarning("Peringatan", "Isi omor rekening Tujuan dengan benar!!!")
            self.rek_entry.delete(0,"end")
            return
        self.datatujuanTF = cnr(int(self.rek_entry.get()))[0]
        if self.rek_entry.get() and bool(self.datatujuanTF):
            self.next_button1.place_forget()
            self.rek_label.place_forget()
            self.rek_entry.place_forget()
            
            self.inforek_label = Label(self.root, text= f"Nama Tujuan: \n{self.datatujuanTF[2]}")
            self.rek_label.place(relx=0.5, rely=0.3, anchor="center")
            self.rek_label.config(text="rekening :")
            self.rek_entry.config(state="readonly")

            # Tombol "Tambah Uang" di sebelah kanan atas
            self.rek_entry.place(relx=0.5, rely=0.35, anchor="center")
            # Tombol "Lihat Saldo" di kiri
            self.inforek_label.place(relx=0.5, rely=0.42, anchor="center")

            self.nominal_label.place(relx=0.5, rely= 0.49, anchor="center")
            # Tombol "Transfer" di kiri
            self.nominal_entry.place(relx=0.5, rely=0.54, anchor="center")
            # Tombol "Transfer" di kiri
            self.hapus_button.place(relx=0.43, rely=0.60, anchor="center")  
            # Tombol "Transfer" di kiri
            self.next_button22.place(relx=0.57, rely=0.60, anchor="center")

    def transfer(self):
        if tfu(int(self.username_entry.get()), self.datatujuanTF[0], int(self.nominal_entry.get())):
            tanggal = datetime.now().strftime("%A, %d %B %Y")
            messagebox.showinfo("Notifikasi", f"Transfer Berhasil\n\nNama Penerima\t: {self.datatujuanTF[2]}\nJumlah Transfer\t: {int(self.nominal_entry.get())}\n\nTanggal Transfer\t: {tanggal}")
            print(f"uang ditransfer {self.nominal_entry.get()}")
            # self.backTF()
        if messagebox.askquestion("QUESTION", "ingin melanjutkan transaksi?" ) == "yes":
            self.pm()
            self.backTF()
        else : 
            self.root.destroy()

    #AAAAAAAAAAAAAAAAADDMIIIINNN
    def homepageadmin(self):
        # Clear login widgets
        self.label.place_forget()
        self.username_label.place_forget()
        self.username_entry.place_forget()
        self.password_label.place_forget()
        self.password_entry.place_forget()
        self.login_button.place_forget()
        self.sort_button.place_forget()
        self.sort2_button.place_forget()
        self.sort3_button.place_forget()
        # self.footer.place_forget()
        # self.cari_button.place_forget()
        self.childview_label.place_forget()
        # self.cari_entry.place_forget()
        self.table_frame.pack_forget()

        # Widgets for main menu
        self.greeting_label.place(x=300,y=10)
        self.admin_label.place(x=35,y=10)
        self.sidebar.place(x=0, y=0)
        self.atasbar.place(x=0, y=0)
        self.childhome_label.place(x=188, y=60)

        self.home_button.place(x=10,y=40)
        self.view_button.place(x=10,y=90)
        # self.search_button.place(x=10,y=140)
        self.exit_button.place(x=10,y=450)

    def viewadmin(self):
        self.childhome_label.place_forget()
        # self.cari_button.place_forget()
        # self.cari_entry.place_forget()
        self.table_frame.pack_forget()
        self.table()

        #kanan
        self.childview_label.place(x=188, y=60)
        self.sort_button.place(x=597,y=350)
        self.sort2_button.place(x=497,y=350)
        self.sort3_button.place(x=397,y=350)
        # self.footer.place(x=188, y=450)

    def view_balance(self):
        messagebox.showinfo("Saldo", f"Saldo Anda: {self.saldo.view()}")


    def table(self):

        # self.tabell = self.saldo , = 
        self.table_frame.pack()

        self.tables.pack()


        #define our column
        
        self.tables['columns'] = ('id_user', 'user_name', 'saldo_user')

        # format our column
        self.tables.column("#0", width=0,  stretch=NO)
        self.tables.column("id_user",anchor=CENTER, width=135)
        # self.tables.column("pin_user",anchor=CENTER,width145)
        self.tables.column("user_name",anchor=CENTER,width=165)
        self.tables.column("saldo_user",anchor=CENTER,width=165)

        #Create Headings 
        self.tables.heading("#0",text="",anchor=CENTER)
        self.tables.heading("id_user",text="id_user",anchor=CENTER)
        # self.tables.heading("pin_user",text="pin_user",anchor=CENTER)
        self.tables.heading("user_name",text="user_name",anchor=CENTER)
        self.tables.heading("saldo_user",text="saldo_user",anchor=CENTER)

        try:
            conn_string = "host='localhost' port=5432 dbname='funcpro' user='postgres' password='QWERTY30'"
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            query = f"SELECT * from user_saldoo"
            # query = f"SELECT up.id_user, up.pin_user, up.user_name, us.saldo_user FROM user_pin up JOIN user_saldo us ON up.id_user = us.id_user;"
            cursor.execute(query)
            self.dt = cursor.fetchall()
            for row in self.dt:
                self.tables.insert("", "end", values=row)

            # Closing the cursor and connection after use
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Error connecting to the database: {e}")

        

    def urutkan(self,kolom):
        #megngapus elemen
        self.tables.delete(*self.tables.get_children())
        conn_string = "host='localhost' port=5432 dbname='funcpro' user='postgres' password='QWERTY30'"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_saldoo")
        hasil = cursor.fetchall()

        #menulis ulang (HOF)
        for row in sorted(hasil, key=lambda x: x[kolom]):
            self.tables.insert("", "end", values=row)
        cursor.close()
        conn.close()


if __name__ == "__main__":
    root = Tk()
    app = BankApp(root)
    root.geometry("700x500")
    root.mainloop()

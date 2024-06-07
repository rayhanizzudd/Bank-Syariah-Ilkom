import psycopg2, locale


class login:
    def __init__(self,iduser, pin):
        self.Iduser = None
        self.Log = False
        conn_string = "host='localhost' port=5432 dbname='funcpro' user='postgres' password='QWERTY30'" #pw master 123456
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        query = f"SELECT * FROM user_pin where id_user = {iduser}"
        cursor.execute(query)
        self.dt = cursor.fetchall()
        print(self.dt)

        #ternary
        if len(self.dt) != 0:
            self.Log = True  if pin == self.dt[0][1] else "" if iduser == self.dt[0][0] else ""
                
            self.Iduser = self.dt[0][0] if self.Log else ""
        else : 
            self.Iduser = False

    def view(self):
        return self.Iduser
    def status(self):
        return self.Log
    def namauser(self):
        return self.dt[0][2]        
    

class saldo:
    def __init__(self,iduser):
        self.Saldo = None
        self.Iduser = iduser
        self.bagian_anak_laki = 0
        self.bagian_anak_perempuan = 0
        self.bagian_suami = 0
        self.bagian_istri = 0
        self.sisa_kerabat = 0
        self.anak_laki = 0
        self.anak_perempuan = 0
         # self.hasil_warisan = 0
        
        conn_string = "host='localhost' port=5432 dbname='funcpro' user='postgres' password='QWERTY30'" #pw master 123456
        self.conn = psycopg2.connect(conn_string)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"SELECT * FROM user_saldoo where id_user = {self.Iduser}")
        self.Saldo = self.cursor.fetchall()[0][2]
        

    def view(self):
        self.cursor.execute(f"SELECT * FROM user_saldoo where id_user = {self.Iduser}")
        self.Saldo = self.cursor.fetchall()[0][2]
        if self.Saldo == None:
            return "nothing"
        locale.setlocale(locale.LC_ALL,"id_ID")
        uang = locale.currency(self.Saldo, grouping=True).replace(",00","").replace("Rp","Rp ")
        return uang
    
    def duit(self):
        return self.Saldo

    def tambahsaldo(self,inpsaldo):
        self.Saldo += inpsaldo
        self.cursor.execute(f"UPDATE user_saldoo SET saldo_user = {self.Saldo} WHERE id_user = {self.Iduser}")
        self.conn.commit()

    def kurangsaldo(self,inpsaldo):
        self.Saldo -= inpsaldo
        self.cursor.execute(f"UPDATE user_saldoo SET saldo_user = {self.Saldo} WHERE id_user = {self.Iduser}")
        self.conn.commit()



    #WARISAN  
    def pembagian_harta_anak(self,a,b):
        self.anak_laki = a
        self.anak_perempuan = b
        harta3 = print(f"Saldo yang tersisa: Rp {self.Saldo} ")
        if self.anak_laki >= 1 and self.anak_perempuan == 0:
            self.bagian_anak_laki = self.Saldo / self.anak_laki
        elif self.anak_laki == 0 and self.anak_perempuan == 1:
            self.bagian_anak_perempuan = self.Saldo * 1/2
            self.sisa_kerabat = self.Saldo - self.bagian_anak_perempuan
        elif self.anak_laki == 0 and self.anak_perempuan > 1:
            self.bagian_anak_perempuan = (self.Saldo * 2/3)
            self.bagian_anak_masing2 = self.bagian_anak_perempuan / self.anak_perempuan
            self.sisa_kerabat = self.Saldo - self.bagian_anak_perempuan
            self.bagian_anak_perempuan = self.bagian_anak_masing2
        elif self.anak_laki >= 1 and self.anak_perempuan >= 1:
            pecahan_warisan = self.anak_laki * 2 + self.anak_perempuan
            self.bagian_anak_laki = self.anak_laki * 2 / pecahan_warisan * self.Saldo / self.anak_laki
            self.bagian_anak_perempuan = self.bagian_anak_laki / 2 

        self.hasil_warisan = [self.bagian_anak_laki, self.bagian_anak_perempuan,self.sisa_kerabat]
        return self.hasil_warisan
    

    def pembagian_harta_istri(self,a,b):
        self.anak_laki = a
        self.anak_perempuan = b
        harta2 = print(f"Saldo yang tersisa: Rp {self.Saldo} ")
        if self.anak_laki == 0 and self.anak_perempuan == 0:
            self.bagian_suami = self.Saldo * 1/2
            self.sisa_kerabat = self.Saldo - self.bagian_suami
        elif self.anak_laki >= 1 and self.anak_perempuan == 0:
            self.bagian_suami = self.Saldo * 1/6
            sisa_harta = self.Saldo - self.bagian_suam
            self.bagian_anak_laki = sisa_harta / self.anak_laki
        elif self.anak_laki == 0 and self.anak_perempuan == 1:
            part1_bagian_suami= self.Saldo * 1/6
            self.bagian_anak_perempuan = self.Saldo * 1/2
            self.bagian_suami = part1_bagian_suami + (self.Saldo - part1_bagian_suami - self.bagian_anak_perempuan)
        elif self.anak_laki == 0 and self.anak_perempuan > 1:
            part1_bagian_suami = self.Saldo * 1/6
            part1_bagian_anak_perempuan = (self.Saldo * 2/3)
            self.bagian_anak_perempuan = part1_bagian_anak_perempuan / self.anak_perempuan
            self.bagian_suami = part1_bagian_suami +(self.Saldo - part1_bagian_anak_perempuan - part1_bagian_suami)
        elif self.anak_laki >= 1 and self.anak_perempuan >= 1:
            self.bagian_suami = self.Saldo * 1/6
            pecahan_warisan = self.anak_laki * 2 + self.anak_perempuan
            sisa_harta = self.Saldo - self.bagian_suami
            self.bagian_anak_laki = self.anak_laki * 2 / pecahan_warisan * sisa_harta / self.anak_laki
            self.bagian_anak_perempuan = self.bagian_anak_laki / 2 

        hasil_warisan2 = [self.bagian_anak_laki, self.bagian_anak_perempuan, self.bagian_suami,self.sisa_kerabat]
        return hasil_warisan2
    
        print(f"Bagian Warisan Suami adalah: {hasil_warisan2[2]}")
        print(f"Bagian Masing Masing Anak Perempuan adalah: {hasil_warisan2[1]}")
        print(f"Bagian Masing Masing Anak laki laki adalah: {hasil_warisan2[0]}")
        print(f"Bagian kerabat terdekat adalah: {hasil_warisan2[3]}")
        return " Sudah di bagi semua "

    def pembagian_harta_suami(self,a,b):
        self.anak_laki = a
        self.anak_perempuan = b
        # self.anak_laki = int(input("\nBerapa jumlah anak laki-laki? (0 jika tidak ada): "))
        # self.anak_perempuan = int(input("Berapa jumlah anak perempuan? (0 jika tidak ada): "))
        harta = print(f"Saldo yang tersisa: Rp {self.Saldo} ")
        if self.anak_laki == 0 and self.anak_perempuan == 0:
            self.bagian_istri = self.Saldo * 1/3
            self.sisa_kerabat = self.Saldo - self.bagian_istri
        elif self.anak_laki >= 1 and self.anak_perempuan == 0:
            self.bagian_istri = self.Saldo * 1/6
            sisa_harta = self.Saldo - self.bagian_istri
            self.bagian_anak_laki = sisa_harta / self.anak_laki
        elif self.anak_laki == 0 and self.anak_perempuan == 1:
            self.bagian_istri = self.Saldo * 1/6
            self.bagian_anak_perempuan = self.Saldo * 1/2
            self.sisa_kerabat = self.Saldo - self.bagian_anak_perempuan - self.bagian_istri
        elif self.anak_laki == 0 and self.anak_perempuan > 1:
            self.bagian_istri = self.Saldo * 1/6
            self.bagian_anak_perempuan = (self.Saldo * 2/3) / self.anak_perempuan
            self.sisa_kerabat = self.Saldo - self.bagian_anak_perempuan * self.anak_perempuan - self.bagian_istri   
        elif self.anak_laki >= 1 and self.anak_perempuan >= 1:
            self.bagian_istri = self.Saldo * 1/6
            pecahan_warisan = self.anak_laki * 2 + self.anak_perempuan
            sisa_harta = self.Saldo - self.bagian_istri
            self.bagian_anak_laki = self.anak_laki * 2 / pecahan_warisan * sisa_harta / self.anak_laki
            self.bagian_anak_perempuan = self.bagian_anak_laki / 2
            

        hasil_warisan = [self.bagian_anak_laki, self.bagian_anak_perempuan, self.bagian_istri, self.sisa_kerabat]
        return hasil_warisan
        print(f"Bagian Warisan Istri adalah: {hasil_warisan[2]}")
        print(f"Bagian Masing Masing Anak Perempuan adalah: {hasil_warisan[1]}")
        print(f"Bagian Masing Masing Anak laki laki adalah: {hasil_warisan[0]}")
        print(f"Bagian Kerabat Terdekat adalah: {hasil_warisan[3]}")
        return "Sudah dibagi semua"

def cek_no_rek(no_rek):
    conn = psycopg2.connect("host='localhost' port=5432 dbname='funcpro' user='postgres' password='QWERTY30'")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM user_pin where id_user = {no_rek}")
    return cursor.fetchall()

def TransferUang(data1,data2, databaru):
    conn = psycopg2.connect("host='localhost' port=5432 dbname='funcpro' user='postgres' password='QWERTY30'")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE user_saldoo SET saldo_user = saldo_user - {databaru} WHERE id_user = {data1}")
    conn.commit()
    cursor.execute(f"UPDATE user_saldoo SET saldo_user = saldo_user + {databaru} WHERE id_user = {data2}")
    conn.commit()
    return True

# Contoh penggunaan
# warisan = Warisan(2, 3, 1000000)
# hasil_anak = warisan.pembagian_harta_anak()
# hasil_istri = warisan.pembagian

# p = saldo(1)
# print(p.view())
# hasil1 = p.pembagian_harta_anak()
# print(hasil1)
# print(hasil1[0]+hasil1[1]+hasil1[2])
# hasil2 = p.pembagian_harta_istri()
# print(hasil2)
# print(hasil2[0]+hasil2[1]+hasil2[2])
# hasil3 = p.pembagian_harta_suami()
# print(hasil3)
# print(hasil3[0]+hasil3[1]+hasil3[2])


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
from PyQt5.QtTest import *
from PyQt5.QtCore import *

baglanti = sqlite3.connect("staj2_Kutuphane.db")
kalem = baglanti.cursor()

baslikFontu = QFont("Arial",30)
butonFontu = QFont("Century Gothic",20)
hakkimdaFontu = QFont("Arial",18)

def ustBolum(mevcutPencere):
    mevcutPencere.setAutoFillBackground(True)
    renkPaleti = mevcutPencere.palette()
    renkPaleti.setColor(mevcutPencere.backgroundRole(), Qt.darkCyan)
    mevcutPencere.setPalette(renkPaleti)

    geriButon = QPushButton("<",mevcutPencere)
    geriButon.setFont(butonFontu)
    geriButon.setGeometry(1750,20,40,40)
    geriButon.clicked.connect(mevcutPencere.geriDon)

    kapatButon = QPushButton("X",mevcutPencere)
    kapatButon.setFont(baslikFontu)
    kapatButon.setGeometry(1800,20,40,40)
    kapatButon.clicked.connect(Pencere.kapat)

class hGoster(QWidget):
    def __init__(self):
        super().__init__()

        ustBolum(self)
        self.setWindowTitle("Kitap görüntüle")

        self.dikey = QVBoxLayout()
        self.yatay = QHBoxLayout()

        metin1 = QLabel("Türlere göre kütüphanemizde bulunan \nbütün kitapları görüntüleme ekranı")
        metin1.setFont(baslikFontu)

        baslık = QLabel("Kitabın ismi")
        altyazi = QLabel("Kitap hakkında bilgi almak için üstüne tıklayın")
        altyazi.setFont(hakkimdaFontu)
        baslık.setFont(hakkimdaFontu)
        self.kombobox = QComboBox()
        self.kombobox.setFont(butonFontu)
        self.liste = QListWidget()

        self.dikey.addWidget(metin1)
        self.dikey.addWidget(self.kombobox)
        self.dikey.addStretch()
        self.dikey.addWidget(baslık)
        self.dikey.addWidget(self.liste)
        self.dikey.addWidget(altyazi)
        self.dikey.addStretch()
        self.turler = kalem.execute("select * from kitap_turler")
        for i in self.turler.fetchall():
            self.kombobox.addItem(i[1])


        self.kombobox.currentIndexChanged.connect(self.secildi)
        self.liste.itemClicked.connect(self.kitapBilgi)
        self.kombobox.setCurrentIndex(1)

        self.yatay.addStretch()
        self.yatay.addLayout(self.dikey)
        self.yatay.addStretch()

        self.setLayout(self.yatay)

    def kitapBilgi(self,item):
        ki = item.text()
        durumB = kalem.execute("select kitap_durum,yazar_ad,kitap_ad from kitap_bilgi where kitap_ad = ?",(ki,))
        x = durumB.fetchall()

        if (x[0][0]==0):
            QMessageBox.information(self, "Kitap bilgisi","kitabın ismi: "+x[0][2].upper()+"\nkitabın yazarı: "+
                                    x[0][1].upper()+".\nKitap şuanda boşta.\nKitabı ödünç işlemleri ekranından alabilirsiniz")
        else:
            QMessageBox.information(self, "Kitap bilgisi","kitabın ismi: "+x[0][2].upper()+"\nkitabın yazarı: " +
                                    x[0][1].upper() + ".\nKitap şuanda başka birinde. Kitabı almak için sonra geliniz")

    def secildi(self):
        turAdi = self.kombobox.currentText()
        er = kalem.execute("select * from kitap_turler")
        for i in er.fetchall():
            if (turAdi == i[1]):
                turId = i[0]
                self.liste.clear()
                asd = kalem.execute("select kitap_ad,yazar_ad,kitap_durum from kitap_bilgi where tur_id = ?",(turId,))
                for k in asd.fetchall():
                    self.liste.addItem(k[0])

    def geriDon(self):
        self.close()

class bGoster(QWidget):
    def __init__(self):
        super().__init__()
        ustBolum(self)
        self.setWindowTitle("Kitap görüntüle")

        self.dikey = QVBoxLayout()
        self.yatay = QHBoxLayout()

        metin1 = QLabel("Kütüphanemizde şuanda alınabilecek kitaplar")
        metin1.setFont(baslikFontu)

        self.kombobox = QComboBox()
        self.kombobox.setFont(butonFontu)
        self.liste = QListWidget()

        self.dikey.addWidget(metin1)


        self.dikey.addStretch()
        self.dikey.addWidget(self.kombobox)
        self.dikey.addWidget(self.liste)
        self.dikey.addStretch()
        self.turler = kalem.execute("select * from kitap_turler")
        for i in self.turler.fetchall():
            self.kombobox.addItem(i[1])



        self.kombobox.currentIndexChanged.connect(self.secildi)
        self.liste.itemClicked.connect(self.msj)
        self.kombobox.setCurrentIndex(1)

        self.yatay.addStretch()
        self.yatay.addLayout(self.dikey)
        self.yatay.addStretch()
        self.setLayout(self.yatay)

    def msj(self,item):
        QMessageBox.information(self,"Bilgi",item.text()+" kitabını ödünç işlemleri bölümünden alabilirsiniz")

    def secildi(self):
        turAdi = self.kombobox.currentText()
        er = kalem.execute("select * from kitap_turler")
        for i in er.fetchall():
            if (turAdi == i[1]):
                turId = i[0]
                self.liste.clear()
                asd = kalem.execute("select kitap_ad,yazar_ad,kitap_durum from kitap_bilgi where tur_id = ?",(turId,))
                for k in asd.fetchall():
                    if(k[2]==0):
                        self.liste.addItem(k[0])

    def geriDon(self):
        self.close()

class intro(QWidget):
    def __init__(self):
        super().__init__()

        yatay = QHBoxLayout()

        self.yazi = QLabel("Kütüphane Staj Proje V1")

        yatay.addStretch()
        yatay.addWidget(self.yazi)
        yatay.addStretch()

        self.yazi.setFont(baslikFontu)

        self.setLayout(yatay)

class yeniKitap(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yeni kitap ekle")

        self.dikey = QVBoxLayout()

        baslik = QLabel("Yeni Kitap ekle")
        baslik.setFont(baslikFontu)

        self.kitapismi = QLineEdit()
        self.kitapismi.setPlaceholderText("Kitap ismi giriniz")
        self.yazar = QLineEdit()
        self.yazar.setPlaceholderText("Yazarın ismi")
        l = QLabel("Kitabın türünü seçiniz")
        self.kombobox = QComboBox()
        self.kombobox.setFont(hakkimdaFontu)

        turler = kalem.execute("select tur_ad from kitap_turler")
        for i in turler.fetchall():
            self.kombobox.addItem(i[0])

        kaydet = QPushButton("Kaydet")
        kaydet.clicked.connect(self.kaydet)

        self.dikey.addWidget(baslik)
        self.dikey.addWidget(self.kitapismi)
        self.dikey.addWidget(self.yazar)
        self.dikey.addWidget(l)
        self.dikey.addWidget(self.kombobox)
        self.dikey.addWidget(kaydet)

        self.setLayout(self.dikey)

    def kaydet(self):
        kaydediliyor = QLabel("Kayıt ediliyor...")
        self.dikey.addWidget(kaydediliyor)
        QTest.qWait(1000)

        isim = self.kitapismi.text()
        yazar = self.yazar.text()
        secilenTur = self.kombobox.currentText()
        turId = kalem.execute("select tur_id from kitap_turler where tur_ad= ?",(secilenTur,))
        tId = turId.fetchall()[0][0]

        kalem.execute("insert into kitap_bilgi (kitap_ad,kitap_durum,tur_id,yazar_ad) values (?,?,?,?)", (isim,0,tId,yazar))
        baglanti.commit()
        kaydediliyor.setText("Kayıt başarılı")
        QTest.qWait(1000)
        self.close()

class yeniOgrenci(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yeni öğrenci ekle")

        self.dikey = QVBoxLayout()
        self.uyari = QLabel("")

        baslik = QLabel("Yeni öğrenci ekle")
        baslik.setFont(baslikFontu)

        self.ogrenciismi = QLineEdit()
        self.ogrenciismi.setPlaceholderText("Öğrencinin adı: ")
        self.ogrencisoyad = QLineEdit()
        self.ogrencisoyad.setPlaceholderText("Öğrencinin soyadı: ")
        self.bolum = QLineEdit()
        self.bolum.setPlaceholderText("Öğrencinin bölümü: ")
        self.numara = QLineEdit()
        self.numara.setPlaceholderText("Öğrencinin numarasını giriniz")

        kaydet = QPushButton("Kaydet")
        kaydet.clicked.connect(self.kaydet)

        self.dikey.addWidget(baslik)
        self.dikey.addWidget(self.ogrenciismi)
        self.dikey.addWidget(self.ogrencisoyad)
        self.dikey.addWidget(self.bolum)
        self.dikey.addWidget(self.numara)
        self.dikey.addWidget(kaydet)
        self.dikey.addWidget(self.uyari)

        self.setLayout(self.dikey)

    def kaydet(self):
        self.uyari.setText("Kayıt ediliyor...")
        QTest.qWait(1000)

        if (len(self.numara.text())!=12):
            self.uyari.setText("Girilen numara geçersiz!\n Öğrenci numaraları 12 haneli olmalıdır!")
            QTest.qWait(2000)
        else:
            kalem.execute("insert into ogrenciler (ogrenci_ad,ogrenci_soyad,bolum,numara) values (?,?,?,?)", (self.ogrenciismi.text(),self.ogrencisoyad.text(),self.bolum.text(),self.numara.text()))
            baglanti.commit()
            self.uyari.setText("Kayıt başarılı...")
            QTest.qWait(2000)

            self.close()

class yeniOdunc(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yeni odunc alma işlemi ekle")

        self.dikey = QVBoxLayout()

        baslik = QLabel("Yeni ödünç alma işlemi ekle")
        baslik.setFont(baslikFontu)
        self.kaydediliyor = QLabel("")

        self.ogrenciismi = QLineEdit()
        self.ogrenciismi.setPlaceholderText("Öğrencinin adını giriniz")
        self.ogrencisoyad = QLineEdit()
        self.ogrencisoyad.setPlaceholderText("Öğrencinin soyadını giriniz")
        self.numara = QLineEdit()
        self.numara.setPlaceholderText("Öğrencinin numarasını giriniz")
        self.kitapismi = QLineEdit()
        self.kitapismi.setPlaceholderText("Kitabın ismini giriniz")
        self.tarih = QLineEdit()
        self.tarih.setPlaceholderText("Kitabın alındığı günün tarihini giriniz")

        kaydet = QPushButton("Kaydet")
        kaydet.clicked.connect(self.kaydet)

        self.dikey.addWidget(baslik)
        self.dikey.addWidget(self.ogrenciismi)
        self.dikey.addWidget(self.ogrencisoyad)
        self.dikey.addWidget(self.numara)
        self.dikey.addWidget(self.tarih)
        self.dikey.addWidget(self.kitapismi)
        self.dikey.addWidget(kaydet)
        self.dikey.addWidget(self.kaydediliyor)

        self.setLayout(self.dikey)

    def kaydet(self):
        self.kaydediliyor.setText("Kayıt ediliyor")
        QTest.qWait(1000)

        ogrenciAd = self.ogrenciismi.text()
        ogrenciSoyad = self.ogrencisoyad.text()
        ogrenciNumara = self.numara.text()
        kitapismi = self.kitapismi.text()
        tarih = self.tarih.text()
        ogrenciKontrol=0
        kitapKontrol=0
        oId=0
        kId=0

        ogrenciBul = kalem.execute("Select * from ogrenciler")
        for i in ogrenciBul.fetchall():
            if(i[1]==ogrenciAd and i[2]==ogrenciSoyad and i[4]==ogrenciNumara):
                oId = i[0]
                ogrenciKontrol=1

        if(ogrenciKontrol==1):
            kitapBul = kalem.execute("Select * from kitap_bilgi")
            for i in kitapBul.fetchall():
                if(i[1]==kitapismi and i[2]==0):
                    kId = i[0]
                    kalem.execute("update kitap_bilgi set kitap_durum=(?) where kitap_ad= (?)",(1,kitapismi,) )
                    baglanti.commit()
                    kitapKontrol=1

        self.kaydediliyor.setText("")
        if(ogrenciKontrol==1 and kitapKontrol==1):
            kalem.execute("insert into odunc_bilgi (kitap_id,ogrenci_id,tarih) values (?,?,?)", (kId,oId,tarih))
            baglanti.commit()
            self.kaydediliyor.setText("Kayıt başarılı")
            QTest.qWait(500)
            self.close()
        elif(kitapKontrol==1 and ogrenciKontrol==0):
            self.kaydediliyor.setText("HATALI GİRİŞ!!!\nGirilen öğrenci bilgilerine ait kayıt bulunamadı!")
        elif(kitapKontrol==0 and ogrenciKontrol==1):
            self.kaydediliyor.setText("HATALI GİRİŞ!!!\nGirilen kitap bilgilerine ait kayıt bulunamadı!")
        else:
            self.kaydediliyor.setText("HATALI GİRİŞ!!!\nGirilen kitap ismi ve öğrenci bilgileri hatalı!")

class yeniiade(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yeni iade etme işlemi ekle")

        self.dikey = QVBoxLayout()

        baslik = QLabel("Yeni iade etme işlemi ekle")
        baslik.setFont(baslikFontu)
        self.kaydediliyor = QLabel("")

        self.numara = QLineEdit()
        self.numara.setPlaceholderText("Öğrencinin numarasını giriniz")
        self.kitapismi = QLineEdit()
        self.kitapismi.setPlaceholderText("Kitabın ismini giriniz")

        kaydet = QPushButton("Kaydet")
        kaydet.clicked.connect(self.kaydet)

        self.dikey.addWidget(baslik)
        self.dikey.addWidget(self.numara)
        self.dikey.addWidget(self.kitapismi)
        self.dikey.addWidget(kaydet)
        self.dikey.addWidget(self.kaydediliyor)

        self.setLayout(self.dikey)

    def kaydet(self):
        self.kaydediliyor.setText("Kayıt siliniyor...")
        QTest.qWait(1000)

        numara = self.numara.text()
        kitapismi = self.kitapismi.text()
        ogrenciKontrol = 0
        kitapKontrol = 0
        oId = 0
        kId = 0

        ogrenciBul = kalem.execute("Select * from ogrenciler")
        for i in ogrenciBul.fetchall():
            if (i[4] == numara):
                oId = i[0]
                print("ogrenci kontrol")
                ogrenciKontrol = 1

        if (ogrenciKontrol == 1):
            kitapBul = kalem.execute("Select * from kitap_bilgi")
            for i in kitapBul.fetchall():
                if (i[1] == kitapismi and i[2] == 1):
                    kId = i[0]
                    kalem.execute("update kitap_bilgi set kitap_durum=(?) where kitap_ad= (?)", (0, kitapismi,))
                    baglanti.commit()
                    print("kitap kontrol")
                    kitapKontrol = 1

        self.kaydediliyor.setText("")
        if (ogrenciKontrol == 1 and kitapKontrol == 1):
            kalem.execute("delete from odunc_bilgi where kitap_id=(?) and ogrenci_id=(?)",(kId,oId))
            baglanti.commit()
            self.kaydediliyor.setText("Kitap teslim başarılı...")
            QTest.qWait(500)
            self.close()
        elif (kitapKontrol == 1 and ogrenciKontrol == 0):
            self.kaydediliyor.setText("HATALI GİRİŞ!!!\nGirilen öğrenci bilgilerine ait kayıt bulunamadı!")
        elif (kitapKontrol == 0 and ogrenciKontrol == 1):
            self.kaydediliyor.setText("HATALI GİRİŞ!!!\nGirilen kitap bilgilerine ait kayıt bulunamadı!")
        else:
            self.kaydediliyor.setText("HATALI GİRİŞ!!!\nGirilen kitap ismi ve öğrenci bilgileri hatalı!")

class kitapListesi(QWidget):
    def __init__(self):
        super().__init__()
        ustBolum(self)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        baslik = QLabel("Kitap Listesi")
        aciklama = QLabel("Durumunu görmek istediğiniz kitabın üzerine tıklayın")

        hepsini_goster = QPushButton("Kitapların hepsini göster")
        hepsini_goster.setFont(butonFontu)
        hepsini_goster.clicked.connect(self.hepsiniGoster)
        bosta_goster = QPushButton("Boşta olan kitapları göster")
        bosta_goster.setFont(butonFontu)
        bosta_goster.clicked.connect(self.bostaGoster)

        baslik.setFont(baslikFontu)
        liste = QListWidget()
        yeniEkle = QPushButton("Yeni kitap ekle")
        yeniEkle.setFont(butonFontu)
        yeniEkle.clicked.connect(self.yeniEkle)

#        kitaplar = kalem.execute("select * from kitaplar")
#        for i in kitaplar.fetchall():
#            liste.addItem(i[1])

        liste.itemClicked.connect(self.kitapBilgi)

        aciklama.setFont(butonFontu)

        dikey.addWidget(baslik)
        dikey.addStretch()
        dikey.addWidget(hepsini_goster)
        dikey.addWidget(bosta_goster)
        dikey.addStretch()
#        dikey.addWidget(liste)
#        dikey.addWidget(aciklama)
        dikey.addWidget(yeniEkle)


        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)

    def hepsiniGoster(self):
        self.goster = hGoster()
        self.goster.showFullScreen()

    def bostaGoster(self):
        self.goster = bGoster()
        self.goster.showFullScreen()

    def kitapBilgi(self,item):

        kitapismi = item.text()
        kontrol = kalem.execute("Select * from kitaplar where kitap_ad = ?",(kitapismi,))
        durum = kontrol.fetchall()[0][2]

        if(durum==0):
            QMessageBox.information(self,"Kitap durum bilgisi",kitapismi+" isimli kitap boşta")
        else:
            kimde = kalem.execute("select * from odunc where kitap_ad = ?",(kitapismi,))
            ogrenci = kimde.fetchall()[0][1]
            QMessageBox.information(self,"Kitap durum bilgisi",kitapismi+" isimli kitap "+ogrenci+" isimli öğrencide")

    def yeniEkle(self):
        self.yeni = yeniKitap()
        self.yeni.show()

    def geriDon(self):
        self.close()

class ogrenciListesi(QWidget):
    def __init__(self):
        super().__init__()

        ustBolum(self)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        baslik = QLabel("Öğrenci Listesi")
        aciklama = QLabel("Öğrencinin elinde kitap olup olmadığını \nöğrenmek için üzerine tıklayın")
        aciklama.setFont(hakkimdaFontu)

        baslik.setFont(baslikFontu)
        self.liste = QListWidget()
       # self.liste.setStyleSheet("color: black;  background-color: darkCyan")
        yeniEkle = QPushButton("Yeni ogrenci ekle")
        basliklar = QLabel("Numara\t      Ad Soyad\tBölüm")
        basliklar.setFont(hakkimdaFontu)
        yeniEkle.setFont(butonFontu)
        yeniEkle.clicked.connect(self.yeniEkle)

        ogrenciler = kalem.execute("select * from ogrenciler")
        for i in ogrenciler.fetchall():
            self.liste.addItem(i[4]+"\t"+i[1]+" "+i[2]+"\t"+i[3])

        self.liste.itemClicked.connect(self.ogrenciBilgi)

        dikey.addWidget(baslik)
        dikey.addWidget(basliklar)
        dikey.addWidget(self.liste)
        dikey.addWidget(aciklama)
        dikey.addWidget(yeniEkle)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)

    def ogrenciBilgi(self, item):
        self.numaraListe = ""
        self.kitapAdlari = ""
        for i in range(0,12):
            self.numaraListe += item.text()[i]
        secim = kalem.execute("select ogrenci_id from ogrenciler where numara= ?",(self.numaraListe,))
        oduncler = kalem.execute("select kitap_id from odunc_bilgi where ogrenci_id= ?",(secim.fetchall()[0][0],))
        #elimizde öğrenci id ve kitapların idleri var
        for i in oduncler.fetchall():
            yazdır = kalem.execute("select kitap_ad from kitap_bilgi where kitap_id= ?",(i[0],))
            self.kitapAdlari += yazdır.fetchall()[0][0]+"\n"
        if(self.kitapAdlari==""):
            QMessageBox.information(self, "Öğrencideki kitaplar", "Öğrencide hiç kitap yok.")
        else:
            QMessageBox.information(self, "Öğrencideki kitaplar", self.kitapAdlari+"\t\t\t\t")

    def yeniEkle(self):
        self.yeni = yeniOgrenci()
        self.yeni.show()

    def geriDon(self):
        self.close()

class oduncListesi(QWidget):
    def __init__(self):
        super().__init__()

        ustBolum(self)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        baslik = QLabel("Ödünç işlemleri")

        baslik.setFont(baslikFontu)
        sirala = QListWidget()

        yeniEkle = QPushButton("Yeni odunç alma işlemi ekle")
        iadeEkle = QPushButton("Yeni iade alma işlemi ekle")

        yeniEkle.setFont(butonFontu)
        iadeEkle.setFont(butonFontu)
        yeniEkle.clicked.connect(self.yeniEkle)
        iadeEkle.clicked.connect(self.iadeEkle)

        oduncler = kalem.execute("Select kitap_id,ogrenci_id,tarih from odunc_bilgi")
        for i in oduncler.fetchall():
            ogrenci_id = i[1]
            kitap_id = i[0]
            alinanKitap = kalem.execute("select kitap_ad from kitap_bilgi where kitap_id= ?",(kitap_id,))
            for k in alinanKitap.fetchall():
                    kitapisim = k[0]
            alanKisi = kalem.execute("select ogrenci_ad,ogrenci_soyad from ogrenciler where ogrenci_id= ?",(ogrenci_id,))
            for p in alanKisi.fetchall():
                ogrenciAd = p[0]+" "+p[1]

            sirala.addItem(ogrenciAd.upper()+": "+kitapisim.upper()+" kitabını "+i[2]+" tarihinde kütüphanemizden almıştır")

        dikey.addWidget(baslik)
        dikey.addWidget(sirala)
        dikey.addWidget(yeniEkle)
        dikey.addWidget(iadeEkle)


        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)

    def yeniEkle(self):
        self.yeni = yeniOdunc()
        self.yeni.show()
    def iadeEkle(self):
        self.yeni = yeniiade()
        self.yeni.show()

    def geriDon(self):
        self.close()

class yardimHakkimizda(QWidget):
    def __init__(self):
        super().__init__()

        ustBolum(self)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        baslik = QLabel("Yardım - Hakkımızda")
        baslik.setFont(baslikFontu)
        yazi = QLabel("Kütüphane sistemi staj2 dersi için yapılmış projedir. ")
        yazi.setFont(hakkimdaFontu)

        dikey.addWidget(baslik)
        dikey.addStretch()
        dikey.addWidget(yazi)
        dikey.addStretch()

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()


        self.setLayout(yatay)

    def geriDon(self):
        self.close()

class Pencere(QWidget):

    def __init__(self):
        super().__init__()

        self.giris = intro()
        self.giris.showFullScreen()
        QTest.qWait(2000)
        self.setAutoFillBackground(True)
        renkPaleti = self.palette()
        renkPaleti.setColor(self.backgroundRole(), Qt.darkCyan)
        self.setPalette(renkPaleti)


        kapatButon = QPushButton("X", self)
        kapatButon.setFont(baslikFontu)
        kapatButon.setGeometry(1800, 20, 40, 40)
        kapatButon.clicked.connect(self.kapat)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        baslik = QLabel("Kütüphane v1")
        baslik.setStyleSheet("color: black")

        kitapButon = QPushButton("Kitap Listesi")
        ogrenciButon = QPushButton("Oğrenci listesi")
        islemlerButon = QPushButton("Odünç işlemleri")
        yardimButon = QPushButton("Yardım- Hakkımızda")

        kitapButon.setFont(butonFontu)
        ogrenciButon.setFont(butonFontu)
        islemlerButon.setFont(butonFontu)
        yardimButon.setFont(butonFontu)
        baslik.setFont(baslikFontu)

        kitapButon.clicked.connect(self.kitapAc)
        ogrenciButon.clicked.connect(self.ogrenciAc)
        islemlerButon.clicked.connect(self.islemAc)
        yardimButon.clicked.connect(self.yardimAc)

        dikey.addWidget(baslik)
        dikey.addStretch()
        dikey.addWidget(kitapButon)
        dikey.addStretch()
        dikey.addWidget(ogrenciButon)
        dikey.addStretch()
        dikey.addWidget(islemlerButon)
        dikey.addStretch()
        dikey.addWidget(yardimButon)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
        self.showFullScreen()

    def kitapAc(self):
        self.kitap = kitapListesi()
        self.kitap.showFullScreen()

    def ogrenciAc(self):
        self.ogrenci = ogrenciListesi()
        self.ogrenci.showFullScreen()
    def islemAc(self):
        self.islem = oduncListesi()
        self.islem.showFullScreen()
    def yardimAc(self):
        self.yardim = yardimHakkimizda()
        self.yardim.showFullScreen()
    def kapat(self):
        qApp.quit()

uygulama = QApplication(sys.argv)
pencere = Pencere()
sys.exit(uygulama.exec_())
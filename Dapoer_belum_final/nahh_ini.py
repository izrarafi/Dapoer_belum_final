import os
import csv
from datetime import datetime
import pandas as pd


FILE_MENU = "menu.csv"
FILE_VOUCHER = "Voucher.csv"
FILE_TRANSAKSI = "Transaksi.csv"

# ================== INISIALISASI FILE ==================
try:
    df = pd.read_csv('users.csv', dtype=str)
    if 'ceo' not in df['Nama'].values:
        df.loc[len(df)] = ['ceo', 'ceo123', 'ceo']
        df.to_csv('users.csv', index=False)
except FileNotFoundError:
    df = pd.DataFrame({'Nama': [], 'Password': [], 'Sebagai': []})
    df.loc[len(df)] = ['ceo', 'ceo123', 'ceo']
    df.to_csv('users.csv', index=False)

# Inisialisasi file Transaksi.csv jika belum ada
try:
    pd.read_csv(FILE_TRANSAKSI)
except FileNotFoundError:
    df_trx = pd.DataFrame(columns=['ID', 'Waktu', 'Item_Pesanan', 'Jumlah', 'Harga'])
    df_trx.to_csv(FILE_TRANSAKSI, index=False)

nama_akun = ''

# keranjang pesanan
keranjang = []


# ================== BERANDA, REGISTRASI, LOGIN ==================
def df_beranda():
    while True:
        os.system('cls')
        print('======================================================')
        print('|     SELAMAT DATANG DI CAFE DAPOER DIGITAL          |')
        print('======================================================')
        print()
        print('==================== MENU MASUK ======================')
        print()
        print('(1) Login sebagai admin')
        print('(2) Login')
        print('(3) Registrasi')
        print('(0) Keluar')
        print()

        pilih = input("Masukkan nomer pilihan (1),(2),(3),(0): ")
        if pilih == '1':
            df_login()
        elif pilih == '2':
            df_login()
        elif pilih == '3':
            df_registrasi()
        elif pilih == '0':
            print('Terima kasih telah berkunjung, sampai jumpa lagi!! ')
            break
        else:
            print('pilihan tidak valid!!')
            input('Tekan enter...')


def df_registrasi():
    while True:
        os.system('cls')
        print('======================================================')
        print('|               REGISTRASI AKUN BARU                 |')
        print('======================================================')
        print()
        dfuser = pd.read_csv('users.csv', dtype=str)
        nama = input("Masukkan nama anda : ").strip()

        if nama == '':
            print('Nama tidak boleh kosong!!')
            input("Tekan enter...")
            return

        if nama in dfuser['Nama'].values:
            print('Nama sudah digunakan!!')
            input("Tekan enter...")
            return

        while True:
            password = input('Masukkan password anda (minimal 8 karakter): ')
            if len(password) < 8:
                print('Password minimal memiliki 8 karakter!!')
            else:
                print('Password sudah valid')
                break

        while True:
            cek = input('Apakah Nama dan Password sudah benar? (y/t) : ')
            if cek == 'y':
                dfuser.loc[len(dfuser)] = [nama, password, 'customer']
                dfuser.to_csv('users.csv', index=False)
                input('Registrasi sudah berhasil!! Tekan enter.....')
                return
            elif cek == 't':
                input('Silahkan registrasi ulang dengan menekan enter...')
                return df_registrasi()
            else:
                print('tidak valid!! silahkan ulangi!!')


def df_login():
    global nama_akun
    while True:
        os.system('cls')
        print('======================================================')
        print('|          SUDAH PUNYA AKUN? SILAHKAN LOGIN          |')
        print('======================================================')
        print('(ketik 0 pada nama untuk kembali)')
        print()

        nama = input('Masukkan nama akun : ').strip()
        if nama == '0':
            return
        password = input('Masukkan password : ')

        loginberhasil = False
        sebagai = ''

        with open('users.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if str(row.get('Nama', '')).strip() == nama and str(row.get('Password', '')).strip() == password:
                    nama_akun = row.get('Nama').strip()
                    sebagai = row.get('Sebagai').strip().lower()
                    loginberhasil = True
                    break

        if loginberhasil:
            print(f'Login berhasil!!! Halo, {nama_akun}, sebagai {sebagai}!')
            input('\nTekan enter....')
            if sebagai == 'customer':
                df_menucustomer()
            elif sebagai == 'ceo':
                df_menuceo()
            else:
                print('siapa anda??, kembali ke halaman utama....')
                input('\nTekan enter........')
            return
        else:
            print('Nama atau password salah!!')
            input('Tekan enter untuk coba lagi...')


# ================== MENU CEO ==================
def df_menuceo():
    while True:
        os.system('cls')
        print('======================================================')
        print(f'|           MENU CEO - {nama_akun}                  |')
        print('======================================================')
        print('(1) Lihat daftar akun')
        print('(2) Kelola daftar menu')
        print('(3) Rekap transaksi (Struk & Arsip)')
        print('(0) Logout')
        pilih = input('Masukkan pilihan (angka) : ')
        if pilih == '1':
            os.system('cls')
            dfuser = pd.read_csv('users.csv', dtype=str)
            print()
            print(dfuser[['Nama', 'Sebagai']])
            input('\nTekan enter...')
        elif pilih == '2':
            df_kelola_daftar_menu()
        elif pilih == '3':
            rekap_transaksi()
        elif pilih == '0':
            return
        else:
            print('Pilihan tidak valid!!')
            input('Tekan enter...')


def rekap_transaksi():
    while True:
        os.system('cls')
        print("======================================================")
        print("|          REKAP TRANSAKSI (STRUK & ARSIP)           |")
        print("======================================================")
        print("(1) Lihat arsip transaksi & total pemasukan")
        print("(2) Cari & cetak ulang struk")
        print("(0) Kembali")
        pilih = input("Pilih menu (angka): ").strip()

        df_trx = pd.read_csv(FILE_TRANSAKSI)

        if pilih == '1':
            os.system('cls')
            print("======================================================")
            print("|               ARSIP TRANSAKSI PENJUALAN            |")
            print("======================================================")
            if df_trx.empty:
                print("\nBelum ada data transaksi.")
            else:
                for i, row in df_trx.iterrows():
                    print(f"[{row['ID']}] {row['Waktu']} | {row['Item_Pesanan']} ({row['Jumlah']}x) = Rp {int(row['Harga']):,}")
                print("-" * 54)
                total_pemasukan = int(df_trx['Harga'].sum())
                print(f"Total Item Terjual : {int(df_trx['Jumlah'].sum())} porsi")
                print(f"TOTAL PEMASUKAN    : Rp {total_pemasukan:,}")
            input("\nTekan enter untuk kembali...")

        elif pilih == '2':
            os.system('cls')
            print("======================================================")
            print("|              CARI & CETAK ULANG STRUK              |")
            print("======================================================")
            if df_trx.empty:
                print("\nBelum ada data transaksi.")
            else:
                print("\nDaftar ID Transaksi:")
                for id_unik in df_trx['ID'].unique():
                    print(f"- {id_unik}")

                cari_id = input("\nMasukkan ID Transaksi (contoh TRX-001): ").strip().upper()
                hasil = df_trx[df_trx['ID'].astype(str).str.upper() == cari_id]

                if hasil.empty:
                    print("\n[!] ID Transaksi tidak ditemukan!")
                else:
                    waktu_trx = hasil['Waktu'].values[0]
                    total_struk = int(hasil['Harga'].sum())
                    print("\n" + "=" * 38)
                    print("         CAFE DAPOER DIGITAL          ")
                    print("            STRUK PESANAN             ")
                    print("=" * 38)
                    print(f"ID Transaksi : {cari_id}")
                    print(f"Waktu        : {waktu_trx}")
                    print("-" * 38)
                    for i, row in hasil.iterrows():
                        print(f"{row['Jumlah']}x {row['Item_Pesanan']} = Rp {int(row['Harga']):,}")
                    print("-" * 38)
                    print(f"TOTAL        : Rp {total_struk:,}")
                    print("=" * 38)
            input("\nTekan enter untuk kembali...")

        elif pilih == '0':
            return
        else:
            print("Pilihan tidak valid!!")
            input("Tekan enter...")


def tampilkan_menu():
    df = pd.read_csv(FILE_MENU)
    kategori_list = ["Makanan", "Minuman", "Dessert"]

    for kat in kategori_list:
        print(f"\n--- [ {kat.upper()} ] ---")
        menu_kat = df[df['Kategori'].str.lower() == kat.lower()]
        for i, row in menu_kat.iterrows():
            print(f"{row['No']} - {row['Menu']} : {row['Harga']}")


def baca_menu():
    tampilkan_menu()


def tambah_menu():
    tampilkan_menu()
    print("\nTambahkan menu baru:")
    
    df = pd.read_csv(FILE_MENU)
    No = input("Masukkan nomor menu baru : ").strip()
    kategori = input("Masukkan kategori : ").strip()
    menu = input("Masukkan menu baru : ").strip()
    harga = int(input("Masukkan harga menu : "))

    data_baru = pd.DataFrame([{'No': No, 'Kategori': kategori, 'Menu': menu, 'Harga': harga}])
    df = pd.concat([df, data_baru], ignore_index=True)
    df.to_csv(FILE_MENU, index=False)
    print("\n[✓] Menu berhasil ditambahkan!")
    input("Tekan enter untuk kembali...")


def ubah_menu():
    tampilkan_menu()
    print("\nUbah menu yang sudah ada:")
    
    No = input("Masukkan nomor menu yang ingin diubah: ").strip()
    kategori = input("Masukkan kategori yang ingin diubah: ").strip()
    menu_lama = input("Masukkan nama menu yang ingin diubah: ").strip()
    menu_baru = input("Masukkan nama menu baru: ").strip()
    harga_baru = int(input("Masukkan harga menu baru: "))

    df = pd.read_csv(FILE_MENU)

    mask = (
        df['No'].astype(str).str.strip() == No
    ) & (
        df['Kategori'].astype(str).str.strip().str.lower() == kategori.lower()
    ) & (df['Menu'].astype(str).str.strip().str.lower() == menu_lama.lower())

    if df[mask].empty:
        print('\n[!] Menu atau kategori tidak ditemukan. Tidak ada perubahan!!')
    else:
        df.loc[mask, 'Menu'] = menu_baru
        df.loc[mask, 'Harga'] = harga_baru
        df.to_csv(FILE_MENU, index=False)
        print('\n✅ Menu berhasil diubah!')

    input('tekan enter untuk kembali..')


def hapus_menu():
    df = pd.read_csv(FILE_MENU, dtype=str)
    tampilkan_menu()

    no_hapus = input("\nMasukkan nomor menu yang ingin dihapus: ").strip()
    if (df['No'] == no_hapus).any():
        df = df[df['No'] != no_hapus]
        df.to_csv(FILE_MENU, index=False)
        print("\n✅ Menu berhasil dihapus!")
    else:
        print("\n[!] Nomor menu tidak ditemukan!")
    input("Tekan enter untuk kembali...")


def df_kelola_daftar_menu():
    os.system('cls')
    print("=========================================")
    print("|          KELOLA DAFTAR MENU           |")
    print("=========================================")
    print()
    print('(1) tampilkan daftar menu')
    print('(2) tambah menu')
    print('(3) ubah menu')
    print('(4) hapus menu')
    print('(0) kembali')

    pilih = input('pilih menu (angka): ')
    if pilih == '1':
        os.system('cls')
        print("==============================")
        print("|        DAFTAR MENU         |")
        print("==============================")
        print()
        baca_menu()
        input('tekan enter untuk kembali')
        return df_kelola_daftar_menu()

    elif pilih == '2':
        os.system('cls')
        print("==============================")
        print("|         TAMBAH MENU        |")
        print("==============================")
        print()
        tambah_menu()
        return df_kelola_daftar_menu()

    elif pilih == '3':
        os.system('cls')
        print("==============================")
        print("|         UBAH MENU          |")
        print("==============================")
        print()
        ubah_menu()
        return df_kelola_daftar_menu()

    elif pilih == '4':
        os.system('cls')
        print("==============================")
        print("|       HAPUS MENU         |")
        print("==============================")
        print()
        hapus_menu()
        return df_kelola_daftar_menu()

    elif pilih == '0':
        os.system('cls')
        return

    else:
        print('input tidak sesuai!!!')
        input('tekan enter untuk kembali')
        return df_kelola_daftar_menu()


# ================== MENU CUSTOMER ==================
def checkout():
    os.system('cls')
    print("==============================")
    print("|         KERANJANG        |")
    print("==============================")
    print()
    if len(keranjang) == 0:
        print("Keranjang masih kosong!")
        input("Tekan enter...")
        return

    total = 0
    for item in keranjang:
        nama = item['menu']
        jumlah = item['jumlah']
        subtotal = item['total']
        print(f"{jumlah}x {nama} = Rp{subtotal:,}")
        total += subtotal
    print("-" * 30)
    print(f"TOTAL BAYAR : Rp{total:,}")

    pakai_voucher = input('Punya voucher ga? (y/t) : ').strip().lower()
    potongan = 0

    if pakai_voucher == 'y':
        kode_input = input("Masukkan kode voucher: ").strip().upper()
        df_voucher = pd.read_csv(FILE_VOUCHER)

        while True:
            kode_input = input("Masukkan kode voucher: ").strip().upper()
            voucher_cocok = df_voucher[df_voucher['Kode'].astype(str).str.strip().str.upper() == kode_input]

            if not voucher_cocok.empty:
                potongan = int(voucher_cocok['Potongan'].values[0])
                total = max(0, total - potongan)
                print(f'Voucher {kode_input} berlaku!! Potongan : Rp. {potongan:,}')
                break
            else:
                print('Voucher tidak ditemukan!')
                coba_lagi = input('Mau coba masukkan kode voucher lagi? (y/t) : ').strip().lower()
                if coba_lagi != 'y':
                    break

        print(f'TOTAL BAYAR : Rp. {total:,}')
        print('-' * 30)

    konfirmasi = input("\nLanjut bayar? (y/t) : ").lower()
    if konfirmasi == 'y':
        total_akhir = total
        while True:
            try:
                bayar = int(input(f"Masukkan uang pembayaran (Rp {total_akhir:,}): Rp "))
                if bayar < total_akhir:
                    print(f"Uang kurang Rp {total_akhir - bayar:,}. Silakan bayar dengan nominal yang cukup.")
                else:
                    kembalian = bayar - total_akhir

                    # 1. Buat ID Transaksi baru berdasarkan jumlah ID unik yang sudah ada
                    df_trx = pd.read_csv(FILE_TRANSAKSI)
                    nomor_urut = df_trx['ID'].nunique() + 1
                    id_trx = f"TRX-{nomor_urut:03d}"
                    waktu = datetime.now().strftime("%Y-%m-%d %H:%M")

                    # 2. Simpan setiap item di keranjang ke Transaksi.csv
                    for item in keranjang:
                        baris_baru = pd.DataFrame([{
                            'ID': id_trx,
                            'Waktu': waktu,
                            'Item_Pesanan': item['menu'],
                            'Jumlah': item['jumlah'],
                            'Harga': item['total']
                        }])
                        df_trx = pd.concat([df_trx, baris_baru], ignore_index=True)
                    df_trx.to_csv(FILE_TRANSAKSI, index=False)

                    # 3. Cetak Struk Pesanan
                    print("\n" + "=" * 38)
                    print("         CAFE DAPOER DIGITAL          ")
                    print("            STRUK PESANAN             ")
                    print("=" * 38)
                    print(f"ID Transaksi  : {id_trx}")
                    print(f"Waktu         : {waktu}")
                    print("-" * 38)
                    for item in keranjang:
                        print(f"{item['jumlah']}x {item['menu']} = Rp {item['total']:,}")
                    print("-" * 38)
                    print(f"Total Akhir   : Rp {total_akhir:,}")
                    print(f"Uang Diterima : Rp {bayar:,}")
                    print(f"Kembalian     : Rp {kembalian:,}")
                    print("=" * 38)
                    print("Pembayaran berhasil! Terima kasih telah berkunjung!")
                    keranjang.clear()
                    break
            except ValueError:
                print("Masukkan nominal uang berupa angka!")
    else:
        print("Pesanan tetap disimpan di keranjang.")
    input("Tekan enter...")


def pesan_menu():
    os.system('cls')
    print("==============================")
    print("|        PESAN MENU          |")
    print("==============================")
    print()
    baca_menu()
    pesanan = input('masukkan nomor pesanan : ')
    jumlah_pesanan = int(input('untuk berapa porsi : '))
    df = pd.read_csv(FILE_MENU)
    menu_ditemukan = df[df['No'].astype(str) == pesanan.strip()]

    if not menu_ditemukan.empty:
        nama_menu = menu_ditemukan['Menu'].values[0]
        harga_satuan = menu_ditemukan['Harga'].values[0]
        total_harga = harga_satuan * jumlah_pesanan

        keranjang.append({'menu': nama_menu, 'jumlah': jumlah_pesanan, 'total': total_harga})
        print()
        print(f'✅ Berhasil menambahkan {jumlah_pesanan} {nama_menu} ke keranjang!')
        input('tekan enter untuk melanjutkan..')

    else:
        print()
        print('Menu tidak ditemukan di daftar menu!!! Silahkan periksa kembali!')
        input('tekan enter untuk kembali')


def liat_keranjang():
    os.system('cls')
    print("==============================")
    print("|         KERANJANG          |")
    print("==============================")
    print()

    if not keranjang:
        print('Keranjang belanja masih kosong!')
    else:
        total_bayar = 0
        for i, item in enumerate(keranjang, 1):
            print(
                f"{i}. No/Menu : {item['menu']} | Jumlah : {item['jumlah']} | Total: Rp. {item['total']}"
            )
            total_bayar += item['total']
        print("-" * 30)
        print(f'Total keseluruhan: Rp.{total_bayar}')

    print()
    input('tekan enter untuk kembali..')


def df_menucustomer():
    while True:
        os.system('cls')
        print('======================================================')
        print(f'|           MENU CUSTOMER - {nama_akun}             |')
        print('======================================================')
        print('(1) Pesan menu')
        print('(2) Lihat keranjang belanja')
        print('(3) Checkout / Pembayaran')
        print('(0) Logout')
        pilih = input('Masukkan pilihan : ')

        if pilih == '1':
            pesan_menu()
        elif pilih == '2':
            liat_keranjang()
        elif pilih == '3':
            checkout()
        elif pilih == '0':
            keranjang.clear()
            return
        else:
            print('Pilihan tidak valid!!')
            input('Tekan enter...')


df_beranda()
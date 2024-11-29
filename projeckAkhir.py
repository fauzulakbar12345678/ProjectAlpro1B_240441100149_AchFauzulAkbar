from collections import defaultdict

data_pemasukkan = []
data_pengeluaran = []
saldo_per_bulan = {}
batas_pengeluaran = None

def konversi_bulan(bulan_input):
    bulan_input = bulan_input.lower()
    nama_bulan = {
        "januari": "01", "februari": "02", "maret": "03", "april": "04",
        "mei": "05", "juni": "06", "juli": "07", "agustus": "08",
        "september": "09", "oktober": "10", "november": "11", "desember": "12"
    }
    angka_bulan = {
        "01": "01", "02": "02", "03": "03", "04": "04",
        "05": "05", "06": "06", "07": "07", "08": "08",
        "09": "09", "10": "10", "11": "11", "12": "12"
    }
    return nama_bulan.get(bulan_input, angka_bulan.get(bulan_input, None))

def tambahkan_data():
    global saldo_per_bulan
    jenis = input("Tambahkan data [Pengeluaran/Pemasukan]: ").lower()
    try:
        tanggal_input = int(input("Masukkan tanggal (1-31): ").strip())
        bulan_input = input("Masukkan bulan (nama/angka[01-31]): ").strip()
        tahun_input = int(input("Masukkan tahun (yyyy): ").strip())

        if not (1 <= tanggal_input <= 31):
            raise ValueError("Tanggal tidak valid!")
        
        bulan_angka = konversi_bulan(bulan_input)
        if not bulan_angka:
            raise ValueError("Bulan tidak valid!")
    except ValueError as e:
        print(e)
        return

    tanggal_lengkap = f"{str(tanggal_input).zfill(2)}-{bulan_angka}-{tahun_input}"
    bulan_tahun = f"{bulan_angka}-{tahun_input}"
    
    if jenis == "pemasukan":
        judul = input("Masukkan judul: ")
        nominal = int(input("Masukkan nominal: "))
        data_pemasukkan.append({'judul': judul, 'nominal': nominal, 'tanggal': tanggal_lengkap})
        saldo_per_bulan[bulan_tahun] = saldo_per_bulan.get(bulan_tahun, 0) + nominal
        print("Data Pemasukan Berhasil Ditambahkan")
        
    elif jenis == "pengeluaran":
        judul = input("Masukkan judul: ")
        nominal = int(input("Masukkan nominal: "))
        kategori = input("Masukkan kategori yang sesuai: ")
        data_pengeluaran.append({'judul': judul, 'nominal': nominal, 'kategori': kategori, 'tanggal': tanggal_lengkap})
        saldo_per_bulan[bulan_tahun] = saldo_per_bulan.get(bulan_tahun, 0) - nominal
        print("Data Pengeluaran Berhasil Ditambahkan")
    else:
        print("Pilihan jenis tidak sesuai!")

def tampilkan_rekapan_perhari():
    pemasukan_perhari = defaultdict(list)
    pengeluaran_perhari = defaultdict(list)

    for data in data_pemasukkan:
        tanggal = data['tanggal']
        pemasukan_perhari[tanggal].append(f"{data['judul']} ({data['nominal']})")
    
    for data in data_pengeluaran:
        tanggal = data['tanggal']
        pengeluaran_perhari[tanggal].append(f"{data['judul']} ({data['nominal']})")

    print("\n====== Rekapan Pemasukan dan Pengeluaran Perhari ======")
    tanggal_rekap = set(pemasukan_perhari.keys()).union(set(pengeluaran_perhari.keys()))
    for tanggal in sorted(tanggal_rekap):
        pemasukan = pemasukan_perhari.get(tanggal, [])
        pengeluaran = pengeluaran_perhari.get(tanggal, [])
        print(f"\nTanggal: {tanggal}")
        print("  Pemasukan:")
        for item in pemasukan:
            print(f"    - {item}")
        print("  Pengeluaran:")
        for item in pengeluaran:
            print(f"    - {item}")

def tampilkan_data_perbulan():
    try:
        bulan_input = input("Masukkan bulan (nama/angka): ").strip()
        tahun_input = int(input("Masukkan tahun (yyyy): ").strip())
        
        bulan_angka = konversi_bulan(bulan_input)
        if not bulan_angka:
            raise ValueError("Bulan tidak valid!")
    except ValueError as e:
        print(e)
        return

    bulan_tahun = f"{bulan_angka}-{tahun_input}"

    pemasukan_bulanan = [data for data in data_pemasukkan if data['tanggal'].endswith(bulan_tahun)]
    pengeluaran_bulanan = [data for data in data_pengeluaran if data['tanggal'].endswith(bulan_tahun)]

    print(f"\n====== Rekapan Bulanan ({bulan_input.capitalize()} {tahun_input}) ======")
    print("Pemasukan:")
    if pemasukan_bulanan:
        for i, data in enumerate(sorted(pemasukan_bulanan, key=lambda x: x['tanggal']), start=1):
            tanggal, nominal, judul = data['tanggal'], data['nominal'], data['judul']
            print(f"{i}. {tanggal} | {nominal} | {judul}")
    else:
        print("- Tidak ada data pemasukan -")

    print("\nPengeluaran:")
    if pengeluaran_bulanan:
        for i, data in enumerate(sorted(pengeluaran_bulanan, key=lambda x: x['tanggal']), start=1):
            tanggal, nominal, judul, kategori = data['tanggal'], data['nominal'], data['judul'], data['kategori']
            print(f"{i}. {tanggal} | {nominal} | {judul} | {kategori}")
    else:
        print("- Tidak ada data pengeluaran -")

    saldo = saldo_per_bulan.get(bulan_tahun, 0)
    print(f"\nSaldo Bulan {bulan_input.capitalize()}: {saldo}")

def update_data():
    global saldo_per_bulan
    print('Pilih data yang ingin diupdate:')
    print('1. Pemasukan')
    print('2. Pengeluaran')

    pilih_update = input('Masukkan pilihan anda [1/2]: ')

    if pilih_update == "1" or pilih_update == "pemasukan":
        update_judul = input('Masukkan judul data pemasukan yang ingin diupdate: ')
        for data in data_pemasukkan:
            if data['judul'] == update_judul:
                bulan_tahun_lama = data['tanggal'][3:]
                saldo_per_bulan[bulan_tahun_lama] -= data['nominal']

                nominal_baru = int(input('Masukkan nominal baru: '))
                tanggal_baru = input('Masukkan tanggal baru (dd): ')
                bulan_baru = input('Masukkan bulan baru (contoh: 01): ')
                tahun_baru = input('Masukkan tahun baru (yyyy): ')

                bulan_angka_baru = bulan_baru.zfill(2)
                tanggal_lengkap_baru = f"{tanggal_baru.zfill(2)}-{bulan_angka_baru}-{tahun_baru}"
                bulan_tahun_baru = f"{bulan_angka_baru}-{tahun_baru}"

                data['nominal'] = nominal_baru
                data['tanggal'] = tanggal_lengkap_baru

                saldo_per_bulan[bulan_tahun_baru] = saldo_per_bulan.get(bulan_tahun_baru, 0) + nominal_baru
                print("Data Pemasukan berhasil diupdate.")
                return
        print("Data tidak ditemukan.")

    elif pilih_update == "2" or pilih_update == "pengeluaran":
        update_judul = input('Masukkan judul data pengeluaran yang ingin diupdate: ')
        for data in data_pengeluaran:
            if data['judul'] == update_judul:
                bulan_tahun_lama = data['tanggal'][3:]
                saldo_per_bulan[bulan_tahun_lama] += data['nominal']

                nominal_baru = int(input('Masukkan nominal baru: '))
                tanggal_baru = input('Masukkan tanggal baru (dd): ')
                bulan_baru = input('Masukkan bulan baru (contoh: 01): ')
                tahun_baru = input('Masukkan tahun baru (yyyy): ')
                kategori_baru = input('Masukkan kategori baru: ')

                bulan_angka_baru = bulan_baru.zfill(2)
                tanggal_lengkap_baru = f"{tanggal_baru.zfill(2)}-{bulan_angka_baru}-{tahun_baru}"
                bulan_tahun_baru = f"{bulan_angka_baru}-{tahun_baru}"

                data['nominal'] = nominal_baru
                data['tanggal'] = tanggal_lengkap_baru
                data['kategori'] = kategori_baru

                saldo_per_bulan[bulan_tahun_baru] = saldo_per_bulan.get(bulan_tahun_baru, 0) - nominal_baru
                print("Data Pengeluaran berhasil diupdate.")
                return
        print("Data tidak ditemukan.")
    else:
        print("Pilihan tidak valid.")

def hapus():
    global saldo_per_bulan
    print("\nHapus Data")
    print("1. Hapus Pemasukan")
    print("2. Hapus Pengeluaran")
    jenis_hapus = input("Masukkan pilihan [1/2]: ")
    
    if jenis_hapus == "1" or jenis_hapus == "pemasukan":
        judul_hapus = input("Masukkan judul pemasukan yang ingin dihapus: ")
        for data in data_pemasukkan:
            if data['judul'] == judul_hapus:
                bulan_tahun = data['tanggal'][3:]
                saldo_per_bulan[bulan_tahun] -= data['nominal']
                data_pemasukkan.remove(data)
                print("Data Pemasukan berhasil dihapus.")
                return
        print("Data tidak ditemukan.")
    
    elif jenis_hapus == "2" or jenis_hapus == "pengeluaran":
        judul_hapus = input("Masukkan judul pengeluaran yang ingin dihapus: ")
        for data in data_pengeluaran:
            if data['judul'] == judul_hapus:
                bulan_tahun = data['tanggal'][3:]
                saldo_per_bulan[bulan_tahun] += data['nominal']
                data_pengeluaran.remove(data)
                print("Data Pengeluaran berhasil dihapus.")
                return
        print("Data tidak ditemukan.")
    else:
        print("Pilihan tidak valid.")

def set_batas_pengeluaran():
    global batas_pengeluaran
    try:
        batas_pengeluaran = int(input("Masukkan batas pengeluaran perbulan (dalam angka): "))
        print(f"Batas pengeluaran perbulan berhasil diset: {batas_pengeluaran}")
    except ValueError:
        print("Input tidak valid! Masukkan angka.")

def cek_batas_pengeluaran():
    global batas_pengeluaran
    if batas_pengeluaran is None:
        print("Batas pengeluaran perbulan belum diset.")
        return

    try:
        bulan_input = input("Masukkan bulan (nama/angka): ").strip()
        tahun_input = int(input("Masukkan tahun (yyyy): ").strip())
        
        bulan_angka = konversi_bulan(bulan_input)
        if not bulan_angka:
            raise ValueError("Bulan tidak valid!")
        
        bulan_tahun = f"{bulan_angka}-{tahun_input}"
        
    except ValueError as e:
        print(e)
        return

    total_pengeluaran = sum(data['nominal'] for data in data_pengeluaran if data['tanggal'].endswith(bulan_tahun))
    
    print(f"\nTotal Pengeluaran untuk {bulan_input.capitalize()} {tahun_input}: {total_pengeluaran}")
    print(f"Batas Pengeluaran: {batas_pengeluaran}")

    if total_pengeluaran > batas_pengeluaran:
        print("Peringatan! Pengeluaran melebihi batas yang telah ditentukan.")
    else:
        print("Pengeluaran masih dalam batas yang ditentukan.")

def menu_utama():
    while True:
        print("\n===== Menu Utama =====")
        print("1. Tambahkan Data")
        print("2. Tampilkan Rekapan Perhari")
        print("3. Tampilkan Data Perbulan")
        print("4. Update Data")
        print("5. Hapus Data")
        print("6. Set Batas Pengeluaran")
        print("7. Cek Batas Pengeluaran")
        print("8. Keluar")

        pilihan = input("Masukkan pilihan: ").strip()
        
        if pilihan == "1":
            tambahkan_data()
        elif pilihan == "2":
            tampilkan_rekapan_perhari()
        elif pilihan == "3":
            tampilkan_data_perbulan()
        elif pilihan == "4":
            update_data()
        elif pilihan == "5":
            hapus()
        elif pilihan == "6":
            set_batas_pengeluaran()
        elif pilihan == "7":
            cek_batas_pengeluaran()
        elif pilihan == "8":
            print("Keluar dari program. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

nama = input("Masukkan nama anda: ")
status = input("Apa status anda sekarang?")
print(f"Hai {nama}, mungkin program ini dapat membantu mengelola keuangan anda saat {status}")

menu_utama() 
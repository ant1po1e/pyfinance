import csv
import os
import math
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

FILE_NAME = "log.csv"
PAGE_SIZE = 5 


def clear():
    """
    Membersihkan layar terminal.
    Menyesuaikan perintah clear sesuai dengan sistem operasi
    """
    os.system("cls" if os.name == "nt" else "clear")


def init_file():
    """
    Mengecek keberadaan file CSV penyimpanan data transaksi.
    Jika file belum ada, maka file akan dibuat beserta header kolom.
    """
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "type", "money", "reason"])


def read_logs():
    """
    Membaca seluruh data transaksi dari file CSV.

    Return:
        list: daftar transaksi dalam bentuk list of dictionary.
    """
    logs = []
    with open(FILE_NAME, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            logs.append(row)
    return logs


def calculate_summary(logs):
    """
    Menghitung ringkasan keuangan dari daftar transaksi.
    Mengabaikan baris data yang tidak lengkap atau tidak valid.
    """
    total_income = 0
    total_expense = 0

    for l in logs:
        # Pastikan key penting ada
        if "type" not in l or "money" not in l:
            continue

        # Pastikan nilai money valid
        try:
            amount = int(l["money"])
        except (ValueError, TypeError):
            continue

        if l["type"] == "income":
            total_income += amount
        elif l["type"] == "expense":
            total_expense += amount

    current_money = total_income - total_expense
    return current_money, total_income, total_expense


def pause():
    """
    Memberhentikan sementara program sampai pengguna menekan ENTER.
    Digunakan agar output dapat dibaca sebelum kembali ke menu.
    """
    input("\nTekan ENTER untuk kembali...")


def show_paginated_logs(logs):
    """
    Menampilkan daftar transaksi secara bertahap (pagination).
    Mengabaikan data yang tidak lengkap.
    """
    if not logs:
        print("Belum ada log.")
        return

    # Filter hanya log yang valid
    valid_logs = []
    for l in logs:
        if all(k in l for k in ("date", "type", "money", "reason")):
            valid_logs.append(l)

    if not valid_logs:
        print("Tidak ada data valid untuk ditampilkan.")
        pause()
        return

    page = 0
    max_page = math.ceil(len(valid_logs) / PAGE_SIZE)

    while True:
        clear()
        start = page * PAGE_SIZE
        end = start + PAGE_SIZE
        subset = valid_logs[start:end]

        print(f"=== LOG TRANSAKSI (Page {page+1}/{max_page}) ===")
        for i, log in enumerate(subset, start):
            print(f"{i}. {log['date']} | {log['type']} | {log['money']} | {log['reason']}")

        print("\n[N] Next Page | [P] Previous Page | [X] Exit")
        nav = input("Navigasi: ").lower()

        if nav == "n" and page < max_page - 1:
            page += 1
        elif nav == "p" and page > 0:
            page -= 1
        elif nav == "x":
            break

def show_summary():
    """
    Menampilkan ringkasan saldo, pemasukan, dan pengeluaran.
    Setelah itu menampilkan daftar log transaksi secara bertahap.
    """
    clear()
    logs = read_logs()
    current, inc, exp = calculate_summary(logs)

    print("╔══════════════════════════════╗")
    print("║      RINGKASAN TABUNGAN      ║")
    print("╚══════════════════════════════╝")
    print(f"Saldo Sekarang : {current}")
    print(f"Pemasukan      : {inc}")
    print(f"Pengeluaran    : {exp}")
    print("────────────────────────────────\n")

    show_paginated_logs(logs)
    pause()


def exit_option(check):
    """
    Mengecek apakah pengguna memilih keluar (X).

    Parameter:
        check (str): input dari pengguna.

    Return:
        bool: True jika dibatalkan, False jika lanjut.
    """
    if check.lower() == "x":
        print("Dibatalkan!")
        pause()
        return True
    return False


def add_log():
    """
    Menambahkan transaksi baru ke dalam file CSV.
    Tanggal transaksi otomatis menggunakan tanggal hari ini.
    """
    clear()
    print("=== TAMBAH TRANSAKSI ===")
    print("Tekan X untuk batal\n")

    date = datetime.today().strftime("%Y-%m-%d")
    print(f"Tanggal: {date}")

    tipe = input("Tipe (income/expense): ").lower()
    if exit_option(tipe): return
    if tipe not in ["income", "expense"]:
        print("Tipe salah!")
        pause()
        return

    while True:
        money = input("Jumlah uang: ")
        if exit_option(money): return

        if not money.isdigit():
            print("Jumlah uang harus berupa angka dan tidak boleh kosong!")
            continue

        money = int(money)
        if money <= 0:
            print("Jumlah uang harus lebih dari 0!")
            continue

        break

    reason = ""
    if tipe == "expense":
        reason = input("Alasan: ")
        if exit_option(reason): return
        if not reason.strip():
            print("Reason wajib untuk expense!")
            pause()
            return

    with open(FILE_NAME, "a", newline="") as f:
        csv.writer(f).writerow([date, tipe, money, reason])

    print("✔ Transaksi sukses ditambahkan!")
    pause()


def edit_log():
    """
    Mengedit data transaksi berdasarkan indeks yang dipilih pengguna.
    """
    clear()
    logs = read_logs()
    if not logs:
        print("Tidak ada data!")
        pause()
        return

    show_paginated_logs(logs)

    idx = input("Index log yang diedit (X untuk batal): ")
    if exit_option(idx): return

    try:
        idx = int(idx)
        log = logs[idx]
    except:
        print("Index salah!")
        pause()
        return

    print("\nKosongkan untuk tidak mengubah")
    date = input(f"Tanggal baru ({log['date']}): ") or log["date"]
    tipe = input(f"Tipe baru ({log['type']}): ") or log["type"]
    money = input(f"Money baru ({log['money']}): ") or log["money"]
    reason = log["reason"]
    if tipe == "expense":
        reason = input(f"Reason baru ({log['reason']}): ") or log["reason"]

    logs[idx] = {"date": date, "type": tipe, "money": money, "reason": reason}
    write_logs(logs)
    print("✔ Log diperbarui!")
    pause()


def delete_log():
    """
    Menghapus transaksi berdasarkan indeks yang dipilih pengguna.
    """
    clear()
    logs = read_logs()
    if not logs:
        print("Tidak ada data!")
        pause()
        return

    show_paginated_logs(logs)

    idx = input("Index log yang dihapus (X untuk batal): ")
    if exit_option(idx): return

    try:
        logs.pop(int(idx))
        write_logs(logs)
        print("✔ Log dihapus!")
    except:
        print("Index salah!")
    pause()


def write_logs(logs):
    """
    Menyimpan ulang seluruh data transaksi ke file CSV.

    Parameter:
        logs (list): daftar transaksi yang akan ditulis.
    """
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "type", "money", "reason"])
        for l in logs:
            writer.writerow([l["date"], l["type"], l["money"], l["reason"]])


def show_main_summary():
    """
    Menampilkan ringkasan singkat saldo, pemasukan, dan pengeluaran
    pada menu utama.
    """
    logs = read_logs()
    current, inc, exp = calculate_summary(logs)
    print(f"Saldo: {current} | Pemasukan: {inc} | Pengeluaran: {exp}")


def show_graph():
    """
    Menampilkan grafik garis yang menunjukkan tren bulanan:
    - Income
    - Expense
    - Saldo kumulatif
    """
    clear()
    logs = read_logs()

    if not logs:
        print("Belum ada data untuk grafik!")
        pause()
        return

    monthly_income = defaultdict(int)
    monthly_expense = defaultdict(int)

    for l in logs:
        for l in logs:
            date = l.get("date", "").strip()
            tipe = l.get("type", "").strip()
            money = l.get("money", "").strip()

            if not date or not tipe or not money:
                continue

            try:
                amount = int(money)
            except ValueError:
                continue

            month = date[:7]

            if tipe == "income":
                monthly_income[month] += amount
            elif tipe == "expense":
                monthly_expense[month] += amount

            try:
                amount = int(l["money"])
            except (ValueError, TypeError):
                continue

        month = l["date"][:7]

        if l["type"] == "income":
            monthly_income[month] += amount
        elif l["type"] == "expense":
            monthly_expense[month] += amount

    months = sorted(set(monthly_income.keys()) | set(monthly_expense.keys()))

    incomes, expenses, balances = [], [], []
    saldo = 0

    for m in months:
        inc = monthly_income[m]
        exp = monthly_expense[m]
        saldo += inc - exp

        incomes.append(inc)
        expenses.append(exp)
        balances.append(saldo)

    plt.figure(figsize=(10, 5))
    plt.plot(months, incomes, marker="o", label="Income")
    plt.plot(months, expenses, marker="o", label="Expense")
    plt.plot(months, balances, marker="o", label="Saldo")

    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Uang")
    plt.title("Grafik Tren Income, Expense, dan Saldo Bulanan")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    """
    Fungsi utama program.
    Mengatur alur menu dan pemanggilan seluruh fitur aplikasi.
    """
    init_file()
    while True:
        clear()
        print("╔═══════════════════════════╗")
        print("║     APLIKASI TABUNGAN     ║")
        print("╚═══════════════════════════╝")
        show_main_summary()
        print("""
1. Lihat Ringkasan & Log
2. Tambah Transaksi
3. Edit Log
4. Hapus Log
5. Lihat Grafik
6. Keluar
""")

        pilihan = input("Pilih menu: ")
        if pilihan == "1": show_summary()
        elif pilihan == "2": add_log()
        elif pilihan == "3": edit_log()
        elif pilihan == "4": delete_log()
        elif pilihan == "5": show_graph()
        elif pilihan == "6":
            clear()
            print("👋 Terima kasih sudah menabung!")
            break
        else:
            print("Pilihan salah!")
            pause()


if __name__ == "__main__":
    main()

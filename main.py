import csv
import os
import math
import matplotlib.pyplot as plt

FILE_NAME = "log.csv"
PAGE_SIZE = 5  # jumlah log per halaman

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def init_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "type", "money", "reason"])

def read_logs():
    logs = []
    with open(FILE_NAME, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            logs.append(row)
    return logs

def calculate_summary(logs):
    total_income = sum(int(l["money"]) for l in logs if l["type"] == "income")
    total_expense = sum(int(l["money"]) for l in logs if l["type"] == "expense")
    current_money = total_income - total_expense
    return current_money, total_income, total_expense

def pause():
    input("\nTekan ENTER untuk kembali...")

def show_paginated_logs(logs):
    if not logs:
        print("Belum ada log.")
        return

    page = 0
    max_page = math.ceil(len(logs) / PAGE_SIZE)

    while True:
        clear()
        start = page * PAGE_SIZE
        end = start + PAGE_SIZE
        subset = logs[start:end]

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
    clear()
    logs = read_logs()
    current, inc, exp = calculate_summary(logs)

    print("╔══════════════════════════════╗")
    print("║     RINGKASAN TABUNGAN      ║")
    print("╚══════════════════════════════╝")
    print(f"Saldo Sekarang : {current}")
    print(f"Pemasukan      : {inc}")
    print(f"Pengeluaran    : {exp}")
    print("────────────────────────────────\n")

    show_paginated_logs(logs)
    pause()

def exit_option(check):
    if check.lower() == "x":
        print("Dibatalkan!")
        pause()
        return True
    return False

def add_log():
    clear()
    print("=== TAMBAH TRANSAKSI ===")
    print("Tekan X untuk batal\n")

    date = input("Tanggal (YYYY-MM-DD): ")
    if exit_option(date): return

    tipe = input("Tipe (income/expense): ").lower()
    if exit_option(tipe): return
    if tipe not in ["income", "expense"]:
        print("Tipe salah!")
        pause()
        return

    money = input("Jumlah uang: ")
    if exit_option(money): return

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
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "type", "money", "reason"])
        for l in logs:
            writer.writerow([l["date"], l["type"], l["money"], l["reason"]])

def show_main_summary():
    logs = read_logs()
    current, inc, exp = calculate_summary(logs)
    print(f"Saldo: {current} | Income: {inc} | Expense: {exp}")

def show_graph():
    clear()
    logs = read_logs()
    _, inc, exp = calculate_summary(logs)

    plt.bar(["Income", "Expense"], [inc, exp])
    plt.title("Grafik Pemasukan vs Pengeluaran")
    plt.show()

def main():
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

#!/usr/bin/env python3
import os
import json
import argparse
from datetime import datetime


STORAGE = os.path.join(os.path.dirname(__file__), "todos.json")

# Daftar kategori yang diminta
CATEGORIES = [
	"Tugas Sekolah",
	"Pekerjaan Rumah",
	"Acara Keluarga",
	"Agenda Organisasi",
	"Ulang Tahun",
	"Pertemuan OSIS",
	"Jadwal Olahraga",
	"Hari Penting Lainnya",
	"Nongkrong",
	"Main Bola"
]


def load_todos():
	if not os.path.exists(STORAGE):
		return []
	try:
		with open(STORAGE, "r", encoding="utf-8") as f:
			return json.load(f)
	except Exception:
		return []


def save_todos(todos):
	with open(STORAGE, "w", encoding="utf-8") as f:
		json.dump(todos, f, ensure_ascii=False, indent=2)


def print_todos(todos):
	if not todos:
		print("Belum ada kegiatan tersimpan.")
		return
	print("\nDaftar Kegiatan:")
	print("=" * 72)
	for i, t in enumerate(todos, 1):
		status = "Selesai" if t.get("done") else "Belum selesai"
		date = t.get("date") or "-"
		desc = t.get("desc") or ""
		category = t.get("category") or "Umum"
		title = t.get("title") or "(tanpa judul)"
		print(f"{i:2d}. {title} [{category}]")
		print(f"     Status : {status}")
		print(f"     Tanggal: {date}")
		if desc:
			print(f"     Keterangan: {desc}")
		print("-" * 72)


def choose_category_interactive():
	print("Pilih kategori:")
	for idx, c in enumerate(CATEGORIES, 1):
		print(f"{idx}. {c}")
	print("0. Lainnya (ketik sendiri)")
	while True:
		choice = input("Masukkan nomor kategori: ").strip()
		if not choice:
			return None
		try:
			n = int(choice)
		except ValueError:
			print("Masukan tidak valid. Masukkan nomor.")
			continue
		if n == 0:
			custom = input("Ketik kategori custom: ").strip()
			return custom or None
		if 1 <= n <= len(CATEGORIES):
			return CATEGORIES[n - 1]
		print("Nomor di luar jangkauan.")


def add_todo(title, category=None, desc=None, date=None):
	todos = load_todos()
	todos.append({
		"title": title,
		"category": category or "Umum",
		"desc": desc,
		"date": date,
		"done": False,
	})
	save_todos(todos)
	print("Kegiatan ditambahkan.")
	print_todos(todos)


def edit_todo(index, title=None, category=None, desc=None, date=None):
	todos = load_todos()
	if index < 1 or index > len(todos):
		print("Index tidak valid.")
		return
	t = todos[index - 1]
	if title is not None:
		t["title"] = title
	if category is not None:
		t["category"] = category
	if desc is not None:
		t["desc"] = desc
	if date is not None:
		t["date"] = date
	save_todos(todos)
	print("Kegiatan diperbarui.")
	print_todos(todos)


def set_done(index, done=True):
	todos = load_todos()
	if index < 1 or index > len(todos):
		print("Index tidak valid.")
		return
	todos[index - 1]["done"] = bool(done)
	save_todos(todos)
	print("Status diperbarui.")
	print_todos(todos)


def delete_todo(index):
	todos = load_todos()
	if index < 1 or index > len(todos):
		print("Index tidak valid.")
		return
	todos.pop(index - 1)
	save_todos(todos)
	print("Kegiatan dihapus.")
	print_todos(todos)


def interactive_menu():
	while True:
		print("\n--- To-do List Sederhana ---")
		print("1. Lihat kegiatan")
		print("2. Tambah kegiatan")
		print("3. Edit kegiatan")
		print("4. Tandai selesai/belum")
		print("5. Hapus kegiatan")
		print("6. Keluar")
		choice = input("Pilih (1-6): ").strip()
		if choice == "1":
			print_todos(load_todos())
		elif choice == "2":
			title = input("Judul: ").strip()
			category = choose_category_interactive()
			desc = input("Keterangan (opsional): ").strip() or None
			date = input("Tanggal (YYYY-MM-DD, opsional): ").strip() or None
			add_todo(title, category, desc, date)
		elif choice == "3":
			try:
				idx = int(input("Index kegiatan: ").strip())
			except ValueError:
				print("Index tidak valid.")
				continue
			title = input("Judul baru (kosong = tidak mengubah): ").strip()
			title = title if title else None
			print("Ganti kategori? (tekan enter untuk tidak)")
			category = None
			cchoice = input("Ubah kategori? (y/n): ").strip().lower()
			if cchoice == "y":
				category = choose_category_interactive()
			desc = input("Keterangan baru (kosong = tidak mengubah): ").strip()
			desc = desc if desc else None
			date = input("Tanggal baru (YYYY-MM-DD, kosong = tidak mengubah): ").strip()
			date = date if date else None
			edit_todo(idx, title, category, desc, date)
		elif choice == "4":
			try:
				idx = int(input("Index kegiatan: ").strip())
			except ValueError:
				print("Index tidak valid.")
				continue
			todos = load_todos()
			if idx < 1 or idx > len(todos):
				print("Index tidak valid.")
				continue
			new = not todos[idx - 1].get("done")
			set_done(idx, new)
		elif choice == "5":
			try:
				idx = int(input("Index kegiatan: ").strip())
			except ValueError:
				print("Index tidak valid.")
				continue
			delete_todo(idx)
		elif choice == "6":
			print("Sampai jumpa!")
			break
		else:
			print("Pilihan tidak dikenali.")


def parse_args():
	p = argparse.ArgumentParser(description="To-do List sederhana")
	p.add_argument("--list", action="store_true", help="Lihat semua kegiatan")
	p.add_argument("--add", metavar="JUDUL", help="Tambah kegiatan dengan judul")
	p.add_argument("--category", metavar="KATEGORI", help="Kategori untuk --add atau --edit")
	p.add_argument("--desc", metavar="KETERANGAN", help="Keterangan untuk --add atau --edit")
	p.add_argument("--date", metavar="YYYY-MM-DD", help="Tanggal untuk --add atau --edit")
	p.add_argument("--edit", metavar="INDEX", type=int, help="Edit kegiatan berdasarkan index")
	p.add_argument("--mark", metavar="INDEX", type=int, help="Tandai selesai berdasarkan index")
	p.add_argument("--unmark", metavar="INDEX", type=int, help="Tandai belum selesai berdasarkan index")
	p.add_argument("--delete", metavar="INDEX", type=int, help="Hapus kegiatan berdasarkan index")
	p.add_argument("--interactive", action="store_true", help="Menu interaktif")
	return p.parse_args()


def main():
	args = parse_args()
	if args.list:
		print_todos(load_todos())
		return
	if args.add:
		add_todo(args.add, args.category, args.desc, args.date)
		return
	if args.edit is not None:
		edit_todo(args.edit, args.add, args.category, args.desc, args.date)
		return
	if args.mark is not None:
		set_done(args.mark, True)
		return
	if args.unmark is not None:
		set_done(args.unmark, False)
		return
	if args.delete is not None:
		delete_todo(args.delete)
		return
	if args.interactive or (not any(vars(args).values())):
		interactive_menu()


if __name__ == "__main__":
	main()


"""
v1 baseline CLI (simple console app).
"""
from __future__ import annotations
from datetime import date
from pathlib import Path
from typing import Optional

from login_module import authenticate
from student_module import list_students, add_student
from attendance_module import list_attendance, mark_attendance
from result_module import list_results, upsert_marks
from openpyxl import Workbook

def export_to_excel(filename: str, headers: list[str], rows: list[list]):
    wb = Workbook()
    ws = wb.active
    ws.title = "Export"
    ws.append(headers)
    for r in rows:
        ws.append(r)
    wb.save(filename)

def prompt(msg: str, default: Optional[str]=None) -> str:
    if default is None:
        return input(msg).strip()
    val = input(f"{msg} [{default}]: ").strip()
    return val or default

def main():
    print("Student Result & Attendance Management System (v1)")
    print("-------------------------------------------------")
    u = prompt("Username", "admin")
    p = prompt("Password", "admin")
    if not authenticate(u, p):
        print("Invalid credentials.")
        return

    while True:
        print("\nMenu:")
        print("1) List students")
        print("2) Mark attendance (single student)")
        print("3) List attendance (by date/class)")
        print("4) Enter marks (single student)")
        print("5) List results (by class/subject)")
        print("6) Export attendance to Excel")
        print("7) Export results to Excel")
        print("0) Exit")
        choice = prompt("Select option", "1")

        if choice == "0":
            break

        if choice == "1":
            cls = prompt("Class (e.g., BCA-3)", "BCA-3")
            rows = list_students(cls)
            for r in rows:
                print(f"{r['roll_no']} | {r['full_name']} | {r['class_name']} | {r['status']}")
        elif choice == "2":
            d = prompt("Date (YYYY-MM-DD)", str(date.today()))
            roll = prompt("Roll No", "BCA3-001")
            pres = prompt("Present? (y/n)", "y").lower().startswith("y")
            mark_attendance(d, roll, pres)
            print("Saved.")
        elif choice == "3":
            d = prompt("Date (YYYY-MM-DD)", "2026-01-02")
            cls = prompt("Class", "BCA-3")
            rows = list_attendance(d, cls)
            for r in rows:
                print(f"{r['roll_no']} | {r['full_name']} | {r['attendance_date']} | {r['present']}")
        elif choice == "4":
            roll = prompt("Roll No", "BCA3-001")
            subject = prompt("Subject", "DBMS")
            term = prompt("Term", "Term-1")
            internal = int(prompt("Internal (0-30)", "20"))
            external = int(prompt("External (0-70)", "45"))
            upsert_marks(roll, subject, term, internal, external)
            print("Saved.")
        elif choice == "5":
            cls = prompt("Class", "BCA-3")
            subject = prompt("Subject", "DBMS")
            term = prompt("Term", "Term-1")
            rows = list_results(cls, subject, term)
            for r in rows:
                print(f"{r['roll_no']} | {r['full_name']} | {r['internal_marks']} | {r['external_marks']} | {r['total_marks']} | {r['pass_fail']}")
        elif choice == "6":
            d = prompt("Date (YYYY-MM-DD)", "2026-01-02")
            cls = prompt("Class", "BCA-3")
            rows = list_attendance(d, cls)
            out = Path("export")
            out.mkdir(exist_ok=True)
            filename = out / f"attendance_{cls}_{d}.xlsx"
            export_to_excel(str(filename), ["Roll No","Student Name","Date","Present"], [[r["roll_no"],r["full_name"],r["attendance_date"],r["present"]] for r in rows])
            print(f"Exported: {filename}")
        elif choice == "7":
            cls = prompt("Class", "BCA-3")
            subject = prompt("Subject", "DBMS")
            term = prompt("Term", "Term-1")
            rows = list_results(cls, subject, term)
            out = Path("export")
            out.mkdir(exist_ok=True)
            filename = out / f"results_{cls}_{subject}_{term}.xlsx"
            export_to_excel(str(filename), ["Roll No","Student Name","Internal","External","Total","Pass/Fail"], [[r["roll_no"],r["full_name"],r["internal_marks"],r["external_marks"],r["total_marks"],r["pass_fail"]] for r in rows])
            print(f"Exported: {filename}")
        else:
            print("Unknown option.")

if __name__ == "__main__":
    main()

import sqlite3
import csv
import os
from datetime import datetime

DB_PATH = "data/orbit.db"
CSV_PATH = "data/audit_log.csv"

def init_audit_log():
    """Create audit log table if it doesn't exist"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cv_filename TEXT,
            domain_assigned TEXT,
            confidence_score TEXT,
            offer_status TEXT,
            edited_by TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_event(cv_filename, domain_assigned, confidence_score, offer_status, edited_by="System", notes=""):
    """Save a new event to audit log"""
    init_audit_log()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_log (timestamp, cv_filename, domain_assigned, confidence_score, offer_status, edited_by, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, cv_filename, domain_assigned, str(confidence_score), offer_status, edited_by, notes))
    conn.commit()
    conn.close()

def get_all_logs():
    """Get all logs from database"""
    init_audit_log()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_log ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    conn.close()
    return logs

def export_to_csv():
    """Export all logs to CSV file"""
    logs = get_all_logs()
    os.makedirs("data", exist_ok=True)
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Timestamp", "CV Filename", "Domain", "Confidence Score", "Offer Status", "Edited By", "Notes"])
        writer.writerows(logs)
    return CSV_PATH
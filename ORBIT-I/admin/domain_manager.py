import sqlite3

DB_PATH = "data/orbit.db"

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS domains (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain_name TEXT UNIQUE NOT NULL,
        keywords TEXT,
        required_skills TEXT,
        salary_range TEXT,
        offer_letter_template TEXT
    )
    """)
    conn.commit()
    conn.close()
    return "Table created successfully!"

def add_domain(domain_name, keywords, required_skills, salary_range, offer_letter_template):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO domains
    (domain_name, keywords, required_skills, salary_range, offer_letter_template)
    VALUES (?, ?, ?, ?, ?)
    """, (
        domain_name,
        keywords,
        required_skills,
        salary_range,
        offer_letter_template
    ))
    conn.commit()
    conn.close()
    return "Domain added successfully!"

def view_domains():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM domains")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_domain(old_domain_name, domain_name, keywords, required_skills, salary_range, offer_letter_template):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE domains
    SET
        domain_name = ?,
        keywords = ?,
        required_skills = ?,
        salary_range = ?,
        offer_letter_template = ?
    WHERE domain_name = ?
    """, (
        domain_name,
        keywords,
        required_skills,
        salary_range,
        offer_letter_template,
        old_domain_name
    ))
    conn.commit()
    conn.close()
    return "Domain updated successfully!"

def delete_domain(domain_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM domains
    WHERE domain_name = ?
    """, (
        domain_name,
    ))
    conn.commit()
    conn.close()
    return "Domain deleted successfully!"

if __name__ == "__main__":
    print(create_table())

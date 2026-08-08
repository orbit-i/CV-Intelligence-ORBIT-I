import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'orbit-I'))

import streamlit as st
import sqlite3
import pdfplumber
from docx import Document

# ── DB Path ──
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'orbit-I'))
DB_PATH = os.path.join(BASE, "data", "orbit.db")

# ── DB Functions ──
def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS domains (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain_name TEXT UNIQUE NOT NULL,
        keywords TEXT,
        required_skills TEXT,
        offer_letter_template TEXT
    )
    """)
    conn.commit()
    conn.close()

def get_all_domains():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM domains")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_domain(domain_name, keywords, required_skills, template):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO domains (domain_name, keywords, required_skills, offer_letter_template)
        VALUES (?, ?, ?, ?)
        """, (domain_name, keywords, required_skills, template))
        conn.commit()
        conn.close()
        return True, "Domain added successfully!"
    except Exception as e:
        return False, str(e)

def update_domain(old_name, domain_name, keywords, required_skills, template):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE domains SET domain_name=?, keywords=?, required_skills=?, offer_letter_template=?
        WHERE domain_name=?
        """, (domain_name, keywords, required_skills, template, old_name))
        conn.commit()
        conn.close()
        return True, "Domain updated successfully!"
    except Exception as e:
        return False, str(e)

def delete_domain(domain_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM domains WHERE domain_name=?", (domain_name,))
    conn.commit()
    conn.close()

create_table()

# ── Page Config ──
st.set_page_config(page_title="ORBIT-I | Domain Manager", page_icon="🌐", layout="wide")

# ── CSS ──
st.markdown("""
<style>
    [data-testid="stSidebarNav"] ul li:first-child {display: none;}
    [data-testid="stSidebarNav"]::before {
        content: "ORBIT-I";
        display: block;
        font-size: 20px;
        font-weight: 700;
        color: #1a3a6b;
        padding: 24px 16px 16px 16px;
        letter-spacing: 1px;
    }

    .domain-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .domain-badge {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 13px;
        flex-shrink: 0;
    }

    .level-badge {
        padding: 3px 12px;
        border-radius: 100px;
        font-size: 12px;
        font-weight: 600;
    }

    .merge-tag {
        display: inline-block;
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-family: monospace;
        margin: 3px;
    }

    .section-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .tester-result {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        padding: 16px;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ── Session State ──
if "edit_domain" not in st.session_state:
    st.session_state.edit_domain = None
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None
if "tester_result" not in st.session_state:
    st.session_state.tester_result = None

# ── Page Header ──
col_title, col_btn = st.columns([3, 1])
with col_title:
    st.markdown("## 🌐 Domain & Template Manager")
    st.markdown("Manage hiring domains, templates, keywords and test AI classification.")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Batch Processing", use_container_width=True):
        st.switch_page("pages/batch_processing.py")

st.divider()

# ── Main Layout ──
left_col, right_col = st.columns([1, 1], gap="large")

# ═══════════════════════════════
# LEFT COLUMN
# ═══════════════════════════════
with left_col:

    # ── Domain List ──
    with st.container():
        h1, h2 = st.columns([2, 1])
        with h1:
            st.markdown("### Domain List")
        with h2:
            if st.button("➕ Add Domain", use_container_width=True, type="primary"):
                st.session_state.edit_domain = "new"

        domains = get_all_domains()

        COLORS = [
            ("#dbeafe", "#1d4ed8"),
            ("#fce7f3", "#9d174d"),
            ("#dcfce7", "#15803d"),
            ("#fef3c7", "#b45309"),
            ("#ede9fe", "#6d28d9"),
            ("#fee2e2", "#b91c1c"),
        ]

        if domains:
            st.markdown(f"<p style='color:#64748b; font-size:13px;'>Showing 1 to {len(domains)} of {len(domains)} domains</p>", unsafe_allow_html=True)

            # Table header
            # Table header
            th1, th2, th3 = st.columns([4, 1, 1])
            with th1: st.markdown("<p style='font-size:11px; color:#94a3b8; font-weight:600; letter-spacing:1px;'>DOMAIN NAME</p>", unsafe_allow_html=True)
            with th2: st.markdown("<p style='font-size:11px; color:#94a3b8; font-weight:600; letter-spacing:1px;'>ACTIONS</p>", unsafe_allow_html=True)
            with th3: st.markdown("", unsafe_allow_html=True)

            for i, domain in enumerate(domains):
                did, dname, keywords, skills, *rest = domain
                bg, fg = COLORS[i % len(COLORS)]
                initials = "".join([w[0].upper() for w in dname.split()[:2]])

                c1, c2, c3 = st.columns([4, 1, 1])
                with c1:
                    st.markdown(f"""
                        <div style='display:flex; align-items:center; gap:10px; padding:8px 0;'>
                            <div style='background:{bg}; color:{fg}; width:36px; height:36px; border-radius:8px;
                                display:flex; align-items:center; justify-content:center; font-weight:700; font-size:11px; flex-shrink:0;'>
                                {initials}
                            </div>
                            <div>
                                <div style='font-weight:600; font-size:14px; color:#0f172a;'>{dname}</div>
                                <div style='font-size:11px; color:#94a3b8;'>{(keywords or '').split(',')[0].strip() if keywords else '—'}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if st.button("✏️", key=f"edit_{did}", help="Edit"):
                        st.session_state.edit_domain = domain
                with c3:
                    if st.button("🗑️", key=f"del_{did}", help="Delete"):
                        st.session_state.confirm_delete = dname

            # Confirm delete
            if st.session_state.confirm_delete:
                st.warning(f"Delete **{st.session_state.confirm_delete}**?")
                dc1, dc2 = st.columns(2)
                with dc1:
                    if st.button("✅ Yes, Delete", type="primary"):
                        delete_domain(st.session_state.confirm_delete)
                        st.session_state.confirm_delete = None
                        st.rerun()
                with dc2:
                    if st.button("Cancel"):
                        st.session_state.confirm_delete = None
                        st.rerun()
        else:
            st.info("No domains added yet. Click '➕ Add Domain' to get started.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Offer Letter Template ──
    with st.container():
        st.markdown("### 📄 Offer Letter Template")
        st.markdown("<p style='color:#64748b; font-size:13px;'>Upload and manage offer letter templates.</p>", unsafe_allow_html=True)

        st.markdown("**Template File (.DOCX)**")
        template_file = st.file_uploader("", type=["docx"], label_visibility="collapsed", key="template_upload")
        st.markdown("<p style='font-size:11px; color:#94a3b8;'>Only .docx files are supported</p>", unsafe_allow_html=True)

        st.markdown("**Available Merge Fields**")
        merge_fields = [
            "{{candidate_name}}", "{{position}}", "{{department}}",
            "{{salary}}", "{{start_date}}", "{{work_location}}",
            "{{offer_expiry}}", "{{company_name}}"
        ]
        fields_html = "".join([f'<span class="merge-tag">{f}</span>' for f in merge_fields])
        st.markdown(fields_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Template", use_container_width=True, type="primary"):
            if template_file:
                save_path = os.path.join(BASE, "templates", template_file.name)
                with open(save_path, "wb") as f:
                    f.write(template_file.getbuffer())
                st.success(f"✅ Template saved: {template_file.name}")
            else:
                st.warning("Please select a template file first.")

# ═══════════════════════════════
# RIGHT COLUMN
# ═══════════════════════════════
with right_col:

    # ── Domain Setup Form ──
    is_editing = st.session_state.edit_domain is not None
    is_new = st.session_state.edit_domain == "new"

    form_title = "✏️ Edit Domain" if (is_editing and not is_new) else "➕ Domain Setup"
    st.markdown(f"### {form_title}")

    # Pre-fill if editing
    prefill = {}
    old_name = ""
    if is_editing and not is_new and st.session_state.edit_domain:
        d = st.session_state.edit_domain
        old_name = d[1]
        prefill = {
            "name": d[1],
            "keywords": d[2] or "",
            "skills": d[3] or "",
            "template": d[4] if len(d) > 4 else "",
        }

    domain_name = st.text_input("Domain Name *", value=prefill.get("name", ""), placeholder="Enter domain name")
    keyword_tags = st.text_input("Keyword Tags *", value=prefill.get("keywords", ""), placeholder="Enter keywords separated by comma")
    st.markdown("<p style='font-size:11px; color:#94a3b8; margin-top:-12px;'>Example: Figma, UX, Prototype, Adobe XD</p>", unsafe_allow_html=True)

    required_skills = st.text_input("Required Skills *", value=prefill.get("skills", ""), placeholder="Enter skills separated by comma")
    st.markdown("<p style='font-size:11px; color:#94a3b8; margin-top:-12px;'>Example: Wireframing, Prototyping, User Research</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    btn1, btn2 = st.columns([1, 1])
    with btn1:
        if is_editing:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.edit_domain = None
                st.rerun()
    with btn2:
        save_label = "💾 Update Domain" if (is_editing and not is_new) else "💾 Save Domain"
        if st.button(save_label, use_container_width=True, type="primary"):
            if not domain_name:
                st.error("Domain name is required.")
            else:
                if is_editing and not is_new:
                    ok, msg = update_domain(old_name, domain_name, keyword_tags, required_skills, "")
                else:
                    ok, msg = add_domain(domain_name, keyword_tags, required_skills, "")
                if ok:
                    st.success(f"✅ {msg}")
                    st.session_state.edit_domain = None
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── Classification Tester ──
    st.markdown("### 🧪 Classification Tester")
    st.markdown("<p style='color:#64748b; font-size:13px;'>Upload a sample CV to test AI classification for the selected domain.</p>", unsafe_allow_html=True)

    domains_list = get_all_domains()
    domain_names = [d[1] for d in domains_list]

    if domain_names:
        selected_domain = st.selectbox("Select Domain", domain_names)
        test_cv = st.file_uploader("Upload Sample CV", type=["pdf", "docx"], key="test_cv")

        if st.button("▶ Test Classification", type="primary", use_container_width=True):
            if test_cv:
                with st.spinner("Classifying CV..."):
                    try:
                        # Extract text
                        text = ""
                        if test_cv.name.endswith(".pdf"):
                            with pdfplumber.open(test_cv) as pdf:
                                for page in pdf.pages:
                                    t = page.extract_text()
                                    if t:
                                        text += t + "\n"
                        elif test_cv.name.endswith(".docx"):
                            doc = Document(test_cv)
                            text = "\n".join([p.text for p in doc.paragraphs])

                        # Classify
                        from classifier.domain_classifier import classify_resume
                        result = classify_resume(text)
                        st.session_state.tester_result = result
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please upload a CV first.")

        if st.session_state.tester_result:
            r = st.session_state.tester_result
            predicted = r.get("predicted_domain", "Unknown")
            confidence = r.get("confidence", 0)
            color = "#16a34a" if confidence >= 75 else "#d97706" if confidence >= 50 else "#dc2626"

            st.markdown(f"""
                <div style='background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:16px; margin-top:12px;
                    display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <p style='font-size:12px; color:#64748b; margin-bottom:4px;'>Predicted Domain</p>
                        <p style='font-size:22px; font-weight:800; color:{color}; margin:0;'>{predicted}</p>
                    </div>
                    <div style='text-align:right;'>
                        <p style='font-size:12px; color:#64748b; margin-bottom:4px;'>Match Confidence</p>
                        <p style='font-size:22px; font-weight:800; color:{color}; margin:0;'>{confidence}%</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Add domains first to use the Classification Tester.")

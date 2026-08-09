import streamlit as st
from github import Github
import io
import sys
from contextlib import redirect_stdout

st.set_page_config(page_title="Logical Cognitive Finder & GitHub IDE", layout="wide")

st.title("🧠 Cognitive Functions Finder using Logic")
st.write("ค้นหา Cognitive Functions ด้วยตรรกศาสตร์ พร้อม Streamlit IDE สำหรับ Push ขึ้น GitHub")

# ==========================================
# ส่วนที่ 1: ตรรกศาสตร์การคำนวณ (Logic Engine)
# ==========================================
def deduce_cognitive_functions(e_i, s_n, t_f, j_p):
    """
    ตรรกศาสตร์การหา Function Stack:
    1. ถ้าเป็น J (Judging) -> ฟังก์ชันที่แสดงออกภายนอก (Extraverted) คือ T หรือ F
    2. ถ้าเป็น P (Perceiving) -> ฟังก์ชันที่แสดงออกภายนอก (Extraverted) คือ S หรือ N
    3. ถ้าเป็น E (Extravert) -> ฟังก์ชันหลัก (Dominant) จะเป็น Extraverted
    4. ถ้าเป็น I (Introvert) -> ฟังก์ชันหลัก (Dominant) จะเป็น Introverted
    """
    # หาฟังก์ชัน Extraverted และ Introverted จากแกน S/N และ T/F
    if j_p == 'J':
        ext_func = t_f + 'e'  # Te หรือ Fe
        intro_func = s_n + 'i' # Ni หรือ Si
    else:
        ext_func = s_n + 'e'  # Ne หรือ Se
        intro_func = t_f + 'i' # Ti หรือ Fi
    
    # กำหนด Dominant (หลัก) และ Auxiliary (รอง) ตามแกน E/I
    if e_i == 'E':
        dominant, auxiliary = ext_func, intro_func
    else:
        dominant, auxiliary = intro_func, ext_func

    # ตรรกะของ Tertiary และ Inferior คือขั้วตรงข้าม
    opposites = {'T': 'F', 'F': 'T', 'S': 'N', 'N': 'S', 'e': 'i', 'i': 'e'}
    tertiary = opposites[auxiliary[0]] + opposites[auxiliary[1]]
    inferior = opposites[dominant[0]] + opposites[dominant[1]]
    
    return dominant, auxiliary, tertiary, inferior

# ==========================================
# สร้าง UI ด้วย Tabs
# ==========================================
tab1, tab2 = st.tabs(["🧩 1. ใช้งาน Logic Finder", "💻 2. Code Editor & GitHub Push"])

# ---------------- Tab 1: Logic Finder ----------------
with tab1:
    st.header("ตอบคำถามตรรกะ 4 ข้อ")
    st.write("ระบบจะใช้ IF-THEN Logic เพื่อแปลงคุณสมบัติ 4 ด้านให้เป็น Cognitive Stack")
    
    col1, col2 = st.columns(2)
    with col1:
        e_i = st.radio("1. พลังงาน (Energy):", options=[("E", "โลกภายนอก (Extraversion)"), ("I", "โลกภายใน (Introversion)")], format_func=lambda x: x[1])[0]
        s_n = st.radio("2. ข้อมูล (Information):", options=[("S", "รูปธรรม/ปัจจุบัน (Sensing)"), ("N", "นามธรรม/อนาคต (Intuition)")], format_func=lambda x: x[1])[0]
    with col2:
        t_f = st.radio("3. การตัดสินใจ (Decision):", options=[("T", "เหตุผล/ตรรกะ (Thinking)"), ("F", "ความรู้สึก/ค่านิยม (Feeling)")], format_func=lambda x: x[1])[0]
        j_p = st.radio("4. การใช้ชีวิต (Lifestyle):", options=[("J", "แบบแผน/โครงสร้าง (Judging)"), ("P", "ยืดหยุ่น/เปิดกว้าง (Perceiving)")], format_func=lambda x: x[1])[0]

    if st.button("ประมวลผลทางตรรกศาสตร์ (Run Logic)"):
        dom, aux, ter, inf = deduce_cognitive_functions(e_i, s_n, t_f, j_p)
        mb_type = f"{e_i}{s_n}{t_f}{j_p}"
        
        st.success(f"**ผลลัพธ์บุคลิกภาพของคุณคือ: {mb_type}**")
        st.markdown(f"""
        **โครงสร้าง Cognitive Functions (Function Stack):**
        * 🥇 **Dominant Function:** `{dom}` (กระบวนการหลักที่ใช้เป็นอัตโนมัติ)
        * 🥈 **Auxiliary Function:** `{aux}` (กระบวนการสนับสนุน)
        * 🥉 **Tertiary Function:** `{ter}` (กระบวนการที่ใช้เพื่อผ่อนคลาย)
        * 🎯 **Inferior Function:** `{inf}` (กระบวนการที่เป็นจุดอ่อนหรือทำงานเมื่อเครียด)
        """)

# ---------------- Tab 2: Code Editor & GitHub ----------------
with tab2:
    st.header("📝 Python Code Editor")
    
    # โค้ดตัวอย่างที่โหลดเข้า Editor (ผู้ใช้สามารถแก้ไขและรันได้)
    default_code = """# ตรรกะคำนวณ Cognitive Functions ใน Python
def calculate_functions(mbti_type):
    e_i, s_n, t_f, j_p = mbti_type[0], mbti_type[1], mbti_type[2], mbti_type[3]
    
    if j_p == 'J':
        ext_func, intro_func = t_f + 'e', s_n + 'i'
    else:
        ext_func, intro_func = s_n + 'e', t_f + 'i'
        
    dom = ext_func if e_i == 'E' else intro_func
    aux = intro_func if e_i == 'E' else ext_func
    
    print(f"Type: {mbti_type} -> Dom: {dom}, Aux: {aux}")

# ทดสอบรัน
calculate_functions("INTJ")
calculate_functions("ENFP")
"""
    
    code_input = st.text_area("แก้โค้ด Python ได้ที่นี่", height=250, value=default_code)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("▶️ รันโค้ด (Run Code)"):
            st.markdown("**Output:**")
            f = io.StringIO()
            with redirect_stdout(f):
                try:
                    exec(code_input)
                    st.success("รันสำเร็จ")
                except Exception as e:
                    st.error(f"Error: {e}")
            if f.getvalue():
                st.code(f.getvalue(), language="text")

    with c2:
        st.subheader("☁️ Push to GitHub")
        gh_token = st.text_input("GitHub Token (PAT)", type="password")
        repo_name = st.text_input("Repository (e.g., username/repo_name)")
        file_path = st.text_input("File Path (e.g., logic.py)")
        
        if st.button("Push Code"):
            if not gh_token or not repo_name or not file_path:
                st.warning("กรุณากรอกข้อมูล GitHub ให้ครบ")
            else:
                with st.spinner("Connecting to GitHub..."):
                    try:
                        g = Github(gh_token)
                        repo = g.get_repo(repo_name)
                        try:
                            # อัปเดตไฟล์เดิม
                            contents = repo.get_contents(file_path)
                            repo.update_file(contents.path, "Update code via Streamlit", code_input, contents.sha)
                            st.success(f"Updated {file_path} in {repo_name}")
                        except:
                            # สร้างไฟล์ใหม่
                            repo.create_file(file_path, "Create code via Streamlit", code_input)
                            st.success(f"Created {file_path} in {repo_name}")
                    except Exception as e:
                        st.error(f"GitHub Error: {e}")

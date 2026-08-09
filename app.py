import streamlit as st
from github import Github
import sys
import io
from contextlib import redirect_stdout

st.set_page_config(page_title="Streamlit GitHub Editor", layout="wide")

st.title("💻 Streamlit to GitHub Code Editor")
st.write("แอปสำหรับเขียน รัน และพุชโค้ด Python ขึ้น GitHub")

# แถบด้านข้างสำหรับตั้งค่า GitHub
st.sidebar.header("⚙️ ตั้งค่า GitHub")
github_token = st.sidebar.text_input("GitHub Token (PAT)", type="password", help="รับได้จาก GitHub Settings -> Developer settings -> Personal access tokens")
repo_name = st.sidebar.text_input("ชื่อ Repository (เช่น username/repo_name)")
file_path = st.sidebar.text_input("ชื่อไฟล์ (เช่น main.py หรือ folder/script.py)")
commit_msg = st.sidebar.text_input("Commit Message", value="Update code from Streamlit")

# พื้นที่สำหรับเขียนโค้ด
st.subheader("📝 เขียนโค้ด Python ของคุณที่นี่")
code_input = st.text_area("Code Editor", height=300, value="print('Hello, Streamlit and GitHub!')")

col1, col2 = st.columns(2)

# ส่วนของการรันโค้ด
with col1:
    if st.button("▶️ รันโค้ด (Run Code)"):
        st.markdown("### ผลลัพธ์ (Output):")
        # ดักจับ output ที่ได้จากการใช้คำสั่ง print
        f = io.StringIO()
        with redirect_stdout(f):
            try:
                # คำเตือน: exec() รันโค้ดทุกอย่างที่ถูกป้อนเข้ามา
                exec(code_input)
                st.success("รันโค้ดสำเร็จ!")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
        
        # แสดงผลลัพธ์
        output = f.getvalue()
        if output:
            st.code(output, language="text")
        else:
            st.info("ไม่มี Output ส่งออกมาจากการรันโค้ด")

# ส่วนของการส่งโค้ดขึ้น GitHub
with col2:
    if st.button("☁️ พุชขึ้น GitHub (Push Code)"):
        if not github_token or not repo_name or not file_path:
            st.warning("⚠️ กรุณากรอก GitHub Token, ชื่อ Repository และ ชื่อไฟล์ ในแถบด้านข้างให้ครบถ้วน")
        else:
            with st.spinner("กำลังเชื่อมต่อกับ GitHub..."):
                try:
                    # ล็อกอินเข้า GitHub
                    g = Github(github_token)
                    repo = g.get_repo(repo_name)
                    
                    try:
                        # กรณีที่ 1: มีไฟล์นี้อยู่แล้ว -> ทำการอัปเดตไฟล์ (Update)
                        contents = repo.get_contents(file_path)
                        repo.update_file(
                            path=contents.path, 
                            message=commit_msg, 
                            content=code_input, 
                            sha=contents.sha
                        )
                        st.success(f"✅ อัปเดตไฟล์ `{file_path}` ใน `{repo_name}` สำเร็จ!")
                    
                    except Exception as e:
                        # กรณีที่ 2: ยังไม่มีไฟล์นี้ -> ทำการสร้างไฟล์ใหม่ (Create)
                        # PyGithub จะโยน Exception ถ้าหาไฟล์ไม่เจอ
                        repo.create_file(
                            path=file_path, 
                            message=commit_msg, 
                            content=code_input
                        )
                        st.success(f"✅ สร้างไฟล์ใหม่ `{file_path}` ใน `{repo_name}` สำเร็จ!")
                        
                except Exception as e:
                    st.error(f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อ GitHub: {e}")

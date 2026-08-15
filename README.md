# Cognitive Compass

แบบประเมิน Streamlit ภาษาไทยสำหรับสำรวจ Cognitive Functions ทั้ง 8 ด้าน,
จัดอันดับ MBTI จาก cognitive stack และเชื่อมโยงผลลัพธ์กับความถนัดรายวิชา
เป้าหมายอาชีพ งบประมาณการศึกษา ภาระทางการเงิน ทุน และข้อจำกัดการเดินทาง

## เริ่มใช้งาน

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

แอปนี้ไม่ต้องใช้ API key หรือฐานข้อมูล และสามารถนำไฟล์ `streamlit_app.py`,
`requirements.txt` และ `README.md` ไปวางใน GitHub เพื่อ deploy บน
Streamlit Community Cloud ได้โดยเลือกไฟล์ `streamlit_app.py` เป็น entrypoint

## วิธีคิดคะแนน

- คำถาม Cognitive Functions 80 ข้อ แบ่งเป็น 8 ฟังก์ชัน ฟังก์ชันละ 10 ข้อ
- คำตอบระดับ 1–5 ถูกแปลงเป็นคะแนน 0–100
- MBTI ถูกจัดอันดับด้วยการเทียบคะแนนกับลำดับ Dominant, Auxiliary, Tertiary และ Inferior ของแต่ละ type
- ความถนัดรายวิชา 5 กลุ่มและเป้าหมายการทำงานถูกนำไปประกอบกับข้อจำกัดด้านทุนและการเดินทาง

ผลลัพธ์เป็นเครื่องมือสะท้อนตัวเอง ไม่ใช่การวินิจฉัยทางจิตวิทยา

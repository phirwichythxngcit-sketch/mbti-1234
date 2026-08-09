import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="Cognitive Functions Analyzer",
    page_icon="🧠",
    layout="centered"
)

# ---------------------------------------------------------
# 1. คลังคำถามแยกตาม Cognitive Functions (ตรรกะการจัดหมวด)
# ---------------------------------------------------------
COGNITIVE_QUESTIONS = {
    "Ne": [
        "คุณมักจะเห็นความเป็นไปได้และไอเดียใหม่ๆ ที่เชื่อมโยงกันอย่างรวดเร็ว",
        "คุณชอบการระดมสมองและเริ่มโปรเจกต์ใหม่มากกว่าการนั่งทำสิ่งเดิมให้เสร็จ"
    ],
    "Ni": [
        "คุณมักจะคาดการณ์อนาคตหรือเห็นภาพรวมล่วงหน้าได้อย่างมีสัญชาตญาณ",
        "คุณให้ความสำคัญกับความหมายที่ซ่อนอยู่เบื้องหลังและเป้าหมายระยะยาว"
    ],
    "Se": [
        "คุณตอบสนองต่อสิ่งแวดล้อมรอบตัวได้ไว และชื่นชอบการลงมือทำจริงในปัจจุบัน",
        "คุณมีความสุขกับประสบการณ์ทางประสาทสัมผัส (แสง สี เสียง กิจกรรมกลางแจ้ง)"
    ],
    "Si": [
        "คุณมีความจำที่แม่นยำเกี่ยวกับรายละเอียดในอดีตและชอบความมั่นคง",
        "คุณให้ความสำคัญกับขั้นตอน ประเพณี และข้อมูลที่ผ่านการพิสูจน์แล้ว"
    ],
    "Te": [
        "คุณเน้นผลลัพธ์ ประสิทธิภาพ และการจัดระบบระเบียบเพื่อให้บรรลุเป้าหมาย",
        "คุณใช้ตรรกะภายนอกและข้อมูลเชิงประจักษ์ในการตัดสินใจอย่างตรงไปตรงมา"
    ],
    "Ti": [
        "คุณชอบวิเคราะห์ว่าสิ่งต่างๆ ทำงานอย่างไร และมองหาความถูกต้องทางตรรกะส่วนตัว",
        "คุณชอบแก้ปัญหาที่ซับซ้อนด้วยการแยกแยะและตั้งคำถามกับโครงสร้างความคิด"
    ],
    "Fe": [
        "คุณแคร์ความรู้สึกของคนรอบข้างและพยายามสร้างความกลมกลืนในสังคม",
        "คุณปรับตัวและตัดสินใจโดยคำนึงถึงบรรยากาศและค่านิยมของส่วนรวม"
    ],
    "Fi": [
        "คุณยึดมั่นในค่านิยมและความจริงแท้ของตนเอง ไม่ชอบการเสแสร้ง",
        "คุณตัดสินใจโดยถามตัวเองว่าสิ่งนั้นตรงกับความรู้สึกและความเชื่อภายในหรือไม่"
    ]
}

# คำอธิบายฟังก์ชันแต่ละตัว
FUNCTION_DESCRIPTIONS = {
    "Ne": "Extraverted Intuition — การมองหาความเป็นไปได้และเชื่อมโยงไอเดียภายนอก",
    "Ni": "Introverted Intuition — การมองภาพรวม สัญชาตญาณ และวิสัยทัศน์ระยะยาว",
    "Se": "Extraverted Sensing — การรับรู้โลกกายภาพและการอยู่กับปัจจุบัน",
    "Si": "Introverted Sensing — การอ้างอิงประสบการณ์ ประเพณี และรายละเอียดในอดีต",
    "Te": "Extraverted Thinking — ตรรกะการบริหารจัดการ ประสิทธิภาพ และผลลัพธ์",
    "Ti": "Introverted Thinking — ตรรกะการวิเคราะห์เชิงลึกและความเข้าใจโครงสร้าง",
    "Fe": "Extraverted Feeling — การสร้างความกลมกลืนและความรู้สึกของกลุ่ม",
    "Fi": "Introverted Feeling — ค่านิยมส่วนตัว ความจริงแท้ และความรู้สึกภายใน"
}

# ---------------------------------------------------------
# 2. ฟังก์ชันตรรกศาสตร์ในการวิเคราะห์ผลลัพธ์
# ---------------------------------------------------------
def analyze_cognitive_stack(scores):
    """
    ตรรกะการประมวลผล:
    1. แปลงคะแนนดิบเป็นเปอร์เซ็นต์
    2. จัดอันดับฟังก์ชันจากมากไปน้อย
    3. หา Dominant (ฟังก์ชันหลัก) และ Auxiliary (ฟังก์ชันรอง)
    """
    max_score_per_func = 10  # คำถาม 2 ข้อ x ข้อละ 5 คะแนน
    percentages = {func: (score / max_score_per_func) * 100 for func, score in scores.items()}
    
    # เรียงลำดับคะแนน
    sorted_funcs = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
    
    dom_func = sorted_funcs[0][0]
    aux_func = sorted_funcs[1][0]
    
    return percentages, sorted_funcs, dom_func, aux_func

# ---------------------------------------------------------
# 3. ส่วนการแสดงผลบนหน้าเว็บ (Streamlit UI)
# ---------------------------------------------------------
st.title("🧠 แบบทดสอบ Cognitive Functions")
st.write("ประเมินกระบวนการทางความคิดของคุณตามทฤษฎี Jungian Typology")
st.caption("ให้คะแนนแต่ละข้อตั้งแต่ 1 (ไม่ตรงเลย) ถึง 5 (ตรงมากที่สุด)")

# สร้าง Form สำหรับทำแบบทดสอบ
with st.form("cognitive_test_form"):
    user_responses = {}
    
    for func, questions in COGNITIVE_QUESTIONS.items():
        st.subheader(f"กลุ่มคำถามชุดที่ ({func})")
        user_responses[func] = 0
        
        for idx, q in enumerate(questions):
            key = f"{func}_{idx}"
            score = st.slider(
                label=q,
                min_value=1,
                max_value=5,
                value=3,
                key=key
            )
            user_responses[func] += score
        st.divider()

    submit_btn = st.form_submit_button("วิเคราะห์ผลลัพธ์", type="primary")

# ---------------------------------------------------------
# 4. ส่วนคำนวณและแสดงผลหลังกด Submit
# ---------------------------------------------------------
if submit_btn:
    percentages, sorted_funcs, dom, aux = analyze_cognitive_stack(user_responses)
    
    st.header("📊 ผลการวิเคราะห์ Cognitive Functions")
    
    # แสดงการเปรียบเทียบด้วย Bar Chart
    df_chart = pd.DataFrame({
        "Cognitive Function": list(percentages.keys()),
        "Percentage (%)": list(percentages.values())
    }).set_index("Cognitive Function")
    
    st.bar_chart(df_chart)
    
    # สรุปผลลัพธ์เชิงตรรกะ
    st.subheader("🎯 สรุปฟังก์ชันเด่นของคุณ")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Dominant Function (ฟังก์ชันหลัก)", value=dom)
        st.caption(FUNCTION_DESCRIPTIONS[dom])
    
    with col2:
        st.metric(label="Auxiliary Function (ฟังก์ชันรอง)", value=aux)
        st.caption(FUNCTION_DESCRIPTIONS[aux])
        
    st.divider()
    
    # ตารางแสดงคะแนนละเอียด
    st.subheader("📋 คะแนนแยกตามรายฟังก์ชัน")
    results_data = []
    for rank, (func, score) in enumerate(sorted_funcs, 1):
        results_data.append({
            "อันดับ": rank,
            "Function": func,
            "คะแนน (%)": f"{score:.1f}%",
            "คำอธิบาย": FUNCTION_DESCRIPTIONS[func]
        })
    
    st.table(pd.DataFrame(results_data))

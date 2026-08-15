import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# 1. PAGE CONFIG & CUSTOM CSS (16P Style)
# ==========================================
st.set_page_config(page_title="Advanced MBTI & Career Assessment", page_icon="🧠", layout="wide")

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Kanit', sans-serif;
    }
    
    /* Main container background */
    .stApp {
        background-color: #f3f4f6;
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Card-like styling for tabs and content */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: white;
        padding: 10px 20px 0px 20px;
        border-radius: 10px 10px 0 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #7f8c8d;
    }
    .stTabs [aria-selected="true"] {
        color: #3498db !important;
        border-bottom: 4px solid #3498db !important;
    }
    
    /* Button styling */
    div.stButton > button:first-child {
        background-color: #3498db;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        border: none;
        box-shadow: 0 4px 6px rgba(52, 152, 219, 0.3);
        transition: all 0.3s ease;
        font-weight: 500;
    }
    div.stButton > button:first-child:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
    }

    /* Style the result cards */
    .result-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 24px;
        border-top: 4px solid #8e44ad;
    }
    
    .type-header {
        font-size: 3rem;
        font-weight: 700;
        color: #8e44ad;
        margin-bottom: 0;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 2. DATA STRUCTURES & QUESTIONS
# ==========================================
COGNITIVE_QUESTIONS = {
    "Ne": [
        "มักเชื่อมโยงเรื่องราวที่ไม่เกี่ยวข้องกันได้อย่างรวดเร็ว", "ชอบระดมสมองหาไอเดียใหม่", 
        "มักพูดว่า 'ถ้าเกิดว่า...'", "เบื่อง่ายกับงานซ้ำซาก", "เห็นโอกาสหลายอย่างจนเลือกไม่ถูก", 
        "สนทนากระโดดข้ามเรื่องตามไอเดีย", "เห็นศักยภาพที่ซ่อนอยู่", "ให้ความสำคัญกับนวัตกรรม", 
        "ชอบทดลองวิธีใหม่", "แรงบันดาลใจพุ่งช่วงเริ่มโปรเจกต์"
    ],
    "Ni": [
        "มีอาการ 'อ๋อ!' เข้าใจเรื่องยากได้เอง", "เน้นความหมายเบื้องหลัง", "คาดการณ์แนวโน้มจาก Patterns", 
        "มองภาพรวมมากกว่ารายละเอียด", "ใช้อุปมาอุปไมย", "เชื่อสัญชาตญาณอย่างแรงกล้า", 
        "จดจ่อเป้าหมายระยะยาว", "หาความจริงเพียงหนึ่งเดียว", "เข้าใจเรื่องซับซ้อนลึกซึ้ง", "วางวิสัยทัศน์ 5-10 ปีชัดเจน"
    ],
    "Se": [
        "ตอบสนองสิ่งรอบตัวไว", "ชอบกิจกรรมท้าทายทางกาย", "ชอบสิ่งที่จับต้องได้", 
        "สังเกตรายละเอียดทางกายภาพชัดเจน", "เรียนรู้ผ่านการลงมือทำ", "ตัดสินใจตามสถานการณ์เฉพาะหน้า", 
        "ปรับตัวเข้ากับสิ่งแวดล้อมเก่ง", "ชื่นชอบสุนทรียภาพ", "ไม่ชอบรอคอย ต้องการผลทันที", "สังเกตการเปลี่ยนแปลงเล็กๆ น้อยๆ ได้ดี"
    ],
    "Si": [
        "จำอดีตและรายละเอียดแม่นยำ", "เน้นความมั่นคงประเพณี", "ทำตามขั้นตอนที่เคยสำเร็จ", 
        "อุ่นใจกับกิจวัตรประจำวัน", "สังเกตความผิดปกติของร่างกายไว", "เปรียบเทียบปัจจุบันกับอดีต", 
        "ละเอียดรอบคอบเน้นความถูกต้อง", "ชอบวางแผนมีโครงสร้าง", "เก็บของมีค่าทางจิตใจ", "เชื่อข้อมูลที่พิสูจน์แล้ว"
    ],
    "Te": [
        "เน้นผลลัพธ์และประสิทธิภาพ", "ชอบจัดระเบียบเพื่อให้บรรลุเป้า", "ใช้ตรรกะภายนอกตัดสินใจ", 
        "พูดตรงไปตรงมาเน้นความจริง", "ชอบสร้างตาราง/To-do list", "ตัดสินใจเด็ดขาดเมื่อข้อมูลครบ", 
        "หงุดหงิดกับความไม่เป็นระเบียบ", "ใช้ทรัพยากรคุ้มค่า", "ใช้สถิติสนับสนุนความคิด", "มองว่ากฎเกณฑ์เป็นสิ่งจำเป็น"
    ],
    "Ti": [
        "ชอบแยกแยะดูการทำงาน", "เน้นความถูกต้องทางตรรกะมากกว่าความเร็ว", "มีโครงสร้างตรรกะส่วนตัว", 
        "ตั้งคำถามกับกฎที่ไม่สมเหตุสมผล", "แก้ปัญหาซับซ้อนในหัว", "ต้องการคำนิยามชัดเจน", 
        "วิจารณ์ความคิดตัวเองอย่างเป็นกลาง", "ชอบความรู้เพื่อความรู้", "สันโดษเวลาใช้สมาธิ", "หาจุดบกพร่องทางตรรกะเก่ง"
    ],
    "Fe": [
        "เน้นความรู้สึกคนรอบข้าง", "รักษากลมกลืนเลี่ยงขัดแย้ง", "รับรู้อารมณ์ผู้อื่นด้วยสัญชาตญาณ", 
        "ปรับตัวให้คนอื่นสบายใจ", "เน้นมารยาทสังคม", "สุขเมื่อได้ดูแลคนอื่น", 
        "ประสานรอยร้าวเก่ง", "ตัดสินใจโดยคำนึงถึงความสัมพันธ์", "ต้องการการยอมรับ", "แสดงความรู้สึกทางสีหน้าชัดเจน"
    ],
    "Fi": [
        "มีค่านิยมส่วนตัวเคร่งครัด", "เน้นความจริงแท้และเป็นตัวของตัวเอง", "ประเมินดีเลวตามความรู้สึก", 
        "เห็นอกเห็นใจคนถูกเอาเปรียบ", "เก็บความรู้สึกแชร์แค่คนไว้ใจ", "ไม่ตามกระแสถ้าขัดความรู้สึก", 
        "เข้าใจอารมณ์ซับซ้อน", "หาความสอดคล้องของการกระทำกับค่านิยม", "ไวต่อความเสแสร้ง", "ตัดสินใจโดยถามว่า 'นี่คือตัวเราไหม'"
    ]
}

INTERESTS = [
    "1. คณิตศาสตร์และคอมพิวเตอร์ (เน้นตรรกะ ตัวเลข อัลกอริทึม)",
    "2. วิทยาศาสตร์และเทคโนโลยี (เน้นตั้งคำถาม ทดลอง นวัตกรรม)",
    "3. ภาษาและวรรณกรรม (เน้นสื่อสาร วัฒนธรรม เล่าเรื่อง)",
    "4. สังคมศึกษาและมนุษยศาสตร์ (เน้นเข้าใจมนุษย์ ประวัติศาสตร์ กฎหมาย)",
    "5. ศิลปะ ดนตรี และการออกแบบ (เน้นจินตนาการ สุนทรียภาพ อิสระ)"
]

WORK_GOALS = [
    "อาชีพยืดหยุ่น บริหารเวลา/สถานที่เอง", "โครงสร้างชัดเจน มั่นคง เป็นระบบ", "ท้าทาย แปลกใหม่ ได้สร้างสรรค์",
    "ช่วยเหลือ ดูแล รักษาชีวิตผู้อื่น", "พัฒนาสังคม ยกระดับความเป็นอยู่", "ถ่ายทอดความรู้ เป็นแรงบันดาลใจ",
    "ผู้เชี่ยวชาญเฉพาะทาง หาคนแทนยาก", "ผู้นำ ผู้บริหาร องค์กรขนาดใหญ่", "สร้างนวัตกรรมหรือธุรกิจของตัวเอง"
]

FINANCIALS = {
    "budget": ["ก. จำกัดสูง (ไม่เกิน 15k/ต้องกู้)", "ข. ปานกลาง (15k-40k/รัฐได้)", "ค. ไม่จำกัด (40k+/เอกชน/อินเตอร์)"],
    "goal": ["ก. มั่นคงสูง", "ข. รายได้เร็ว/คืนทุนไว", "ค. อิสระ/เป็นตัวเอง"],
    "burden": ["ก. ต้องรีบทำงานใช้หนี้/ส่งบ้าน", "ข. ไม่มีภาระเร่งด่วน"],
    "scholarship": ["ก. สนใจมาก (ใช้ทุนแลกเรียนฟรี)", "ข. ไม่สนใจ (ต้องการอิสระ)"],
    "location": ["ก. จำกัด (ต้องเรียนใกล้บ้าน)", "ข. ยืดหยุ่น (ไปต่างจังหวัด/อยู่หอได้)"]
}

# ==========================================
# 3. PROCESSING LOGIC
# ==========================================
def calculate_mbti(scores):
    """
    Calculates MBTI using pure Jungian cognitive function logic.
    """
    # 1. Identify Dominant Function
    dom_func = max(scores, key=scores.get)
    
    # 2. Identify Auxiliary Function (Must be opposite attitude E/I and opposite category Judging/Perceiving)
    is_dom_extraverted = dom_func.endswith('e')
    is_dom_perceiving = dom_func.startswith('N') or dom_func.startswith('S')
    
    aux_candidates = []
    for f in scores.keys():
        if f == dom_func: continue
        is_f_extraverted = f.endswith('e')
        is_f_perceiving = f.startswith('N') or f.startswith('S')
        
        # Aux must be opposite attitude (E <-> I) and opposite preference (P <-> J)
        if is_f_extraverted != is_dom_extraverted and is_f_perceiving != is_dom_perceiving:
            aux_candidates.append(f)
            
    # Find the highest scoring valid auxiliary function
    aux_func = max(aux_candidates, key=lambda x: scores[x]) if aux_candidates else None
    
    # Deduce MBTI Type
    mbti = ""
    # I/E
    mbti += "E" if is_dom_extraverted else "I"
    
    # S/N & T/F (Look at Dom and Aux)
    funcs = [dom_func, aux_func]
    mbti += "N" if any(f.startswith('N') for f in funcs) else "S"
    mbti += "T" if any(f.startswith('T') for f in funcs) else "F"
    
    # J/P 
    # Extraverted Judging function (Te, Fe) means J. Extraverted Perceiving (Ne, Se) means P.
    if (dom_func.endswith('e') and not is_dom_perceiving) or (aux_func and aux_func.endswith('e') and not is_f_perceiving):
        mbti += "J"
    else:
        mbti += "P"
        
    # Stack Deduction
    stack = [dom_func, aux_func]
    # Tertiary is opposite of Aux
    tert_func = aux_func[0] + ('e' if aux_func[1] == 'i' else 'i')
    # Inferior is opposite of Dom
    inf_func = dom_func[0] + ('e' if dom_func[1] == 'i' else 'i')
    stack.extend([tert_func, inf_func])
    
    return mbti, stack

def plot_radar(scores):
    categories = ['Ne', 'Ni', 'Se', 'Si', 'Te', 'Ti', 'Fe', 'Fi']
    values = [scores[cat] for cat in categories]
    values.append(values[0]) # close loop
    categories.append(categories[0])
    
    fig = go.Figure(data=go.Scatterpolar(
      r=values,
      theta=categories,
      fill='toself',
      fillcolor='rgba(52, 152, 219, 0.4)',
      line=dict(color='#2980b9')
    ))
    fig.update_layout(
      polar=dict(
        radialaxis=dict(visible=True, range=[10, 50])
      ),
      showlegend=False,
      margin=dict(l=40, r=40, t=40, b=40),
      height=400
    )
    return fig

def generate_recommendation(mbti, top_interests, work_goals, financial):
    """
    Synthesizes career and education path based on inputs.
    """
    rec = {"career": "", "education": "", "strategy": ""}
    
    # Career Logic based on MBTI + Goals
    if "T" in mbti and "J" in mbti: 
        rec["career"] = "สายผู้บริหาร, วิศวกรรม, การจัดการระบบ, นักวิเคราะห์ข้อมูล, ที่ปรึกษาด้านธุรกิจ"
    elif "T" in mbti and "P" in mbti:
        rec["career"] = "โปรแกรมเมอร์, นักวิจัย, ช่างเทคนิคเฉพาะทาง, สถาปนิกระบบ, นักวิเคราะห์ทางการเงิน"
    elif "F" in mbti and "J" in mbti:
        rec["career"] = "นักจิตวิทยา, ครูบาอาจารย์, งานทรัพยากรบุคคล (HR), นักสังคมสงเคราะห์, แพทย์/พยาบาล"
    else: # FP
        rec["career"] = "ศิลปิน, ครีเอทีฟ, นักเขียน, นักออกแบบ, เจ้าของธุรกิจส่วนตัว (SME)"

    # Adjust based on goals
    if "ผู้เชี่ยวชาญเฉพาะทาง หาคนแทนยาก" in work_goals:
        rec["career"] += " (เน้นการเป็น Specialist แบบเจาะลึกเฉพาะทาง)"
    if "สร้างนวัตกรรมหรือธุรกิจของตัวเอง" in work_goals:
        rec["career"] += " (โดยมีเป้าหมายระยะยาวคือการเป็น Entrepreneur)"
        
    # Education & Strategy Logic based on Financials
    budget = financial["budget"]
    burden = financial["burden"]
    
    if "จำกัดสูง" in budget or "ใช้หนี้" in burden:
        rec["education"] = "แนะนำมหาวิทยาลัยของรัฐ (เช่น ม.รามคำแหง, มสธ.) หรือสายอาชีพ (ปวส.) ที่เน้นจบเร็วได้ทำงานทันที"
        rec["strategy"] = "ควรสมัครขอทุนการศึกษาแบบให้เปล่า หรือพิจารณาคณะที่เรียนไปทำงานไปได้ (Work-Study) เน้นสาขาที่ตลาดงานมีความต้องการสูงเพื่อคืนทุนไว"
        if "สนใจมาก" in financial["scholarship"]:
            rec["strategy"] += " แนะนำสอบชิงทุนผูกพันของรัฐบาล หรือทุนพยาบาล/ครู ที่จบมาแล้วมีงานทำแน่นอน"
    elif "ปานกลาง" in budget:
        rec["education"] = "มหาวิทยาลัยของรัฐทั่วไป หรือมหาวิทยาลัยเอกชนที่สามารถกู้ กยศ. ได้"
        rec["strategy"] = "สามารถเลือกเรียนในสายที่ตรงกับความสนใจได้มากขึ้น ควรทำกิจกรรมเสริมระหว่างเรียนเพื่อสร้าง Portfolio"
    else:
        rec["education"] = "มหาวิทยาลัยชั้นนำ (รัฐ/เอกชน) หรือหลักสูตรนานาชาติ (International College) / ศึกษาต่อต่างประเทศ"
        rec["strategy"] = "ไม่มีข้อจำกัดทางการเงิน ควรเน้นการสร้าง Connection ระดับสูง การไปแลกเปลี่ยนต่างประเทศ และการฝึกงานในบริษัทข้ามชาติ"

    return rec


# ==========================================
# 4. APP STATE MANAGEMENT
# ==========================================
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.scores = {f: 0 for f in COGNITIVE_QUESTIONS.keys()}
    st.session_state.interests = {}
    st.session_state.goals = []
    st.session_state.finances = {}

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1


# ==========================================
# 5. UI LAYOUT
# ==========================================
st.title("✨ Advanced MBTI & Career Assessment Tool")
st.markdown("ค้นพบศักยภาพที่แท้จริงของคุณผ่าน **Jungian Cognitive Functions** ผสานปัจจัยชีวิตจริง เพื่อหาเส้นทางอาชีพที่ใช่ที่สุด")

# --- STEP 0: INTRO ---
if st.session_state.step == 0:
    st.markdown("""
    <div class="result-card">
        <h3>ยินดีต้อนรับสู่แบบทดสอบ 16 Personalities เชิงลึก</h3>
        <p>แบบทดสอบนี้ไม่ได้ใช้แค่ตัวอักษร 4 ตัว แต่เจาะลึกไปถึง <b>Cognitive Functions (การทำงานของสมองทั้ง 8 แบบ)</b><br>
        ผสมผสานกับเป้าหมายชีวิตและข้อจำกัดทางการเงินของคุณ เพื่อออกแบบเส้นทางอาชีพที่ "เป็นไปได้จริง"</p>
        <hr>
        <b>แบบทดสอบแบ่งออกเป็น 4 ส่วน:</b>
        <ul>
            <li>ส่วนที่ 1: การทำงานของสมอง (Cognitive Functions) - 80 ข้อ</li>
            <li>ส่วนที่ 2: ความสนใจด้านวิชาการและทักษะ</li>
            <li>ส่วนที่ 3: สไตล์การทำงานในอนาคต</li>
            <li>ส่วนที่ 4: ข้อจำกัดทางการเงินและเงื่อนไขชีวิต</li>
        </ul>
        <i>*โปรดตอบตามความเป็นจริงที่เกิดขึ้นกับคุณ ไม่ใช่สิ่งที่คุณอยากเป็น</i>
    </div>
    """, unsafe_allow_html=True)
    st.button("เริ่มทำแบบทดสอบ 🚀", on_click=next_step)

# --- STEP 1: COGNITIVE FUNCTIONS ---
elif st.session_state.step == 1:
    st.progress(25, text="ส่วนที่ 1/4: Cognitive Functions")
    st.subheader("ส่วนที่ 1: ประเมินกระบวนการคิด (Cognitive Functions)")
    st.markdown("ให้คะแนน 1-5 (1 = ไม่ตรงเลย, 5 = ตรงมากที่สุด)")
    
    with st.form("cognitive_form"):
        # We group by function visually, but interleave them in a real app. For code simplicity, group by function.
        for func, questions in COGNITIVE_QUESTIONS.items():
            st.markdown(f"#### หมวด {func}")
            for i, q in enumerate(questions):
                st.session_state.scores[func] += st.slider(f"{q}", 1, 5, 3, key=f"q_{func}_{i}")
                
        submit = st.form_submit_button("ถัดไป ➔")
        if submit:
            next_step()
            st.rerun()

# --- STEP 2: INTERESTS ---
elif st.session_state.step == 2:
    st.progress(50, text="ส่วนที่ 2/4: ความสนใจ")
    st.subheader("ส่วนที่ 2: ความสนใจด้านวิชาการและทักษะ")
    
    with st.form("interest_form"):
        st.markdown("ให้คะแนนความสนใจในศาสตร์ต่อไปนี้ (1 = ไม่สนใจเลย, 5 = สนใจมากที่สุด)")
        for interest in INTERESTS:
            st.session_state.interests[interest] = st.slider(interest, 1, 5, 3)
            
        col1, col2 = st.columns([1, 8])
        with col1:
            st.form_submit_button("⬅️ กลับ", on_click=prev_step)
        with col2:
            if st.form_submit_button("ถัดไป ➔"):
                next_step()
                st.rerun()

# --- STEP 3: WORK GOALS ---
elif st.session_state.step == 3:
    st.progress(75, text="ส่วนที่ 3/4: เป้าหมายการทำงาน")
    st.subheader("ส่วนที่ 3: สไตล์การทำงานในอนาคต")
    
    with st.form("goals_form"):
        st.markdown("เลือกเป้าหมายการทำงานสูงสุด 3 อันดับที่คุณต้องการ (เลือกได้หลายข้อ)")
        st.session_state.goals = st.multiselect("สไตล์การทำงานที่ชอบ", WORK_GOALS, max_selections=3)
        
        col1, col2 = st.columns([1, 8])
        with col1:
            st.form_submit_button("⬅️ กลับ", on_click=prev_step)
        with col2:
            if st.form_submit_button("ถัดไป ➔"):
                if len(st.session_state.goals) == 0:
                    st.error("กรุณาเลือกอย่างน้อย 1 ข้อ")
                else:
                    next_step()
                    st.rerun()

# --- STEP 4: FINANCIALS ---
elif st.session_state.step == 4:
    st.progress(100, text="ส่วนที่ 4/4: เงื่อนไขชีวิต")
    st.subheader("ส่วนที่ 4: ข้อจำกัดทางการเงินและเงื่อนไขชีวิต")
    
    with st.form("financials_form"):
        st.session_state.finances["budget"] = st.radio("1. งบประมาณการศึกษา:", FINANCIALS["budget"])
        st.session_state.finances["goal"] = st.radio("2. เป้าหมายหลังเรียนจบ:", FINANCIALS["goal"])
        st.session_state.finances["burden"] = st.radio("3. ภาระทางบ้าน:", FINANCIALS["burden"])
        st.session_state.finances["scholarship"] = st.radio("4. ความสนใจทุนผูกพัน (ใช้ทุนแลกเรียนฟรี):", FINANCIALS["scholarship"])
        st.session_state.finances["location"] = st.radio("5. ข้อจำกัดการเดินทาง/ที่พัก:", FINANCIALS["location"])
        
        col1, col2 = st.columns([1, 8])
        with col1:
            st.form_submit_button("⬅️ กลับ", on_click=prev_step)
        with col2:
            if st.form_submit_button("ประมวลผลผลลัพธ์ 🎉"):
                next_step()
                st.rerun()

# --- STEP 5: RESULTS DASHBOARD ---
elif st.session_state.step == 5:
    st.balloons()
    
    # Run Calculations
    mbti_type, function_stack = calculate_mbti(st.session_state.scores)
    radar_chart = plot_radar(st.session_state.scores)
    recommendations = generate_recommendation(
        mbti_type, 
        st.session_state.interests, 
        st.session_state.goals, 
        st.session_state.finances
    )
    
    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>ผลการวิเคราะห์ส่วนบุคคลของคุณ</h2><br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🧑‍💼 MBTI Profile", "🧠 Cognitive Functions", "🎯 Career & Education Path"])
    
    with tab1:
        st.markdown(f"""
        <div class="result-card">
            <p style="text-align:center; font-size: 1.2rem; margin-bottom: -15px;">บุคลิกภาพของคุณคือ</p>
            <h1 class="type-header" style="text-align:center;">{mbti_type}</h1>
            <hr>
            <h4>โครงสร้างกระบวนการคิด (Function Stack)</h4>
            <ul>
                <li><b>Dominant (ฟังก์ชันหลัก):</b> {function_stack[0]} - เป็นตัวขับเคลื่อนหลัก พลังงานธรรมชาติของคุณ</li>
                <li><b>Auxiliary (ฟังก์ชันรอง):</b> {function_stack[1]} - เครื่องมือช่วยตัดสินใจและรักษาสมดุล</li>
                <li><b>Tertiary (ฟังก์ชันอันดับสาม):</b> {function_stack[2]} - จุดที่คุณใช้พักผ่อน หรือพัฒนาเมื่อเติบโตขึ้น</li>
                <li><b>Inferior (ฟังก์ชันด้อย):</b> {function_stack[3]} - จุดอ่อนไหวและสิ่งที่ทำให้คุณเครียดได้ง่าย</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with tab2:
        st.markdown("""
        <div class="result-card">
            <h4>กราฟแสดงการทำงานของสมอง (Cognitive Functions Radar)</h4>
            <p>ยิ่งกราฟกว้างในจุดใด แสดงว่าคุณมีแนวโน้มใช้กระบวนการคิดรูปแบบนั้นเป็นธรรมชาติมากที่สุด</p>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(radar_chart, use_container_width=True)
        
    with tab3:
        st.markdown("""
        <div class="result-card">
            <h3 style="color:#27ae60;">💼 คำแนะนำสายอาชีพ (Career Recommendations)</h3>
            <p>วิเคราะห์จากโครงสร้างบุคลิกภาพและความสนใจของคุณ:</p>
            <p style="font-size: 1.1rem; padding: 10px; background-color: #f8f9fa; border-left: 5px solid #27ae60;">
                <b>สายอาชีพที่เหมาะสม:</b><br>{career}
            </p>
            <hr>
            <h3 style="color:#2980b9;">🎓 เส้นทางการศึกษาที่แนะนำ (Education Strategy)</h3>
            <p>วิเคราะห์จากงบประมาณ ข้อจำกัดทางบ้าน และไลฟ์สไตล์:</p>
            <p style="font-size: 1.1rem; padding: 10px; background-color: #f8f9fa; border-left: 5px solid #2980b9;">
                <b>รูปแบบมหาวิทยาลัย/สถาบัน:</b><br>{education}
            </p>
            <p style="font-size: 1.1rem; padding: 10px; background-color: #f8f9fa; border-left: 5px solid #e67e22;">
                <b>กลยุทธ์และคำแนะนำเพิ่มเติม:</b><br>{strategy}
            </p>
        </div>
        """.format(
            career=recommendations["career"],
            education=recommendations["education"],
            strategy=recommendations["strategy"]
        ), unsafe_allow_html=True)
        
    if st.button("🔄 ทำแบบทดสอบอีกครั้ง"):
        st.session_state.step = 0
        st.session_state.scores = {f: 0 for f in COGNITIVE_QUESTIONS.keys()}
        st.rerun()

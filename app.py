import streamlit as st
from questions import (
    COGNITIVE_QUESTIONS, 
    SUBJECT_QUESTIONS, 
    HOBBY_QUESTIONS, 
    GOAL_QUESTIONS, 
    FINANCIAL_QUESTIONS, 
    MBTI_DESCRIPTIONS
)

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="ระบบวิเคราะห์อาชีพด้วยตรรกศาสตร์ MBTI & Subject Logic",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------------------------------------
# 2. Session State Management
# ---------------------------------------------------------
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'mbti_result' not in st.session_state:
    st.session_state.mbti_result = "INTJ"
if 'category_scores' not in st.session_state:
    st.session_state.category_scores = {}

SCALE_OPTIONS = {
    "1 - ไม่ตรงเลย": 1,
    "2 - ไม่ค่อยตรง": 2,
    "3 - ปานกลาง / ไม่แน่ใจ": 3,
    "4 - ค่อนข้างตรง": 4,
    "5 - ตรงมากที่สุด": 5
}

# ---------------------------------------------------------
# STEP 1: ประเมิน MBTI (Cognitive Functions)
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.title("🧩 ขั้นตอนที่ 1: ประเมินบุคลิกภาพ (MBTI)")
    st.write("เลือกสเกลที่ตรงกับตัวคุณมากที่สุดเพื่อสรุปหาประพจน์ทางบุคลิกภาพ")
    
    with st.form("mbti_form"):
        raw_answers = {}
        for idx, q in enumerate(COGNITIVE_QUESTIONS, 1):
            q_id = q.get('id', idx)
            st.markdown(f"**ข้อที่ {idx}:** {q['text']}")
            ans = st.radio(
                f"ระดับความตรง (ข้อ {idx}):", 
                options=list(SCALE_OPTIONS.keys()), 
                index=2, 
                key=f"cog_{q_id}",
                horizontal=True
            )
            raw_answers[q_id] = {"func": q["func"], "score": SCALE_OPTIONS[ans]}
            st.markdown("<hr style='margin: 0.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)
            
        submitted = st.form_submit_button("🚀 ประมวลผล MBTI (ไปขั้นตอนที่ 2)")
        
        if submitted:
            func_scores = {"Ne": 0, "Ni": 0, "Se": 0, "Si": 0, "Te": 0, "Ti": 0, "Fe": 0, "Fi": 0}
            for item in raw_answers.values():
                func_scores[item["func"]] += item["score"]

            func_percentages = {func: round((score / 50) * 100, 1) for func, score in func_scores.items()}
            sorted_funcs = sorted(func_scores.items(), key=lambda x: x[1], reverse=True)

            dom_func = max(func_scores, key=func_scores.get)
            
            aux_candidates_map = {
                "Ne": ["Ti", "Fi"], "Se": ["Ti", "Fi"],
                "Ni": ["Te", "Fe"], "Si": ["Te", "Fe"],
                "Te": ["Ni", "Si"], "Fe": ["Ni", "Si"],
                "Ti": ["Ne", "Se"], "Fi": ["Ne", "Se"]
            }
            possible_aux = aux_candidates_map.get(dom_func, ["Te", "Fe"])
            aux_func = max(possible_aux, key=lambda f: func_scores[f])

            opposite_map = {
                "Ne": "Si", "Si": "Ne",
                "Ni": "Se", "Se": "Ni",
                "Te": "Fi", "Fi": "Te",
                "Ti": "Fe", "Fe": "Ti"
            }
            tertiary_func = opposite_map[aux_func]
            inferior_func = opposite_map[dom_func]

            st.session_state.func_scores = func_scores
            st.session_state.func_percentages = func_percentages
            st.session_state.sorted_funcs = sorted_funcs
            st.session_state.possible_aux = possible_aux
            st.session_state.mbti_stack = {
                "Dom": dom_func,
                "Aux": aux_func,
                "Tert": tertiary_func,
                "Inf": inferior_func
            }

            type_mapping = {
                ("Ne", "Ti"): "ENTP", ("Ne", "Fi"): "ENFP",
                ("Ni", "Te"): "INTJ", ("Ni", "Fe"): "INFJ",
                ("Se", "Ti"): "ESTP", ("Se", "Fi"): "ESFP",
                ("Si", "Te"): "ISTJ", ("Si", "Fe"): "ISFJ",
                ("Te", "Ni"): "ENTJ", ("Te", "Si"): "ESTJ",
                ("Ti", "Ne"): "INTP", ("Ti", "Se"): "ISTP",
                ("Fe", "Ni"): "ENFJ", ("Fe", "Si"): "ESFJ",
                ("Fi", "Ne"): "INFP", ("Fi", "Se"): "ISFP"
            }
            
            st.session_state.mbti_result = type_mapping.get((dom_func, aux_func), "INTJ")
            st.session_state.step = 2
            st.rerun()

# ---------------------------------------------------------
# STEP 2: สรุปผล MBTI และแสดงสมการตรรกศาสตร์
# ---------------------------------------------------------
elif st.session_state.step == 2:
    st.title("🌟 ขั้นตอนที่ 2: สรุปผลลัพธ์และแบบจำลองตรรกศาสตร์ MBTI")
    
    mbti = st.session_state.mbti_result
    info = MBTI_DESCRIPTIONS.get(mbti, MBTI_DESCRIPTIONS["INTJ"])
    sorted_funcs = st.session_state.get("sorted_funcs", [])
    func_pct = st.session_state.get("func_percentages", {})
    stack = st.session_state.get("mbti_stack", {})
    possible_aux = st.session_state.get("possible_aux", [])
    
    st.success(f"### ผลการวิเคราะห์ MBTI: **{mbti}** ({info['title']})")
    st.info(f"**ลักษณะตัวตน:** {info['desc']}")

    st.subheader("📊 ลำดับคะแนนและ Cognitive Stack")
    col_chart, col_rank = st.columns([3, 2])
    
    with col_chart:
        st.markdown("**ระดับความเข้มข้นของฟังก์ชัน (%):**")
        for func_code, score in sorted_funcs:
            pct = func_pct.get(func_code, 0)
            st.write(f"**{func_code}**: {score}/50 คะแนน ({pct}%)")
            st.progress(pct / 100)
            
    with col_rank:
        st.markdown("**ฟังก์ชันการทำงานหลัก:**")
        if stack:
            st.write(f"🥇 **Dominant:** `{stack['Dom']}` ({func_pct.get(stack['Dom'], 0)}%)")
            st.write(f"🥈 **Auxiliary:** `{stack['Aux']}` ({func_pct.get(stack['Aux'], 0)}%)")
            st.write(f"🥉 **Tertiary:** `{stack['Tert']}` ({func_pct.get(stack['Tert'], 0)}%)")
            st.write(f"⚓ **Inferior:** `{stack['Inf']}` ({func_pct.get(stack['Inf'], 0)}%)")
            
    # ---------------------------------------------------------
    # แสดงตรรกศาสตร์สไตล์ ม.4 (Propositions & Truth Logic)
    # ---------------------------------------------------------
    st.markdown("---")
    with st.expander("📚 คลิกเพื่อดูตรรกศาสตร์การคำนวณ (ระดับ ม.4: เรื่องประพจน์และเงื่อนไข)"):
        st.markdown("### 1. การกำหนดประพจน์ (Propositions)")
        st.write("* ให้ **Score(f)** แทน คะแนนของฟังก์ชัน f")
        st.write("* ให้ประพจน์ **P**: *ฟังก์ชัน A มีคะแนนสูงที่สุด*")
        
        st.markdown("---")

        st.markdown("### 2. เงื่อนไขทางตรรกศาสตร์ในการหา Dominant (ฟังก์ชันหลัก)")
        st.latex(r"\text{Dom} = A \iff \forall f \, (\text{Score}(A) \ge \text{Score}(f))")
        st.caption("แปลว่า: ฟังก์ชัน A จะเป็น Dominant ก็ต่อเมื่อ คะแนนของ A มากกว่าหรือเท่ากับคะแนนของทุกๆ ฟังก์ชัน (f)")

        st.markdown("---")

        st.markdown("### 3. ตรรกศาสตร์การเลือก Auxiliary (ฟังก์ชันรอง)")
        st.markdown("**กรณีที่ Dom = Ne:**")
        st.latex(r"(\text{Dom} = Ne) \implies (\text{Aux} \in \{Ti, Fi\})")
        st.write("* **เงื่อนไขที่ 1:** ถ้า `Score(Ti) > Score(Fi)` แล้ว `(Aux = Ti ∧ Type = ENTP)`")
        st.write("* **เงื่อนไขที่ 2:** ถ้า `Score(Fi) > Score(Ti)` แล้ว `(Aux = Fi ∧ Type = ENFP)`")

        st.markdown("---")

        st.markdown("### 4. กฎคู่สมดุลตรงข้าม (สมมูลทางตรรกศาสตร์ ⇔)")
        st.latex(r"\text{Dom} = Ne \iff \text{Inferior} = Si")
        st.latex(r"\text{Aux} = Ti \iff \text{Tertiary} = Fe")
        st.latex(r"\text{Aux} = Fi \iff \text{Tertiary} = Te")
        
    st.markdown("---")
    if st.button("➡️ ไปต่อ: ประเมินความชอบ 5 หมวดหมู่ (Step 3)"):
        st.session_state.step = 3
        st.rerun()

# ---------------------------------------------------------
# STEP 3: ประเมินความชอบ 5 หมวดหมู่ (วิชา, งานอดิเรก, เป้าหมาย, การเงิน)
# ---------------------------------------------------------
elif st.session_state.step == 3:
    st.title("📚 ขั้นตอนที่ 3: ประเมินความชอบและศักยภาพ 5 หมวดหมู่")
    st.write("กรุณาทำแบบประเมินให้ครบทั้ง 5 หมวด เพื่อนำไปสรุปเป็นประพจน์ทางตรรกศาสตร์")
    
    all_question_sets = [
        ("📖 1. วิชาความรู้ (Subject Knowledge)", SUBJECT_QUESTIONS, "sub"),
        ("🎨 2. งานอดิเรกและความสนใจ (Hobbies & Interests)", HOBBY_QUESTIONS, "hobby"),
        ("🎯 3. เป้าหมายอาชีพและค่านิยม (Career Goals)", GOAL_QUESTIONS, "goal"),
        ("💰 4. การบริหารและการเงิน (Financial & Management)", FINANCIAL_QUESTIONS, "fin")
    ]
    
    with st.form("all_categories_form"):
        category_scores = {}
        
        for tab_name, questions_list, prefix in all_question_sets:
            st.subheader(tab_name)
            for idx, q in enumerate(questions_list, 1):
                if isinstance(q, dict):
                    # 1. ดึงข้อความคำถาม (รองรับคีย์ label, text, และ question)
                    q_text = q.get('label') or q.get('text') or q.get('question') or str(q)
                    category = q.get('category', 'ทั่วไป')
                    q_id = q.get('id', f"{prefix}_{idx}")
                    options = q.get('options') # ดึงตัวเลือกเฉพาะคำถาม (ถ้ามี)
                else:
                    q_text = str(q)
                    category = 'ทั่วไป'
                    q_id = f"{prefix}_{idx}"
                    options = None
                
                st.markdown(f"**ข้อที่ {idx}:** {q_text} *(หมวด: {category})*")
                
                # 2. แสดงตัวเลือก: ถ้ามี options เฉพาะข้อให้แสดงแบบ Choice ถ้าไม่มีให้ใช้สเกล 1-5
                if options and isinstance(options, list):
                    ans = st.radio(
                        f"เลือกคำตอบที่ตรงกับคุณมากที่สุด ({q_id}):", 
                        options=options, 
                        index=0, 
                        key=f"{prefix}_{q_id}",
                        horizontal=False
                    )
                    # คำนวณคะแนนตามลำดับตัวเลือกที่เลือก
                    score_val = (options.index(ans) + 1) * (5 / len(options))
                    category_scores[category] = category_scores.get(category, 0) + score_val
                else:
                    ans = st.radio(
                        f"ระดับความตรง ({q_id}):", 
                        options=list(SCALE_OPTIONS.keys()), 
                        index=2, 
                        key=f"{prefix}_{q_id}", 
                        horizontal=True
                    )
                    category_scores[category] = category_scores.get(category, 0) + SCALE_OPTIONS[ans]
                    
                st.markdown("<hr style='margin: 0.2rem 0 0.8rem 0;'>", unsafe_allow_html=True)
            st.markdown("---")

        submitted_step3 = st.form_submit_button("🚀 สรุปประพจน์และประมวลผลหาคณะ/อาชีพ (Step 4)")
        
        if submitted_step3:
            st.session_state.category_scores = category_scores
            st.session_state.step = 4
            st.rerun()
# ---------------------------------------------------------
# STEP 4: เชื่อมประพจน์ (AND/OR Logic) & ตรวจสอบเงื่อนไขคณะ/อาชีพ
# ---------------------------------------------------------
elif st.session_state.step == 4:
    st.title("🎓 ขั้นตอนที่ 4: ประมวลผลตรรกศาสตร์เชื่อมประพจน์และสรุปคณะ/อาชีพ")
    
    mbti = st.session_state.mbti_result
    cat_scores = st.session_state.get("category_scores", {})

    # ฟังก์ชันช่วยเช็กคะแนนในแต่ละหมวดว่าสูงกว่าเกณฑ์ปานกลางไหม
    # category_scores เป็นคะแนนรวมของคำถามในหมวดนั้น
    def is_category_high(keywords):
        for cat, score in cat_scores.items():
            if any(kw.lower() in cat.lower() for kw in keywords):
                if score >= 6: # มีความสนใจในระดับปานกลางขึ้นไป
                    return True
        return False

    # กำหนดประพจน์หลักตามหมวดหมู่
    is_math_sci = is_category_high(["math", "คณิต", "science", "วิทย์", "ฟิสิกส์", "เคมี", "ชีว"])
    is_tech = is_category_high(["tech", "คอมพิวเตอร์", "เทคโนโลยี", "it", "coding", "นวัตกรรม"])
    is_art_design = is_category_high(["art", "ศิลปะ", "ออกแบบ", "design", "สร้างสรรค์", "บันเทิง"])
    is_biz_finance = is_category_high(["finance", "การเงิน", "ธุรกิจ", "การบริหาร", "การลงทุน", "การตลาด", "การค้า"])
    is_social_people = is_category_high(["social", "สังคม", "ภาษา", "จิตวิทยา", "การบริการ", "การสื่อสาร", "บริหารคน"])
    
    # ประพจน์ย่อยสำหรับจำแนกสายอาชีพเฉพาะทาง
    is_healthcare = is_category_high([
        "สุขภาพ", "health", "แพทย", "พยาบาล", "เภสัช", "สาธารณสุข",
        "กายภาพ", "วิทยาศาสตร์การแพทย์", "โภชนาการ"
    ])
    is_language = is_category_high([
        "ภาษา", "language", "อังกฤษ", "ไทย", "จีน", "ญี่ปุ่น",
        "แปล", "ล่าม", "วรรณกรรม", "มนุษยศาสตร์"
    ])
    is_education = is_category_high([
        "การศึกษา", "an�รู", "สอน", "education", "พัฒนาคน", "ฝึกอบรม"
    ])
    is_helping = is_category_high([
        "ช่วยเหลือ", "จิตอาสา", "สังคมสงเคราะห์", "ชุมชน", "ผู้คน",
        "สุขภาพจิต", "ให้คำปรึกษา", "counseling", "พัฒนาสังคม"
    ])
    is_nature = is_category_high([
        "ธรรมชาติ", "สิ่งแวดล้อม", "เกษตร", "ป่าไม้", "สัตว์",
        "ทะเล", "ภูมิศาสตร์", "ทรัพยากร", "environment", "เกษตรกรรม"
    ])
    is_research = is_category_high([
        "วิจัย", "research", "ทดลอง", "ห้องปฏิบัติการ", "วิชาการ",
        "วิเคราะห์ข้อมูล", "สถิติ", "ค้นคว้า"
    ])
    is_operations = is_category_high([
        "การจัดการ", "ปฏิบัติการ", "โลจิสติกส์", "ขนส่ง", "ซัพพลายเชน",
        "วางแผน", "ระบบงาน", "ควบคุมคุณภาพ", "operations"
    ])
    is_security = is_category_high([
        "ความปลอดภัย", "ทหาร", "ตำรวจ", "กู้ภัย", "ฉุกเฉิน",
        "นิติวิทยาศาสตร์", "security", "ป้องกันประเทศ"
    ])
    is_sport = is_category_high([
        "กีฬา", "ออกกำลังกาย", "ฟิตเนส", "sport", "การเคลื่อนไหว",
        "สุขภาพกาย", "โค้ชกีฬา"
    ])
    is_food = is_category_high([
        "อาหาร", "ทำอาหาร", "เชฟ", "เบเกอรี่", "เครื่องดื่ม",
        "โภชนาการ", "food", "คหกรรม"
    ])
    is_travel = is_category_high([
        "ท่องเที่ยว", "โรงแรม", "การบิน", "การโรงแรม", "ทัวร์",
        "บริการ", "hospitality", "tourism"
    ])
    is_practical = is_category_high([
        "ช่าง", "งานฝีมือ", "เครื่องจักร", "ก่อสร้าง", "ลงมือทำ",
        "ประดิษฐ์", "ซ่อมแซม", "อุตสาหกรรม", "ช่างยนต์"
    ])
    is_legal = is_category_high([
        "กฎหมาย", "การเมือง", "รัฐศาสตร์", "นโยบาย", "การปกครอง",
        "สิทธิมนุษยชน", "law", "การทูต"
    ])

    st.markdown("### 1. สรุปประพจน์ความสนใจและศักยภาพ (Propositions Setup)")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.write(f"- **ประพจน์ $M_{{{mbti}}}$**: บุคลิกภาพแบบ {mbti} = `True`")
        st.write(f"- **ประพจน์ $P$ (สนใจสายวิทยาศาสตร์/คณิตศาสตร์)** = `{is_math_sci}`")
        st.write(f"- **ประพจน์ $Q$ (สนใจเทคโนโลยี/ไอที/นวัตกรรม)** = `{is_tech}`")
    with col_p2:
        st.write(f"- **ประพจน์ $R$ (สนใจศิลปะ/การออกแบบ/งานสร้างสรรค์)** = `{is_art_design}`")
        st.write(f"- **ประพจน์ $S$ (สนใจบริหาร/การเงิน/ธุรกิจ)** = `{is_biz_finance}`")
        st.write(f"- **ประพจน์ $T$ (สนใจมนุษยศาสตร์/สังคม/จิตวิทยา/ภาษา)** = `{is_social_people}`")
    
    with st.expander("ดูประพจน์ย่อยสำหรับสายอาชีพเฉพาะทาง"):
        secondary_props = {
            "H": ("สุขภาพและการแพทย์", is_healthcare),
            "L": ("ภาษาและมนุษยศาสตร์", is_language),
            "E": ("การศึกษาและการพัฒนาคน", is_education),
            "C": ("การช่วยเหลือคนและชุมชน", is_helping),
            "N": ("ธรรมชาติและสิ่งแวดล้อม", is_nature),
            "X": ("การวิจัยและวิชาการ", is_research),
            "O": ("ปฏิบัติการและการจัดการระบบ", is_operations),
            "K": ("ความปลอดภัยและงานฉุกเฉิน", is_security),
            "A": ("กีฬาและการเคลื่อนไหว", is_sport),
            "F": ("อาหารและโภชนาการ", is_food),
            "V": ("การเดินทางและการบริการ", is_travel),
            "W": ("งานช่างและงานปฏิบัติ", is_practical),
            "J": ("กฎหมายและนโยบาย", is_legal),
        }
        prop_cols = st.columns(3)
        for idx, (code, (label, value)) in enumerate(secondary_props.items()):
            with prop_cols[idx % 3]:
                st.write(f"**{code}** — {label}: `{value}`")

    st.markdown("---")
    st.markdown("### 2. ตรวจสอบเงื่อนไขทางตรรกศาสตร์ของแต่ละสายคณะและอาชีพ")
    
    # นิยามเงื่อนไขตรรกศาสตร์ครอบคลุมสายคณะและอาชีพหลัก
    faculties_rules = [
        {
            "faculty": "🏛️ คณะวิศวกรรมศาสตร์ / เทคโนโลยีสารสนเทศ (Engineers & Developers)",
            "condition_symbol": r"(M_{INTJ} \lor M_{INTP} \lor M_{ENTP} \lor M_{ISTP}) \land Q \land (P \lor S)",
            "eval": (mbti in ["INTJ", "INTP", "ENTP", "ISTP"]) and is_tech and (is_math_sci or is_biz_finance),
            "rule_desc": "ต้องเป็น (INTJ, INTP, ENTP, ISTP) AND สนใจเทคโนโลยี (Q) AND (สนใจวิทย์/คณิต หรือ การเงิน)",
            "careers": "วิศวกรซอฟต์แวร์, นักพัฒนาระบบ, Data Scientist, วิศวกรเครือข่าย"
        },
        {
            "faculty": "🏛️ คณะแพทยศาสตร์ / เภสัชศาสตร์ / จิตวิทยาคลินิก (Healthcare & Medical Sciences)",
            "condition_symbol": r"(M_{INFJ} \lor M_{INTJ} \lor M_{ISFJ} \lor M_{ENFJ}) \land P \land T",
            "eval": (mbti in ["INFJ", "INTJ", "ISFJ", "ENFJ"]) and is_math_sci and is_social_people,
            "rule_desc": "ต้องเป็น (INFJ, INTJ, ISFJ, ENFJ) AND สนใจวิทย์ (P) AND สนใจสังคม/ช่วยเหลือคน (T)",
            "careers": "แพทย์, เภสัชกร, นักจิตวิทยาคลินิก, นักวิจัยทางแพทย์"
        },
        {
            "faculty": "🏛️ คณะบริหารธุรกิจ / เศรษฐศาสตร์ / การบัญชีและการเงิน (Business & Finance)",
            "condition_symbol": r"(M_{ENTJ} \lor M_{ESTJ} \lor M_{ESTP} \lor M_{ENTP}) \land S",
            "eval": (mbti in ["ENTJ", "ESTJ", "ESTP", "ENTP"]) and is_biz_finance,
            "rule_desc": "ต้องเป็น (ENTJ, ESTJ, ESTP, ENTP) AND สนใจธุรกิจและการเงิน (S)",
            "careers": "นักลงทุน, ผู้ประกอบการ, นักวิเคราะห์การเงิน, ผู้จัดการฝ่ายกลยุทธ์"
        },
        {
            "faculty": "🏛️ คณะศิลปกรรมศาสตร์ / UX-UI Design / สื่อดิจิทัล (Arts & Creative Design)",
            "condition_symbol": r"(M_{INFP} \lor M_{ISFP} \lor M_{ENFP} \lor M_{ENTP}) \land R",
            "eval": (mbti in ["INFP", "ISFP", "ENFP", "ENTP"]) and is_art_design,
            "rule_desc": "ต้องเป็น (INFP, ISFP, ENFP, ENTP) AND สนใจงานศิลป์/สร้างสรรค์ (R)",
            "careers": "UX/UI Designer, กราฟิกดีไซเนอร์, ครีเอทีฟ, แอนิเมเตอร์"
        },
        {
            "faculty": "🏛️ คณะนิเทศศาสตร์ / อักษรศาสตร์ / การตลาดและสื่อสาร (Communications & Media)",
            "condition_symbol": r"(M_{ENFP} \lor M_{ESFP} \lor M_{ENFJ} \lor M_{ENTP}) \land (R \lor S \lor T)",
            "eval": (mbti in ["ENFP", "ESFP", "ENFJ", "ENTP"]) and (is_art_design or is_biz_finance or is_social_people),
            "rule_desc": "ต้องเป็น (ENFP, ESFP, ENFJ, ENTP) AND (สนใจศิลป์ หรือ ธุรกิจ หรือ สื่อสารสังคม)",
            "careers": "นักการตลาดดิจิทัล, PR Manager, นักเขียน/นักคอนเทนต์, ผู้จัดรายการ"
        },
        {
            "faculty": "🏛️ คณะนิติศาสตร์ / รัฐศาสตร์ / สังคมสงเคราะห์ (Law & Public Administration)",
            "condition_symbol": r"(M_{ISTJ} \lor M_{ESTJ} \lor M_{INTJ} \lor M_{ENFJ}) \land T",
            "eval": (mbti in ["ISTJ", "ESTJ", "INTJ", "ENFJ"]) and is_social_people,
            "rule_desc": "ต้องเป็น (ISTJ, ESTJ, INTJ, ENFJ) AND สนใจสังคม/กฎหมาย/การเมือง (T)",
            "careers": "ทนายความ, ผู้พิพากษา, นักการเมือง, นักการทูต, ข้าราชการบริหาร"
        },
        {
            "faculty": "🏛️ คณะวิทยาการข้อมูล / ปัญญาประดิษฐ์ / สถิติ (Data & AI)",
            "condition_symbol": r"(M_{INTJ} \lor M_{INTP} \lor M_{ENTJ} \lor M_{ENTP}) \land Q \land (P \lor S \lor X)",
            "eval": (mbti in ["INTJ", "INTP", "ENTJ", "ENTP"]) and is_tech and (is_math_sci or is_biz_finance or is_research),
            "rule_desc": "ต้องเป็น (INTJ, INTP, ENTJ, ENTP) AND สนใจเทคโนโลยี AND (วิทย์/คณิต หรือ ธุรกิจ หรือ วิจัย)",
            "careers": "นักวิทยาศาสตร์ข้อมูล, นักวิจัย AI, Machine Learning Engineer, นักสถิติ"
        },
        {
            "faculty": "🏛️ คณะวิทยาศาสตร์ / วิจัยและห้องปฏิบัติการ (Pure Science & Research)",
            "condition_symbol": r"(M_{INTP} \lor M_{INTJ} \lor M_{ISTJ} \lor M_{INFJ}) \land P \land (X \lor N)",
            "eval": (mbti in ["INTP", "INTJ", "ISTJ", "INFJ"]) and is_math_sci and (is_research or is_nature),
            "rule_desc": "ต้องเป็น (INTP, INTJ, ISTJ, INFJ) AND สนใจวิทย์/คณิต AND (วิจัย หรือ ธรรมชาติ/สิ่งแวดล้อม)",
            "careers": "นักวิทยาศาสตร์, นักวิจัย, นักดาราศาสตร์, นักวิเคราะห์ห้องปฏิบัติการ"
        },
        {
            "faculty": "🏛️ คณะสหเวชศาสตร์ / พยาบาลศาสตร์ / สาธารณสุข (Allied Health)",
            "condition_symbol": r"(M_{ISFJ} \lor M_{ESFJ} \lor M_{ISTJ} \lor M_{ENFJ}) \land H \land (P \lor T \lor C)",
            "eval": (mbti in ["ISFJ", "ESFJ", "ISTJ", "ENFJ"]) and is_healthcare and (is_math_sci or is_social_people or is_helping),
            "rule_desc": "ต้องเป็น (ISFJ, ESFJ, ISTJ, ENFJ) AND สนใจสุขภาพ AND (วิทย์/คณิต หรือ ผู้คน/การช่วยเหลือ)",
            "careers": "พยาบาล, นักกายภาพบำบัด, นักเทคนิคการแพทย์, นักสาธารณสุข"
        },
        {
            "faculty": "🏛️ คณะโภชนาการ / วิทยาศาสตร์การอาหาร (Nutrition & Food Science)",
            "condition_symbol": r"(M_{ISFJ} \lor M_{ISTJ} \lor M_{ISFP} \lor M_{ESFJ}) \land (H \lor F) \land P",
            "eval": (mbti in ["ISFJ", "ISTJ", "ISFP", "ESFJ"]) and (is_healthcare or is_food) and is_math_sci,
            "rule_desc": "ต้องเป็น (ISFJ, ISTJ, ISFP, ESFJ) AND สนใจสุขภาพ/อาหาร AND สนใจวิทย์/คณิต",
            "careers": "นักกำหนดอาหาร, นักวิทยาศาสตร์การอาหาร, นักพัฒนาผลิตภัณฑ์อาหาร"
        },
        {
            "faculty": "🏛️ คณะสถาปัตยกรรมศาสตร์ / ภูมิสถาปัตย์ (Architecture)",
            "condition_symbol": r"(M_{INTJ} \lor M_{ISTP} \lor M_{ISFP} \lor M_{ENTJ}) \land R \land (P \lor W)",
            "eval": (mbti in ["INTJ", "ISTP", "ISFP", "ENTJ"]) and is_art_design and (is_math_sci or is_practical),
            "rule_desc": "ต้องเป็น (INTJ, ISTP, ISFP, ENTJ) AND สนใจการออกแบบ AND (วิทย์/คณิต หรือ งานปฏิบัติ)",
            "careers": "สถาปนิก, ภูมิสถาปนิก, นักออกแบบอาคาร, นักออกแบบพื้นที่"
        },
        {
            "faculty": "🏛️ คณะบัญชี / ตรวจสอบ / ภาษี (Accounting & Audit)",
            "condition_symbol": r"(M_{ISTJ} \lor M_{ESTJ} \lor M_{INTJ} \lor M_{ISTP}) \land S \land (P \lor O)",
            "eval": (mbti in ["ISTJ", "ESTJ", "INTJ", "ISTP"]) and is_biz_finance and (is_math_sci or is_operations),
            "rule_desc": "ต้องเป็น (ISTJ, ESTJ, INTJ, ISTP) AND สนใจการเงิน AND (วิทย์/คณิต หรือ ระบบงาน)",
            "careers": "นักบัญชี, ผู้สอบบัญชี, ที่ปรึกษาภาษี, ผู้ควบคุมภายใน"
        },
        {
            "faculty": "🏛️ คณะผู้ประกอบการ / การขาย / พาณิชย์อิเล็กทรอนิกส์ (Entrepreneurship & Sales)",
            "condition_symbol": r"(M_{ENTJ} \lor M_{ENTP} \lor M_{ENFP} \lor M_{ESTP}) \land S \land (R \lor T)",
            "eval": (mbti in ["ENTJ", "ENTP", "ENFP", "ESTP"]) and is_biz_finance and (is_art_design or is_social_people),
            "rule_desc": "ต้องเป็น (ENTJ, ENTP, ENFP, ESTP) AND สนใจธุรกิจ AND (ความคิดสร้างสรรค์ หรือ การสื่อสาร)",
            "careers": "ผู้ประกอบการ, นักขาย, Business Development, เจ้าของธุรกิจออนไลน์"
        },
        {
            "faculty": "🏛️ คณะดนตรี / ศิลปะการแสดง / ภาพยนตร์ (Performing Arts)",
            "condition_symbol": r"(M_{ISFP} \lor M_{ESFP} \lor M_{ENFP} \lor M_{INFP}) \lan� R \land (T \lor A)",
            "eval": (mbti in ["ISFP", "ESFP", "ENFP", "INFP"]) and is_art_design and (is_social_people or is_sport),
            "rule_desc": "ต้องเป็น (ISFP, ESFP, ENFP, INFP) AND สนใจศิลปะ AND (การสื่อสารกับผู้คน หรือ การเคลื่อนไหว)",
            "careers": "นักดนตรี, นักแสดง, ผู้กำกับ, นักตัดต่อภาพยนตร์, ศิลปิน"
        },
        {
            "faculty": "🏛️ คณะภาษา / มนุษยศาสตร์ / ล่ามและการแปล (Languages & Humanities)",
            "condition_symbol": r"(M_{ENFJ} \lor M_{ENFP} \lor M_{INFJ} \lor M_{INTP}) \land L \land (T \lor R)",
            "eval": (mbti in ["ENFJ", "ENFP", "INFJ", "INTP"]) and is_language and (is_social_people or is_art_design),
            "rule_desc": "ต้องเป็น (ENFJ, ENFP, INFJ, INTP) AND สนใจภาษา AND (สังคม/ผู้คน หรือ งานสร้างสรรค์)",
            "careers": "นักแปล, ล่าม, นักเขียน, บรรณาธิการ, นักภาษาศาสตร์"
        },
        {
            "faculty": "🏛️ คณะครุศาสตร์ / ศึกษาศาสตร์ / การฝึกอบรม (Education)",
            "condition_symbol": r"(M_{ENFJ} \lor M_{ESFJ} \lor M_{INFJ} \lor M_{ISFJ}) \land E \land (T \lor L \lor C)",
            "eval": (mbti in ["ENFJ", "ESFJ", "INFJ", "ISFJ"]) and is_education and (is_social_people or is_language or is_helping),
            "rule_desc": "ต้องเป็น (ENFJ, ESFJ, INFJ, ISFJ) AND สนใจการศึกษา AND (ผู้คน ภาษา หรือ การช่วยเหลือ)",
            "careers": "ครู, อาจารย์, นักออกแบบการเรียนรู้, วิทยากร, ผู้เชี่ยวชาญพัฒนาบุคลากร"
        },
        {
            "faculty": "🏛️ คณะจิตวิทยา / ทรัพยากรมนุษย์ / การแนะแนว (Psychology & HR)",
            "condition_symbol": r"(M_{INFJ} \lor M_{INFP} \lor M_{ENFJ} \lor M_{ENFP}) \land (T \lor C) \land (H \lor E)",
            "eval": (mbti in ["INFJ", "INFP", "ENFJ", "ENFP"]) and (is_social_people or is_helping) and (is_healthcare or is_education),
            "rule_desc": "ต้องเป็น (INFJ, INFP, ENFJ, ENFP) AND สนใจผู้คน/การช่วยเหลือ AND (สุขภาพจิต หรือ การพัฒนาคน)",
            "careers": "นักจิตวิทยา, นักแนะแนว, HR Business Partner, นักพัฒนาทรัพยากรมนุษย์"
        },
        {
            "faculty": "🏛️ คณะความสัมพันธ์ระหว่างประเทศ / การทูต (International Relations)",
            "condition_symbol": r"(M_{ENFJ} \lor M_{ENFP} \lor M_{INFJ} \lor M_{ENTJ}) \land J \land (L \lor T)",
            "eval": (mbti in ["ENFJ", "ENFP", "INFJ", "ENTJ"]) and is_legal and (is_language or is_social_people),
            "rule_desc": "ต้องเป็น (ENFJ, ENFP, INFJ, ENTJ) AND สนใจกฎหมาย/นโยบาย AND (ภาษา หรือ สังคม)",
            "careers": "นักการทูต, นักวิเคราะห์นโยบายต่างประเทศ, เจ้าหน้าที่องค์กรระหว่างประเทศ"
        },
        {
            "faculty": "🏛️ คณะสังคมสงเคราะห์ / พัฒนาชุมชน / NGO (Social Development)",
            "condition_symbol": r"(M_{INFJ} \lor M_{ENFJ} \lor M_{ISFJ} \lor M_{INFP}) \land C \land (T \lor J)",
            "eval": (mbti in ["INFJ", "ENFJ", "ISFJ", "INFP"]) and is_helping and (is_social_people or is_legal),
            "rule_desc": "ต้องเป็น (INFJ, ENFJ, ISFJ, INFP) AND สนใจการช่วยเหลือ AND (สังคม หรือ สิทธิ/นโยบาย)",
            "careers": "นักสังคมสงเคราะห์, นักพัฒนาชุมชน, เจ้าหน้าที่ NGO, นักสิทธิมนุษยชน"
        },
        {
            "faculty": "🏛️ คณะเกษตรศาสตร์ / สิ่งแวดล้อม / ทรัพยากรธรรมชาติ (Environment & Agriculture)",
            "condition_symbol": r"(M_{ISFP} \lor M_{ISTP} \lor M_{ISFJ} \lor M_{ESTP}) \land N \land (P \lor W)",
            "eval": (mbti in ["ISFP", "ISTP", "ISFJ", "ESTP"]) and is_nature and (is_math_sci or is_practical),
            "rule_desc": "ต้องเป็น (ISFP, ISTP, ISFJ, ESTP) AND สนใจธรรมชาติ AND (วิทย์/คณิต หรือ งานปฏิบัติ)",
            "careers": "นักสิ่งแวดล้อม, นักวิชาการเกษตร, นักวนศาสตร์, นักอนุรักษ์ทรัพยากร"
        },
        {
            "faculty": "🏛️ คณะสัตวแพทยศาสตร์ / ประมง / วิทยาศาสตร์สัตว์ (Animal & Marine Science)",
            "condition_symbol": r"(M_{ISTJ} \lor M_{ISFJ} \lor M_{ISFP} \lor M_{INTJ}) \land N \land (H \lor P)",
            "eval": (mbti in ["ISTJ", "ISFJ", "ISFP", "INTJ"]) and is_nature and (is_healthcare or is_math_sci),
            "rule_desc": "ต้องเป็น (ISTJ, ISFJ, ISFP, INTJ) AND สนใจธรรมชาติ/สัตว์ AND (สุขภาพ หรือ วิทย์/คณิต)",
            "careers": "สัตวแพทย์, นักประมง, นักวิทยาศาสตร์ทางทะเล, นักวิจัยสัตว์"
        },
        {
            "faculty": "🏛️ คณะวิทยาศาสตร์การกีฬา / พลศึกษา / ฟิตเนส (Sports Science)",
            "condition_symbol": r"(M_{ESTP} \lor M_{ESFP} \lor M_{ISTP} \lor M_{ISFP}) \land A \land (H \lor T \lor C)",
            "eval": (mbti in ["ESTP", "ESFP", "ISTP", "ISFP"]) and is_sport and (is_healthcare or is_social_people or is_helping),
            "rule_desc": "ต้องเป็น (ESTP, ESFP, ISTP, ISFP) AND สนใจกีฬา AND (สุขภาพ หรือ ผู้คน/การช่วยเหลือ)",
            "careers": "นักวิทยาศาสตร์การกีฬา, เทรนเนอร์, โค้ช, นักกายภาพด้านกีฬา"
        },
        {
            "faculty": "🏛️ คณะคหกรรมศาสตร์ / การอาหาร / การโรงแรม (Culinary & Hospitality)",
            "condition_symbol": r"(M_{ISFP} \lor M_{ESFP} \lor M_{ISTP} \lor M_{ESTP}) \land (F \lor V) \land (R \lor T)",
            "eval": (mbti in ["ISFP", "ESFP", "ISTP", "ESTP"]) and (is_food or is_travel) and (is_art_design or is_social_people),
            "rule_desc": "ต้องเป็น (ISFP, ESFP, ISTP, ESTP) AND สนใจอาหาร/บริการ AND (สร้างสรรค์ หรือ ผู้คน)",
            "careers": "เชฟ, นักพัฒนาเมนู, ผู้จัดการโรงแรม, ผู้ประกอบการร้านอาหาร"
        },
        {
            "faculty": "🏛️ คณะการท่องเที่ยว / การโรงแรม / ธุรกิจการบิน (Tourism & Aviation)",
            "condition_symbol": r"(M_{ESFP} \lor M_{ENFP} \lor M_{ESFJ} \lor M_{ESTP}) \land V \land (L \lor T)",
            "eval": (mbti in ["ESFP", "ENFP", "ESFJ", "ESTP"]) and is_travel and (is_language or is_social_people),
            "rule_desc": "ต้องเป็น (ESFP, ENFP, ESFJ, ESTP) AND สนใจท่องเที่ยว/บริการ AND (ภาษา หรือ ผู้คน)",
            "careers": "มัคคุเทศก์, ผู้จัดการโรงแรม, เจ้าหน้าที่สายการบิน, นักวางแผนท่องเที่ยว"
        },
        {
            "faculty": "🏛️ คณะโลจิสติกส์ / ซัพพลายเชน / การจัดการปฏิบัติการ (Operations & Logistics)",
            "condition_symbol": r"(M_{ESTJ} \lor M_{ISTJ} \lor M_{ENTJ} \lor M_{ESTP}) \land O \land (S \lor P)",
            "eval": (mbti in ["ESTJ", "ISTJ", "ENTJ", "ESTP"]) and is_operations and (is_biz_finance or is_math_sci),
            "rule_desc": "ต้องเป็น (ESTJ, ISTJ, ENTJ, ESTP) AND สนใจระบบงาน AND (ธุรกิจ หรือ วิทย์/คณิต)",
            "careers": "ผู้จัดการโลจิสติกส์, นักวางแผนซัพพลายเชน, Operations Manager, ผู้ควบคุมคลังสินค้า"
        },
        {
            "faculty": "🏛️ คณะอุตสาหกรรมการผลิต / วิศวกรรมเครื่องกล / งานช่าง (Industrial & Skilled Trades)",
            "condition_symbol": r"(M_{ISTP} \lor M_{ISFP} \lor M_{ESTP} \lor M_{ISTJ}) \land W \land (P \lor O)",
            "eval": (mbti in ["ISTP", "ISFP", "ESTP", "ISTJ"]) and is_practical and (is_math_sci or is_operations),
            "rule_desc": "ต้องเป็น (ISTP, ISFP, ESTP, ISTJ) AND สนใจงานช่าง/ลงมือทำ AND (วิทย์/คณิต หรือ ระบบงาน)",
            "careers": "ช่างเทคนิค, วิศวกรเครื่องกล, ช่างยนต์, ผู้ควบคุมการผลิต, ช่างไฟฟ้า"
        },
        {
            "faculty": "🏛️ คณะก่อสร้าง / โยธา / อสังหาริมทรัพย์ (Construction & Property)",
            "condition_symbol": r"(M_{ESTJ} \lor M_{ENTJ} \lor M_{ISTP} \lor M_{ESTP}) \land W \land (S \lor P)",
            "eval": (mbti in ["ESTJ", "ENTJ", "ISTP", "ESTP"]) and is_practical and (is_biz_finance or is_math_sci),
            "rule_desc": "ต้องเป็น (ESTJ, ENTJ, ISTP, ESTP) AND สนใจงานก่อสร้าง/ปฏิบัติ AND (ธุรกิจ หรือ วิทย์/คณิต)",
            "careers": "วิศวกรโยธา, ผู้ควบคุมงานก่อสร้าง, นักประเมินอสังหาริมทรัพย์, ผู้จัดการโครงการ"
        },
        {
            "faculty": "🏛️ คณะความมั่นคง / ตำรวจ / ทหาร / กู้ภัย (Security & Emergency)",
            "condition_symbol": r"(M_{ISTJ} \lor M_{ESTJ} \lor M_{ISTP} \lor M_{ESTP}) \land K \land (T \lor W)",
            "eval": (mbti in ["ISTJ", "ESTJ", "ISTP", "ESTP"]) and is_security and (is_social_people or is_practical),
            "rule_desc": "ต้องเป็น (ISTJ, ESTJ, ISTP, ESTP) AND สนใจความปลอดภัย AND (สังคม/กฎระเบียบ หรือ งานปฏิบัติ)",
            "careers": "ตำรวจ, ทหาร, นักกู้ภัย, เจ้าหน้าที่ความปลอดภัย, นักนิติวิทยาศาสตร์"
        },
        {
            "faculty": "🏛️ คณะสารสนเทศศาสตร์ / บรรณารักษศาสตร์ / จดหมายเหตุ (Information & Archives)",
            "condition_symbol": r"(M_{ISTJ} \lor M_{ISFJ} \lor M_{INTP} \lor M_{INTJ}) \land (Q \lor T) \land (X \lor L)",
            "eval": (mbti in ["ISTJ", "ISFJ", "INTP", "INTJ"]) and (is_tech or is_social_people) and (is_research or is_language),
            "rule_desc": "ต้องเป็น (ISTJ, ISFJ, INTP, INTJ) AND สนใจเทคโนโลยี/ข้อมูล AND (วิจัย หรือ ภาษา)",
            "careers": "นักสารสนเทศ, บรรณารักษ์ดิจิทัล, นักจดหมายเหตุ, ผู้ดูแลฐานข้อมูล"
        },
        {
            "faculty": "🏛️ คณะการบิน / การขนส่ง / ควบคุมการจราจร (Transportation)",
            "condition_symbol": r"(M_{ESTP} \lor M_{ISTP} \lor M_{ENTJ} \lor M_{ESTJ}) \land (V \lor O) \land (P \lor K)",
            "eval": (mbti in ["ESTP", "ISTP", "ENTJ", "ESTJ"]) and (is_travel or is_operations) and (is_math_sci or is_security),
            "rule_desc": "ต้องเป็น (ESTP, ISTP, ENTJ, ESTJ) AND สนใจการเดินทาง/ระบบงาน AND (วิทย์/คณิต หรือ ความปลอดภัย)",
            "careers": "นักบิน, เจ้าหน้าที่ควบคุมการจราจรทางอากาศ, ผู้จัดการขนส่ง, เจ้าหน้าที่ปฏิบัติการสนามบิน"
        }
    ]

    matched_faculties = []

    for item in faculties_rules:
        st.markdown(f"#### {item['faculty']}")
        st.latex(rf"\text{{เงื่อนไข: }} {item['condition_symbol']}")
        st.write(f"**คำอธิบายเงื่อนไข:** {item['rule_desc']}")
        st.write(f"**อาชีพที่แนะนำ:** {item['careers']}")
        
        if item['eval']:
            st.success("ผลลัพธ์ทางตรรกศาสตร์: **TRUE (จริง - ตรงตามเงื่อนไขสายนี้)**")
            matched_faculties.append((item['faculty'], item['careers']))
        else:
            st.error("ผลลัพธ์ทางตรรกศาสตร์: **FALSE (เท็จ - ไม่ตรงตามเงื่อนไข)**")
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🎯 สรุปคณะและอาชีพที่ตรงตามเงื่อนไขตรรกศาสตร์ของคุณ")
    
    if matched_faculties:
        st.balloons()
        for fac_title, careers in matched_faculties:
            st.markdown(f"- ✅ **{fac_title}**")
            st.caption(f"  └ อาชีพที่เหมาะสม: {careers}")
    else:
        st.warning("ยังไม่พบคณะที่ตรงตามเงื่อนไขตรรกศาสตร์แบบสมบูรณ์ (ลองปรับเปลี่ยนการประเมินความชอบใน Step 3)")

    st.markdown("---")
    if st.button("🔄 เริ่มทำแบบประเมินใหม่ทั้งหมด"):
        st.session_state.clear()
        st.rerun()

import streamlit as st
from questions import (
    COGNITIVE_QUESTIONS,
    SUBJECT_QUESTIONS,
    HOBBY_QUESTIONS,
    GOAL_QUESTIONS,
    MBTI_DESCRIPTIONS,
)
from funding_step import FUNDING_QUESTIONS, FUNDING_SCALE, FUNDING_PROPOSITIONS, funding_result
from university_logic import build_faculty_results, build_university_results

st.set_page_config(
    page_title="MBTI + คณะ + เงินทุน + มหาวิทยาลัย",
    page_icon="🎓",
    layout="wide",
)

if "step" not in st.session_state:
    st.session_state.step = 1
if "mbti_result" not in st.session_state:
    st.session_state.mbti_result = "INTJ"
if "category_scores" not in st.session_state:
    st.session_state.category_scores = {}

SCALE_OPTIONS = {
    "1 - ไม่ตรงเลย": 1,
    "2 - ไม่ค่อยตรง": 2,
    "3 - ปานกลาง / ไม่แน่ใจ": 3,
    "4 - ค่อนข้างตรง": 4,
    "5 - ตรงมากที่สุด": 5,
}


def reset_app():
    st.session_state.clear()
    st.rerun()


# -----------------------------------------------------------------------------
# STEP 1: MBTI
# -----------------------------------------------------------------------------
if st.session_state.step == 1:
    st.title("🧩 ขั้นตอนที่ 1: ประเมินบุคลิกภาพ MBTI")
    st.caption("ผลลัพธ์ MBTI จะถูกนำไปเป็นเงื่อนไขหนึ่งของประพจน์คณะ")

    with st.form("mbti_form"):
        raw_answers = {}
        for idx, q in enumerate(COGNITIVE_QUESTIONS, 1):
            q_id = q.get("id", idx)
            st.markdown(f"**ข้อที่ {idx}:** {q['text']}")
            answer = st.radio(
                f"ระดับความตรง (ข้อ {idx})",
                options=list(SCALE_OPTIONS.keys()),
                index=2,
                key=f"cog_{q_id}",
                horizontal=True,
            )
            raw_answers[q_id] = {"func": q["func"], "score": SCALE_OPTIONS[answer]}

        if st.form_submit_button("🚀 ประมวลผล MBTI"):
            func_scores = {"Ne": 0, "Ni": 0, "Se": 0, "Si": 0, "Te": 0, "Ti": 0, "Fe": 0, "Fi": 0}
            for item in raw_answers.values():
                func_scores[item["func"]] += item["score"]

            dom_func = max(func_scores, key=func_scores.get)
            aux_candidates = {
                "Ne": ["Ti", "Fi"], "Se": ["Ti", "Fi"],
                "Ni": ["Te", "Fe"], "Si": ["Te", "Fe"],
                "Te": ["Ni", "Si"], "Fe": ["Ni", "Si"],
                "Ti": ["Ne", "Se"], "Fi": ["Ne", "Se"],
            }
            aux_func = max(aux_candidates[dom_func], key=lambda f: func_scores[f])
            opposite = {"Ne": "Si", "Si": "Ne", "Ni": "Se", "Se": "Ni", "Te": "Fi", "Fi": "Te", "Ti": "Fe", "Fe": "Ti"}
            type_mapping = {
                ("Ne", "Ti"): "ENTP", ("Ne", "Fi"): "ENFP",
                ("Ni", "Te"): "INTJ", ("Ni", "Fe"): "INFJ",
                ("Se", "Ti"): "ESTP", ("Se", "Fi"): "ESFP",
                ("Si", "Te"): "ISTJ", ("Si", "Fe"): "ISFJ",
                ("Te", "Ni"): "ENTJ", ("Te", "Si"): "ESTJ",
                ("Ti", "Ne"): "INTP", ("Ti", "Se"): "ISTP",
                ("Fe", "Ni"): "ENFJ", ("Fe", "Si"): "ESFJ",
                ("Fi", "Ne"): "INFP", ("Fi", "Se"): "ISFP",
            }
            st.session_state.mbti_result = type_mapping.get((dom_func, aux_func), "INTJ")
            st.session_state.func_scores = func_scores
            st.session_state.mbti_stack = {
                "Dom": dom_func,
                "Aux": aux_func,
                "Tert": opposite[aux_func],
                "Inf": opposite[dom_func],
            }
            st.session_state.step = 2
            st.rerun()

# -----------------------------------------------------------------------------
# STEP 2: MBTI summary
# -----------------------------------------------------------------------------
elif st.session_state.step == 2:
    mbti = st.session_state.mbti_result
    info = MBTI_DESCRIPTIONS.get(mbti, MBTI_DESCRIPTIONS.get("INTJ", {}))
    stack = st.session_state.get("mbti_stack", {})
    st.title("🌟 ขั้นตอนที่ 2: สรุป MBTI")
    st.success(f"ผลการวิเคราะห์: **{mbti}** — {info.get('title', '')}")
    st.write(info.get("desc", ""))

    if stack:
        st.write(f"Dominant: `{stack['Dom']}`")
        st.write(f"Auxiliary: `{stack['Aux']}`")
        st.write(f"Tertiary: `{stack['Tert']}`")
        st.write(f"Inferior: `{stack['Inf']}`")

    st.markdown("### 🔤 ประพจน์ MBTI")
    st.info(f"M_{mbti} = True")
    st.caption("M_x ใช้แทนประพจน์บุคลิกภาพ และไม่ใช้ซ้ำกับ Fxx (คณะ) หรือ B_x (เงินทุน)")

    if st.button("➡️ ไปต่อ: ประเมินความสนใจ"):
        st.session_state.step = 3
        st.rerun()

# -----------------------------------------------------------------------------
# STEP 3: Interest categories
# -----------------------------------------------------------------------------
elif st.session_state.step == 3:
    st.title("📚 ขั้นตอนที่ 3: ประเมินความสนใจเพื่อหาคณะ")
    st.write("ตอบคำถามเพื่อสร้างประพจน์ความสนใจ แล้วนำไปจับคู่กับ MBTI")

    question_sets = [
        ("📖 วิชาความรู้", SUBJECT_QUESTIONS, "sub"),
        ("🎨 งานอดิเรกและความสนใจ", HOBBY_QUESTIONS, "hobby"),
        ("🎯 เป้าหมายอาชีพ", GOAL_QUESTIONS, "goal"),
    ]

    with st.form("interest_form"):
        scores = {}
        for title, questions, prefix in question_sets:
            st.subheader(title)
            for idx, q in enumerate(questions, 1):
                if isinstance(q, dict):
                    text = q.get("label") or q.get("text") or q.get("question") or str(q)
                    category = q.get("category", "ทั่วไป")
                    q_id = q.get("id", f"{prefix}_{idx}")
                    options = q.get("options")
                else:
                    text, category, q_id, options = str(q), "ทั่วไป", f"{prefix}_{idx}", None

                st.markdown(f"**ข้อ {idx}:** {text} *(หมวด: {category})*")
                if options and isinstance(options, list):
                    answer = st.radio(
                        f"เลือกคำตอบ ({q_id})",
                        options=options,
                        index=0,
                        key=f"{prefix}_{q_id}",
                    )
                    value = (options.index(answer) + 1) * (5 / len(options))
                else:
                    answer = st.radio(
                        f"ระดับความตรง ({q_id})",
                        options=list(SCALE_OPTIONS.keys()),
                        index=2,
                        key=f"{prefix}_{q_id}",
                        horizontal=True,
                    )
                    value = SCALE_OPTIONS[answer]
                scores[category] = scores.get(category, 0) + value

        if st.form_submit_button("🚀 บันทึกผลและไปประเมินเงินทุน"):
            st.session_state.category_scores = scores
            st.session_state.step = 4
            st.rerun()

# -----------------------------------------------------------------------------
# STEP 4: Funding assessment
# -----------------------------------------------------------------------------
elif st.session_state.step == 4:
    st.title("💰 ขั้นตอนที่ 4: ประเมินเงินทุนสำหรับการเรียนต่อ")
    st.write("คะแนนส่วนนี้ใช้เฉพาะเพื่อจัดระดับทุนทรัพย์: สูง / กลาง / ต่ำ")

    with st.form("funding_form"):
        total = 0.0
        max_score = 0.0
        for idx, question in enumerate(FUNDING_QUESTIONS, 1):
            answer = st.radio(
                f"ข้อ {idx}: {question['text']}",
                options=list(FUNDING_SCALE.keys()),
                index=2,
                key=question["id"],
                horizontal=True,
            )
            total += FUNDING_SCALE[answer] * question.get("weight", 1)
            max_score += 5 * question.get("weight", 1)

        if st.form_submit_button("🚀 สรุประดับเงินทุน"):
            result = funding_result(total, max_score)
            st.session_state.funding_result = result
            st.session_state.step = 5
            st.rerun()

# -----------------------------------------------------------------------------
# STEP 5: Faculty proposition AND funding proposition -> university
# -----------------------------------------------------------------------------
elif st.session_state.step == 5:
    mbti = st.session_state.mbti_result
    funding = st.session_state.funding_result
    scores = st.session_state.get("category_scores", {})

    def category_high(keywords, threshold=6):
        for category, score in scores.items():
            category_text = str(category).lower()
            if any(keyword.lower() in category_text for keyword in keywords) and score >= threshold:
                return True
        return False

    interests = {
        "math": category_high(["math", "คณิต", "science", "วิทย์", "ฟิสิกส์", "เคมี", "ชีว"]),
        "tech": category_high(["tech", "คอมพิวเตอร์", "เทคโนโลยี", "it", "coding", "นวัตกรรม"]),
        "art": category_high(["art", "ศิลปะ", "ออกแบบ", "design", "สร้างสรรค์", "บันเทิง"]),
        "business": category_high(["finance", "การเงิน", "ธุรกิจ", "บริหาร", "การลงทุน", "การตลาด", "การค้า"]),
        "social": category_high(["social", "สังคม", "ภาษา", "จิตวิทยา", "บริการ", "การสื่อสาร", "บริหารคน"]),
    }

    faculty_results = build_faculty_results(mbti, interests)
    matched = [item for item in faculty_results if item["true"]]
    universities = build_university_results(faculty_results, funding["level"])

    st.title("🏫 ขั้นตอนที่ 5: เชื่อมประพจน์คณะ + เงินทุน = มหาวิทยาลัย")

    st.markdown("### 1. ประพจน์ของคณะ")
    if matched:
        for item in matched:
            st.success(f"**{item['id']} = True** → {item['faculty']}")
    else:
        st.warning("ยังไม่พบประพจน์คณะที่เป็น True ตามเงื่อนไขที่กำหนด")

    st.markdown("### 2. ประพจน์ของเงินทุน")
    funding_prop = FUNDING_PROPOSITIONS[funding["level"]]
    st.info(
        f"**{funding_prop['symbol']} = True** → เงินทุนระดับ{funding['level']} "
        f"({funding['percent']}%, {funding['score']}/{funding['max_score']})"
    )

    st.markdown("### 3. การเชื่อมด้วย AND (∧)")
    st.latex(r"F_{xx} \land B_H \Rightarrow U_{xx}")
    st.caption("ตัวอย่าง: F01 ∧ B_H = True จึงสร้างผลลัพธ์ Uxx ได้ โดย Fxx, Bx และ Uxx เป็นคนละ namespace และไม่ซ้ำกัน")

    if universities:
        st.subheader("🎓 มหาวิทยาลัยที่ตรงกับคณะและระดับเงินทุน")
        for university in universities:
            st.success(
                f"**{university['id']} — {university['name']}**\n\n"
                f"{university['faculty_id']} ∧ {funding_prop['symbol']} = **True**"
            )
    else:
        st.warning(
            "ยังไม่พบมหาวิทยาลัยในชุดตัวอย่างที่ตรงทั้งคณะและระดับเงินทุนนี้ "
            "สามารถแก้รายการมหาวิทยาลัยได้ใน university_logic.py"
        )

    st.markdown("---")
    st.caption("หมายเหตุ: รายชื่อมหาวิทยาลัยเป็นตัวอย่างสำหรับระบบตรรกศาสตร์ ไม่ใช่การรับรองโอกาสสอบติดหรือค่าเล่าเรียนจริง")

    if st.button("🔄 เริ่มทำแบบประเมินใหม่ทั้งหมด"):
        reset_app()

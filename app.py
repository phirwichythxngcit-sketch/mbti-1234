import streamlit as st
from questions import (
    COGNITIVE_QUESTIONS,
    SUBJECT_QUESTIONS,
    HOBBY_QUESTIONS,
    GOAL_QUESTIONS,
    FINANCIAL_QUESTIONS,
    MBTI_DESCRIPTIONS,
)
from funding_step import render_funding_step, render_university_result

st.set_page_config(
    page_title="ระบบวิเคราะห์อาชีพด้วยตรรกศาสตร์ MBTI & Funding Logic",
    page_icon="🎓",
    layout="wide",
)

# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# STEP 1: MBTI
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.title("🧩 ขั้นตอนที่ 1: ประเมินบุคลิกภาพ (MBTI)")
    st.write("เลือกสเกลที่ตรงกับตัวคุณมากที่สุดเพื่อสรุปหาประพจน์ทางบุคลิกภาพ")

    with st.form("mbti_form"):
        raw_answers = {}
        for idx, q in enumerate(COGNITIVE_QUESTIONS, 1):
            q_id = q.get("id", idx)
            st.markdown(f"**ข้อที่ {idx}:** {q['text']}")
            ans = st.radio(
                f"ระดับความตรง (ข้อ {idx}):",
                options=list(SCALE_OPTIONS.keys()),
                index=2,
                key=f"cog_{q_id}",
                horizontal=True,
            )
            raw_answers[q_id] = {"func": q["func"], "score": SCALE_OPTIONS[ans]}
            st.markdown("<hr style='margin: 0.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)

        submitted = st.form_submit_button("🚀 ประมวลผล MBTI (ไปขั้นตอนที่ 2)")

    if submitted:
        func_scores = {"Ne": 0, "Ni": 0, "Se": 0, "Si": 0, "Te": 0, "Ti": 0, "Fe": 0, "Fi": 0}
        for item in raw_answers.values():
            func_scores[item["func"]] += item["score"]

        func_percentages = {
            func: round((score / 50) * 100, 1)
            for func, score in func_scores.items()
        }
        sorted_funcs = sorted(func_scores.items(), key=lambda x: x[1], reverse=True)
        dom_func = max(func_scores, key=func_scores.get)

        aux_candidates_map = {
            "Ne": ["Ti", "Fi"], "Se": ["Ti", "Fi"],
            "Ni": ["Te", "Fe"], "Si": ["Te", "Fe"],
            "Te": ["Ni", "Si"], "Fe": ["Ni", "Si"],
            "Ti": ["Ne", "Se"], "Fi": ["Ne", "Se"],
        }
        possible_aux = aux_candidates_map.get(dom_func, ["Te", "Fe"])
        aux_func = max(possible_aux, key=lambda f: func_scores[f])

        opposite_map = {
            "Ne": "Si", "Si": "Ne", "Ni": "Se", "Se": "Ni",
            "Te": "Fi", "Fi": "Te", "Ti": "Fe", "Fe": "Ti",
        }
        tertiary_func = opposite_map[aux_func]
        inferior_func = opposite_map[dom_func]

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

        st.session_state.func_scores = func_scores
        st.session_state.func_percentages = func_percentages
        st.session_state.sorted_funcs = sorted_funcs
        st.session_state.possible_aux = possible_aux
        st.session_state.mbti_stack = {
            "Dom": dom_func,
            "Aux": aux_func,
            "Tert": tertiary_func,
            "Inf": inferior_func,
        }
        st.session_state.mbti_result = type_mapping.get((dom_func, aux_func), "INTJ")
        st.session_state.step = 2
        st.rerun()

# ---------------------------------------------------------
# STEP 2: MBTI Result + Propositions
# ---------------------------------------------------------
elif st.session_state.step == 2:
    mbti = st.session_state.mbti_result
    info = MBTI_DESCRIPTIONS.get(mbti, MBTI_DESCRIPTIONS["INTJ"])
    sorted_funcs = st.session_state.get("sorted_funcs", [])
    func_pct = st.session_state.get("func_percentages", {})
    stack = st.session_state.get("mbti_stack", {})

    st.title("🌟 ขั้นตอนที่ 2: สรุปผล MBTI และตรรกศาสตร์")
    st.success(f"### ผลการวิเคราะห์ MBTI: **{mbti}** ({info['title']})")
    st.info(f"**ลักษณะตัวตน:** {info['desc']}")

    st.subheader("📊 Cognitive Stack")
    for func_code, score in sorted_funcs:
        pct = func_pct.get(func_code, 0)
        st.write(f"**{func_code}**: {score}/50 คะแนน ({pct}%)")
        st.progress(pct / 100)

    if stack:
        st.write(f"🥇 Dominant: `{stack['Dom']}`")
        st.write(f"🥈 Auxiliary: `{stack['Aux']}`")
        st.write(f"🥉 Tertiary: `{stack['Tert']}`")
        st.write(f"⚓ Inferior: `{stack['Inf']}`")

    with st.expander("📚 ดูตรรกศาสตร์ระดับ ม.4"):
        st.markdown("### การกำหนดประพจน์")
        st.write("ให้ **Score(f)** แทนคะแนนของฟังก์ชัน f")
        st.write(f"ให้ประพจน์ **M**: บุคลิกภาพแบบ `{mbti}` เป็นจริง")
        st.latex(r"\mathrm{Dom}=A \iff \forall f\,(Score(A)\ge Score(f))")
        st.latex(r"\mathrm{Dom}=Ne \iff \mathrm{Inferior}=Si")
        st.latex(r"\mathrm{Aux}=Ti \iff \mathrm{Tertiary}=Fe")

    if st.button("➡️ ไปต่อ: ประเมินความชอบและศักยภาพ (Step 3)"):
        st.session_state.step = 3
        st.rerun()

# ---------------------------------------------------------
# STEP 3: Subject / Hobby / Goal / Finance
# ---------------------------------------------------------
elif st.session_state.step == 3:
    st.title("📚 ขั้นตอนที่ 3: ประเมินความชอบและศักยภาพ")
    st.write("ทำแบบประเมินให้ครบ เพื่อนำไปสร้างประพจน์คณะ")

    all_question_sets = [
        ("📖 วิชาและความรู้", SUBJECT_QUESTIONS, "sub"),
        ("🎨 งานอดิเรกและความสนใจ", HOBBY_QUESTIONS, "hobby"),
        ("🎯 เป้าหมายอาชีพและค่านิยม", GOAL_QUESTIONS, "goal"),
        ("💰 การบริหารและการเงิน", FINANCIAL_QUESTIONS, "fin"),
    ]

    with st.form("all_categories_form"):
        category_scores = {}

        for tab_name, questions_list, prefix in all_question_sets:
            st.subheader(tab_name)
            for idx, q in enumerate(questions_list, 1):
                if isinstance(q, dict):
                    q_text = q.get("label") or q.get("text") or q.get("question") or str(q)
                    category = q.get("category", "ทั่วไป")
                    q_id = q.get("id", f"{prefix}_{idx}")
                    options = q.get("options")
                else:
                    q_text = str(q)
                    category = "ทั่วไป"
                    q_id = f"{prefix}_{idx}"
                    options = None

                st.markdown(f"**ข้อที่ {idx}:** {q_text} *(หมวด: {category})*")

                if options and isinstance(options, list):
                    ans = st.radio(
                        f"เลือกคำตอบ ({q_id}):",
                        options=options,
                        index=0,
                        key=f"{prefix}_{q_id}",
                    )
                    score_val = (options.index(ans) + 1) * (5 / len(options))
                else:
                    ans = st.radio(
                        f"ระดับความตรง ({q_id}):",
                        options=list(SCALE_OPTIONS.keys()),
                        index=2,
                        key=f"{prefix}_{q_id}",
                        horizontal=True,
                    )
                    score_val = SCALE_OPTIONS[ans]

                category_scores[category] = category_scores.get(category, 0) + score_val
                st.markdown("<hr style='margin: 0.2rem 0 0.8rem 0;'>", unsafe_allow_html=True)

        submitted_step3 = st.form_submit_button("🚀 สรุปประพจน์คณะและไปประเมินเงินทุน (Step 4)")

    if submitted_step3:
        st.session_state.category_scores = category_scores
        st.session_state.step = 4
        st.rerun()

# ---------------------------------------------------------
# STEP 4: Funding assessment from funding_step.py
# ---------------------------------------------------------
elif st.session_state.step == 4:
    render_funding_step(next_step=5)

# ---------------------------------------------------------
# STEP 5: Faculty proposition AND funding proposition
# ---------------------------------------------------------
elif st.session_state.step == 5:
    st.title("🎓 ขั้นตอนที่ 5: เชื่อมประพจน์คณะ AND ประพจน์เงินทุน")

    mbti = st.session_state.get("mbti_result", "INTJ")
    category_scores = st.session_state.get("category_scores", {})

    st.success(f"MBTI = **{mbti}**")
    render_university_result(mbti, category_scores)

    st.markdown("---")
    if st.button("🔄 เริ่มทำแบบประเมินใหม่ทั้งหมด"):
        st.session_state.clear()
        st.rerun()

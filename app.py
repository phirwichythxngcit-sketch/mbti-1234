import streamlit as st
from questions import (
    COGNITIVE_QUESTIONS, SUBJECT_QUESTIONS, HOBBY_QUESTIONS,
    GOAL_QUESTIONS, FINANCIAL_QUESTIONS, MBTI_DESCRIPTIONS,
)
from funding_step import render_funding_step, render_university_result
from funding_university import get_faculty_results

st.set_page_config(page_title="ระบบวิเคราะห์อาชีพด้วยตรรกศาสตร์ MBTI & Subject Logic", page_icon="🎓", layout="wide")

if "step" not in st.session_state:
    st.session_state.step = 1
if "mbti_result" not in st.session_state:
    st.session_state.mbti_result = "INTJ"
if "category_scores" not in st.session_state:
    st.session_state.category_scores = {}

SCALE_OPTIONS = {
    "1 - ไม่ตรงเลย": 1, "2 - ไม่ค่อยตรง": 2, "3 - ปานกลาง / ไม่แน่ใจ": 3,
    "4 - ค่อนข้างตรง": 4, "5 - ตรงมากที่สุด": 5,
}

# STEP 1: MBTI
if st.session_state.step == 1:
    st.title("🧩 ขั้นตอนที่ 1: ประเมินบุคลิกภาพ (MBTI)")
    st.write("เลือกสเกลที่ตรงกับตัวคุณมากที่สุดเพื่อสรุปหาประพจน์ทางบุคลิกภาพ")
    with st.form("mbti_form"):
        raw_answers = {}
        for idx, q in enumerate(COGNITIVE_QUESTIONS, 1):
            q_id = q.get("id", idx)
            st.markdown(f"**ข้อที่ {idx}:** {q['text']}")
            ans = st.radio(f"ระดับความตรง (ข้อ {idx}):", list(SCALE_OPTIONS.keys()), index=2, key=f"cog_{q_id}", horizontal=True)
            raw_answers[q_id] = {"func": q["func"], "score": SCALE_OPTIONS[ans]}
        if st.form_submit_button("🚀 ประมวลผล MBTI (ไปขั้นตอนที่ 2)"):
            func_scores = {f: 0 for f in ["Ne", "Ni", "Se", "Si", "Te", "Ti", "Fe", "Fi"]}
            for item in raw_answers.values():
                func_scores[item["func"]] += item["score"]
            func_percentages = {f: round((s / 50) * 100, 1) for f, s in func_scores.items()}
            sorted_funcs = sorted(func_scores.items(), key=lambda x: x[1], reverse=True)
            dom_func = max(func_scores, key=func_scores.get)
            aux_candidates = {
                "Ne": ["Ti", "Fi"], "Se": ["Ti", "Fi"], "Ni": ["Te", "Fe"], "Si": ["Te", "Fe"],
                "Te": ["Ni", "Si"], "Fe": ["Ni", "Si"], "Ti": ["Ne", "Se"], "Fi": ["Ne", "Se"],
            }
            possible_aux = aux_candidates.get(dom_func, ["Te", "Fe"])
            aux_func = max(possible_aux, key=lambda f: func_scores[f])
            opposite = {"Ne": "Si", "Si": "Ne", "Ni": "Se", "Se": "Ni", "Te": "Fi", "Fi": "Te", "Ti": "Fe", "Fe": "Ti"}
            st.session_state.func_scores = func_scores
            st.session_state.func_percentages = func_percentages
            st.session_state.sorted_funcs = sorted_funcs
            st.session_state.mbti_stack = {"Dom": dom_func, "Aux": aux_func, "Tert": opposite[aux_func], "Inf": opposite[dom_func]}
            type_mapping = {
                ("Ne", "Ti"): "ENTP", ("Ne", "Fi"): "ENFP", ("Ni", "Te"): "INTJ", ("Ni", "Fe"): "INFJ",
                ("Se", "Ti"): "ESTP", ("Se", "Fi"): "ESFP", ("Si", "Te"): "ISTJ", ("Si", "Fe"): "ISFJ",
                ("Te", "Ni"): "ENTJ", ("Te", "Si"): "ESTJ", ("Ti", "Ne"): "INTP", ("Ti", "Se"): "ISTP",
                ("Fe", "Ni"): "ENFJ", ("Fe", "Si"): "ESFJ", ("Fi", "Ne"): "INFP", ("Fi", "Se"): "ISFP",
            }
            st.session_state.mbti_result = type_mapping.get((dom_func, aux_func), "INTJ")
            st.session_state.step = 2
            st.rerun()

# STEP 2: MBTI summary
elif st.session_state.step == 2:
    st.title("🌟 ขั้นตอนที่ 2: สรุปผลลัพธ์และแบบจำลองตรรกศาสตร์ MBTI")
    mbti = st.session_state.mbti_result
    info = MBTI_DESCRIPTIONS.get(mbti, MBTI_DESCRIPTIONS["INTJ"])
    sorted_funcs = st.session_state.get("sorted_funcs", [])
    func_pct = st.session_state.get("func_percentages", {})
    stack = st.session_state.get("mbti_stack", {})
    st.success(f"### ผลการวิเคราะห์ MBTI: **{mbti}** ({info['title']})")
    st.info(f"**ลักษณะตัวตน:** {info['desc']}")
    c1, c2 = st.columns([3, 2])
    with c1:
        for func, score in sorted_funcs:
            pct = func_pct.get(func, 0)
            st.write(f"**{func}**: {score}/50 คะแนน ({pct}%)")
            st.progress(pct / 100)
    with c2:
        if stack:
            st.write(f"🥇 Dominant: `{stack['Dom']}`")
            st.write(f"🥈 Auxiliary: `{stack['Aux']}`")
            st.write(f"🥉 Tertiary: `{stack['Tert']}`")
            st.write(f"⚓ Inferior: `{stack['Inf']}`")
    with st.expander("📚 ดูตรรกศาสตร์การคำนวณระดับ ม.4"):
        st.latex(r"\text{Dom}=A \iff \forall f\,(\text{Score}(A)\ge\text{Score}(f))")
        st.latex(r"\text{Dom}=Ne \Rightarrow \text{Aux}\in\{Ti,Fi\}")
        st.latex(r"\text{Dom}=Ne \iff \text{Inferior}=Si")
    if st.button("➡️ ไปต่อ: ประเมินความชอบ 5 หมวดหมู่ (Step 3)"):
        st.session_state.step = 3
        st.rerun()

# STEP 3: category assessment
elif st.session_state.step == 3:
    st.title("📚 ขั้นตอนที่ 3: ประเมินความชอบและศักยภาพ 5 หมวดหมู่")
    st.write("กรุณาทำแบบประเมินให้ครบทุกหมวด เพื่อนำไปสร้างประพจน์คณะ")
    question_sets = [
        ("📖 วิชาความรู้", SUBJECT_QUESTIONS, "sub"),
        ("🎨 งานอดิเรกและความสนใจ", HOBBY_QUESTIONS, "hobby"),
        ("🎯 เป้าหมายอาชีพและค่านิยม", GOAL_QUESTIONS, "goal"),
        ("💰 การบริหารและการเงิน", FINANCIAL_QUESTIONS, "fin"),
    ]
    with st.form("all_categories_form"):
        category_scores = {}
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
                st.markdown(f"**ข้อที่ {idx}:** {text} *(หมวด: {category})*")
                if options and isinstance(options, list):
                    answer = st.radio(f"เลือกคำตอบ ({q_id}):", options, index=0, key=f"{prefix}_{q_id}")
                    score = (options.index(answer) + 1) * (5 / len(options))
                else:
                    answer = st.radio(f"ระดับความตรง ({q_id}):", list(SCALE_OPTIONS.keys()), index=2, key=f"{prefix}_{q_id}", horizontal=True)
                    score = SCALE_OPTIONS[answer]
                category_scores[category] = category_scores.get(category, 0) + score
        if st.form_submit_button("🚀 บันทึกผลและไปประเมินเงินทุน (Step 4)"):
            st.session_state.category_scores = category_scores
            st.session_state.step = 4
            st.rerun()

# STEP 4: funding_step.py
elif st.session_state.step == 4:
    st.title("💰 ขั้นตอนที่ 4: ประเมินเงินทุน")
    render_funding_step(next_step=5)

# STEP 5: final summary
elif st.session_state.step == 5:
    st.title("🏆 ขั้นตอนที่ 5: สรุปผลการวิเคราะห์ทั้งหมด")
    mbti = st.session_state.get("mbti_result", "INTJ")
    category_scores = st.session_state.get("category_scores", {})
    funding_level = st.session_state.get("funding_level")
    funding_average = st.session_state.get("funding_average")
    funding_proposition = st.session_state.get("funding_proposition")

    if not funding_proposition:
        st.warning("ยังไม่มีผลประเมินเงินทุน กรุณาทำ Step 4 ก่อน")
        if st.button("⬅️ กลับไป Step 4"):
            st.session_state.step = 4
            st.rerun()
    else:
        st.success(f"MBTI ของคุณ: **{mbti}**")
        st.subheader("💰 สรุปประพจน์เงินทุน")
        c1, c2, c3 = st.columns(3)
        c1.metric("คะแนนเฉลี่ย", f"{funding_average:.2f}/5")
        c2.metric("ระดับเงินทุน", funding_level.upper())
        c3.metric("ประพจน์ทุน", funding_proposition)

        st.markdown("---")
        st.subheader("🧠 สรุปประพจน์คณะ")
        faculty_results = get_faculty_results(mbti, category_scores)
        true_faculties = [(prop, result) for prop, result in faculty_results.items() if result["value"]]
        if true_faculties:
            for prop, result in true_faculties:
                st.success(f"**{prop}** = TRUE → {result['name']}")
                st.caption(f"MBTI = {result['mbti_ok']} | ความสนใจ/ศักยภาพ = {result['interest_ok']}")
        else:
            st.warning("ยังไม่พบประพจน์คณะที่เป็น TRUE จาก MBTI และคะแนนความสนใจ")

        st.markdown("---")
        st.subheader("🔗 สรุปตรรกศาสตร์สุดท้าย: คณะ ∧ เงินทุน")
        st.write("นำประพจน์คณะที่เป็น TRUE มาเชื่อมกับประพจน์เงินทุนด้วย AND (∧) แล้วค้นหามหาวิทยาลัยจาก UNIVERSITY_RULES")
        render_university_result(mbti, category_scores)

        st.markdown("---")
        if st.button("🔄 เริ่มทำแบบประเมินใหม่ทั้งหมด"):
            st.session_state.clear()
            st.rerun()

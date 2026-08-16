import streamlit as st
from funding_university import (
    FUNDING_QUESTIONS, FUNDING_OPTIONS, FUNDING_PROPOSITIONS,
    UNIVERSITY_RULES, get_faculty_results, funding_level_from_average,
)


def render_funding_step(next_step=4):
    """แสดงแบบประเมินเงินทุน แล้วแสดงหน้าสรุปผลพร้อมปุ่มไปต่อ"""
    # ---------------------------------------------------------
    # STEP 4A: Funding questionnaire
    # ---------------------------------------------------------
    if not st.session_state.get("funding_summary_ready", False):
        st.title("💰 แบบประเมินความพร้อมด้านเงินทุนเพื่อการเรียนต่อ")
        st.write("ตอบคำถามเพื่อจัดระดับเงินทุนเป็น สูง / กลาง / ต่ำ")

        with st.form("funding_form"):
            scores = []
            for index, question in enumerate(FUNDING_QUESTIONS, 1):
                answer = st.radio(
                    f"ข้อ {index}: {question['text']}",
                    options=list(FUNDING_OPTIONS.keys()),
                    index=2,
                    key=question["id"],
                    horizontal=True,
                )
                scores.append(FUNDING_OPTIONS[answer])

            submitted = st.form_submit_button("🚀 สรุปผลเงินทุน")

        if submitted:
            average = sum(scores) / len(scores)
            level = funding_level_from_average(average)
            proposition = FUNDING_PROPOSITIONS[level]

            st.session_state.funding_scores = scores
            st.session_state.funding_average = average
            st.session_state.funding_level = level
            st.session_state.funding_proposition = proposition
            st.session_state.funding_summary_ready = True
            st.rerun()

        return

    # ---------------------------------------------------------
    # STEP 4B: Full funding summary
    # ---------------------------------------------------------
    scores = st.session_state.get("funding_scores", [])
    average = st.session_state.get("funding_average", 0)
    level = st.session_state.get("funding_level", "")
    proposition = st.session_state.get("funding_proposition", "")

    level_display = {
        "high": "สูง (HIGH)",
        "mid": "กลาง (MID)",
        "low": "ต่ำ (LOW)",
    }.get(str(level).lower(), str(level).upper())

    st.title("📊 สรุปผลการประเมินเงินทุน")
    st.success("🎉 ประเมินความพร้อมด้านเงินทุนเสร็จเรียบร้อยแล้ว")

    # Main metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("คะแนนเฉลี่ย", f"{average:.2f} / 5")
    with col2:
        st.metric("ระดับเงินทุน", level_display)
    with col3:
        st.metric("ประพจน์เงินทุน", proposition)

    st.markdown("---")

    st.subheader("🧠 สรุปในรูปแบบตรรกศาสตร์")
    st.markdown(
        f"**ประพจน์เงินทุน:** `{proposition}`  "
        f"\n\nหมายความว่า ผู้ประเมินมีระดับความพร้อมด้านเงินทุนอยู่ในระดับ **{level_display}** "
        f"จากคะแนนเฉลี่ย **{average:.2f}/5**"
    )

    with st.expander("📋 ดูรายละเอียดคะแนนรายข้อ"):
        for index, score in enumerate(scores, 1):
            st.write(f"ข้อ {index}: **{score:g} / 5**")
            st.progress(min(max(score / 5, 0.0), 1.0))

    st.info(
        "ขั้นตอนถัดไป ระบบจะนำประพจน์เงินทุนนี้ไปเชื่อมกับประพจน์คณะด้วยตัวเชื่อมตรรกศาสตร์ **AND (∧)** "
        "เพื่อค้นหาผลลัพธ์มหาวิทยาลัยตามกฎของโปรเจกต์"
    )

    if st.button("➡️ ไปต่อ: สรุปผลคณะและมหาวิทยาลัย", type="primary"):
        st.session_state.funding_summary_ready = False
        st.session_state.step = next_step
        st.rerun()


def render_university_result(mbti, category_scores):
    """เชื่อมประพจน์คณะ AND ประพจน์ทุน แล้วแสดงมหาวิทยาลัย"""
    faculty_results = get_faculty_results(mbti, category_scores)
    funding_proposition = st.session_state.get("funding_proposition")
    funding_level = st.session_state.get("funding_level")
    average = st.session_state.get("funding_average", 0)

    if not funding_proposition:
        st.warning("กรุณาทำแบบประเมินเงินทุนก่อน")
        return

    st.subheader("🔗 การเชื่อมประพจน์ด้วย AND")
    st.write(
        f"ประพจน์ทุน = **{funding_proposition}** → "
        f"ระดับ **{str(funding_level).upper()}** (เฉลี่ย {average:.2f}/5)"
    )

    matched = []
    for faculty_prop, result in faculty_results.items():
        if result["value"]:
            final_prop = f"{faculty_prop} ∧ {funding_proposition}"
            university = UNIVERSITY_RULES.get((faculty_prop, funding_proposition))
            if university:
                matched.append((faculty_prop, result["name"], final_prop, university))

    if matched:
        st.success("พบผลลัพธ์จากการเชื่อมประพจน์คณะ AND เงินทุน")
        for faculty_prop, faculty_name, final_prop, university in matched:
            st.markdown(f"### 🏫 {university}")
            st.write(f"คณะ: **{faculty_name}**")
            st.code(f"{final_prop} → {university}")
    else:
        st.warning("ยังไม่พบมหาวิทยาลัยที่ตรงทั้งประพจน์คณะและประพจน์เงินทุน")

    st.caption(
        "หมายเหตุ: รายชื่อมหาวิทยาลัยในตารางนี้เป็นกฎตัวอย่างสำหรับโปรเจกต์ตรรกศาสตร์ "
        "ไม่ใช่เกณฑ์รับเข้าหรือการรับรองทุนจริง"
    )

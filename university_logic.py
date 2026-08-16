"""Faculty -> funding -> university proposition rules.

Faculty propositions use F01..F10 and never reuse P/Q/R/S/T from the old
interest propositions. Funding uses B_H/B_M/B_L. University propositions use
U01..U30. A university result is produced only when FACULTY ∧ FUNDING is true.
"""

FACULTY_RULES = [
    {"id": "F01", "faculty": "วิศวกรรมศาสตร์ / เทคโนโลยีสารสนเทศ", "mbti": {"INTJ", "INTP", "ENTP", "ISTP"}, "needs": ("tech", "math_or_business")},
    {"id": "F02", "faculty": "วิทยาการข้อมูล / ปัญญาประดิษฐ์ / สถิติ", "mbti": {"INTJ", "INTP", "ISTJ", "ENTP"}, "needs": ("math", "tech")},
    {"id": "F03", "faculty": "แพทยศาสตร์ / เภสัชศาสตร์ / สหเวชศาสตร์", "mbti": {"INFJ", "INTJ", "ISFJ", "ENFJ"}, "needs": ("math", "social")},
    {"id": "F04", "faculty": "บริหารธุรกิจ / เศรษฐศาสตร์ / การบัญชีและการเงิน", "mbti": {"ENTJ", "ESTJ", "ESTP", "ENTP"}, "needs": ("business",)},
    {"id": "F05", "faculty": "การตลาด / การขาย / พาณิชย์อิเล็กทรอนิกส์", "mbti": {"ENTP", "ENFP", "ESTP", "ESFP"}, "needs": ("business_or_art", "social")},
    {"id": "F06", "faculty": "ศิลปกรรมศาสตร์ / UX-UI / สื่อดิจิทัล", "mbti": {"INFP", "ISFP", "ENFP", "ENTP"}, "needs": ("art",)},
    {"id": "F07", "faculty": "สถาปัตยกรรมศาสตร์ / ออกแบบผลิตภัณฑ์", "mbti": {"INTJ", "ENTP", "ISFP", "ISTP"}, "needs": ("art", "math_or_tech")},
    {"id": "F08", "faculty": "นิติศาสตร์ / รัฐศาสตร์ / รัฐประศาสนศาสตร์", "mbti": {"ISTJ", "ESTJ", "INTJ", "ENFJ"}, "needs": ("social",)},
    {"id": "F09", "faculty": "ครุศาสตร์ / ศึกษาศาสตร์ / การฝึกอบรม", "mbti": {"ENFJ", "ESFJ", "INFJ", "ISFJ"}, "needs": ("social",)},
    {"id": "F10", "faculty": "มนุษยศาสตร์ / ภาษา / การแปล / ความสัมพันธ์ระหว่างประเทศ", "mbti": {"INFJ", "INFP", "ENFP", "ENFJ"}, "needs": ("social", "art_or_business")},
]

UNIVERSITY_RULES = [
    {"id": "U01", "name": "จุฬาลงกรณ์มหาวิทยาลัย", "faculty_ids": {"F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10"}, "funding": "สูง"},
    {"id": "U02", "name": "มหาวิทยาลัยมหิดล", "faculty_ids": {"F02", "F03", "F06", "F09", "F10"}, "funding": "สูง"},
    {"id": "U03", "name": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี", "faculty_ids": {"F01", "F02", "F07"}, "funding": "สูง"},
    {"id": "U04", "name": "สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง", "faculty_ids": {"F01", "F02", "F06", "F07"}, "funding": "กลาง"},
    {"id": "U05", "name": "มหาวิทยาลัยเชียงใหม่", "faculty_ids": {"F01", "F02", "F03", "F04", "F06", "F07", "F08", "F09", "F10"}, "funding": "กลาง"},
    {"id": "U06", "name": "มหาวิทยาลัยขอนแก่น", "faculty_ids": {"F01", "F02", "F03", "F04", "F08", "F09", "F10"}, "funding": "กลาง"},
    {"id": "U07", "name": "มหาวิทยาลัยสงขลานครินทร์", "faculty_ids": {"F01", "F02", "F03", "F04", "F08", "F09", "F10"}, "funding": "กลาง"},
    {"id": "U08", "name": "มหาวิทยาลัยรามคำแหง", "faculty_ids": {"F04", "F05", "F08", "F09", "F10"}, "funding": "ต่ำ"},
    {"id": "U09", "name": "มหาวิทยาลัยสุโขทัยธรรมาธิราช", "faculty_ids": {"F04", "F05", "F08", "F09", "F10"}, "funding": "ต่ำ"},
    {"id": "U10", "name": "มหาวิทยาลัยราชภัฏ", "faculty_ids": {"F04", "F05", "F08", "F09", "F10"}, "funding": "ต่ำ"},
]

FUNDING_SYMBOLS = {"สูง": "B_H", "กลาง": "B_M", "ต่ำ": "B_L"}


def evaluate_faculty(rule: dict, mbti: str, interests: dict) -> bool:
    if mbti not in rule["mbti"]:
        return False
    for need in rule["needs"]:
        if need == "tech" and not interests["tech"]:
            return False
        if need == "math" and not interests["math"]:
            return False
        if need == "social" and not interests["social"]:
            return False
        if need == "business" and not interests["business"]:
            return False
        if need == "art" and not interests["art"]:
            return False
        if need == "math_or_business" and not (interests["math"] or interests["business"]):
            return False
        if need == "math_or_tech" and not (interests["math"] or interests["tech"]):
            return False
        if need == "business_or_art" and not (interests["business"] or interests["art"]):
            return False
        if need == "art_or_business" and not (interests["art"] or interests["business"]):
            return False
    return True


def build_faculty_results(mbti: str, interests: dict) -> list[dict]:
    return [
        {**rule, "proposition": rule["id"], "true": evaluate_faculty(rule, mbti, interests)}
        for rule in FACULTY_RULES
    ]


def build_university_results(faculty_results: list[dict], funding_level: str) -> list[dict]:
    matched_ids = {item["id"] for item in faculty_results if item["true"]}
    funding_symbol = FUNDING_SYMBOLS[funding_level]
    results = []
    for university in UNIVERSITY_RULES:
        faculty_ids = sorted(matched_ids.intersection(university["faculty_ids"]))
        if faculty_ids and university["funding"] == funding_level:
            for faculty_id in faculty_ids:
                results.append({
                    **university,
                    "faculty_id": faculty_id,
                    "proposition": university["id"],
                    "logic": f"{faculty_id} ∧ {funding_symbol}",
                    "true": True,
                })
    return results

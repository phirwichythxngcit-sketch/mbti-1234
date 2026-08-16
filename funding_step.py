"""Funding assessment and proposition helpers.

This module deliberately gives funding propositions their own namespace so they
cannot collide with the existing faculty propositions P/Q/R/S/T.
"""

FUNDING_QUESTIONS = [
    {"id": "fund_01", "text": "ครอบครัว/ผู้สนับสนุนสามารถรับผิดชอบค่าเล่าเรียนได้ในระดับสูง", "weight": 1},
    {"id": "fund_02", "text": "สามารถรับค่าใช้จ่ายด้านที่พัก อุปกรณ์ และการเดินทางเพื่อเรียนต่อได้", "weight": 1},
    {"id": "fund_03", "text": "มีเงินสำรองสำหรับค่าใช้จ่ายฉุกเฉินระหว่างเรียน", "weight": 1},
    {"id": "fund_04", "text": "สามารถเลือกมหาวิทยาลัยที่มีค่าใช้จ่ายสูงขึ้นได้หากตรงกับคณะที่ต้องการ", "weight": 1},
    {"id": "fund_05", "text": "มีแผนหรือแหล่งทุน เช่น ทุนการศึกษา กยศ. หรือทุนจากมหาวิทยาลัย", "weight": 1},
    {"id": "fund_06", "text": "สามารถหารายได้เสริม/ทำงานพิเศษโดยไม่กระทบการเรียนมากเกินไป", "weight": 1},
    {"id": "fund_07", "text": "มีความยืดหยุ่นในการเลือกมหาวิทยาลัยโดยพิจารณาค่าใช้จ่ายเป็นหลัก", "weight": 1},
    {"id": "fund_08", "text": "พร้อมวางแผนงบประมาณรายเดือนสำหรับการเรียนต่ออย่างจริงจัง", "weight": 1},
    {"id": "fund_09", "text": "หากค่าใช้จ่ายสูงขึ้น สามารถปรับแผนหรือหาแหล่งเงินทุนเพิ่มเติมได้", "weight": 1},
    {"id": "fund_10", "text": "มีเงินทุน/ทุนการศึกษาที่คาดว่าจะได้รับสำหรับการเรียนต่อ", "weight": 1},
]

FUNDING_SCALE = {
    "1 - ไม่พร้อมเลย": 1,
    "2 - พร้อมน้อย": 2,
    "3 - ปานกลาง": 3,
    "4 - พร้อมมาก": 4,
    "5 - พร้อมมากที่สุด": 5,
}

# Unique propositions: F is reserved for faculty, B for budget/funding.
FUNDING_PROPOSITIONS = {
    "สูง": {"symbol": "B_H", "description": "มีศักยภาพด้านเงินทุนสูง"},
    "กลาง": {"symbol": "B_M", "description": "มีศักยภาพด้านเงินทุนระดับกลาง"},
    "ต่ำ": {"symbol": "B_L", "description": "มีศักยภาพด้านเงินทุนต่ำ"},
}


def classify_funding(score: float, max_score: float) -> str:
    """Classify funding capacity into สูง/กลาง/ต่ำ using normalized score."""
    if max_score <= 0:
        return "ต่ำ"
    percent = score / max_score
    if percent >= 0.67:
        return "สูง"
    if percent >= 0.45:
        return "กลาง"
    return "ต่ำ"


def funding_result(score: float, max_score: float) -> dict:
    level = classify_funding(score, max_score)
    proposition = FUNDING_PROPOSITIONS[level]
    return {
        "score": round(score, 2),
        "max_score": round(max_score, 2),
        "percent": round((score / max_score) * 100, 1) if max_score else 0.0,
        "level": level,
        "symbol": proposition["symbol"],
        "description": proposition["description"],
    }

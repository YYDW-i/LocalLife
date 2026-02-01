from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


def bmi(weight_kg: float, height_cm: float) -> float:
    h_m = height_cm / 100.0
    return weight_kg / (h_m * h_m)


def bmi_category_adult(bmi_value: float) -> str:
    # WHO 常见成人阈值：<18.5 偏瘦；18.5-24.9 正常；25-29.9 超重；>=30 肥胖
    if bmi_value < 18.5:
        return "偏瘦"
    if bmi_value < 25:
        return "正常"
    if bmi_value < 30:
        return "超重"
    return "肥胖"


def mifflin_st_jeor_bmr(weight_kg: float, height_cm: float, age_years: int, sex: str) -> Optional[float]:
    # Mifflin-St Jeor：
    # 男：10w + 6.25h - 5a + 5
    # 女：10w + 6.25h - 5a - 161
    # sex 若未知就返回 None
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age_years
    if sex == "male":
        return base + 5
    if sex == "female":
        return base - 161
    return None


def activity_factor(level: str) -> float:
    # 常见活动系数（用于 TDEE = BMR * factor）
    return {
        "sedentary": 1.2,      # 久坐
        "light": 1.375,        # 轻度
        "moderate": 1.55,      # 中度
        "active": 1.725,       # 高度
        "very_active": 1.9,    # 极高
    }.get(level, 1.2)

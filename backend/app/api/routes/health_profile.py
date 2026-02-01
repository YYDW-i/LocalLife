from __future__ import annotations

from fastapi import APIRouter, HTTPException
import sqlite3

from app.db.connection import get_conn  # 你项目里如果函数名不同，把这里改成你已有的连接函数
from app.core.time import now_iso
from app.services.health_calc import bmi, bmi_category_adult, mifflin_st_jeor_bmr, activity_factor

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("/profile")
def get_profile():
    conn: sqlite3.Connection = get_conn()
    row = conn.execute(
        "SELECT id, height_cm, weight_kg, age_years, sex, activity_level, updated_at FROM health_profile WHERE id=1"
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=500, detail="health_profile missing")
    return dict(row)


@router.put("/profile")
def upsert_profile(payload: dict):
    # 允许字段：height_cm, weight_kg, age_years, sex, activity_level
    height_cm = payload.get("height_cm")
    weight_kg = payload.get("weight_kg")
    age_years = payload.get("age_years")
    sex = payload.get("sex", "unspecified")
    activity_level = payload.get("activity_level", "sedentary")

    if sex not in ("male", "female", "unspecified"):
        raise HTTPException(status_code=400, detail="sex must be male/female/unspecified")

    conn: sqlite3.Connection = get_conn()
    conn.execute(
        """
        UPDATE health_profile
        SET height_cm=?, weight_kg=?, age_years=?, sex=?, activity_level=?, updated_at=?
        WHERE id=1
        """,
        (height_cm, weight_kg, age_years, sex, activity_level, now_iso()),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@router.get("/summary")
async def get_summary():
    conn = get_conn()

    # 获取用户健康数据
    row = conn.execute(
        "SELECT height_cm, weight_kg, age_years, sex, activity_level FROM health_profile WHERE id=1"
    ).fetchone()

    if row is None:
        return {"error": "No health profile found"}

    # 获取BMI
    height_m = row[0] / 100  # 转换为米
    weight_kg = row[1]
    bmi = weight_kg / (height_m ** 2)

    # 基础代谢率 BMR (Mifflin-St Jeor Equation)
    # 男性: BMR = 10 * 体重(kg) + 6.25 * 身高(cm) - 5 * 年龄 + 5
    # 女性: BMR = 10 * 体重(kg) + 6.25 * 身高(cm) - 5 * 年龄 - 161
    age_years = row[2]
    sex = row[3]

    if sex == "male":
        bmr = 10 * weight_kg + 6.25 * row[0] - 5 * age_years + 5
    else:
        bmr = 10 * weight_kg + 6.25 * row[0] - 5 * age_years - 161

    # 总日消耗能量 TDEE (TDEE = BMR * 活动因子)
    activity_level = row[4]  # 活动级别（例如：low, moderate, high）
    activity_factor = {
        "low": 1.2,
        "moderate": 1.55,
        "high": 1.9
    }
    tdee = bmr * activity_factor.get(activity_level, 1.2)

    # 生成健康建议
    health_advice = generate_health_advice(bmi, bmr, tdee)

    return {
        "bmi": round(bmi, 2),
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
        "health_advice": health_advice
    }

# 根据 BMI, BMR 和 TDEE 生成健康建议
def generate_health_advice(bmi, bmr, tdee):
    if bmi < 18.5:
        advice = "您的体重过轻，建议增加营养摄入，均衡饮食，并进行适度的锻炼。"
    elif 18.5 <= bmi < 24.9:
        advice = "您的体重正常，保持健康饮食和规律运动即可。"
    elif 25 <= bmi < 29.9:
        advice = "您的体重偏重，建议通过健康饮食和有氧运动减重。"
    else:
        advice = "您的体重过重，建议制定减肥计划，结合饮食和运动降低体重。"

    if bmr < 1800:
        advice += " 另外，您的基础代谢率较低，可以考虑增加高蛋白食物的摄入。"
    
    if tdee > 2500:
        advice += " 您的日常活动量较大，请确保摄入足够的能量来维持健康。"

    return advice
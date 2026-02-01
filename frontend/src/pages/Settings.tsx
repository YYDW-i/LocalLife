import React, { useEffect, useState } from "react";
import { apiGet, apiPut } from "../api/http";

type Profile = {
  id: number;
  height_cm: number | null;
  weight_kg: number | null;
  age_years: number | null;
  sex: "male" | "female" | "unspecified";
  activity_level: "sedentary" | "light" | "moderate" | "active" | "very_active";
  updated_at: string;
};

export default function Settings() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  useEffect(() => {
    apiGet<Profile>("/api/health/profile")
      .then(setProfile)
      .catch((e) => setMsg(String(e)));
  }, []);

  async function save() {
    if (!profile) return;
    setSaving(true);
    setMsg(null);
    try {
      await apiPut<{ ok: boolean }>("/api/health/profile", {
        height_cm: profile.height_cm,
        weight_kg: profile.weight_kg,
        age_years: profile.age_years,
        sex: profile.sex,
        activity_level: profile.activity_level,
      });
      setMsg("已保存 ✅");
    } catch (e) {
      setMsg(`保存失败：${String(e)}`);
    } finally {
      setSaving(false);
    }
  }

  if (!profile) return <div className="glass" style={{ padding: 16 }}>加载中… {msg}</div>;

  return (
    <div className="glass" style={{ padding: 16 }}>
      <h2>设置</h2>

      <div className="glass" style={{ padding: 16, marginTop: 12 }}>
        <h3>健康资料（手动输入）</h3>
        <p style={{ opacity: 0.8 }}>
          本地存储，仅用于计算 BMI / 基础代谢（估算）/ 日消耗（估算）。
        </p>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(220px, 1fr))", gap: 12 }}>
          <label>
            身高(cm)
            <input
              value={profile.height_cm ?? ""}
              onChange={(e) => setProfile({ ...profile, height_cm: e.target.value === "" ? null : Number(e.target.value) })}
              style={{ width: "100%" }}
              placeholder="例如 170"
            />
          </label>

          <label>
            体重(kg)
            <input
              value={profile.weight_kg ?? ""}
              onChange={(e) => setProfile({ ...profile, weight_kg: e.target.value === "" ? null : Number(e.target.value) })}
              style={{ width: "100%" }}
              placeholder="例如 60"
            />
          </label>

          <label>
            年龄(岁)
            <input
              value={profile.age_years ?? ""}
              onChange={(e) => setProfile({ ...profile, age_years: e.target.value === "" ? null : Number(e.target.value) })}
              style={{ width: "100%" }}
              placeholder="例如 22"
            />
          </label>

          <label>
            生理性别（用于代谢公式，可选）
            <select
              value={profile.sex}
              onChange={(e) => setProfile({ ...profile, sex: e.target.value as Profile["sex"] })}
              style={{ width: "100%" }}
            >
              <option value="unspecified">不填</option>
              <option value="male">男</option>
              <option value="female">女</option>
            </select>
          </label>

          <label style={{ gridColumn: "1 / -1" }}>
            活动水平
            <select
              value={profile.activity_level}
              onChange={(e) => setProfile({ ...profile, activity_level: e.target.value as Profile["activity_level"] })}
              style={{ width: "100%" }}
            >
              <option value="sedentary">久坐（几乎不运动）</option>
              <option value="light">轻度（每周 1–3 次）</option>
              <option value="moderate">中度（每周 3–5 次）</option>
              <option value="active">高度（每周 6–7 次）</option>
              <option value="very_active">极高（高强度体力/训练）</option>
            </select>
          </label>
        </div>

        <div style={{ marginTop: 12, display: "flex", gap: 12, alignItems: "center" }}>
          <button onClick={save} disabled={saving}>
            {saving ? "保存中…" : "保存"}
          </button>
          {msg && <span style={{ opacity: 0.9 }}>{msg}</span>}
        </div>
      </div>
    </div>
  );
}

import React, { useEffect, useState } from "react";
import { apiGet } from "../api/http";

type HealthCheck = { status: string; version: string };

type Summary = {
  has_profile: boolean;
  bmi: number | null;
  bmi_category: string | null;
  bmr: number | null;
  tdee: number | null;
  activity_level: string;
  note: string | null;
};

export default function Dashboard() {
  const [health, setHealth] = useState<HealthCheck | null>(null);
  const [summary, setSummary] = useState<Summary | null>(null);

  // 获取健康检查和健康摘要数据
  useEffect(() => {
    apiGet<HealthCheck>("/api/health").then(setHealth).catch(() => setHealth(null));
    apiGet<Summary>("/api/health/summary").then(setSummary).catch(() => setSummary(null));
  }, []);

  // 健康建议的生成（基于BMI分类）
  const generateHealthAdvice = (summary: Summary) => {
    if (!summary.bmi) return "没有足够数据生成建议";

    if (summary.bmi < 18.5) {
      return "您的BMI偏低，建议增加营养，保持均衡饮食。";
    } else if (summary.bmi >= 18.5 && summary.bmi < 24.9) {
      return "您的BMI正常，继续保持健康的生活方式。";
    } else if (summary.bmi >= 25 && summary.bmi < 29.9) {
      return "您的BMI偏高，建议适度增加运动，并注意饮食控制。";
    } else {
      return "您的BMI过高，建议咨询医生并制定适合的减重计划。";
    }
  };

  return (
    <div style={{ padding: 16 }}>
      {/* 健康状态显示 */}
      <div className="glass" style={{ padding: 16, marginBottom: 12 }}>
        <h2>健康状态</h2>
        {health ? (
          <>
            <div>API: {health.status}</div>
            <div>Version: {health.version}</div>
          </>
        ) : (
          <div>健康检查中…</div>
        )}
      </div>

      {/* 健康摘要显示 */}
      <div className="glass" style={{ padding: 16 }}>
        <h2>健康摘要（本地手动输入）</h2>
        {!summary ? (
          <div>加载中…</div>
        ) : !summary.has_profile ? (
          <div>
            <div>{summary.note ?? "请先去 Settings 填写身高/体重"}</div>
          </div>
        ) : (
          <>
            <div>BMI: {summary.bmi}（{summary.bmi_category}）</div>
            <div style={{ marginTop: 8 }}>
              {summary.bmr ? <div>BMR（基础代谢估算）: {summary.bmr} kcal/天</div> : <div>BMR: 暂无（需要年龄+性别）</div>}
              {summary.tdee ? <div>TDEE（日消耗估算）: {summary.tdee} kcal/天</div> : <div>TDEE: 暂无</div>}
            </div>
            {summary.note && <div style={{ marginTop: 8, opacity: 0.85 }}>提示：{summary.note}</div>}

            {/* 添加健康建议 */}
            <div style={{ marginTop: 16, opacity: 0.85 }}>
              <strong>健康建议：</strong>
              <p>{generateHealthAdvice(summary)}</p>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

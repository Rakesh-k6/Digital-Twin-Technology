import React from 'react';

export default function PredictorPanel({ predictionData, onApplyMitigation }) {
  const predictions = predictionData?.predictions || [];
  const risk = predictionData?.overall_system_risk || 'LOW';
  const horizon = predictionData?.prediction_horizon_min || 20;

  return (
    <div className="glass-panel" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: 6 }}>
            <span>🔮</span> AI Cascade Predictive Engine
          </h3>
          <span style={{ fontSize: 11, color: '#94a3b8' }}>Target Horizon: {horizon} Simulated Minutes</span>
        </div>
        <button
          onClick={onApplyMitigation}
          style={{
            background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            color: '#fff',
            border: 'none',
            padding: '6px 14px',
            borderRadius: 6,
            fontWeight: 700,
            fontSize: 12,
            cursor: 'pointer',
            boxShadow: '0 0 14px rgba(16, 185, 129, 0.4)'
          }}
        >
          ⚡ Apply Recommended Mitigation
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {predictions.map((p, idx) => {
          const isCritical = p.risk_level === 'CRITICAL';
          const isHigh = p.risk_level === 'HIGH';

          return (
            <div
              key={idx}
              style={{
                background: isCritical ? 'rgba(239, 68, 68, 0.12)' : (isHigh ? 'rgba(245, 158, 11, 0.10)' : 'rgba(15, 23, 42, 0.6)'),
                border: `1px solid ${isCritical ? '#ef4444' : (isHigh ? '#f59e0b' : '#334155')}`,
                borderRadius: 8,
                padding: '10px 12px',
                display: 'flex',
                flexDirection: 'column',
                gap: 6
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontWeight: 700, fontSize: 13, color: '#f8fafc' }}>{p.incident}</span>
                <span
                  style={{
                    fontSize: 10,
                    fontWeight: 700,
                    padding: '2px 8px',
                    borderRadius: 4,
                    background: isCritical ? '#ef4444' : (isHigh ? '#f59e0b' : '#10b981'),
                    color: '#000'
                  }}
                >
                  {p.risk_level}
                </span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6, fontSize: 11 }}>
                <div>
                  <span style={{ color: '#94a3b8' }}>Time to Overload: </span>
                  <span style={{ color: '#f1f5f9', fontWeight: 600 }}>{p.expected_time_to_incident}</span>
                </div>
                <div>
                  <span style={{ color: '#94a3b8' }}>Affected: </span>
                  <span style={{ color: '#38bdf8', fontWeight: 600 }}>{p.zone}</span>
                </div>
              </div>

              <div style={{ fontSize: 11, color: '#cbd5e1' }}>
                <span style={{ color: '#94a3b8' }}>Root Cause: </span>
                {p.root_cause}
              </div>

              <div style={{ fontSize: 11, color: '#34d399', background: 'rgba(16, 185, 129, 0.1)', padding: '4px 8px', borderRadius: 4 }}>
                <span style={{ fontWeight: 700 }}>AI Action: </span>
                {p.recommended_action}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

import React from 'react';

export default function CyberSecurityPanel({ securityData, onInjectAttack, onClearAttacks }) {
  const activeAttacks = securityData?.active_attacks || [];
  const incidentLog = securityData?.incident_log || [];
  const threatLevel = securityData?.system_threat_level || 'NOMINAL';

  return (
    <div className="glass-panel" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: 6 }}>
            <span>🛡</span> Cyber Security Operations Center (CSOC)
          </h3>
          <span style={{ fontSize: 11, color: '#94a3b8' }}>Physics-Informed Residual Anomaly Detection Engine</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span
            style={{
              fontSize: 11,
              fontWeight: 700,
              padding: '3px 8px',
              borderRadius: 4,
              background: threatLevel === 'ELEVATED' ? 'rgba(239, 68, 68, 0.25)' : 'rgba(16, 185, 129, 0.2)',
              color: threatLevel === 'ELEVATED' ? '#ef4444' : '#10b981',
              border: `1px solid ${threatLevel === 'ELEVATED' ? '#ef4444' : '#10b981'}`
            }}
          >
            {threatLevel}
          </span>
        </div>
      </div>

      {/* Attack Injection Controls */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
        <button
          onClick={() => onInjectAttack('fdi_power', 'FEEDER_SLK', 5.5)}
          className="btn-danger"
          style={{ fontSize: 11, padding: '6px 10px' }}
        >
          Inject FDI (Feeder F-SLK)
        </button>
        <button
          onClick={() => onInjectAttack('traffic_sensor_spoof', 'Zone_D', 0.1)}
          className="btn-danger"
          style={{ fontSize: 11, padding: '6px 10px' }}
        >
          Spoof Traffic Loop (Zone D)
        </button>
        <button
          onClick={() => onInjectAttack('signal_tampering', 'INT_SLK_2')}
          className="btn-danger"
          style={{ fontSize: 11, padding: '6px 10px' }}
        >
          Tamper Signal (INT_SLK_2)
        </button>
        <button
          onClick={onClearAttacks}
          className="btn-primary"
          style={{ fontSize: 11, padding: '6px 10px' }}
        >
          Neutralize & Resync Defenses
        </button>
      </div>

      {/* Incident Log Terminal */}
      <div
        style={{
          background: 'rgba(5, 8, 15, 0.85)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          borderRadius: 8,
          padding: '10px 12px',
          maxHeight: 140,
          overflowY: 'auto',
          fontSize: 11,
          fontFamily: 'JetBrains Mono, monospace'
        }}
      >
        <div style={{ color: '#64748b', marginBottom: 6, fontSize: 10 }}>[SECURITY LOG STREAM]</div>
        {incidentLog.length === 0 ? (
          <div style={{ color: '#10b981' }}>✔ No security anomalies detected. Telemetry integrity verified.</div>
        ) : (
          incidentLog.slice().reverse().map((item, idx) => (
            <div key={idx} style={{ marginBottom: 4, lineHeight: 1.4 }}>
              <span style={{ color: '#64748b' }}>[{item.timestamp}] </span>
              <span style={{ color: item.severity === 'CRITICAL' ? '#ef4444' : (item.severity === 'HIGH' ? '#f59e0b' : '#38bdf8'), fontWeight: 600 }}>
                [{item.severity}]
              </span>{' '}
              <span style={{ color: '#f1f5f9' }}>{item.title}</span>
              <div style={{ color: '#94a3b8', fontSize: 10, paddingLeft: 10 }}>{item.details}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

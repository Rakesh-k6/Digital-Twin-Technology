import React from 'react';

export default function MitigationModal({ data, onClose }) {
  if (!data) return null;

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.75)',
        backdropFilter: 'blur(6px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 100,
        padding: 20
      }}
    >
      <div
        className="glass-panel"
        style={{
          width: '100%',
          maxWidth: 620,
          padding: 24,
          background: '#0f172a',
          border: '1px solid #38bdf8',
          boxShadow: '0 0 30px rgba(56, 189, 248, 0.3)',
          display: 'flex',
          flexDirection: 'column',
          gap: 16
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2 style={{ margin: 0, fontSize: 18, color: '#38bdf8', fontWeight: 800 }}>
              ✔ Automated Resilience Mitigation Applied
            </h2>
            <span style={{ fontSize: 12, color: '#94a3b8' }}>Real-time physical state adjustment & cascade containment</span>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'transparent', border: 'none', color: '#94a3b8', fontSize: 20, cursor: 'pointer' }}
          >
            ✕
          </button>
        </div>

        {/* Key KPI Improvements */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 10 }}>
          <div style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid #10b981', borderRadius: 8, padding: 12, textAlign: 'center' }}>
            <div style={{ fontSize: 20, fontWeight: 800, color: '#34d399' }}>+{data.traffic_density_improvement_pct}%</div>
            <div style={{ fontSize: 11, color: '#94a3b8', marginTop: 4 }}>Density Improvement</div>
          </div>
          <div style={{ background: 'rgba(56, 189, 248, 0.15)', border: '1px solid #38bdf8', borderRadius: 8, padding: 12, textAlign: 'center' }}>
            <div style={{ fontSize: 20, fontWeight: 800, color: '#38bdf8' }}>{Math.abs(data.power_load_shed_mw)} MW</div>
            <div style={{ fontSize: 11, color: '#94a3b8', marginTop: 4 }}>Peak Load Shed</div>
          </div>
          <div style={{ background: 'rgba(245, 158, 11, 0.15)', border: '1px solid #f59e0b', borderRadius: 8, padding: 12, textAlign: 'center' }}>
            <div style={{ fontSize: 20, fontWeight: 800, color: '#fbbf24' }}>{data.incidents_prevented}</div>
            <div style={{ fontSize: 11, color: '#94a3b8', marginTop: 4 }}>Failures Prevented</div>
          </div>
        </div>

        {/* Executed Actions List */}
        <div>
          <div style={{ fontSize: 12, fontWeight: 700, color: '#cbd5e1', marginBottom: 8 }}>Executed Control Actions:</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {data.actions_executed?.map((act, i) => (
              <div key={i} style={{ fontSize: 12, color: '#f1f5f9', display: 'flex', alignItems: 'center', gap: 8 }}>
                <span style={{ color: '#10b981' }}>✓</span> {act}
              </div>
            ))}
          </div>
        </div>

        <button
          onClick={onClose}
          className="btn-primary"
          style={{ width: '100%', padding: '10px 0', fontSize: 13, fontWeight: 700, marginTop: 8 }}
        >
          Confirm & Return to Live Twin
        </button>
      </div>
    </div>
  );
}

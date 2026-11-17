import React from 'react';

export default function FeederPanel({ powerData }) {
  const feeders = powerData?.feeders || {};

  const getStatusColor = (status, breakerClosed) => {
    if (!breakerClosed || status === 'TRIPPED') return { bg: 'rgba(100, 116, 139, 0.2)', text: '#94a3b8', border: '#475569', label: 'OFFLINE' };
    if (status === 'OVERLOADED') return { bg: 'rgba(239, 68, 68, 0.25)', text: '#ef4444', border: '#ef4444', label: 'OVERLOAD' };
    if (status === 'WARNING') return { bg: 'rgba(245, 158, 11, 0.2)', text: '#f59e0b', border: '#f59e0b', label: 'WARNING' };
    return { bg: 'rgba(16, 185, 129, 0.2)', text: '#10b981', border: '#10b981', label: 'NORMAL' };
  };

  return (
    <div className="glass-panel" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: 6 }}>
            <span>⚡</span> Electrical Distribution Grid
          </h3>
          <span style={{ fontSize: 11, color: '#94a3b8' }}>66kV Substation • 4 Radial 11kV Feeders</span>
        </div>
        <div style={{ textAlign: 'right' }}>
          <span style={{ fontSize: 12, fontWeight: 600, color: '#38bdf8' }}>
            {powerData?.total_physical_mw || 0} MW
          </span>
          <span style={{ fontSize: 11, color: '#64748b' }}> / {powerData?.total_capacity_mw || 0} MW</span>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 10 }}>
        {Object.values(feeders).map(f => {
          const cfg = getStatusColor(f.status, f.breaker_closed);
          const isFDI = f.fdi_attacked;

          return (
            <div
              key={f.feeder_id}
              style={{
                background: 'rgba(15, 23, 42, 0.65)',
                border: `1px solid ${cfg.border}`,
                borderRadius: 8,
                padding: '10px 12px',
                display: 'flex',
                flexDirection: 'column',
                gap: 8,
                position: 'relative'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <div style={{ fontSize: 13, fontWeight: 700, color: '#f1f5f9' }}>{f.feeder_id}</div>
                  <div style={{ fontSize: 11, color: '#94a3b8' }}>{f.zone_name}</div>
                </div>
                <span
                  style={{
                    fontSize: 10,
                    fontWeight: 700,
                    padding: '2px 8px',
                    borderRadius: 4,
                    background: cfg.bg,
                    color: cfg.text,
                    border: `1px solid ${cfg.border}`
                  }}
                >
                  {cfg.label}
                </span>
              </div>

              {/* Load Bar */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, marginBottom: 4 }}>
                  <span style={{ color: '#94a3b8' }}>Physical Load</span>
                  <span style={{ fontWeight: 600, color: cfg.text }}>
                    {f.physical_load_mw} MW ({f.loading_percentage}%)
                  </span>
                </div>
                <div style={{ width: '100%', height: 6, background: '#1e293b', borderRadius: 3, overflow: 'hidden' }}>
                  <div
                    style={{
                      width: `${Math.min(100, f.loading_percentage)}%`,
                      height: '100%',
                      background: cfg.text,
                      transition: 'width 0.3s ease'
                    }}
                  />
                </div>
              </div>

              {/* FDI Attack Badge if SCADA is compromised */}
              {isFDI && (
                <div
                  style={{
                    background: 'rgba(239, 68, 68, 0.2)',
                    border: '1px dashed #ef4444',
                    borderRadius: 4,
                    padding: '4px 6px',
                    fontSize: 10,
                    color: '#f87171'
                  }}
                >
                  ⚠ FDI COMPROMISED: SCADA reports <b>{f.telemetry_load_mw} MW</b>
                </div>
              )}

              {/* Overload Trip Countdown */}
              {f.status === 'OVERLOADED' && f.trip_countdown_sec > 0 && (
                <div style={{ fontSize: 10, color: '#f87171', fontWeight: 600 }}>
                  Breaker Trip in: {f.trip_countdown_sec}s
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

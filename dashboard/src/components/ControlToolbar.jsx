import React from 'react';

export default function ControlToolbar({
  currentScenario,
  isPaused,
  simSpeed,
  onSelectScenario,
  onTogglePause,
  onReset,
  onSetSpeed
}) {
  const scenarios = [
    { id: 'NORMAL_CITY', label: '1. Normal City' },
    { id: 'TRAFFIC_CONGESTION', label: '2. Traffic Congestion' },
    { id: 'POWER_FAILURE', label: '3. Power Failure' },
    { id: 'CYBERATTACK', label: '4. Cyberattack' },
    { id: 'AUTOMATIC_RECOVERY', label: '5. Auto Recovery' }
  ];

  return (
    <div
      className="glass-panel"
      style={{
        padding: '10px 16px',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: 12
      }}
    >
      {/* Hackathon Scenarios */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
        <span style={{ fontSize: 11, fontWeight: 700, color: '#94a3b8', marginRight: 4 }}>SCENARIOS:</span>
        {scenarios.map(s => {
          const isActive = currentScenario === s.id;
          return (
            <button
              key={s.id}
              onClick={() => onSelectScenario(s.id)}
              style={{
                background: isActive ? 'linear-gradient(135deg, #0284c7 0%, #0369a1 100%)' : 'rgba(30, 41, 59, 0.7)',
                color: isActive ? '#fff' : '#cbd5e1',
                border: `1px solid ${isActive ? '#38bdf8' : 'rgba(255,255,255,0.08)'}`,
                padding: '6px 12px',
                borderRadius: 6,
                fontSize: 11,
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
            >
              {s.label}
            </button>
          );
        })}
      </div>

      {/* Playback Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <button
          onClick={onTogglePause}
          className="btn-secondary"
          style={{ fontSize: 11, padding: '6px 12px' }}
        >
          {isPaused ? '▶ Resume' : '⏸ Pause'}
        </button>

        <button
          onClick={onReset}
          className="btn-secondary"
          style={{ fontSize: 11, padding: '6px 12px', color: '#f87171' }}
        >
          ↺ Reset
        </button>

        {/* Speed Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 4, background: 'rgba(15, 23, 42, 0.8)', padding: '3px 6px', borderRadius: 6 }}>
          {[1.0, 2.0, 5.0].map(sp => (
            <button
              key={sp}
              onClick={() => onSetSpeed(sp)}
              style={{
                background: simSpeed === sp ? '#38bdf8' : 'transparent',
                color: simSpeed === sp ? '#000' : '#94a3b8',
                border: 'none',
                borderRadius: 4,
                padding: '3px 8px',
                fontSize: 10,
                fontWeight: 700,
                cursor: 'pointer'
              }}
            >
              {sp}x
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

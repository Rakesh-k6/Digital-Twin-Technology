import React, { useState, useEffect, useRef } from 'react';
import CityTwinCanvas from './components/CityTwinCanvas';
import FeederPanel from './components/FeederPanel';
import CyberSecurityPanel from './components/CyberSecurityPanel';
import PredictorPanel from './components/PredictorPanel';
import MitigationModal from './components/MitigationModal';
import ControlToolbar from './components/ControlToolbar';

export default function App() {
  const [state, setState] = useState(null);
  const [connected, setConnected] = useState(false);
  const [mitigationModalData, setMitigationModalData] = useState(null);
  const wsRef = useRef(null);

  useEffect(() => {
    let ws;
    let fallbackInterval;

    const connectWS = () => {
      try {
        ws = new WebSocket('ws://localhost:8000/ws/live');
        wsRef.current = ws;

        ws.onopen = () => {
          setConnected(true);
        };

        ws.onmessage = evt => {
          try {
            const data = JSON.parse(evt.data);
            setState(data);
          } catch (e) {
            console.error('WS parse error:', e);
          }
        };

        ws.onclose = () => {
          setConnected(false);
          setTimeout(connectWS, 2000);
        };

        ws.onerror = () => {
          ws.close();
        };
      } catch (e) {
        console.warn('WS Init failed, polling REST:', e);
      }
    };

    connectWS();

    fallbackInterval = setInterval(async () => {
      if (!connected) {
        try {
          const res = await fetch('http://localhost:8000/api/status');
          if (res.ok) {
            const json = await res.json();
            setState(json);
            setConnected(true);
          }
        } catch (e) {
          setConnected(false);
        }
      }
    }, 500);

    return () => {
      if (ws) ws.close();
      clearInterval(fallbackInterval);
    };
  }, [connected]);

  const handleSelectScenario = async scenarioName => {
    try {
      const res = await fetch(`http://localhost:8000/api/scenario/${scenarioName}`, { method: 'POST' });
      if (scenarioName === 'AUTOMATIC_RECOVERY') {
        const json = await res.json();
        setMitigationModalData(json);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleApplyMitigation = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/mitigation/apply', { method: 'POST' });
      if (res.ok) {
        const json = await res.json();
        setMitigationModalData(json);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleInjectAttack = async (type, target, val) => {
    try {
      await fetch('http://localhost:8000/api/cyber/inject', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ attack_type: type, target_id: target, spoof_value: val })
      });
    } catch (e) {
      console.error(e);
    }
  };

  const handleClearAttacks = async () => {
    try {
      await fetch('http://localhost:8000/api/cyber/clear', { method: 'POST' });
    } catch (e) {
      console.error(e);
    }
  };

  const handleTogglePause = async () => {
    const isPaused = state?.is_paused;
    const endpoint = isPaused ? 'resume' : 'pause';
    await fetch(`http://localhost:8000/api/control/${endpoint}`, { method: 'POST' });
  };

  const handleReset = async () => {
    await fetch('http://localhost:8000/api/reset', { method: 'POST' });
  };

  const handleSetSpeed = async speed => {
    await fetch('http://localhost:8000/api/control/speed', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ speed })
    });
  };

  const traffic = state?.traffic || {};
  const power = state?.power || {};
  const security = state?.security || {};
  const predictions = state?.predictions || {};

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: '#070a12', padding: '14px', gap: 12 }}>
      {/* Top Header */}
      <header
        className="glass-panel glow-blue"
        style={{
          padding: '12px 20px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: 12
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: connected ? '#10b981' : '#ef4444', boxShadow: `0 0 10px ${connected ? '#10b981' : '#ef4444'}` }} />
          <div>
            <h1 style={{ margin: 0, fontSize: 18, fontWeight: 800, letterSpacing: -0.4, color: '#f8fafc' }}>
              CITYLINK <span style={{ color: '#38bdf8', fontWeight: 600, fontSize: 14 }}>| 3D VIRTUAL WORLD OF BANGALORE</span>
            </h1>
            <span style={{ fontSize: 11, color: '#94a3b8' }}>
              Silk Board Flyover • Namma Metro Viaduct • Koramangala • HSR Layout • Bellandur RMZ Ecospace • BESCOM 11kV Grid
            </span>
          </div>
        </div>

        {/* Global KPIs Bar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
          <div>
            <div style={{ fontSize: 10, color: '#94a3b8', textTransform: 'uppercase' }}>BMTC Buses</div>
            <div style={{ fontSize: 16, fontWeight: 700, color: '#38bdf8' }}>{traffic?.bmtc_buses_count || 8}</div>
          </div>
          <div>
            <div style={{ fontSize: 10, color: '#94a3b8', textTransform: 'uppercase' }}>Namma Autos</div>
            <div style={{ fontSize: 16, fontWeight: 700, color: '#facc15' }}>{traffic?.auto_rickshaws_count || 14}</div>
          </div>
          <div>
            <div style={{ fontSize: 10, color: '#94a3b8', textTransform: 'uppercase' }}>Active Fleet</div>
            <div style={{ fontSize: 16, fontWeight: 700, color: '#38bdf8' }}>{traffic?.active_vehicles || 42}</div>
          </div>
          <div>
            <div style={{ fontSize: 10, color: '#94a3b8', textTransform: 'uppercase' }}>Pedestrians</div>
            <div style={{ fontSize: 16, fontWeight: 700, color: '#34d399' }}>{traffic?.pedestrian_count || 48}</div>
          </div>
          <div>
            <div style={{ fontSize: 10, color: '#94a3b8', textTransform: 'uppercase' }}>Avg Speed</div>
            <div style={{ fontSize: 16, fontWeight: 700, color: '#f1f5f9' }}>{traffic?.average_speed_kmh || 0} km/h</div>
          </div>
          <div>
            <div style={{ fontSize: 10, color: '#94a3b8', textTransform: 'uppercase' }}>BESCOM Feeders</div>
            <div style={{ fontSize: 16, fontWeight: 700, color: power?.tripped_feeders_count > 0 ? '#ef4444' : '#10b981' }}>
              {power?.tripped_feeders_count || 0} TRIPPED
            </div>
          </div>
        </div>
      </header>

      {/* Control Toolbar */}
      <ControlToolbar
        currentScenario={state?.current_scenario || 'NORMAL_CITY'}
        isPaused={state?.is_paused || false}
        simSpeed={state?.sim_speed || 1.0}
        onSelectScenario={handleSelectScenario}
        onTogglePause={handleTogglePause}
        onReset={handleReset}
        onSetSpeed={handleSetSpeed}
      />

      {/* Main Grid: Viewport + Right Side Intelligence Panels */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.35fr 1fr', gap: 14, flex: 1, minHeight: 'calc(100vh - 180px)' }}>
        {/* Left: Interactive Canvas Twin */}
        <div className="glass-panel" style={{ overflow: 'hidden', minHeight: 540 }}>
          <CityTwinCanvas state={state} />
        </div>

        {/* Right: Telemetry & Security Panels */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14, overflowY: 'auto' }}>
          <FeederPanel powerData={power} />
          <CyberSecurityPanel
            securityData={security}
            onInjectAttack={handleInjectAttack}
            onClearAttacks={handleClearAttacks}
          />
          <PredictorPanel
            predictionData={predictions}
            onApplyMitigation={handleApplyMitigation}
          />
        </div>
      </div>

      {/* Mitigation Analytics Modal */}
      {mitigationModalData && (
        <MitigationModal
          data={mitigationModalData}
          onClose={() => setMitigationModalData(null)}
        />
      )}
    </div>
  );
}

import React, { useRef, useEffect, useState } from 'react';

export default function CityTwinCanvas({ state }) {
  const canvasRef = useRef(null);
  const [zoom, setZoom] = useState(1.7);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const isDragging = useRef(false);
  const dragStart = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const dpr = window.devicePixelRatio || 1;
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.scale(dpr, dpr);

    // Deep tech Bengaluru night backdrop
    ctx.fillStyle = '#080c16';
    ctx.fillRect(0, 0, width, height);

    ctx.save();
    ctx.translate(width / 2 + pan.x, height / 2 + pan.y);
    ctx.scale(zoom, zoom);

    // 1. Grid
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.035)';
    ctx.lineWidth = 1;
    for (let x = -320; x <= 320; x += 40) {
      ctx.beginPath(); ctx.moveTo(x, -320); ctx.lineTo(x, 320); ctx.stroke();
    }
    for (let y = -320; y <= 320; y += 40) {
      ctx.beginPath(); ctx.moveTo(-320, y); ctx.lineTo(320, y); ctx.stroke();
    }

    // 2. Bangalore 4 Zones
    const zones = [
      { id: 'Zone_A', name: 'KORAMANGALA', landmark: 'Sony World • 80ft Rd', cx: -90, cy: -90, color: 'rgba(37, 99, 235, 0.12)' },
      { id: 'Zone_B', name: 'HSR LAYOUT', landmark: '27th Main • BDA Complex', cx: 90, cy: -90, color: 'rgba(22, 163, 74, 0.12)' },
      { id: 'Zone_C', name: 'BELLANDUR', landmark: 'RMZ Ecospace • Tech Park', cx: 90, cy: 90, color: 'rgba(2, 132, 199, 0.12)' },
      { id: 'Zone_D', name: 'SILK BOARD', landmark: 'Central Flyover & Metro Junction', cx: -90, cy: 90, color: 'rgba(220, 38, 38, 0.15)' },
    ];

    zones.forEach(z => {
      const density = state?.traffic?.zone_densities?.[z.id] || 0.25;
      let fillColor = z.color;
      if (density > 0.6) fillColor = 'rgba(239, 68, 68, 0.24)';
      else if (density > 0.4) fillColor = 'rgba(245, 158, 11, 0.18)';

      ctx.fillStyle = fillColor;
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.roundRect(z.cx - 68, z.cy - 68, 136, 136, 10);
      ctx.fill();
      ctx.stroke();

      // Zone Names
      ctx.fillStyle = '#f8fafc';
      ctx.font = 'bold 10px "JetBrains Mono"';
      ctx.textAlign = 'center';
      ctx.fillText(z.name, z.cx, z.cy - 50);

      ctx.fillStyle = '#94a3b8';
      ctx.font = '8px "Plus Jakarta Sans"';
      ctx.fillText(z.landmark, z.cx, z.cy - 38);
      ctx.fillText(`${Math.round(density * 100)}% CONGESTION`, z.cx, z.cy + 60);
    });

    // 3. Road Corridors
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 16;
    ctx.lineCap = 'round';
    const drawR = (x1, y1, x2, y2) => { ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke(); };

    // Outer Ring Road (ORR) Arterials
    drawR(-90, -90, 90, -90); // Koramangala - HSR
    drawR(90, -90, 90, 90);   // HSR - Bellandur
    drawR(90, 90, -90, 90);   // Bellandur - Silk Board Outer Ring Road
    drawR(-90, 90, -90, -90); // Hosur Road

    // Yellow Highway Dividers
    ctx.strokeStyle = '#facc15';
    ctx.lineWidth = 1.2;
    drawR(-90, -90, 90, -90);
    drawR(90, -90, 90, 90);
    drawR(90, 90, -90, 90);
    drawR(-90, 90, -90, -90);

    // 4. Central Silk Board Elevated Flyover Deck
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 8;
    drawR(-90, 40, -90, 140);
    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 8px "JetBrains Mono"';
    ctx.fillText('SILK BOARD ELEVATED FLYOVER', -90, 32);

    // 5. Namma Metro Elevated Track along Outer Ring Road
    ctx.strokeStyle = '#9333ea'; // Purple / Yellow Line
    ctx.lineWidth = 3;
    drawR(-120, 90, 120, 90);

    // 6. BESCOM 66kV Substation at Center
    ctx.fillStyle = '#10b981';
    ctx.beginPath(); ctx.arc(0, 0, 9, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 8px "JetBrains Mono"';
    ctx.fillText('BESCOM 66kV SUBSTATION', 0, 18);

    // 7. BESCOM Power Feeder Transmission Lines
    const feeders = state?.power?.feeders || {};
    ctx.lineWidth = 2.2;
    Object.values(feeders).forEach(f => {
      let tx = -90, ty = -90;
      if (f.zone_id === 'Zone_B') { tx = 90; ty = -90; }
      else if (f.zone_id === 'Zone_C') { tx = 90; ty = 90; }
      else if (f.zone_id === 'Zone_D') { tx = -90; ty = 90; }

      let col = '#10b981';
      if (!f.breaker_closed || f.status === 'TRIPPED') col = '#64748b';
      else if (f.status === 'OVERLOADED') col = '#ef4444';
      else if (f.status === 'WARNING') col = '#f59e0b';

      ctx.strokeStyle = col;
      ctx.setLineDash([4, 4]);
      drawR(0, 0, tx, ty);
      ctx.setLineDash([]);
    });

    // 8. Traffic Signals with Live Green/Red/Amber Flashing
    Object.values(state?.traffic?.signals || {}).forEach(s => {
      const sx = s.pos[0];
      const sy = -s.pos[2];

      let col = '#ef4444';
      if (s.status === 'FAIL_FLASHING_AMBER') {
        col = (Math.floor(Date.now() / 400) % 2 === 0) ? '#f59e0b' : '#1e293b';
      } else if (s.ns_light === 'GREEN' || s.ew_light === 'GREEN') {
        col = '#10b981';
      } else if (s.ns_light === 'YELLOW' || s.ew_light === 'YELLOW') {
        col = '#f59e0b';
      }

      ctx.fillStyle = '#0f172a';
      ctx.beginPath(); ctx.arc(sx, sy, 5.5, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = col;
      ctx.beginPath(); ctx.arc(sx, sy, 3.5, 0, Math.PI * 2); ctx.fill();
    });

    // 9. Bangalore Pedestrians (Techies, Commuters)
    (state?.entities?.pedestrians || []).forEach(p => {
      ctx.fillStyle = (p.state === 'WAITING_CROSSING') ? '#f43f5e' : '#38bdf8';
      ctx.beginPath(); ctx.arc(p.x, -p.z, 2.2, 0, Math.PI * 2); ctx.fill();
    });

    // 10. Bangalore Vehicle Fleet (BMTC Buses, Auto-rickshaws, Delivery Bikes, IT Cabs)
    (state?.entities?.vehicles || []).forEach(v => {
      ctx.save();
      ctx.translate(v.x, -v.z);
      ctx.rotate((v.heading * Math.PI) / 180);

      if (v.type === 'bmtc_bus') {
        // BMTC Bus (Large Blue or Green body)
        ctx.fillStyle = v.color || '#0284c7';
        ctx.beginPath(); ctx.roundRect(-3, -7, 6, 14, 2); ctx.fill();
        // Yellow Destination board
        ctx.fillStyle = '#facc15'; ctx.fillRect(-2, 5, 4, 1.5);

      } else if (v.type === 'auto_rickshaw') {
        // Bengaluru Auto (Yellow Hood + Green Base)
        ctx.fillStyle = '#15803d'; // Green Base
        ctx.beginPath(); ctx.roundRect(-2, -3.5, 4, 7, 2); ctx.fill();
        ctx.fillStyle = '#facc15'; // Yellow Top
        ctx.beginPath(); ctx.roundRect(-1.8, -1, 3.6, 4.5, 2); ctx.fill();

      } else if (v.type === 'delivery_bike') {
        // Delivery Bike with Box
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(-1, -2, 2, 4);
        ctx.fillStyle = v.color || '#ea580c'; // Swiggy Orange or Zomato Red Box
        ctx.fillRect(-1.2, -3.2, 2.4, 2);

      } else if (v.is_emergency) {
        // 108 Ambulance
        ctx.fillStyle = '#ffffff';
        ctx.beginPath(); ctx.roundRect(-2.5, -5, 5, 10, 2); ctx.fill();
        ctx.fillStyle = (Math.floor(Date.now() / 150) % 2 === 0) ? '#ef4444' : '#38bdf8';
        ctx.beginPath(); ctx.arc(0, 0, 2.5, 0, Math.PI * 2); ctx.fill();

      } else {
        // IT Cab / Private car
        ctx.fillStyle = v.in_queue ? '#ef4444' : (v.color || '#f8fafc');
        ctx.beginPath(); ctx.roundRect(-2, -4, 4, 8, 2); ctx.fill();
      }

      ctx.restore();
    });

    ctx.restore();
  }, [state, zoom, pan]);

  const handleMouseDown = e => {
    isDragging.current = true;
    dragStart.current = { x: e.clientX - pan.x, y: e.clientY - pan.y };
  };
  const handleMouseMove = e => {
    if (!isDragging.current) return;
    setPan({ x: e.clientX - dragStart.current.x, y: e.clientY - dragStart.current.y });
  };
  const handleMouseUp = () => { isDragging.current = false; };
  const handleWheel = e => {
    e.preventDefault();
    const factor = e.deltaY < 0 ? 1.15 : 0.85;
    setZoom(prev => Math.min(4.0, Math.max(0.6, prev * factor)));
  };

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', overflow: 'hidden' }}>
      <canvas
        ref={canvasRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onWheel={handleWheel}
        style={{ width: '100%', height: '100%', cursor: isDragging.current ? 'grabbing' : 'grab', display: 'block' }}
      />
      <div style={{ position: 'absolute', bottom: 12, right: 12, display: 'flex', gap: 6, zIndex: 10 }}>
        <button onClick={() => setZoom(prev => Math.min(4.0, prev * 1.2))} className="btn">+</button>
        <button onClick={() => setZoom(prev => Math.max(0.6, prev * 0.8))} className="btn">-</button>
        <button onClick={() => { setZoom(1.7); setPan({ x: 0, y: 0 }); }} className="btn">Reset View</button>
      </div>
      <div style={{ position: 'absolute', top: 12, left: 12, display: 'flex', gap: 8, alignItems: 'center' }}>
        <span style={{ background: 'rgba(15, 23, 42, 0.9)', padding: '4px 10px', borderRadius: 6, fontSize: 11, border: '1px solid rgba(255,255,255,0.1)', color: '#38bdf8' }}>
          BENGALURU 3D TWIN • BMTC BUSES & NAMMA AUTOS
        </span>
      </div>
    </div>
  );
}

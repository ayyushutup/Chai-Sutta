import React, { useEffect, useState } from 'react';
import { Navigation, AlertTriangle, Train, ArrowUpRight } from 'lucide-react';
import { getCityTraffic, TrafficPoint } from '../services/api';

interface TrafficWidgetProps {
  city?: string;
}

export const TrafficWidget: React.FC<TrafficWidgetProps> = ({ city = 'Mumbai' }) => {
  const [trafficPoints, setTrafficPoints] = useState<TrafficPoint[]>([]);

  useEffect(() => {
    getCityTraffic(city).then((data) => setTrafficPoints(data));
  }, [city]);

  const getStatusBadge = (congestion: string) => {
    switch (congestion.toLowerCase()) {
      case 'light':
      case 'clear':
        return { label: 'Clear', color: 'text-[#00ff66]', bg: 'bg-[#00ff66]/10 border-[#00ff66]/30', dot: 'bg-[#00ff66] shadow-[0_0_8px_#00ff66]' };
      case 'moderate':
      case 'slow':
        return { label: 'Slow', color: 'text-[#ff9100]', bg: 'bg-[#ff9100]/10 border-[#ff9100]/30', dot: 'bg-[#ff9100] shadow-[0_0_8px_#ff9100]' };
      default:
        return { label: 'Gridlock', color: 'text-[#ff2a00]', bg: 'bg-[#ff2a00]/20 border-[#ff2a00]/40', dot: 'bg-[#ff2a00] shadow-[0_0_8px_#ff2a00]' };
    }
  };

  return (
    <div className="dark-card p-6 rounded-2xl relative overflow-hidden bg-[#180533] border border-purple-400/20 shadow-xl space-y-4 group hover:border-[#ffee00]/50 transition-all">
      <div className="flex items-center justify-between pb-3 border-b border-purple-400/20">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-[#ffee00]/15 text-[#ffee00] border border-[#ffee00]/30">
            <Navigation className="w-5 h-5 stroke-[2.5]" />
          </div>
          <div>
            <h3 className="font-marker font-bold text-white text-xl tracking-wide">
              LIVE TRAFFIC & TRANSIT
            </h3>
            <span className="text-[10px] font-mono text-purple-300">kettli Telemetry Stream</span>
          </div>
        </div>

        <div className="w-7 h-7 rounded-full bg-purple-900/40 border border-purple-400/30 flex items-center justify-center text-purple-200 group-hover:text-[#ffee00] group-hover:border-[#ffee00]/50 transition-all">
          <ArrowUpRight className="w-4 h-4" />
        </div>
      </div>

      {/* Corridor Statuses */}
      <div className="space-y-2.5 text-xs">
        {trafficPoints.slice(0, 3).map((pt, idx) => {
          const badge = getStatusBadge(pt.congestion_level);
          return (
            <div key={idx} className="p-3 rounded-xl bg-[#120327] border border-purple-400/15 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className={`w-2.5 h-2.5 rounded-full ${badge.dot}`} />
                <div>
                  <div className="font-bold text-purple-100">{pt.road_name || 'Corridor Route'}</div>
                  <div className="text-[11px] text-purple-300">
                    Speed {pt.current_speed} km/h (Free-flow {pt.free_flow_speed} km/h)
                  </div>
                </div>
              </div>
              <span className={`text-[10px] font-extrabold ${badge.color} ${badge.bg} px-2.5 py-0.5 rounded-full border`}>
                {badge.label}
              </span>
            </div>
          );
        })}
      </div>

      {/* Train / Local Metro Tracker */}
      <div className="pt-3 border-t border-purple-400/20 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-purple-100 flex items-center gap-1.5 font-marker text-sm">
            <Train className="w-4 h-4 text-[#ffee00]" /> Metro & Local Trains
          </span>
          <span className="text-[10px] font-mono text-[#00e5ff]">GPS Synced</span>
        </div>

        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="p-2.5 rounded-xl bg-[#120327] border border-purple-400/15">
            <div className="text-[10px] text-purple-300 uppercase font-mono">Western Line AC Local</div>
            <div className="font-semibold text-purple-100 flex items-center justify-between mt-1">
              <span>Platform 2</span>
              <span className="text-[#00ff66] font-bold">In 3 mins</span>
            </div>
          </div>

          <div className="p-2.5 rounded-xl bg-[#120327] border border-purple-400/15">
            <div className="text-[10px] text-purple-300 uppercase font-mono">Central Line Fast</div>
            <div className="font-semibold text-purple-100 flex items-center justify-between mt-1">
              <span>Platform 1</span>
              <span className="text-[#ff9100] font-bold">On Time</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};


import React from 'react';
import { Navigation, AlertTriangle, Train, ArrowUpRight } from 'lucide-react';

export const TrafficWidget: React.FC = () => {
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
        <div className="p-3 rounded-xl bg-[#120327] border border-purple-400/15 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-2.5 h-2.5 rounded-full bg-[#00ff66] shadow-[0_0_8px_#00ff66]" />
            <div>
              <div className="font-bold text-purple-100">Western Express Highway</div>
              <div className="text-[11px] text-purple-300">Flow smooth • Avg Speed 45 km/h</div>
            </div>
          </div>
          <span className="text-[10px] font-extrabold text-[#00ff66] bg-[#00ff66]/10 px-2.5 py-0.5 rounded-full border border-[#00ff66]/30">Clear</span>
        </div>

        <div className="p-3 rounded-xl bg-[#120327] border border-purple-400/15 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-2.5 h-2.5 rounded-full bg-[#ff9100] shadow-[0_0_8px_#ff9100]" />
            <div>
              <div className="font-bold text-purple-100">Outer Ring Road Flyover</div>
              <div className="text-[11px] text-purple-300">Moderate congestion (+12 min delay)</div>
            </div>
          </div>
          <span className="text-[10px] font-extrabold text-[#ff9100] bg-[#ff9100]/10 px-2.5 py-0.5 rounded-full border border-[#ff9100]/30">Slow</span>
        </div>

        <div className="p-3 rounded-xl bg-[#ff2a00]/15 border border-[#ff2a00]/30 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <AlertTriangle className="w-4 h-4 text-[#ff2a00] shrink-0" />
            <div>
              <div className="font-bold text-red-200">Central Underpass Junction</div>
              <div className="text-[11px] text-red-300/80">Roadwork bottleneck • Diversion active</div>
            </div>
          </div>
          <span className="text-[10px] font-extrabold text-[#ff2a00] bg-[#ff2a00]/20 px-2.5 py-0.5 rounded-full border border-[#ff2a00]/40">Blocked</span>
        </div>
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
            <div className="text-[10px] text-purple-300 uppercase font-mono">Northbound Local</div>
            <div className="font-semibold text-purple-100 flex items-center justify-between mt-1">
              <span>Platform 2</span>
              <span className="text-[#00ff66] font-bold">In 3 mins</span>
            </div>
          </div>

          <div className="p-2.5 rounded-xl bg-[#120327] border border-purple-400/15">
            <div className="text-[10px] text-purple-300 uppercase font-mono">Airport Line Express</div>
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

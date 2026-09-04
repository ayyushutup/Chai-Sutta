import React from 'react';
import { Flame, ArrowUpRight } from 'lucide-react';

export const CityMoodWidget: React.FC = () => {
  return (
    <div className="dark-card p-6 rounded-2xl relative overflow-hidden bg-[#180533] border border-purple-400/20 shadow-xl h-full flex flex-col justify-between group hover:border-[#ffee00]/50 transition-all">
      {/* Header artwork area */}
      <div className="relative rounded-xl overflow-hidden bg-gradient-to-r from-[#ff2a00]/25 via-[#8b5cf6]/30 to-[#ffee00]/25 p-4 border border-purple-400/20 mb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-xl bg-[#ff2a00]/20 text-[#ff2a00] border border-[#ff2a00]/30">
              <Flame className="w-5 h-5 stroke-[2.5]" />
            </div>
            <div>
              <span className="text-[10px] font-mono font-bold text-purple-200 uppercase tracking-widest block">
                AGGREGATED PULSE
              </span>
              <h3 className="font-marker font-bold text-white text-xl tracking-wide">
                CITY MOOD MATRIX
              </h3>
            </div>
          </div>

          <span className="bg-[#ffee00] text-black text-xs font-marker font-bold px-3 py-1 rounded-full shadow-[0_0_15px_rgba(255,238,0,0.4)]">
            92% VIBRANT
          </span>
        </div>
      </div>

      {/* Progress Bars */}
      <div className="space-y-3.5 text-xs font-sans">
        <div>
          <div className="flex justify-between mb-1.5 font-semibold">
            <span className="text-purple-100 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-[#ff2a00]" /> kettli Tapri Buzz & Energy
            </span>
            <span className="text-[#ff2a00] font-mono font-bold">94%</span>
          </div>
          <div className="w-full h-2.5 bg-black/60 rounded-full overflow-hidden p-0.5 border border-purple-400/20">
            <div className="h-full bg-gradient-to-r from-[#ff2a00] to-[#ff9100] rounded-full" style={{ width: '94%' }} />
          </div>
        </div>

        <div>
          <div className="flex justify-between mb-1.5 font-semibold">
            <span className="text-purple-100 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-[#ffee00]" /> Traffic Flow Velocity
            </span>
            <span className="text-[#ffee00] font-mono font-bold">68%</span>
          </div>
          <div className="w-full h-2.5 bg-black/60 rounded-full overflow-hidden p-0.5 border border-purple-400/20">
            <div className="h-full bg-gradient-to-r from-[#ffee00] to-[#00ff66] rounded-full" style={{ width: '68%' }} />
          </div>
        </div>

        <div>
          <div className="flex justify-between mb-1.5 font-semibold">
            <span className="text-purple-100 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-[#00e5ff]" /> Public Sentiment Index
            </span>
            <span className="text-[#00e5ff] font-mono font-bold">89% POSITIVE</span>
          </div>
          <div className="w-full h-2.5 bg-black/60 rounded-full overflow-hidden p-0.5 border border-purple-400/20">
            <div className="h-full bg-gradient-to-r from-[#00e5ff] to-[#c084fc] rounded-full" style={{ width: '89%' }} />
          </div>
        </div>
      </div>

      {/* Hashtag Pills */}
      <div className="mt-5 pt-3 border-t border-purple-400/20 flex flex-wrap items-center justify-between gap-2">
        <div className="flex flex-wrap gap-1.5">
          <span className="text-[10px] font-mono font-bold text-purple-200 bg-purple-900/40 border border-purple-400/30 px-2.5 py-1 rounded-full">
            #KETTLI_CHAI
          </span>
          <span className="text-[10px] font-mono font-bold text-[#ff2a00] bg-[#ff2a00]/15 border border-[#ff2a00]/30 px-2.5 py-1 rounded-full">
            #HAR_GHAR_KHABAR
          </span>
          <span className="text-[10px] font-mono font-bold text-[#ffee00] bg-[#ffee00]/15 border border-[#ffee00]/30 px-2.5 py-1 rounded-full">
            #METRO_LINE_3
          </span>
        </div>

        <div className="w-7 h-7 rounded-full bg-purple-900/40 border border-purple-400/30 flex items-center justify-center text-purple-200 group-hover:text-[#ffee00] group-hover:border-[#ffee00]/50 transition-all">
          <ArrowUpRight className="w-4 h-4" />
        </div>
      </div>
    </div>
  );
};

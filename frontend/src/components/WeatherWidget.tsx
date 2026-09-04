import React from 'react';
import { Sun, Wind, Eye, Droplets, Play } from 'lucide-react';

interface WeatherProps {
  city: string;
}

export const WeatherWidget: React.FC<WeatherProps> = ({ city }) => {
  return (
    <div className="dark-card p-6 sm:p-8 rounded-3xl relative overflow-hidden bg-gradient-to-br from-[#27084e] via-[#1a0535] to-[#120324] border border-purple-400/20 shadow-[0_15px_40px_rgba(0,0,0,0.5)]">
      {/* Background neon ambient glow */}
      <div className="absolute -right-20 -top-20 w-80 h-80 bg-[#c084fc]/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -left-20 -bottom-20 w-80 h-80 bg-[#ffee00]/15 rounded-full blur-3xl pointer-events-none" />

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center relative z-10">
        {/* Left Side: Handwritten Title & Info */}
        <div className="lg:col-span-5 space-y-4">
          <div className="flex items-center gap-2">
            <span className="text-[#ffee00] font-marker text-xl">⚡</span>
            <span className="text-xs font-bold uppercase tracking-wider text-[#ffee00] bg-[#ffee00]/15 px-3 py-1 rounded-full border border-[#ffee00]/30 font-mono">
              kettli Live Telemetry
            </span>
          </div>

          <h2 className="text-3xl sm:text-4xl font-extrabold font-marker text-white tracking-wide">
            SHOWREEL <span className="text-[#ffee00] font-accent text-3xl font-normal">& Weather</span>
          </h2>

          <p className="text-xs sm:text-sm text-purple-100 font-sans leading-relaxed">
            Real-time climate telemetry, air quality index, and nocturnal tea/chai suitability stream for <strong className="text-[#ffee00] font-semibold">{city}</strong>.
          </p>

          <div className="pt-2 flex items-center gap-3">
            <button className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#ffee00] text-black font-marker font-bold text-sm hover:bg-[#ffe600] transition-all shadow-[0_0_25px_rgba(255,238,0,0.4)] hover:scale-105">
              <span className="text-xs">Watch Telemetry</span>
              <div className="w-5 h-5 rounded-full bg-black text-[#ffee00] flex items-center justify-center">
                <Play className="w-3 h-3 fill-current ml-0.5" />
              </div>
            </button>

            <span className="text-xs font-bold text-purple-200 font-mono bg-purple-950/60 px-3 py-1.5 rounded-full border border-purple-400/20">AQI 48 [GOOD]</span>
          </div>
        </div>

        {/* Right Side: Cyberpunk Sunset City Media Card with Play Button */}
        <div className="lg:col-span-7 relative group rounded-2xl overflow-hidden border border-purple-300/20 bg-[#120324] h-56 sm:h-64 flex items-center justify-center shadow-xl">
          {/* Atmospheric Cyberpunk Sunset / Skyline Background */}
          <div 
            className="absolute inset-0 bg-cover bg-center transition-transform duration-700 group-hover:scale-105 opacity-85"
            style={{
              backgroundImage: `linear-gradient(to top, rgba(18,3,36,0.95), rgba(120,40,200,0.3)), url('https://images.unsplash.com/photo-1514565131-fce0801e5785?auto=format&fit=crop&w=1000&q=80')`
            }}
          />

          {/* Live Data Badge Overlays on Image */}
          <div className="absolute top-4 left-4 z-10 flex items-center gap-2 bg-black/70 backdrop-blur-md px-3 py-1.5 rounded-full border border-purple-400/30">
            <Sun className="w-4 h-4 text-[#ff9100]" />
            <span className="text-xs font-extrabold text-white font-mono">29°C</span>
            <span className="text-[10px] text-purple-200">| Feels 31°C</span>
          </div>

          <div className="absolute top-4 right-4 z-10 bg-[#ffee00] text-black backdrop-blur-md px-3 py-1 rounded-full text-[11px] font-marker font-bold shadow-[0_0_15px_rgba(255,238,0,0.4)]">
            kettli Approved 🫖
          </div>

          {/* Glowing Central Yellow Play Button */}
          <button className="relative z-10 w-16 h-16 rounded-full bg-[#ffee00] text-black flex items-center justify-center shadow-[0_0_35px_rgba(255,238,0,0.7)] group-hover:scale-110 transition-transform duration-300">
            <Play className="w-7 h-7 fill-current ml-1" />
          </button>

          {/* Metrics Overlay Bar at Bottom */}
          <div className="absolute bottom-3 inset-x-3 z-10 grid grid-cols-3 gap-2 bg-[#120324]/85 backdrop-blur-md p-2.5 rounded-xl border border-purple-400/20 text-xs font-mono">
            <div className="flex items-center gap-2 text-purple-100">
              <Wind className="w-3.5 h-3.5 text-[#00e5ff]" />
              <div>
                <span className="text-[9px] text-purple-300 block uppercase">Wind</span>
                <span className="font-bold text-[#00e5ff]">14 km/h</span>
              </div>
            </div>
            <div className="flex items-center gap-2 text-purple-100">
              <Droplets className="w-3.5 h-3.5 text-[#ff9100]" />
              <div>
                <span className="text-[9px] text-purple-300 block uppercase">Humidity</span>
                <span className="font-bold text-[#ff9100]">72%</span>
              </div>
            </div>
            <div className="flex items-center gap-2 text-purple-100">
              <Eye className="w-3.5 h-3.5 text-[#ffee00]" />
              <div>
                <span className="text-[9px] text-purple-300 block uppercase">Visibility</span>
                <span className="font-bold text-[#ffee00]">6.0 km</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

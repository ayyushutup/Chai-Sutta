import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { AIChatDrawer } from './components/AIChatDrawer';
import { Play } from 'lucide-react';

export function App() {
  const [currentCity] = useState('Mumbai');
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <div 
      className="min-h-screen bg-[#1c053c] text-white flex flex-col font-sans relative overflow-x-hidden bg-fixed bg-cover bg-center"
      style={{
        backgroundImage: `linear-gradient(to bottom, rgba(28, 5, 60, 0.78), rgba(18, 3, 40, 0.92)), url('/purple-map-bg.jpg')`
      }}
    >
      {/* Background Liquid Vector Blob Accents */}
      <div 
        className="absolute -top-20 -left-20 w-[36rem] h-[36rem] bg-gradient-to-br from-[#7c3aed]/30 via-[#a855f7]/20 to-transparent rounded-full blur-3xl pointer-events-none z-0"
      />
      <div 
        className="absolute top-1/3 -right-20 w-[32rem] h-[32rem] bg-[#ffee00]/15 rounded-full blur-3xl pointer-events-none z-0"
      />
      <div 
        className="absolute bottom-10 -left-20 w-[32rem] h-[32rem] bg-[#00e5ff]/15 rounded-full blur-3xl pointer-events-none z-0"
      />

      {/* Main Navbar */}
      <Navbar 
        onLoginClick={() => setIsChatOpen(true)}
        onSignUpClick={() => setIsChatOpen(true)}
      />

      {/* Main Content Container - Hero Section Only */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-16 flex flex-col items-center justify-center relative z-10">
        
        {/* LANDING PAGE HERO SECTION */}
        <section id="hero" className="relative pt-6 pb-12 text-center flex flex-col items-center justify-center space-y-8">
          
          {/* CENTER TOP: BIG CLEAN CUTOUT KETTLI LOGO */}
          <div className="relative cursor-pointer animate-fade-in">
            <img 
              src="/kettli-logo.png" 
              alt="kettli Logo" 
              className="h-36 sm:h-52 md:h-64 w-auto object-contain hover:scale-105 transition-transform duration-300"
            />
          </div>

          {/* HERO BADGE */}
          <div className="space-y-4 max-w-4xl mx-auto">
            <p className="text-xl sm:text-2xl font-accent font-bold text-[#ffee00] tracking-wide">
              Har ghar har gali jaayegi khabar
            </p>

            {/* CLASSY HERO HEADLINE */}
            <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold font-heading text-white tracking-tight leading-[1.1]">
              Unfiltered Hyperlocal Intelligence for Every Street <span className="text-[#ffee00] font-marker font-normal">& Neighborhood.</span>
            </h1>

            {/* CLASSY HERO DESCRIPTION */}
            <p className="text-base sm:text-xl font-sans text-purple-100/90 leading-relaxed max-w-3xl mx-auto font-normal">
              Empowering citizens and urban commuters with real-time transit streams, climate telemetry, and instant AI insights. From arterial highways to quiet local lanes—stay seamlessly connected to the heartbeat of your city.
            </p>
          </div>

          {/* LANDING ACTION BUTTONS */}
          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <button 
              onClick={() => setIsChatOpen(true)}
              className="flex items-center gap-3 px-8 py-4 rounded-full bg-[#ffee00] text-black font-sans font-extrabold text-base hover:bg-[#ffe600] transition-all shadow-[0_0_30px_rgba(255,238,0,0.5)] hover:scale-105"
            >
              <div className="w-6 h-6 rounded-full bg-black text-[#ffee00] flex items-center justify-center">
                <Play className="w-3.5 h-3.5 fill-current ml-0.5" />
              </div>
              <span>Launch Live AI Assistant</span>
            </button>
          </div>
        </section>

      </main>

      {/* AI Chat Terminal Drawer */}
      <AIChatDrawer
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        city={currentCity}
      />
    </div>
  );
}

export default App;

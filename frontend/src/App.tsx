import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { AIChatDrawer } from './components/AIChatDrawer';
import { Play } from 'lucide-react';

export function App() {
  const [currentCity] = useState('Mumbai');
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <div 
      className="min-h-screen text-white flex flex-col font-sans relative overflow-x-hidden bg-cover bg-center"
      style={{
        backgroundImage: `linear-gradient(to bottom, rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.35)), url('/hero-bg.jpg')`
      }}
    >
      {/* Main Navbar */}
      <Navbar 
        onLoginClick={() => setIsChatOpen(true)}
        onSignUpClick={() => setIsChatOpen(true)}
      />

      {/* Main Content Container - Hero Section Only */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-12 flex flex-col items-center justify-center relative z-10">
        
        {/* LANDING PAGE HERO SECTION */}
        <section id="hero" className="relative pt-4 pb-10 text-center flex flex-col items-center justify-center space-y-6">
          
          {/* CENTER TOP: BIG CLEAN CUTOUT KETTLI LOGO */}
          <div className="relative cursor-pointer animate-fade-in">
            <img 
              src="/kettli-logo.png" 
              alt="kettli Logo" 
              className="h-40 sm:h-56 md:h-72 w-auto object-contain hover:scale-105 transition-transform duration-300 drop-shadow-[0_10px_25px_rgba(0,0,0,0.7)]"
            />
          </div>

          {/* HERO HEADLINE ONLY */}
          <div className="space-y-4 max-w-5xl mx-auto drop-shadow-[0_4px_12px_rgba(0,0,0,0.8)]">
            <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold font-heading text-white tracking-tight leading-[1.1]">
              Unfiltered Hyperlocal Intelligence for Every Street <span className="text-[#ffee00] font-marker font-normal">& Neighborhood.</span>
            </h1>
          </div>

          {/* LANDING ACTION BUTTON */}
          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <button 
              onClick={() => setIsChatOpen(true)}
              className="flex items-center gap-3 px-8 py-4 rounded-full bg-[#ffee00] text-black font-sans font-extrabold text-base hover:bg-[#ffe600] transition-all shadow-[0_0_35px_rgba(255,238,0,0.6)] hover:scale-105"
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

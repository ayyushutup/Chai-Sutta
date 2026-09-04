import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { WeatherWidget } from './components/WeatherWidget';
import { CityMoodWidget } from './components/CityMoodWidget';
import { NewsFeed } from './components/NewsFeed';
import { TrafficWidget } from './components/TrafficWidget';
import { ReportsFeed } from './components/ReportsFeed';
import { AIChatDrawer } from './components/AIChatDrawer';
import { EventsWidget } from './components/EventsWidget';
import { ArrowUpRight, Play, Cpu } from 'lucide-react';

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

      {/* Main Navbar (Status bar removed, logo top left, Log In / Sign Up buttons) */}
      <Navbar 
        onLoginClick={() => setIsChatOpen(true)}
        onSignUpClick={() => setIsChatOpen(true)}
      />

      {/* Main Content Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-16 relative z-10">
        
        {/* LANDING PAGE HERO SECTION */}
        <section id="hero" className="relative pt-6 pb-12 text-center flex flex-col items-center justify-center space-y-8">
          
          {/* CENTER TOP: BIG CLEAN CUTOUT KETTLI LOGO (NO SPARKLE / NO BOX) */}
          <div className="relative cursor-pointer animate-fade-in">
            <img 
              src="/kettli-logo.png" 
              alt="kettli Logo" 
              className="h-32 sm:h-48 md:h-56 w-auto object-contain hover:scale-105 transition-transform duration-300"
            />
          </div>

          {/* HERO BADGE (No borders, classy font text) */}
          <div className="space-y-4 max-w-4xl mx-auto">
            <p className="text-xl sm:text-2xl font-accent font-bold text-[#ffee00] tracking-wide">
              Har ghar har gali jaayegi khabar
            </p>

            {/* CLASSY NON-GENERIC HERO HEADLINE */}
            <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold font-heading text-white tracking-tight leading-[1.1]">
              Unfiltered Hyperlocal Intelligence for Every Street <span className="text-[#ffee00] font-marker font-normal">& Neighborhood.</span>
            </h1>

            {/* CLASSY PROFESSIONAL HERO DESCRIPTION */}
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
              <span>Launch Live Dashboard</span>
            </button>

            <a 
              href="#telemetry"
              className="flex items-center gap-2 px-8 py-4 rounded-full bg-[#27084e]/90 text-white border border-purple-400/30 font-sans font-bold text-base hover:border-[#ffee00] hover:text-[#ffee00] transition-all hover:scale-105 backdrop-blur-md"
            >
              <span>Explore Live Telemetry</span>
              <ArrowUpRight className="w-5 h-5" />
            </a>
          </div>

          {/* Scroll Indicator */}
          <div className="pt-6">
            <a href="#telemetry" className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#27084e]/80 border border-purple-400/30 text-purple-200 font-sans text-xs hover:text-[#ffee00] hover:border-[#ffee00]/50 transition-all backdrop-blur-md">
              <span>Scroll Down to View Live Feeds</span>
            </a>
          </div>
        </section>


        {/* SECTION 1: SHOWREEL & LIVE MAUSAM TELEMETRY */}
        <section id="telemetry" className="scroll-mt-24">
          <WeatherWidget city={currentCity} />
        </section>


        {/* SECTION 2: FEATURED CITY FEEDS GRID */}
        <section id="feeds" className="scroll-mt-24 space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-[#ffee00] font-marker text-2xl">〰️</span>
              <h2 className="text-3xl font-heading font-extrabold text-white">
                FEATURED CITY FEEDS
              </h2>
            </div>
            <a href="#feeds" className="text-xs font-sans font-bold text-[#ffee00] flex items-center gap-1 hover:underline">
              <span>View All Feeds</span>
              <ArrowUpRight className="w-4 h-4" />
            </a>
          </div>

          {/* Grid Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <TrafficWidget />
            <CityMoodWidget />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <NewsFeed />
            </div>
            <div className="space-y-6">
              <ReportsFeed />
              <EventsWidget />
            </div>
          </div>
        </section>


        {/* SECTION 3: ENGINE STACK & APIS */}
        <section id="stack" className="scroll-mt-24 dark-card p-8 rounded-3xl bg-gradient-to-br from-[#27084e]/90 to-[#120327]/90 border border-purple-400/30 space-y-6 backdrop-blur-md">
          <div className="flex items-center justify-between border-b border-purple-400/20 pb-4">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-2xl bg-[#ffee00]/15 text-[#ffee00] border border-[#ffee00]/30">
                <Cpu className="w-6 h-6 stroke-[2.5]" />
              </div>
              <div>
                <h2 className="text-3xl font-heading font-extrabold text-white">
                  ENGINE STACK & TELEMETRY
                </h2>
                <p className="text-xs text-purple-200 font-sans">Powering real-time city vector search & telemetry</p>
              </div>
            </div>
            <span className="text-3xl text-[#ffee00] font-marker hidden sm:inline-block">➰</span>
          </div>

          {/* Icon Badges Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {[
              { name: 'FastAPI', category: 'Backend Engine', color: '#00e5ff', icon: '⚡' },
              { name: 'React 19', category: 'Frontend Framework', color: '#c084fc', icon: '⚛️' },
              { name: 'Python RAG', category: 'Qdrant Vectors', color: '#ffee00', icon: '🐍' },
              { name: 'Weather API', category: 'Climate Stream', color: '#ff9100', icon: '☀️' },
              { name: 'TomTom Mesh', category: 'Traffic Routing', color: '#ff2a00', icon: '🗺️' },
              { name: 'Lucide Icons', category: 'UI Telemetry', color: '#00ff66', icon: '🎨' },
            ].map((skill, idx) => (
              <div 
                key={idx} 
                className="dark-card p-4 rounded-2xl bg-[#180533]/90 border border-purple-400/20 hover:border-[#ffee00]/50 text-center space-y-2 group transition-all"
              >
                <div className="w-12 h-12 rounded-2xl bg-purple-950/60 border border-purple-400/20 mx-auto flex items-center justify-center text-2xl group-hover:scale-110 transition-transform" style={{ borderColor: skill.color }}>
                  {skill.icon}
                </div>
                <h4 className="font-sans font-bold text-white text-sm">{skill.name}</h4>
                <p className="text-[10px] font-mono text-purple-300">{skill.category}</p>
              </div>
            ))}
          </div>
        </section>


        {/* SECTION 4: ABOUT THE PLATFORM */}
        <section id="about" className="scroll-mt-24 grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
          {/* Left Yellow Accent Card */}
          <div className="lg:col-span-5 bg-[#ffee00] text-black rounded-3xl p-8 flex flex-col justify-between relative overflow-hidden shadow-[0_0_45px_rgba(255,238,0,0.5)]">
            <div className="space-y-4">
              <span className="bg-black text-[#ffee00] text-xs font-mono font-bold px-4 py-1.5 rounded-full inline-block">
                HAR GHAR HAR GALI JAAYEGI KHABAR
              </span>
              <h3 className="font-heading text-3xl sm:text-4xl font-extrabold uppercase leading-tight">
                HYPERLOCAL INTELLIGENCE PLATFORM
              </h3>
            </div>

            {/* Cutout Logo Graphic */}
            <div className="my-6 flex justify-center">
              <img src="/kettli-logo.png" alt="kettli" className="h-32 w-auto object-contain filter drop-shadow-[0_0_15px_rgba(0,0,0,0.5)]" />
            </div>

            <div className="font-mono text-xs font-extrabold uppercase tracking-wider text-black border-t-2 border-black/20 pt-3">
              EST. 2026 // kettli OS
            </div>
          </div>

          {/* Right Bio & Info Card */}
          <div className="lg:col-span-7 dark-card p-8 rounded-3xl bg-[#180533]/90 border border-purple-400/30 flex flex-col justify-between space-y-6 backdrop-blur-md">
            <div className="space-y-4">
              <h2 className="text-3xl font-heading font-extrabold text-white">
                ABOUT kettli
              </h2>
              <p className="text-sm text-purple-100 font-sans leading-relaxed">
                kettli is a hyperlocal real-time city intelligence platform with one core mission: <strong className="text-[#ffee00] font-bold">"Har ghar har gali jaayegi khabar!"</strong>
              </p>
              <p className="text-sm text-purple-100 font-sans leading-relaxed">
                We fuse live traffic streams, weather climate telemetry, citizen incident alerts, and AI vector search into a vibrant, high-energy dashboard.
              </p>
            </div>

            <div className="pt-4 border-t border-purple-400/20 flex items-center justify-between">
              <button 
                onClick={() => setIsChatOpen(true)}
                className="flex items-center gap-2 text-sm font-sans font-bold text-[#ffee00] hover:underline"
              >
                <span>Know More About kettli</span>
                <ArrowUpRight className="w-4 h-4" />
              </button>

              <span className="text-xs font-mono text-purple-300">v0.1.0_PROD</span>
            </div>
          </div>
        </section>


        {/* SECTION 5: FOOTER */}
        <footer className="pt-8 border-t border-purple-400/20 space-y-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            {/* Headline & Quote */}
            <div className="space-y-2 text-center md:text-left">
              <h2 className="text-3xl sm:text-4xl font-extrabold font-heading text-white tracking-wide">
                kettli<span className="text-[#ffee00]">.</span> HAR GHAR KHABAR
              </h2>
              <p className="text-sm font-accent font-bold text-[#ffee00]">
                "Har ghar har gali jaayegi khabar"
              </p>
            </div>

            {/* Contact Details & Mascot Gesture */}
            <div className="flex flex-col sm:flex-row items-center gap-6">
              <div className="text-center sm:text-right font-mono text-xs space-y-1">
                <p className="text-purple-100 font-bold">hello@kettli.io</p>
                <p className="text-purple-300">India 🇮🇳</p>
              </div>

              {/* Social Buttons */}
              <div className="flex items-center gap-2">
                {['📸', '🌐', '📺', '💼'].map((icon, i) => (
                  <button 
                    key={i}
                    className="w-10 h-10 rounded-full bg-[#27084e] border border-purple-400/20 hover:border-[#ffee00] hover:text-[#ffee00] flex items-center justify-center text-sm transition-all"
                  >
                    {icon}
                  </button>
                ))}
              </div>

              <div className="text-3xl font-marker rotate-12">
                ✌️
              </div>
            </div>
          </div>

          <div className="pt-6 border-t border-purple-400/10 flex flex-col sm:flex-row items-center justify-between text-xs font-mono text-purple-300 gap-4">
            <div>
              kettli OS // HAR GHAR HAR GALI JAAYEGI KHABAR 2026
            </div>
            <div className="flex gap-4">
              <a href="#" className="hover:text-white">PRIVACY</a>
              <a href="#" className="hover:text-white">TERMS</a>
              <a href="#" className="hover:text-white">API_DOCS</a>
            </div>
          </div>
        </footer>

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

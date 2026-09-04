import React from 'react';

interface NavbarProps {
  onLoginClick?: () => void;
  onSignUpClick?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  onLoginClick,
  onSignUpClick,
}) => {
  return (
    <header className="w-full bg-[#16042e]/90 backdrop-blur-xl sticky top-0 z-40 border-b border-purple-500/20 px-4 sm:px-8 py-4 shadow-[0_10px_30px_rgba(0,0,0,0.6)]">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        {/* Extreme Corner Left Logo */}
        <a href="#hero" className="flex items-center group">
          <img 
            src="/kettli-logo.png" 
            alt="kettli logo" 
            className="h-10 sm:h-12 w-auto object-contain transition-transform group-hover:scale-105"
          />
        </a>

        {/* Center Nav Links */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-semibold font-sans text-purple-100">
          <a href="#hero" className="text-[#ffee00] font-bold relative after:content-[''] after:absolute after:-bottom-1 after:left-0 after:w-full after:h-[2px] after:bg-[#ffee00]">
            Home
          </a>
          <a href="#telemetry" className="hover:text-[#ffee00] transition-colors">
            Telemetry
          </a>
          <a href="#feeds" className="hover:text-[#ffee00] transition-colors">
            Live Feeds
          </a>
          <a href="#stack" className="hover:text-[#ffee00] transition-colors">
            Stack
          </a>
          <a href="#about" className="hover:text-[#ffee00] transition-colors">
            About
          </a>
        </nav>

        {/* Right Section: Log In & Sign Up Buttons */}
        <div className="flex items-center gap-3">
          <button 
            onClick={onLoginClick}
            className="px-4 py-2 rounded-full text-xs font-semibold text-purple-200 hover:text-white hover:bg-purple-900/40 border border-purple-400/20 transition-all"
          >
            Log In
          </button>
          
          <button 
            onClick={onSignUpClick}
            className="px-5 py-2 rounded-full text-xs font-extrabold font-sans text-black bg-[#ffee00] hover:bg-[#ffe600] transition-all shadow-[0_0_20px_rgba(255,238,0,0.4)] hover:scale-105"
          >
            Sign Up
          </button>
        </div>
      </div>
    </header>
  );
};

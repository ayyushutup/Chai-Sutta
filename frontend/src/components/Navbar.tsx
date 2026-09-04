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
    <header className="w-full bg-gradient-to-r from-[#6d28ff]/85 via-[#7c3aed]/85 to-[#6d28ff]/85 backdrop-blur-xl sticky top-0 z-40 px-4 sm:px-8 py-3.5 shadow-[0_10px_30px_rgba(109,40,255,0.3)]">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        {/* Extreme Corner Left Logo */}
        <a href="#hero" className="flex items-center group">
          <img 
            src="/kettli-logo.png" 
            alt="kettli logo" 
            className="h-10 sm:h-12 w-auto object-contain transition-transform group-hover:scale-105"
          />
        </a>

        {/* Right Section: Log In & Sign Up Buttons */}
        <div className="flex items-center gap-3">
          <button 
            onClick={onLoginClick}
            className="px-4 py-2 rounded-full text-xs font-semibold text-purple-100 hover:text-white hover:bg-[#6d28ff]/40 border border-purple-300/30 transition-all"
          >
            Log In
          </button>
          
          <button 
            onClick={onSignUpClick}
            className="px-5 py-2 rounded-full text-xs font-extrabold font-sans text-black bg-[#ffee00] hover:bg-[#ffe600] transition-all shadow-[0_0_20px_rgba(255,238,0,0.5)] hover:scale-105"
          >
            Sign Up
          </button>
        </div>
      </div>
    </header>
  );
};

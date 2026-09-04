import React, { useState } from 'react';
import { Bot, Send, X, Sparkles, RefreshCw, MapPin } from 'lucide-react';
import { sendChatMessage } from '../services/api';

interface AIChatDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  city: string;
}

interface Message {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: string;
  sources?: string[];
}

export const AIChatDrawer: React.FC<AIChatDrawerProps> = ({ isOpen, onClose, city }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'm1',
      sender: 'ai',
      text: `Namaste! I am your kettli AI assistant for ${city}. "Har ghar har gali jaayegi khabar!" Ask me anything about local news, traffic streams, weather, or tea & coffee tapri recommendations!`,
      timestamp: 'Just now'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const quickPrompts = [
    `Is MG Road traffic clear right now?`,
    `What is the weather & AQI status?`,
    `Best quiet cafes with Wi-Fi in ${city}`,
    `Any breaking news or transit delays?`
  ];

  const handleSend = async (query?: string) => {
    const textToSend = query || input;
    if (!textToSend.trim()) return;

    const userMsg: Message = {
      id: 'u-' + Date.now(),
      sender: 'user',
      text: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!query) setInput('');
    setLoading(true);

    const apiResult = await sendChatMessage(textToSend, city);

    const aiMsg: Message = {
      id: 'a-' + Date.now(),
      sender: 'ai',
      text: apiResult.reply,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      sources: apiResult.sources?.map((s: any) => s.title || s.name || 'City Sensor') || ['kettli Telemetry']
    };

    setMessages((prev) => [...prev, aiMsg]);
    setLoading(false);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full sm:w-[440px] bg-[#16042e]/95 border-l border-purple-400/20 shadow-[0_0_50px_rgba(0,0,0,0.8)] flex flex-col backdrop-blur-2xl animate-fade-in font-sans">
      {/* Header */}
      <div className="p-4 border-b border-purple-400/20 flex items-center justify-between bg-[#1f063d]/90">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-2xl bg-[#ffee00]/15 text-[#ffee00] border border-[#ffee00]/30 shadow-[0_0_15px_rgba(255,238,0,0.3)]">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <h3 className="font-marker font-bold text-white text-lg">kettli AI Assistant</h3>
              <Sparkles className="w-4 h-4 text-[#ffee00]" />
            </div>
            <p className="text-[11px] text-purple-200 flex items-center gap-1">
              <MapPin className="w-3 h-3 text-[#ffee00]" /> Context: <span className="text-[#ffee00] font-semibold">{city} RAG Engine</span>
            </p>
          </div>
        </div>

        <button 
          onClick={onClose}
          className="p-2 rounded-full hover:bg-purple-900/40 text-purple-300 hover:text-white transition-all"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3.5">
        {messages.map(msg => (
          <div 
            key={msg.id}
            className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div className={`max-w-[88%] p-3.5 rounded-2xl text-xs leading-relaxed ${
              msg.sender === 'user' 
                ? 'bg-[#ffee00] text-black font-semibold rounded-tr-none shadow-[0_0_15px_rgba(255,238,0,0.3)]'
                : 'bg-[#1e073d] border border-purple-400/20 text-purple-100 rounded-tl-none'
            }`}>
              <div className="whitespace-pre-line">{msg.text}</div>

              {msg.sources && msg.sources.length > 0 && (
                <div className="mt-2.5 pt-2 border-t border-purple-400/20 space-y-1">
                  <div className="text-[10px] font-bold text-[#00e5ff] uppercase tracking-wider font-mono">Sources:</div>
                  <div className="flex flex-wrap gap-1">
                    {msg.sources.map((src, i) => (
                      <span key={i} className="text-[10px] px-2 py-0.5 rounded-full bg-[#120327] text-purple-200 border border-purple-400/20 font-mono">
                        {src}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
            <span className="text-[10px] font-mono text-purple-300 mt-1 px-1">{msg.timestamp}</span>
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2 text-xs text-[#ffee00] bg-[#ffee00]/10 p-3 rounded-xl border border-[#ffee00]/20 w-max font-mono">
            <RefreshCw className="w-4 h-4 animate-spin text-[#ffee00]" />
            <span>Scanning live news & RAG embeddings...</span>
          </div>
        )}
      </div>

      {/* Quick Prompts */}
      <div className="px-4 py-2 border-t border-purple-400/20 bg-[#1f063d]/50">
        <div className="text-[10px] font-bold text-purple-300 uppercase tracking-wider mb-1.5 font-mono">Suggested Prompts</div>
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
          {quickPrompts.map((qp, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(qp)}
              className="text-[11px] px-3 py-1 rounded-full bg-[#27084e] hover:bg-[#ffee00]/20 hover:text-[#ffee00] border border-purple-400/20 text-purple-200 whitespace-nowrap transition-all"
            >
              {qp}
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      <div className="p-3 border-t border-purple-400/20 bg-[#120327]">
        <div className="relative flex items-center">
          <input
            type="text"
            placeholder={`Ask kettli AI about ${city}...`}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            className="w-full bg-[#1f063d] border border-purple-400/20 rounded-full pl-4 pr-10 py-2.5 text-xs text-white placeholder-purple-300 focus:outline-none focus:border-[#ffee00]"
          />
          <button
            onClick={() => handleSend()}
            disabled={!input.trim()}
            className="absolute right-1.5 p-2 rounded-full bg-[#ffee00] text-black hover:bg-[#ffe600] disabled:opacity-40 transition-all shadow-[0_0_10px_rgba(255,238,0,0.3)]"
          >
            <Send className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};


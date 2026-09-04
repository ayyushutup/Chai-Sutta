import React, { useState } from 'react';
import { Newspaper, ThumbsUp, Bookmark, Share2, Clock, CheckCircle2 } from 'lucide-react';

interface NewsItem {
  id: string;
  title: string;
  category: 'Civic' | 'Traffic' | 'Weather' | 'Tech' | 'Culture';
  source: string;
  timeAgo: string;
  summary: string;
  upvotes: number;
  commentsCount: number;
  verified: boolean;
}

const SAMPLE_NEWS: NewsItem[] = [
  {
    id: '1',
    title: 'METRO LINE 3 EXPRESS CORRIDOR OPENED FOR PUBLIC COMMUTERS',
    category: 'Traffic',
    source: 'CITY_TRANSIT_AUTH',
    timeAgo: '18 MINS AGO',
    summary: 'Underground transit section reduces travel time by 35 minutes across central hubs during morning peak hours.',
    upvotes: 242,
    commentsCount: 38,
    verified: true,
  },
  {
    id: '2',
    title: 'AUTOMATED STORM DRAINS DEPLOYED IN LOW-LYING SECTORS',
    category: 'Civic',
    source: 'MUNICIPAL_BULLETIN',
    timeAgo: '42 MINS AGO',
    summary: 'Real-time water level telemetry connected to pump stations to avoid underpass flooding.',
    upvotes: 189,
    commentsCount: 15,
    verified: true,
  },
  {
    id: '3',
    title: 'ANNUAL LOCAL COFFEE & STREET CHAI FESTIVAL ANNOUNCED',
    category: 'Culture',
    source: 'URBAN_PULSE',
    timeAgo: '2 HOURS AGO',
    summary: 'Over 50 artisan brewers, street tapri masters, and live indie musical acts featured next weekend.',
    upvotes: 512,
    commentsCount: 84,
    verified: false,
  }
];

export const NewsFeed: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [news, setNews] = useState<NewsItem[]>(SAMPLE_NEWS);

  const categories = ['All', 'Traffic', 'Civic', 'Tech', 'Culture'];

  const filteredNews = selectedCategory === 'All' 
    ? news 
    : news.filter(item => item.category === selectedCategory);

  const handleUpvote = (id: string) => {
    setNews(prev => prev.map(item => item.id === id ? { ...item, upvotes: item.upvotes + 1 } : item));
  };

  return (
    <div className="dark-card p-6 sm:p-7 rounded-3xl relative overflow-hidden bg-[#180533] border border-purple-400/20 shadow-2xl space-y-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-purple-400/20 pb-4 gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-2xl bg-[#ffee00]/15 text-[#ffee00] border border-[#ffee00]/30">
            <Newspaper className="w-6 h-6 stroke-[2.5]" />
          </div>
          <div>
            <h3 className="font-marker font-extrabold text-white text-2xl tracking-wide">
              HYPERLOCAL NEWS STREAM
            </h3>
            <p className="text-xs text-purple-200 font-accent font-bold">Har ghar har gali jaayegi khabar ✨</p>
          </div>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
          {categories.map(cat => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3.5 py-1.5 rounded-full font-mono text-xs font-bold transition-all ${
                selectedCategory === cat 
                  ? 'bg-[#ffee00] text-black shadow-[0_0_15px_rgba(255,238,0,0.4)]' 
                  : 'bg-purple-950/60 text-purple-200 hover:text-white border border-purple-400/20'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* News Cards List */}
      <div className="space-y-4">
        {filteredNews.map(item => (
          <div 
            key={item.id} 
            className="p-4 rounded-2xl bg-[#120327] border border-purple-400/15 hover:border-[#ffee00]/40 transition-all space-y-3 group"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-mono font-bold text-[#ffee00] bg-[#ffee00]/15 border border-[#ffee00]/30 px-2.5 py-0.5 rounded-full">
                  {item.category}
                </span>
                <span className="font-mono text-xs text-purple-300 font-semibold">{item.source}</span>
                {item.verified && (
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#00ff66]" />
                )}
              </div>
              <span className="font-mono text-[11px] text-purple-300 flex items-center gap-1">
                <Clock className="w-3 h-3 text-[#ff9100]" /> {item.timeAgo}
              </span>
            </div>

            <h4 className="text-base sm:text-lg font-bold text-white group-hover:text-[#ffee00] transition-colors leading-snug font-sans">
              {item.title}
            </h4>

            <p className="text-xs text-purple-100 font-sans leading-relaxed">
              {item.summary}
            </p>

            <div className="flex items-center justify-between pt-2 border-t border-purple-400/10 font-mono text-xs">
              <button 
                onClick={() => handleUpvote(item.id)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#00ff66]/15 text-[#00ff66] border border-[#00ff66]/30 hover:bg-[#00ff66]/25 transition-colors font-bold"
              >
                <ThumbsUp className="w-3.5 h-3.5" />
                <span>Confirm ({item.upvotes})</span>
              </button>

              <div className="flex items-center gap-2">
                <button className="p-1.5 rounded-full bg-purple-900/40 border border-purple-400/20 text-purple-300 hover:text-white transition-colors">
                  <Bookmark className="w-3.5 h-3.5" />
                </button>
                <button className="p-1.5 rounded-full bg-purple-900/40 border border-purple-400/20 text-purple-300 hover:text-white transition-colors">
                  <Share2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

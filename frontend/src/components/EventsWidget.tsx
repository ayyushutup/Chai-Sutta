import React from 'react';
import { Calendar, MapPin, Clock, Users, ArrowUpRight } from 'lucide-react';

export const EventsWidget: React.FC = () => {
  const events = [
    {
      id: 'e1',
      title: 'Indie Music & Street Chai Night',
      date: 'Sat, Sep 12 • 6:30 PM',
      venue: 'Cubbon Amphitheatre',
      category: 'Music & Vibes',
      attendees: '340 interested',
    },
    {
      id: 'e2',
      title: 'Hyperlocal Tech Builders Meetup',
      date: 'Sun, Sep 13 • 4:00 PM',
      venue: 'WeWork Galaxy',
      category: 'Networking',
      attendees: '190 interested',
    }
  ];

  return (
    <div className="dark-card p-6 rounded-2xl relative overflow-hidden bg-[#180533] border border-purple-400/20 shadow-xl space-y-4 group hover:border-[#ffee00]/50 transition-all">
      <div className="flex items-center justify-between pb-3 border-b border-purple-400/20">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/30">
            <Calendar className="w-5 h-5 stroke-[2.5]" />
          </div>
          <div>
            <h3 className="font-marker font-bold text-white text-xl tracking-wide">
              LOCAL EVENTS
            </h3>
            <span className="text-[10px] font-mono text-purple-300">This Weekend</span>
          </div>
        </div>

        <div className="w-7 h-7 rounded-full bg-purple-900/40 border border-purple-400/30 flex items-center justify-center text-purple-200 group-hover:text-[#ffee00] group-hover:border-[#ffee00]/50 transition-all">
          <ArrowUpRight className="w-4 h-4" />
        </div>
      </div>

      <div className="space-y-3">
        {events.map(ev => (
          <div 
            key={ev.id} 
            className="p-3.5 rounded-xl bg-[#120327] border border-purple-400/15 hover:border-[#c084fc]/40 transition-all space-y-2"
          >
            <div className="flex items-center justify-between text-[11px]">
              <span className="px-2.5 py-0.5 rounded-full bg-[#c084fc]/20 text-[#c084fc] font-bold border border-[#c084fc]/30">
                {ev.category}
              </span>
              <span className="text-purple-300 flex items-center gap-1 font-mono text-[10px]">
                <Clock className="w-3 h-3 text-[#ff9100]" /> {ev.date}
              </span>
            </div>

            <h4 className="font-bold text-white text-xs hover:text-[#ffee00] transition-colors">
              {ev.title}
            </h4>

            <div className="flex items-center justify-between pt-2 border-t border-purple-400/10 text-[11px] text-purple-300">
              <span className="flex items-center gap-1 text-purple-100">
                <MapPin className="w-3 h-3 text-[#ffee00]" /> {ev.venue}
              </span>
              <span className="flex items-center gap-1 text-[#00e5ff] font-mono text-[10px]">
                <Users className="w-3 h-3" /> {ev.attendees}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { AlertCircle, ThumbsUp, MapPin, Plus, X } from 'lucide-react';

interface ReportItem {
  id: string;
  type: 'Waterlogging' | 'Roadblock' | 'Power Outage' | 'Accident' | 'Other';
  location: string;
  description: string;
  upvotes: number;
  timeAgo: string;
  status: 'Verified' | 'Investigating' | 'Resolved';
}

const SAMPLE_REPORTS: ReportItem[] = [
  {
    id: 'r1',
    type: 'Waterlogging',
    location: 'Underpass near Sector 14 Metro',
    description: 'Ankle-deep water accumulating after heavy evening rain. Avoid two-wheelers on left lane.',
    upvotes: 78,
    timeAgo: '12 mins ago',
    status: 'Verified'
  },
  {
    id: 'r2',
    type: 'Power Outage',
    location: 'Block C & D, Indiranagar',
    description: 'Transformer spark caused localized blackout. Linemen arriving shortly.',
    upvotes: 45,
    timeAgo: '25 mins ago',
    status: 'Investigating'
  },
  {
    id: 'r3',
    type: 'Roadblock',
    location: 'MG Road Junction',
    description: 'Fallen tree branch cleared by traffic police. Normal flow resuming.',
    upvotes: 110,
    timeAgo: '50 mins ago',
    status: 'Resolved'
  }
];

export const ReportsFeed: React.FC = () => {
  const [reports, setReports] = useState<ReportItem[]>(SAMPLE_REPORTS);
  const [showModal, setShowModal] = useState(false);
  const [newLocation, setNewLocation] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [newType, setNewType] = useState<ReportItem['type']>('Roadblock');

  const handleUpvote = (id: string) => {
    setReports(prev => prev.map(r => r.id === id ? { ...r, upvotes: r.upvotes + 1 } : r));
  };

  const handleCreateReport = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newLocation || !newDesc) return;
    
    const newReport: ReportItem = {
      id: 'r-' + Date.now(),
      type: newType,
      location: newLocation,
      description: newDesc,
      upvotes: 1,
      timeAgo: 'Just now',
      status: 'Investigating'
    };

    setReports([newReport, ...reports]);
    setShowModal(false);
    setNewLocation('');
    setNewDesc('');
  };

  return (
    <div className="dark-card p-6 sm:p-7 rounded-3xl relative overflow-hidden bg-[#180533] border border-purple-400/20 shadow-2xl space-y-5">
      <div className="flex items-center justify-between border-b border-purple-400/20 pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-2xl bg-[#ff2a00]/20 text-[#ff2a00] border border-[#ff2a00]/30">
            <AlertCircle className="w-6 h-6 stroke-[2.5]" />
          </div>
          <div>
            <h3 className="font-marker font-extrabold text-white text-2xl tracking-wide">
              CITIZEN REPORTS
            </h3>
            <p className="text-xs text-purple-200 font-sans">Crowdsourced real-time city alerts</p>
          </div>
        </div>

        <button 
          onClick={() => setShowModal(true)}
          className="flex items-center gap-1.5 px-4 py-2 rounded-full bg-[#ff2a00] text-white font-marker text-xs font-bold shadow-[0_0_15px_rgba(255,42,0,0.5)] hover:bg-[#e02500] transition-all hover:scale-105"
        >
          <Plus className="w-4 h-4" /> Report Issue
        </button>
      </div>

      {/* Reports List */}
      <div className="space-y-3.5">
        {reports.map(report => (
          <div key={report.id} className="p-4 rounded-2xl bg-[#120327] border border-purple-400/15 hover:border-[#ff2a00]/40 transition-all space-y-2">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className={`text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full ${
                  report.type === 'Waterlogging' ? 'bg-blue-500/20 text-blue-300 border border-blue-500/40' :
                  report.type === 'Power Outage' ? 'bg-[#ff9100]/20 text-[#ff9100] border border-[#ff9100]/40' :
                  report.type === 'Accident' ? 'bg-[#ff2a00]/20 text-red-300 border border-[#ff2a00]/40' :
                  'bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40'
                }`}>
                  {report.type}
                </span>

                <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                  report.status === 'Verified' ? 'text-[#00ff66] bg-[#00ff66]/10 border border-[#00ff66]/30' :
                  report.status === 'Resolved' ? 'text-[#00e5ff] bg-[#00e5ff]/10 border border-[#00e5ff]/30' :
                  'text-[#ff9100] bg-[#ff9100]/10 border border-[#ff9100]/30'
                }`}>
                  {report.status}
                </span>
              </div>

              <span className="text-[11px] font-mono text-purple-300">{report.timeAgo}</span>
            </div>

            <div className="text-xs font-bold text-white flex items-center gap-1.5">
              <MapPin className="w-3.5 h-3.5 text-[#ffee00] shrink-0" />
              {report.location}
            </div>

            <p className="text-xs text-purple-100 leading-relaxed">
              {report.description}
            </p>

            <div className="flex items-center justify-between pt-2 border-t border-purple-400/10 text-xs">
              <button 
                onClick={() => handleUpvote(report.id)}
                className="flex items-center gap-1.5 text-purple-200 hover:text-[#ffee00] transition-colors font-bold font-mono text-[11px]"
              >
                <ThumbsUp className="w-3.5 h-3.5 text-[#ffee00]" />
                <span>Confirm ({report.upvotes})</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Submission Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
          <div className="dark-card max-w-md w-full p-6 space-y-4 relative border-[#ffee00]/40 bg-[#1e073d] shadow-[0_0_50px_rgba(255,238,0,0.3)]">
            <div className="flex items-center justify-between border-b border-purple-400/20 pb-3">
              <h3 className="text-lg font-bold font-marker text-white">Report Live Incident</h3>
              <button 
                onClick={() => setShowModal(false)}
                className="p-1 rounded-full text-purple-300 hover:text-white hover:bg-purple-900/40"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateReport} className="space-y-3 font-sans">
              <div>
                <label className="block text-xs font-semibold text-purple-200 mb-1">Incident Type</label>
                <select
                  value={newType}
                  onChange={(e) => setNewType(e.target.value as ReportItem['type'])}
                  className="w-full bg-[#120327] border border-purple-400/20 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-[#ffee00]"
                >
                  <option value="Roadblock">Roadblock / Jam</option>
                  <option value="Waterlogging">Waterlogging</option>
                  <option value="Power Outage">Power Outage</option>
                  <option value="Accident">Accident</option>
                  <option value="Other">Other Civic Issue</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-purple-200 mb-1">Exact Location / Landmark</label>
                <input
                  type="text"
                  placeholder="e.g. Near Koramangala 5th Block Signal"
                  value={newLocation}
                  onChange={(e) => setNewLocation(e.target.value)}
                  className="w-full bg-[#120327] border border-purple-400/20 rounded-xl px-3 py-2 text-xs text-white placeholder-purple-400 focus:outline-none focus:border-[#ffee00]"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-purple-200 mb-1">Details</label>
                <textarea
                  rows={3}
                  placeholder="Briefly describe what's happening..."
                  value={newDesc}
                  onChange={(e) => setNewDesc(e.target.value)}
                  className="w-full bg-[#120327] border border-purple-400/20 rounded-xl px-3 py-2 text-xs text-white placeholder-purple-400 focus:outline-none focus:border-[#ffee00]"
                  required
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-purple-400/20">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-full bg-purple-900/40 text-purple-200 text-xs font-semibold hover:bg-purple-800/40"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-full bg-[#ffee00] text-black text-xs font-marker font-bold hover:bg-[#ffe600]"
                >
                  Submit Live Report
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

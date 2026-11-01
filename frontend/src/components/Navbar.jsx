import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  BookOpen, 
  ShieldCheck, 
  LogOut, 
  Store, 
  FileText, 
  HandHeart, 
  HelpCircle,
  Sparkles
} from 'lucide-react';

export function Navbar() {
  const { user, logout, isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!isAuthenticated) return null;

  return (
    <nav className="glass-nav sticky top-0 z-50 py-3.5 px-4 md:px-8 border-b border-white/10 shadow-lg">
      <div className="max-w-7xl mx-auto flex items-center justify-between flex-wrap gap-4">
        {/* Brand Logo */}
        <Link to={isAdmin ? "/admin" : "/student"} className="flex items-center gap-2.5 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-300 flex items-center justify-center text-slate-900 shadow-md group-hover:scale-105 transition-transform">
            <Sparkles className="w-5 h-5 fill-slate-950/20 text-slate-950" />
          </div>
          <div className="flex flex-col">
            <span className="font-mono text-xl font-extrabold tracking-tight text-white flex items-center gap-2">
              NexShelf
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/30 text-indigo-300 border border-indigo-400/30">
                {isAdmin ? 'Admin Console' : 'Scholar OS'}
              </span>
            </span>
          </div>
        </Link>

        {/* Navigation Actions */}
        <div className="flex items-center gap-2 flex-wrap">
          {!isAdmin ? (
            <>
              <a 
                href="#marketplaceSection" 
                className="px-3.5 py-1.5 rounded-full text-xs font-semibold text-slate-200 bg-white/5 border border-white/10 hover:bg-emerald-500/20 hover:border-emerald-500/40 hover:text-white transition flex items-center gap-1.5"
              >
                <Store className="w-3.5 h-3.5 text-emerald-400" />
                Book Market
              </a>
              <a 
                href="#studyNotesSection" 
                className="px-3.5 py-1.5 rounded-full text-xs font-semibold text-slate-200 bg-white/5 border border-white/10 hover:bg-amber-500/20 hover:border-amber-500/40 hover:text-white transition flex items-center gap-1.5"
              >
                <FileText className="w-3.5 h-3.5 text-amber-400" />
                Study Notes
              </a>
              <a 
                href="#peerExchangeSection" 
                className="px-3.5 py-1.5 rounded-full text-xs font-semibold text-slate-200 bg-white/5 border border-white/10 hover:bg-cyan-500/20 hover:border-cyan-500/40 hover:text-white transition flex items-center gap-1.5"
              >
                <HandHeart className="w-3.5 h-3.5 text-cyan-400" />
                Swaps &amp; Grants
              </a>
            </>
          ) : (
            <Link 
              to="/student"
              className="px-3.5 py-1.5 rounded-full text-xs font-semibold text-slate-200 bg-white/5 border border-white/10 hover:bg-indigo-500/20 hover:border-indigo-500/40 hover:text-white transition flex items-center gap-1.5"
            >
              <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
              Student View
            </Link>
          )}

          {/* User Profile Pill */}
          <div className="px-3 py-1 rounded-full bg-white/10 border border-white/15 text-xs font-semibold text-slate-100 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="max-w-[120px] truncate">{user?.full_name || user?.email}</span>
          </div>

          {/* Logout */}
          <button
            onClick={handleLogout}
            className="px-3 py-1.5 rounded-full text-xs font-semibold text-slate-300 bg-white/5 border border-white/10 hover:bg-rose-500/20 hover:border-rose-500/40 hover:text-rose-200 transition flex items-center gap-1.5 cursor-pointer"
            title="Sign out of NexShelf"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Sign Out</span>
          </button>
        </div>
      </div>
    </nav>
  );
}


export default Navbar;

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Mail,
  Lock,
  Sparkles,
  AlertCircle,
  ArrowRight,
  Eye,
  EyeOff,
  BookOpen,
  Repeat,
  FileDown,
  ShieldAlert
} from 'lucide-react';

export function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const user = await login(email, password);
      if (user.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/student');
      }
    } catch (err) {
      setError(err.message || 'Authentication failed. Please verify your academic credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 sm:p-6 relative overflow-hidden bg-[#070b14] text-white selection:bg-indigo-500 selection:text-white">
      {/* Dynamic Cyber Aurora Background */}
      <div className="absolute top-[-10%] left-[-10%] w-[550px] h-[550px] rounded-full bg-gradient-to-tr from-indigo-600/25 to-violet-600/20 blur-[130px] pointer-events-none animate-pulse"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] rounded-full bg-gradient-to-bl from-cyan-500/20 to-blue-600/20 blur-[130px] pointer-events-none"></div>
      <div className="absolute top-[40%] right-[25%] w-[350px] h-[350px] rounded-full bg-amber-500/10 blur-[110px] pointer-events-none"></div>

      {/* Cyber Grid Overlay */}
      <div
        className="absolute inset-0 pointer-events-none opacity-20"
        style={{
          backgroundImage:
            'radial-gradient(circle at 1px 1px, rgba(255,255,255,0.15) 1px, transparent 0)',
          backgroundSize: '32px 32px'
        }}
      ></div>

      <div className="w-full max-w-[460px] relative z-10">
        {/* Top Status Pill */}
        <div className="flex justify-center mb-4">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/[0.06] border border-white/10 backdrop-blur-xl text-[11px] font-mono tracking-wider text-slate-300 shadow-lg">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span className="w-2 h-2 rounded-full bg-emerald-400 absolute"></span>
            <span className="text-slate-400">GATEWAY //</span>
            <span className="text-indigo-300 font-bold">NEXSHELF SCHOLAR OS v2.6</span>
          </div>
        </div>

        {/* Unique Glassmorphic Card */}
        <div className="rounded-[32px] bg-slate-900/75 backdrop-blur-2xl border border-white/15 shadow-[0_25px_60px_-15px_rgba(0,0,0,0.8),0_0_40px_-10px_rgba(99,102,241,0.25)] overflow-hidden transition-all duration-300 hover:border-white/25">
          {/* Brand Header */}
          <div className="pt-8 pb-6 px-8 text-center relative border-b border-white/[0.08] bg-gradient-to-b from-white/[0.04] to-transparent">
            {/* Holographic Glowing Icon Badge */}
            <div className="relative inline-flex items-center justify-center mb-4">
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-amber-400 via-indigo-500 to-cyan-400 blur-lg opacity-70 animate-pulse"></div>
              <div className="relative w-16 h-16 rounded-2xl bg-gradient-to-tr from-amber-400 via-amber-300 to-amber-200 text-slate-950 flex items-center justify-center shadow-xl border border-white/30 transform transition hover:rotate-6 hover:scale-105 duration-300">
                <Sparkles className="w-8 h-8 fill-slate-950/20" />
              </div>
            </div>

            <h1 className="font-mono text-3xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-indigo-200 bg-clip-text text-transparent">
              NexShelf
            </h1>
            <p className="text-slate-400 text-xs mt-1.5 font-medium tracking-wide">
              Smart Academic Library &amp; Scholar Suite
            </p>
          </div>

          {/* Form Body */}
          <div className="p-7 sm:p-8">
            {error && (
              <div className="mb-5 p-3.5 rounded-2xl bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs font-semibold flex items-center gap-2.5 animate-shake">
                <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Email Input */}
              <div>
                <label className="block text-[11px] font-mono font-bold uppercase tracking-wider text-slate-300 mb-1.5">
                  University / Academic Email
                </label>
                <div className="relative group">
                  <Mail className="w-4 h-4 text-slate-400 group-focus-within:text-indigo-400 absolute left-3.5 top-1/2 -translate-y-1/2 transition" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="student@nexshelf.edu"
                    className="w-full pl-10 pr-4 py-3 rounded-2xl border border-slate-700/80 bg-slate-950/60 focus:bg-slate-950 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/40 focus:border-indigo-400 transition shadow-inner"
                  />
                </div>
              </div>

              {/* Password Input with Show/Hide */}
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="block text-[11px] font-mono font-bold uppercase tracking-wider text-slate-300">
                    Security Passcode
                  </label>
                  <span className="text-[11px] text-slate-400 hover:text-indigo-300 transition cursor-pointer">
                    Forgot?
                  </span>
                </div>
                <div className="relative group">
                  <Lock className="w-4 h-4 text-slate-400 group-focus-within:text-indigo-400 absolute left-3.5 top-1/2 -translate-y-1/2 transition" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••••••"
                    className="w-full pl-10 pr-11 py-3 rounded-2xl border border-slate-700/80 bg-slate-950/60 focus:bg-slate-950 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/40 focus:border-indigo-400 transition shadow-inner"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200 transition cursor-pointer p-1"
                    title={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full mt-2 py-3.5 px-6 rounded-2xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-cyan-500 hover:from-indigo-500 hover:via-indigo-400 hover:to-cyan-400 text-white font-mono font-bold text-sm tracking-wider uppercase shadow-[0_10px_25px_-5px_rgba(79,70,229,0.5)] hover:shadow-[0_15px_30px_-5px_rgba(79,70,229,0.7)] hover:-translate-y-0.5 active:translate-y-0 transition duration-200 flex items-center justify-center gap-2.5 disabled:opacity-60 cursor-pointer border border-white/20"
              >
                <span>{loading ? 'Authenticating Scholar…' : 'Sign In To Portal'}</span>
                {!loading && <ArrowRight className="w-4 h-4" />}
              </button>
            </form>

            {/* Feature Highlights Strip */}
            <div className="mt-6 pt-5 border-t border-white/[0.08] grid grid-cols-3 gap-2 text-center">
              <div className="p-2 rounded-xl bg-white/[0.03] border border-white/[0.05]">
                <BookOpen size={14} className="mx-auto text-indigo-400 mb-1" />
                <div className="text-[10px] font-mono text-slate-300 font-bold">330+ Books</div>
                <div className="text-[9px] text-slate-500">Live Catalog</div>
              </div>
              <div className="p-2 rounded-xl bg-white/[0.03] border border-white/[0.05]">
                <Repeat size={14} className="mx-auto text-cyan-400 mb-1" />
                <div className="text-[10px] font-mono text-slate-300 font-bold">Buy/Sell</div>
                <div className="text-[9px] text-slate-500">Peer Exchange</div>
              </div>
              <div className="p-2 rounded-xl bg-white/[0.03] border border-white/[0.05]">
                <FileDown size={14} className="mx-auto text-amber-400 mb-1" />
                <div className="text-[10px] font-mono text-slate-300 font-bold">PDF Notes</div>
                <div className="text-[9px] text-slate-500">Up &amp; Download</div>
              </div>
            </div>

            {/* Footer */}
            <div className="mt-5 pt-4 border-t border-white/[0.08] flex items-center justify-between text-xs text-slate-400">
              <span>
                Need a student card?{' '}
                <Link to="/register" className="font-bold text-indigo-400 hover:text-indigo-300 underline underline-offset-2">
                  Sign up
                </Link>
              </span>
              <Link to="/contact" className="hover:text-slate-200 transition text-slate-400">
                Help Desk
              </Link>
            </div>
          </div>
        </div>

        {/* Ambient Footer Tag */}
        <p className="text-center text-[11px] font-mono text-slate-600 mt-4">
          Powered by NexShelf Smart Engine &bull; End-to-End Encrypted Session
        </p>
      </div>
    </div>
  );
}

export default Login;

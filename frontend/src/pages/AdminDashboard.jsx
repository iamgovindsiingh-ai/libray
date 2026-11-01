import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import {
  ShieldAlert,
  BookOpen,
  Users,
  Repeat,
  Heart,
  Store,
  FileText,
  Mail,
  Plus,
  Trash2,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Search,
  RefreshCw,
  Library,
  DollarSign
} from 'lucide-react';

export default function AdminDashboard() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('books');
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [statusMsg, setStatusMsg] = useState(null);

  // Stats
  const [stats, setStats] = useState({
    total_books: 0,
    active_issues: 0,
    overdue_issues: 0,
    total_fines: 0
  });

  // Tab data collections
  const [books, setBooks] = useState([]);
  const [members, setMembers] = useState([]);
  const [requests, setRequests] = useState([]);
  const [offers, setOffers] = useState([]);
  const [notes, setNotes] = useState([]);
  const [messages, setMessages] = useState([]);

  // Search filter
  const [query, setQuery] = useState('');

  // Form Modals / Inputs
  const [showAddBookModal, setShowAddBookModal] = useState(false);
  const [newBook, setNewBook] = useState({
    title: '',
    author: '',
    category: 'Computer Science',
    quantity: 5,
    shelf_location: 'Zone A · Rack 01 · Shelf 1',
    description: '',
    difficulty_level: 'Intermediate',
    accent_color: '#4f46e5'
  });

  // Member Management State
  const [showAddMemberModal, setShowAddMemberModal] = useState(false);
  const [newMember, setNewMember] = useState({
    student_id: '',
    full_name: '',
    email: '',
    department: 'Computer Science',
    year: '1st Year',
    phone: '',
    password: 'student123'
  });

  // Quick Delete Tool
  const [quickDeleteId, setQuickDeleteId] = useState('');

  const [issueForm, setIssueForm] = useState({ book_id: '', member_id: '' });
  const [returnForm, setReturnForm] = useState({ issue_id: '' });

  const notify = (msg, isError = false) => {
    setStatusMsg({ text: msg, isError });
    setTimeout(() => setStatusMsg(null), 4000);
  };

  const loadAllData = async () => {
    setRefreshing(true);
    try {
      const [statsRes, booksRes, membersRes, reqRes, offersRes, notesRes, msgRes] = await Promise.allSettled([
        api.get('/dashboard/stats'),
        api.get('/books'),
        api.get('/members'),
        api.get('/requests'),
        api.get('/offers'),
        api.get('/notes'),
        api.get('/contact/messages')
      ]);

      if (statsRes.status === 'fulfilled') setStats(statsRes.value || {});
      if (booksRes.status === 'fulfilled') setBooks(booksRes.value?.books || booksRes.value || []);
      if (membersRes.status === 'fulfilled') setMembers(membersRes.value?.members || membersRes.value || []);
      if (reqRes.status === 'fulfilled') setRequests(reqRes.value?.requests || reqRes.value || []);
      if (offersRes.status === 'fulfilled') setOffers(offersRes.value?.offers || offersRes.value || []);
      if (notesRes.status === 'fulfilled') setNotes(notesRes.value?.notes || notesRes.value || []);
      if (msgRes.status === 'fulfilled') setMessages(msgRes.value?.messages || msgRes.value || []);
    } catch (err) {
      console.error('Failed to load admin data:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadAllData();
  }, []);

  // Action Handlers
  const handleCreateBook = async (e) => {
    e.preventDefault();
    try {
      await api.post('/books', newBook);
      notify('New volume cataloged successfully!');
      setShowAddBookModal(false);
      setNewBook({
        title: '',
        author: '',
        category: 'Computer Science',
        quantity: 5,
        shelf_location: 'Zone A · Rack 01 · Shelf 1',
        description: '',
        difficulty_level: 'Intermediate',
        accent_color: '#4f46e5'
      });
      loadAllData();
    } catch (err) {
      notify(err.message || 'Failed to create volume', true);
    }
  };

  const handleDeleteBook = async (id) => {
    if (!window.confirm(`Are you sure you want to remove volume #${id} from library inventory?`)) return;
    try {
      await api.delete(`/books/${id}`);
      notify('Volume successfully removed from library inventory.');
      setBooks((prev) => prev.filter((b) => b.id !== id));
      loadAllData();
    } catch (err) {
      notify(err.message || 'Failed to delete volume', true);
    }
  };

  const handleQuickDeleteBook = (e) => {
    e.preventDefault();
    if (!quickDeleteId) return;
    handleDeleteBook(parseInt(quickDeleteId));
    setQuickDeleteId('');
  };

  const handleCreateMember = async (e) => {
    e.preventDefault();
    try {
      await api.post('/members', newMember);
      notify(`Student Member "${newMember.full_name}" registered successfully!`);
      setShowAddMemberModal(false);
      setNewMember({
        student_id: '',
        full_name: '',
        email: '',
        department: 'Computer Science',
        year: '1st Year',
        phone: '',
        password: 'student123'
      });
      loadAllData();
    } catch (err) {
      notify(err.message || 'Failed to enroll member', true);
    }
  };

  const handleDeleteMember = async (id, studentId) => {
    if (!window.confirm(`Are you sure you want to remove student member ${studentId || '#' + id}?`)) return;
    try {
      await api.delete(`/members/${id}`);
      notify(`Member ${studentId || '#' + id} removed.`);
      setMembers((prev) => prev.filter((m) => m.id !== id));
    } catch (err) {
      notify(err.message || 'Failed to remove member', true);
    }
  };

  const handleIssueBook = async (e) => {
    e.preventDefault();
    try {
      await api.post('/issues', issueForm);
      notify(`Volume #${issueForm.book_id} issued to Member #${issueForm.member_id}`);
      setIssueForm({ book_id: '', member_id: '' });
      loadAllData();
    } catch (err) {
      notify(err.message || 'Issue operation failed', true);
    }
  };

  const handleReturnBook = async (e) => {
    e.preventDefault();
    try {
      await api.post('/returns', returnForm);
      notify(`Issue #${returnForm.issue_id} checked in successfully!`);
      setReturnForm({ issue_id: '' });
      loadAllData();
    } catch (err) {
      notify(err.message || 'Return check-in failed', true);
    }
  };

  const handleRequestStatus = async (id, status) => {
    try {
      await api.put(`/requests/${id}/status`, { status });
      notify(`Request #${id} marked as ${status}`);
      setRequests((prev) => prev.map((r) => (r.id === id ? { ...r, status } : r)));
    } catch (err) {
      notify(err.message || 'Failed to update request', true);
    }
  };

  const handleDeleteRequest = async (id) => {
    if (!window.confirm('Dismiss this acquisition request?')) return;
    try {
      await api.delete(`/requests/${id}`);
      setRequests((prev) => prev.filter((r) => r.id !== id));
      notify('Request dismissed.');
    } catch (err) {
      notify(err.message || 'Failed to delete request', true);
    }
  };

  const handleOfferStatus = async (id, status) => {
    try {
      await api.put(`/offers/${id}/status`, { status });
      notify(`Listing #${id} status set to ${status}`);
      setOffers((prev) => prev.map((o) => (o.id === id ? { ...o, status } : o)));
    } catch (err) {
      notify(err.message || 'Failed to update offer', true);
    }
  };

  const handleDeleteOffer = async (id) => {
    if (!window.confirm('Delete this peer marketplace listing?')) return;
    try {
      await api.delete(`/offers/${id}`);
      setOffers((prev) => prev.filter((o) => o.id !== id));
      notify('Listing removed.');
    } catch (err) {
      notify(err.message || 'Failed to remove listing', true);
    }
  };

  const handleDeleteNote = async (id) => {
    if (!window.confirm('Delete this courseware note?')) return;
    try {
      await api.delete(`/notes/${id}`);
      setNotes((prev) => prev.filter((n) => n.id !== id));
      notify('Note removed.');
    } catch (err) {
      notify(err.message || 'Failed to delete note', true);
    }
  };

  const handleDeleteMessage = async (id) => {
    if (!window.confirm('Delete this contact inquiry?')) return;
    try {
      await api.delete(`/contact/messages/${id}`);
      setMessages((prev) => prev.filter((m) => m.id !== id));
      notify('Inquiry deleted.');
    } catch (err) {
      notify(err.message || 'Failed to delete message', true);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Toast Banner */}
      {statusMsg && (
        <div
          className={`mb-6 p-4 rounded-xl border flex items-center justify-between shadow-lg transition-all ${
            statusMsg.isError
              ? 'bg-rose-50 border-rose-200 text-rose-800'
              : 'bg-emerald-50 border-emerald-200 text-emerald-800'
          }`}
        >
          <span className="font-semibold text-sm">{statusMsg.text}</span>
          <button onClick={() => setStatusMsg(null)} className="text-xs uppercase font-bold tracking-wider ml-4 opacity-70 hover:opacity-100">
            Dismiss
          </button>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-100 text-indigo-700 text-xs font-bold uppercase tracking-wider mb-2">
            <ShieldAlert size={14} /> Executive Command Center
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight font-heading">
            Library Control Console
          </h1>
          <p className="text-slate-500 text-sm mt-1">
            Supervise catalog inventory, circulation desk operations, member registrations, and student community submissions.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={loadAllData}
            disabled={refreshing}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-700 text-sm font-semibold hover:bg-slate-50 transition shadow-sm"
          >
            <RefreshCw size={16} className={refreshing ? 'animate-spin text-indigo-600' : ''} />
            <span>Sync Data</span>
          </button>
          <button
            onClick={() => setShowAddBookModal(true)}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-700 text-white text-sm font-bold shadow-md shadow-indigo-200 hover:from-indigo-500 hover:to-indigo-600 transition"
          >
            <Plus size={16} />
            <span>Add Volume</span>
          </button>
        </div>
      </div>

      {/* KPI Stats Reels */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm relative overflow-hidden group hover:border-indigo-300 transition">
          <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-3">
            <BookOpen size={20} />
          </div>
          <div className="text-3xl font-extrabold text-slate-900 font-mono tracking-tight">
            {stats.total_books || books.length}
          </div>
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mt-1">
            Total Catalog Titles
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm relative overflow-hidden group hover:border-emerald-300 transition">
          <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-3">
            <Repeat size={20} />
          </div>
          <div className="text-3xl font-extrabold text-slate-900 font-mono tracking-tight">
            {stats.active_issues || 0}
          </div>
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mt-1">
            Active Circulations
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm relative overflow-hidden group hover:border-rose-300 transition">
          <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center mb-3">
            <AlertTriangle size={20} />
          </div>
          <div className="text-3xl font-extrabold text-rose-600 font-mono tracking-tight">
            {stats.overdue_issues || 0}
          </div>
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mt-1">
            Overdue Borrowings
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm relative overflow-hidden group hover:border-amber-300 transition">
          <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center mb-3">
            <DollarSign size={20} />
          </div>
          <div className="text-3xl font-extrabold text-amber-600 font-mono tracking-tight">
            ${stats.total_fines || 0}
          </div>
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mt-1">
            Outstanding Penalties
          </div>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="flex border-b border-slate-200 mb-6 overflow-x-auto scrollbar-none gap-2">
        {[
          { id: 'books', label: 'Books Catalog', icon: BookOpen, count: books.length },
          { id: 'circulation', label: 'Circulation Desk', icon: Repeat },
          { id: 'members', label: 'Member Registry', icon: Users, count: members.length },
          { id: 'requests', label: 'Student Wishlists', icon: Heart, count: requests.length },
          { id: 'offers', label: 'Marketplace Posts', icon: Store, count: offers.length },
          { id: 'notes', label: 'Courseware Vault', icon: FileText, count: notes.length },
          { id: 'messages', label: 'Inquiries Desk', icon: Mail, count: messages.length }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => {
                setActiveTab(tab.id);
                setQuery('');
              }}
              className={`flex items-center gap-2.5 px-4 py-3 text-sm font-bold border-b-2 whitespace-nowrap transition ${
                isActive
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300'
              }`}
            >
              <Icon size={16} />
              <span>{tab.label}</span>
              {typeof tab.count === 'number' && (
                <span
                  className={`text-xs px-2 py-0.5 rounded-full font-mono font-semibold ${
                    isActive ? 'bg-indigo-100 text-indigo-700' : 'bg-slate-100 text-slate-600'
                  }`}
                >
                  {tab.count}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* TAB CONTENT: BOOKS */}
      {activeTab === 'books' && (
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
          <div className="p-4 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/50">
            <div className="relative w-full sm:w-80">
              <Search size={16} className="absolute left-3 top-3 text-slate-400" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search catalog titles, authors, shelves..."
                className="w-full pl-9 pr-4 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowAddBookModal(true)}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs shadow-sm transition cursor-pointer"
              >
                <Plus size={14} /> <span>Add Volume</span>
              </button>
              {/* Quick Remove by ID */}
              <form onSubmit={handleQuickDeleteBook} className="flex items-center gap-1.5">
                <input
                  type="number"
                  placeholder="Remove ID"
                  value={quickDeleteId}
                  onChange={(e) => setQuickDeleteId(e.target.value)}
                  className="w-24 px-2.5 py-1.5 bg-white border border-slate-200 rounded-xl text-xs font-mono focus:outline-none focus:ring-1 focus:ring-rose-500"
                />
                <button
                  type="submit"
                  disabled={!quickDeleteId}
                  className="px-2.5 py-1.5 bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs rounded-xl transition disabled:opacity-40 cursor-pointer"
                  title="Remove book by ID"
                >
                  Delete
                </button>
              </form>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 border-b border-slate-100 text-xs uppercase tracking-wider text-slate-500 font-semibold">
                <tr>
                  <th className="px-6 py-3.5">ID</th>
                  <th className="px-6 py-3.5">Title & Author</th>
                  <th className="px-6 py-3.5">Discipline</th>
                  <th className="px-6 py-3.5">Shelf Location</th>
                  <th className="px-6 py-3.5">Inventory</th>
                  <th className="px-6 py-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {books
                  .filter(
                    (b) =>
                      b.title?.toLowerCase().includes(query.toLowerCase()) ||
                      b.author?.name?.toLowerCase().includes(query.toLowerCase()) ||
                      b.shelf_location?.toLowerCase().includes(query.toLowerCase())
                  )
                  .map((book) => (
                    <tr key={book.id} className="hover:bg-slate-50/80 transition">
                      <td className="px-6 py-4 font-mono text-xs text-slate-400">#{book.id}</td>
                      <td className="px-6 py-4">
                        <div className="font-bold text-slate-900">{book.title}</div>
                        <div className="text-xs text-slate-500">{book.author?.name || book.author || 'Unknown Author'}</div>
                      </td>
                      <td className="px-6 py-4">
                        <span className="px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 text-xs font-semibold">
                          {book.category?.name || book.category || 'General'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-xs font-mono text-slate-600">
                        {book.shelf_location || 'Zone A · Rack 01'}
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={`font-mono text-xs font-bold px-2 py-0.5 rounded ${
                            book.available_quantity > 0
                              ? 'bg-emerald-50 text-emerald-700'
                              : 'bg-rose-50 text-rose-700'
                          }`}
                        >
                          {book.available_quantity ?? book.quantity ?? 0} In Stock
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button
                          onClick={() => handleDeleteBook(book.id)}
                          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs border border-rose-200/60 shadow-sm transition cursor-pointer"
                          title={`Remove volume "${book.title}" from catalog`}
                        >
                          <Trash2 size={13} />
                          <span>Remove</span>
                        </button>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB CONTENT: CIRCULATION */}
      {activeTab === 'circulation' && (
        <div className="grid md:grid-cols-2 gap-6">
          {/* Issue Book Card */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
                <BookOpen size={20} />
              </div>
              <div>
                <h3 className="font-bold text-slate-900">Issue Volume to Member</h3>
                <p className="text-xs text-slate-500">Record an outgoing loan for a student or faculty account.</p>
              </div>
            </div>
            <form onSubmit={handleIssueBook} className="space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">Book ID</label>
                <input
                  type="number"
                  required
                  placeholder="e.g. 1"
                  value={issueForm.book_id}
                  onChange={(e) => setIssueForm({ ...issueForm, book_id: e.target.value })}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">Member ID</label>
                <input
                  type="number"
                  required
                  placeholder="e.g. 1"
                  value={issueForm.member_id}
                  onChange={(e) => setIssueForm({ ...issueForm, member_id: e.target.value })}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <button
                type="submit"
                className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl text-sm shadow transition"
              >
                Confirm Issue Record
              </button>
            </form>
          </div>

          {/* Check In / Return Card */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
                <Repeat size={20} />
              </div>
              <div>
                <h3 className="font-bold text-slate-900">Circulation Check-In (Return)</h3>
                <p className="text-xs text-slate-500">Restore inventory quantity and compute applicable overdue fines.</p>
              </div>
            </div>
            <form onSubmit={handleReturnBook} className="space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">Issue Record ID</label>
                <input
                  type="number"
                  required
                  placeholder="e.g. 1"
                  value={returnForm.issue_id}
                  onChange={(e) => setReturnForm({ issue_id: e.target.value })}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 text-xs text-slate-600">
                Returns automatically adjust the book's available stock and calculate daily overdue rates if returned past the due date.
              </div>
              <button
                type="submit"
                className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm shadow transition"
              >
                Complete Check-In
              </button>
            </form>
          </div>
        </div>
      )}

      {/* TAB CONTENT: MEMBERS (ADD & REMOVE SCHOLAR OPTIONS) */}
      {activeTab === 'members' && (
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
          {/* Header Action Bar */}
          <div className="p-5 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/60">
            <div>
              <h3 className="font-extrabold text-slate-900 text-base font-heading">
                Enrolled Scholars &amp; Member Cards
              </h3>
              <p className="text-xs text-slate-500">
                Manage registered students and active library card privileges ({members.length} Total).
              </p>
            </div>
            <button
              onClick={() => setShowAddMemberModal(true)}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white font-bold text-xs shadow-md shadow-indigo-600/20 transition cursor-pointer"
            >
              <Plus size={16} /> <span>Add New Member</span>
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 border-b border-slate-100 text-xs uppercase tracking-wider text-slate-500 font-semibold">
                <tr>
                  <th className="px-6 py-3.5">Student ID</th>
                  <th className="px-6 py-3.5">Student Name / Email</th>
                  <th className="px-6 py-3.5">Department</th>
                  <th className="px-6 py-3.5">Phone Number</th>
                  <th className="px-6 py-3.5">Status</th>
                  <th className="px-6 py-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {members.map((m) => (
                  <tr key={m.id} className="hover:bg-slate-50/80 transition">
                    <td className="px-6 py-4 font-mono text-xs text-indigo-600 font-bold">
                      {m.student_id || `#${m.id}`}
                    </td>
                    <td className="px-6 py-4">
                      <div className="font-bold text-slate-900">{m.full_name || m.user?.full_name || m.name || 'Student Scholar'}</div>
                      <div className="text-xs text-slate-500">{m.email}</div>
                    </td>
                    <td className="px-6 py-4 text-xs text-slate-600">{m.department || 'Computer Science'}</td>
                    <td className="px-6 py-4 text-xs font-mono text-slate-600">{m.phone || 'N/A'}</td>
                    <td className="px-6 py-4">
                      <span className="px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-semibold">
                        Active
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={() => handleDeleteMember(m.id, m.student_id)}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs border border-rose-200/60 shadow-sm transition cursor-pointer"
                        title={`Remove member #${m.student_id}`}
                      >
                        <Trash2 size={13} />
                        <span>Remove Member</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB CONTENT: REQUESTS */}
      {activeTab === 'requests' && (
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
          <div className="p-4 bg-slate-50/50 border-b border-slate-100 text-xs text-slate-500 font-semibold">
            {requests.length} Student Book Acquisition Requests Submitted
          </div>
          <div className="divide-y divide-slate-100">
            {requests.map((r) => (
              <div key={r.id} className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50/50 transition">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-bold text-slate-900">{r.title}</span>
                    <span className="text-xs text-slate-500">by {r.author || 'Unknown'}</span>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider ${
                        r.status === 'approved'
                          ? 'bg-emerald-100 text-emerald-800'
                          : r.status === 'rejected'
                          ? 'bg-rose-100 text-rose-800'
                          : 'bg-amber-100 text-amber-800'
                      }`}
                    >
                      {r.status || 'Pending'}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 italic">"{r.notes || r.reason || 'No additional comment'}"</p>
                  <div className="text-[11px] text-slate-400 mt-1">Requested by: {r.student_name || r.user_email || 'Student'}</div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleRequestStatus(r.id, 'approved')}
                    className="px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-700 hover:bg-emerald-100 text-xs font-bold transition flex items-center gap-1"
                  >
                    <CheckCircle2 size={14} /> Approve
                  </button>
                  <button
                    onClick={() => handleRequestStatus(r.id, 'rejected')}
                    className="px-3 py-1.5 rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200 text-xs font-bold transition flex items-center gap-1"
                  >
                    <XCircle size={14} /> Reject
                  </button>
                  <button
                    onClick={() => handleDeleteRequest(r.id)}
                    className="p-1.5 text-rose-500 hover:bg-rose-50 rounded-lg transition"
                    title="Dismiss"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}
            {requests.length === 0 && (
              <div className="p-8 text-center text-slate-400 text-sm">No student requests currently pending.</div>
            )}
          </div>
        </div>
      )}

      {/* TAB CONTENT: OFFERS */}
      {activeTab === 'offers' && (
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
          <div className="p-4 bg-slate-50/50 border-b border-slate-100 text-xs text-slate-500 font-semibold">
            {offers.length} Student Peer Marketplace Listings
          </div>
          <div className="divide-y divide-slate-100">
            {offers.map((o) => (
              <div key={o.id} className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50/50 transition">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-bold text-slate-900">{o.title}</span>
                    <span className="text-xs text-slate-500">by {o.author}</span>
                    <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">
                      ${o.price || '0.00'}
                    </span>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 uppercase">
                      {o.condition || 'Good'}
                    </span>
                  </div>
                  <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 mt-1.5">
                    <span>{o.offer_type === 'sell' ? 'Seller: ' : 'Listed by: '}<strong className="text-slate-800">{o.donor_name || o.seller_name || o.contact_email || 'Student'}</strong></span>
                    {o.contact_phone && (
                      <span className="font-mono text-xs font-bold text-indigo-700 bg-indigo-50 px-2.5 py-0.5 rounded-md border border-indigo-200">
                        📞 Contact: {o.contact_phone}
                      </span>
                    )}
                    {o.pickup_location && (
                      <span className="text-slate-600">📍 {o.pickup_location}</span>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleOfferStatus(o.id, o.status === 'sold' ? 'available' : 'sold')}
                    className="px-3 py-1.5 rounded-xl border border-slate-200 text-xs font-bold text-slate-700 hover:bg-slate-50 transition cursor-pointer"
                  >
                    Toggle {o.status === 'sold' ? 'Available' : 'Sold'}
                  </button>
                  <button
                    onClick={() => handleDeleteOffer(o.id)}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs border border-rose-200/60 shadow-sm transition cursor-pointer"
                    title="Remove this listing from marketplace"
                  >
                    <Trash2 size={13} />
                    <span>Remove Listing</span>
                  </button>
                </div>
              </div>
            ))}
            {offers.length === 0 && (
              <div className="p-8 text-center text-slate-400 text-sm">No marketplace offers posted yet.</div>
            )}
          </div>
        </div>
      )}

      {/* TAB CONTENT: NOTES */}
      {activeTab === 'notes' && (
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
          <div className="p-4 bg-slate-50/50 border-b border-slate-100 text-xs text-slate-500 font-semibold">
            {notes.length} Courseware Study Materials Uploaded
          </div>
          <div className="divide-y divide-slate-100">
            {notes.map((n) => (
              <div key={n.id} className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50/50 transition">
                <div>
                  <div className="font-bold text-slate-900">{n.title}</div>
                  <div className="text-xs text-slate-500">{n.subject} &bull; Uploaded by {n.uploader_name || 'Scholar'}</div>
                </div>
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => handleDeleteNote(n.id)}
                    className="p-1.5 text-rose-500 hover:bg-rose-50 rounded-lg transition"
                    title="Remove Note"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}
            {notes.length === 0 && (
              <div className="p-8 text-center text-slate-400 text-sm">No study notes uploaded yet.</div>
            )}
          </div>
        </div>
      )}

      {/* TAB CONTENT: MESSAGES */}
      {activeTab === 'messages' && (
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
          <div className="p-4 bg-slate-50/50 border-b border-slate-100 text-xs text-slate-500 font-semibold">
            {messages.length} Desk Inquiries Received
          </div>
          <div className="divide-y divide-slate-100">
            {messages.map((m) => (
              <div key={m.id} className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50/50 transition">
                <div>
                  <div className="font-bold text-slate-900">{m.subject || 'General Inquiry'}</div>
                  <p className="text-xs text-slate-600 mt-1">{m.message}</p>
                  <div className="text-[11px] text-slate-400 mt-1">From: {m.name} ({m.email})</div>
                </div>
                <button
                  onClick={() => handleDeleteMessage(m.id)}
                  className="p-1.5 text-rose-500 hover:bg-rose-50 rounded-lg transition"
                  title="Delete Inquiry"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
            {messages.length === 0 && (
              <div className="p-8 text-center text-slate-400 text-sm">No inquiries in mailbox.</div>
            )}
          </div>
        </div>
      )}

      {/* MODAL: ENROLL NEW MEMBER (ADD MEMBER OPTION) */}
      {showAddMemberModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-7 shadow-2xl border border-slate-100 my-8">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div>
                <h3 className="font-bold text-lg text-slate-900">Enroll New Student Scholar</h3>
                <p className="text-xs text-slate-500">Issue an institutional library card to a university member.</p>
              </div>
              <button onClick={() => setShowAddMemberModal(false)} className="text-slate-400 hover:text-slate-600 p-1">
                <XCircle size={20} />
              </button>
            </div>
            <form onSubmit={handleCreateMember} className="mt-4 space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Student ID *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. STU-2026-042"
                    value={newMember.student_id}
                    onChange={(e) => setNewMember({ ...newMember, student_id: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm font-mono focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Aanya Sengupta"
                    value={newMember.full_name}
                    onChange={(e) => setNewMember({ ...newMember, full_name: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                  Email Address *
                </label>
                <input
                  type="email"
                  required
                  placeholder="aanya@nexshelf.edu"
                  value={newMember.email}
                  onChange={(e) => setNewMember({ ...newMember, email: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Department
                  </label>
                  <select
                    value={newMember.department}
                    onChange={(e) => setNewMember({ ...newMember, department: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="Computer Science">Computer Science</option>
                    <option value="Electronics">Electronics</option>
                    <option value="Mechanical">Mechanical</option>
                    <option value="Information Tech">Information Tech</option>
                    <option value="Civil Engineering">Civil Engineering</option>
                    <option value="Mathematics">Mathematics</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Academic Year
                  </label>
                  <select
                    value={newMember.year}
                    onChange={(e) => setNewMember({ ...newMember, year: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="1st Year">1st Year</option>
                    <option value="2nd Year">2nd Year</option>
                    <option value="3rd Year">3rd Year</option>
                    <option value="4th Year">4th Year</option>
                    <option value="Postgraduate">Postgraduate</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                  Contact Phone Number
                </label>
                <input
                  type="tel"
                  placeholder="+91 98765 43210"
                  value={newMember.phone}
                  onChange={(e) => setNewMember({ ...newMember, phone: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm font-mono focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowAddMemberModal(false)}
                  className="px-4 py-2.5 rounded-xl text-sm font-semibold text-slate-600 hover:bg-slate-100 transition cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow transition cursor-pointer"
                >
                  Confirm Registration
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ADD VOLUME MODAL */}
      {showAddBookModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-100">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <h3 className="font-bold text-lg text-slate-900">Catalog New Volume</h3>
              <button onClick={() => setShowAddBookModal(false)} className="text-slate-400 hover:text-slate-600">
                <XCircle size={20} />
              </button>
            </div>
            <form onSubmit={handleCreateBook} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase text-slate-600 mb-1">Book Title</label>
                <input
                  type="text"
                  required
                  value={newBook.title}
                  onChange={(e) => setNewBook({ ...newBook, title: e.target.value })}
                  placeholder="e.g. Structure and Interpretation of Computer Programs"
                  className="w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold uppercase text-slate-600 mb-1">Author</label>
                  <input
                    type="text"
                    required
                    value={newBook.author}
                    onChange={(e) => setNewBook({ ...newBook, author: e.target.value })}
                    placeholder="e.g. Harold Abelson"
                    className="w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold uppercase text-slate-600 mb-1">Quantity</label>
                  <input
                    type="number"
                    min="1"
                    required
                    value={newBook.quantity}
                    onChange={(e) => setNewBook({ ...newBook, quantity: parseInt(e.target.value) || 1 })}
                    className="w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-bold uppercase text-slate-600 mb-1">Shelf Location</label>
                <input
                  type="text"
                  value={newBook.shelf_location}
                  onChange={(e) => setNewBook({ ...newBook, shelf_location: e.target.value })}
                  placeholder="Zone A · Rack 01 · Shelf 1"
                  className="w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase text-slate-600 mb-1">Summary / Abstract</label>
                <textarea
                  rows="2"
                  value={newBook.description}
                  onChange={(e) => setNewBook({ ...newBook, description: e.target.value })}
                  placeholder="Brief synopsis of core topics covered..."
                  className="w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                ></textarea>
              </div>
              <div className="flex justify-end gap-3 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowAddBookModal(false)}
                  className="px-4 py-2 rounded-xl text-sm font-semibold text-slate-600 hover:bg-slate-100 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl text-sm font-bold bg-indigo-600 hover:bg-indigo-700 text-white shadow transition"
                >
                  Save & Catalog
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}


import React, { useState, useEffect, useRef } from 'react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import {
  Sparkles,
  BookOpen,
  Store,
  FileText,
  HandHeart,
  Search,
  Flame,
  Award,
  Clock,
  ShieldCheck,
  Plus,
  Upload,
  ExternalLink,
  Phone,
  Bookmark,
  Layers,
  ChevronRight,
  Filter,
  CheckCircle2,
  X,
  QrCode,
  Volume2,
  Quote,
  ThumbsUp,
  Eye,
  Grid,
  Columns,
  Copy,
  Check,
  SlidersHorizontal,
  Library,
  User,
  Heart,
  BookMarked,
  Download,
  Share2,
  ChevronLeft,
  FileCheck,
  ArrowUpRight,
  FileUp
} from 'lucide-react';

export default function StudentDashboard() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('notes'); // Open directly to notes vault
  const [viewMode, setViewMode] = useState('grid');
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);

  // Hidden File Inputs
  const fileInputModalRef = useRef(null);
  const fileInputInlineRef = useRef(null);

  // Core Collections
  const [books, setBooks] = useState([]);
  const [myIssues, setMyIssues] = useState([]);
  const [offers, setOffers] = useState([]);
  const [notes, setNotes] = useState([]);
  const [stats, setStats] = useState({ borrowed_books: 0, overdue_books: 0, fine_due: 0 });
  const [profile, setProfile] = useState({});
  const [gamification, setGamification] = useState({
    streak_days: 1,
    reading_score: 120,
    rank_title: 'Freshman Reader',
    badges: [],
    all_available_badges: []
  });

  // Filters & Search
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Notes Vault Filters & Sorting
  const [notesSubjectFilter, setNotesSubjectFilter] = useState('all');
  const [notesSemesterFilter, setNotesSemesterFilter] = useState('all');
  const [notesSortBy, setNotesSortBy] = useState('popular');
  const [notesSearch, setNotesSearch] = useState('');

  // Modals & Sections
  const [showInlineUploader, setShowInlineUploader] = useState(true);
  const [showUploadNoteModal, setShowUploadNoteModal] = useState(false);
  const [selectedBook, setSelectedBook] = useState(null);
  const [selectedNote, setSelectedNote] = useState(null);
  const [previewPageIndex, setPreviewPageIndex] = useState(1);
  const [showPassModal, setShowPassModal] = useState(false);
  const [showWishlistModal, setShowWishlistModal] = useState(false);
  const [showPostOfferModal, setShowPostOfferModal] = useState(false);

  // Upload State
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFileDetails, setUploadedFileDetails] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  // Note Form
  const [noteForm, setNoteForm] = useState({
    title: '',
    subject: 'Computer Science',
    department: 'Computer Science & Engineering',
    semester: 'Semester 4',
    description: '',
    file_url: '',
    file_type: 'pdf'
  });

  // Other Form States
  const [wishlistForm, setWishlistForm] = useState({ title: '', author: '', category: 'Computer Science', reason: '' });
  const [offerForm, setOfferForm] = useState({
    title: '',
    author: '',
    category: 'Computer Science',
    offer_type: 'sell',
    price: '',
    condition: 'Like New',
    donor_name: '',
    contact_phone: '',
    contact_whatsapp: '',
    pickup_location: 'Central Library Lawn / Reading Hall',
    description: '',
  });
  const [marketFilter, setMarketFilter] = useState('all');

  // Citation & Speech States
  const [copiedCitation, setCopiedCitation] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  // Local Note Likes
  const [likedNotes, setLikedNotes] = useState({});

  const showToast = (message, isError = false) => {
    setToast({ message, isError });
    setTimeout(() => setToast(null), 3500);
  };

  const loadAllStudentData = async () => {
    try {
      const [booksRes, statsRes, issuesRes, profileRes, gameRes, offersRes, notesRes] = await Promise.allSettled([
        api.get('/books'),
        api.get('/student/stats'),
        api.get('/student/issues'),
        api.get('/student/profile'),
        api.get('/student/gamification'),
        api.get('/offers'),
        api.get('/notes')
      ]);

      if (booksRes.status === 'fulfilled') setBooks(booksRes.value?.books || booksRes.value || []);
      if (statsRes.status === 'fulfilled') setStats(statsRes.value || {});
      if (issuesRes.status === 'fulfilled') setMyIssues(issuesRes.value?.issues || issuesRes.value || []);
      if (profileRes.status === 'fulfilled') setProfile(profileRes.value || {});
      if (gameRes.status === 'fulfilled') setGamification(gameRes.value || {});
      if (offersRes.status === 'fulfilled') setOffers(offersRes.value?.offers || offersRes.value || []);
      if (notesRes.status === 'fulfilled') setNotes(notesRes.value?.notes || notesRes.value || []);
    } catch (err) {
      console.error('Error fetching student dashboard state:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllStudentData();
  }, []);

  // Process Real File Selection (From Input or Drag & Drop)
  const processSelectedFile = (file) => {
    if (!file) return;
    setSelectedFile(file);
    const sizeStr = file.size > 1024 * 1024 ? `${(file.size / (1024 * 1024)).toFixed(1)} MB` : `${(file.size / 1024).toFixed(0)} KB`;
    setUploadedFileDetails({
      name: file.name,
      size: sizeStr,
      type: file.type.includes('pdf') ? 'PDF Document' : file.type.includes('image') ? 'Scan Image' : 'Document Deck'
    });

    // Auto-populate Title if empty
    if (!noteForm.title.trim()) {
      const cleanName = file.name.replace(/\.[^/.]+$/, '').replace(/[_-]/g, ' ');
      setNoteForm((prev) => ({
        ...prev,
        title: cleanName.charAt(0).toUpperCase() + cleanName.slice(1)
      }));
    }
    showToast(`Attached: ${file.name} (${sizeStr})`);
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) processSelectedFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) processSelectedFile(file);
  };

  // Action: Upload Study Note to Server & Database
  const handleNoteSubmit = async (e) => {
    e.preventDefault();

    if (!noteForm.title.trim()) {
      showToast('Please enter a document title.', true);
      return;
    }

    setIsUploading(true);
    setUploadProgress(20);

    let finalFileUrl = noteForm.file_url || 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=600&q=80';

    // 1. Upload Real File to Flask backend if user attached one
    if (selectedFile) {
      setUploadProgress(45);
      try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        const uploadRes = await api.upload('/upload', formData);
        if (uploadRes && uploadRes.url) {
          finalFileUrl = uploadRes.url;
        }
      } catch (uploadErr) {
        console.warn('Real file upload failed, using fallback document link:', uploadErr);
      }
    }

    setUploadProgress(75);

    // 2. Save Note Metadata in Database
    try {
      const payload = {
        title: noteForm.title,
        subject: noteForm.subject,
        department: noteForm.department,
        semester: noteForm.semester,
        description: noteForm.description || 'Verified courseware study deck.',
        file_url: finalFileUrl,
        file_type: selectedFile?.name?.endsWith('.pdf') ? 'pdf' : 'document',
        author_name: profile.full_name || user?.full_name || 'Scholar Contributor'
      };

      await api.post('/notes', payload);
      setUploadProgress(100);

      setTimeout(async () => {
        setIsUploading(false);
        setUploadProgress(0);
        setSelectedFile(null);
        setUploadedFileDetails(null);
        setShowUploadNoteModal(false);
        showToast('🎉 Courseware note published to vault! +50 Reading Points Awarded.');

        // Refresh Notes collection
        const updatedNotes = await api.get('/notes');
        setNotes(updatedNotes.notes || updatedNotes);

        // Reset form
        setNoteForm({
          title: '',
          subject: 'Computer Science',
          department: 'Computer Science & Engineering',
          semester: 'Semester 4',
          description: '',
          file_url: '',
          file_type: 'pdf'
        });
      }, 500);
    } catch (err) {
      setIsUploading(false);
      setUploadProgress(0);
      showToast(err.message || 'Failed to upload study note.', true);
    }
  };

  // Action: Live Upvote Note
  const handleLikeNote = async (noteId) => {
    setLikedNotes((prev) => ({
      ...prev,
      [noteId]: (prev[noteId] || 0) + 1
    }));
    try {
      await api.post(`/notes/${noteId}/like`);
      showToast('Upvoted study note! Contributor awarded scholar points.');
    } catch (err) {
      showToast('Upvoted note!');
    }
  };

  // Action: Borrow Book
  const handleBorrow = async (bookId) => {
    try {
      await api.post('/student/issues', { book_id: bookId });
      showToast('Volume checked out! Available at Circulation Desk.');
      setBooks((prev) =>
        prev.map((b) => (b.id === bookId ? { ...b, available_quantity: Math.max(0, (b.available_quantity ?? 1) - 1) } : b))
      );
      if (selectedBook && selectedBook.id === bookId) {
        setSelectedBook((prev) => ({ ...prev, available_quantity: Math.max(0, (prev.available_quantity ?? 1) - 1) }));
      }
      const [newStats, newIssues] = await Promise.all([api.get('/student/stats'), api.get('/student/issues')]);
      setStats(newStats);
      setMyIssues(newIssues.issues || newIssues);
    } catch (err) {
      showToast(err.message || 'Unable to borrow book at this time.', true);
    }
  };

  // Action: Submit Acquisition Wishlist
  const handleWishlistSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/requests', wishlistForm);
      showToast('Acquisition ticket submitted to university librarians!');
      setWishlistForm({ title: '', author: '', category: 'Computer Science', reason: '' });
      setShowWishlistModal(false);
    } catch (err) {
      showToast(err.message || 'Failed to submit acquisition request.', true);
    }
  };

  // Action: Post Marketplace Offer (Sell / Buy / Exchange in All Conditions)
  const handleOfferSubmit = async (e) => {
    e.preventDefault();
    // Contact information required in all conditions
    if (!offerForm.contact_phone && !offerForm.contact_whatsapp) {
      showToast('Please provide your contact phone or WhatsApp number so classmates can reach you!', true);
      return;
    }
    try {
      await api.post('/offers', offerForm);
      showToast('Book listing published to student peer marketplace with contact details!');
      setOfferForm({
        title: '',
        author: '',
        category: 'Computer Science',
        offer_type: 'sell',
        price: '',
        condition: 'Like New',
        donor_name: '',
        contact_phone: '',
        contact_whatsapp: '',
        pickup_location: 'Central Library Lawn / Reading Hall',
        description: '',
      });
      setShowPostOfferModal(false);
      const updatedOffers = await api.get('/offers');
      setOffers(updatedOffers.offers || updatedOffers);
    } catch (err) {
      showToast(err.message || 'Failed to post marketplace offer.', true);
    }
  };

  // Action: Speech Readout
  const handleSpeakSummary = (text) => {
    if (!('speechSynthesis' in window)) {
      showToast('Speech synthesis not supported in this browser.', true);
      return;
    }
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    window.speechSynthesis.speak(utterance);
    setIsSpeaking(true);
  };

  // Action: Copy Citation
  const handleCopyCitation = (book) => {
    const authorName = typeof book.author === 'string' ? book.author : book.author?.name || 'Academic Scholar';
    const year = book.publication_year || '2024';
    const citation = `${authorName}. (${year}). ${book.title}. NexShelf University Press.`;
    navigator.clipboard.writeText(citation);
    setCopiedCitation(true);
    showToast('APA citation copied to clipboard!');
    setTimeout(() => setCopiedCitation(false), 2000);
  };

  // Action: Real File Download
  const handleDownloadDeck = (note) => {
    if (!note || !note.id) return;
    showToast(`Downloading "${note.title}"...`);
    const link = document.createElement('a');
    link.href = `/api/notes/${note.id}/download`;
    link.setAttribute('download', `${note.title || 'study_notes'}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  // Categories extraction
  const categories = ['all', ...Array.from(new Set(books.map((b) => (typeof b.category === 'string' ? b.category : b.category?.name || 'General'))))];

  // Filtered books
  const filteredBooks = books.filter((b) => {
    const title = b.title || '';
    const author = typeof b.author === 'string' ? b.author : b.author?.name || '';
    const category = typeof b.category === 'string' ? b.category : b.category?.name || 'General';
    const matchesSearch = title.toLowerCase().includes(searchQuery.toLowerCase()) || author.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || category.toLowerCase() === selectedCategory.toLowerCase();
    return matchesSearch && matchesCategory;
  });

  // Filtered notes
  const filteredNotes = notes
    .filter((n) => {
      const title = n.title || '';
      const subject = n.subject || '';
      const desc = n.description || '';
      const author = n.author_name || n.uploader_name || '';
      const semester = n.semester || '';

      const matchesSearch =
        title.toLowerCase().includes(notesSearch.toLowerCase()) ||
        subject.toLowerCase().includes(notesSearch.toLowerCase()) ||
        desc.toLowerCase().includes(notesSearch.toLowerCase()) ||
        author.toLowerCase().includes(notesSearch.toLowerCase());

      const matchesSubject = notesSubjectFilter === 'all' || subject.toLowerCase().includes(notesSubjectFilter.toLowerCase());
      const matchesSemester = notesSemesterFilter === 'all' || semester.toLowerCase().includes(notesSemesterFilter.toLowerCase());

      return matchesSearch && matchesSubject && matchesSemester;
    })
    .sort((a, b) => {
      const likesA = (a.likes_count || 0) + (likedNotes[a.id] || 0);
      const likesB = (b.likes_count || 0) + (likedNotes[b.id] || 0);
      if (notesSortBy === 'popular') return likesB - likesA;
      if (notesSortBy === 'newest') return (b.id || 0) - (a.id || 0);
      return (a.title || '').localeCompare(b.title || '');
    });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Toast Notification */}
      {toast && (
        <div
          className={`fixed bottom-6 right-6 z-50 px-5 py-3.5 rounded-2xl shadow-2xl flex items-center gap-3 border transition-all animate-bounce ${
            toast.isError
              ? 'bg-rose-900/95 border-rose-500 text-rose-100'
              : 'bg-indigo-950/95 border-indigo-500 text-indigo-100'
          }`}
        >
          {toast.isError ? <X size={18} className="text-rose-400" /> : <CheckCircle2 size={18} className="text-emerald-400" />}
          <span className="text-sm font-semibold">{toast.message}</span>
        </div>
      )}

      {/* Hidden Global File Inputs (Triggers Real Native File Dialog) */}
      <input
        type="file"
        ref={fileInputModalRef}
        onChange={handleFileChange}
        accept=".pdf,.doc,.docx,.png,.jpg,.jpeg,.webp,.txt"
        className="hidden"
      />
      <input
        type="file"
        ref={fileInputInlineRef}
        onChange={handleFileChange}
        accept=".pdf,.doc,.docx,.png,.jpg,.jpeg,.webp,.txt"
        className="hidden"
      />

      {/* 1. Scholar Hero Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 p-6 md:p-8 text-white shadow-xl border border-white/10">
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-80 h-80 rounded-full bg-indigo-500/10 blur-3xl pointer-events-none"></div>
        <div className="relative z-10 flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-white/10 border border-white/15 text-xs font-bold text-slate-200 mb-3 backdrop-blur-md">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              Spring 2026 Academic Session &bull; Active Scholar
            </div>
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight font-heading">
              Welcome, <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-indigo-200 to-cyan-300">{profile.full_name?.split(' ')[0] || user?.full_name?.split(' ')[0] || 'Scholar'}</span> 👋
            </h1>
            <p className="text-slate-400 text-sm mt-1 max-w-xl">
              {profile.department || 'Computer Science & Engineering'} &bull; ID: <span className="font-mono text-indigo-300 font-bold">{profile.student_id || 'STU-0004'}</span>
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Direct Upload Notes Trigger Button */}
            <button
              onClick={() => {
                setActiveTab('notes');
                setShowUploadNoteModal(true);
              }}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 text-xs font-extrabold shadow-lg shadow-amber-500/20 hover:scale-105 transition cursor-pointer"
            >
              <FileUp size={16} />
              <span>Upload Notes (+50 Pts)</span>
            </button>

            {/* Holographic ID Pass Trigger */}
            <button
              onClick={() => setShowPassModal(true)}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-white/10 hover:bg-white/20 border border-white/20 text-xs font-bold text-white transition backdrop-blur-md shadow-md cursor-pointer"
            >
              <QrCode size={16} className="text-cyan-400" />
              <span>Student ID Pass</span>
            </button>

            {/* Streak Counter */}
            <div className="flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-amber-500/15 border border-amber-500/30 text-amber-300 text-xs font-bold shadow-md">
              <Flame size={16} className="text-amber-400 fill-amber-400 animate-bounce" />
              <span>{gamification.streak_days || 1}d Streak</span>
            </div>
          </div>
        </div>
      </div>

      {/* 2. Interactive KPI Reels */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Notes in Vault Reel */}
        <div
          onClick={() => setActiveTab('notes')}
          className="cursor-pointer bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm hover:border-amber-400 hover:shadow-md transition group"
        >
          <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center mb-3 group-hover:scale-110 transition">
            <FileText size={20} />
          </div>
          <div className="text-3xl font-extrabold text-slate-900 font-mono tracking-tight">
            {notes.length}
          </div>
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mt-1 flex items-center justify-between">
            <span>Courseware Notes Decks</span>
            <ChevronRight size={14} className="text-slate-400 group-hover:translate-x-1 transition" />
          </div>
        </div>

        {/* Active Borrowed Books */}
        <div
          onClick={() => setActiveTab('issues')}
          className="cursor-pointer bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm hover:border-indigo-400 hover:shadow-md transition group"
        >
          <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-3 group-hover:scale-110 transition">
            <BookOpen size={20} />
          </div>
          <div className="text-3xl font-extrabold text-slate-900 font-mono tracking-tight">
            {stats.borrowed_books || myIssues.filter((i) => i.status === 'issued').length}
          </div>
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mt-1 flex items-center justify-between">
            <span>Active Borrowings</span>
            <ChevronRight size={14} className="text-slate-400 group-hover:translate-x-1 transition" />
          </div>
        </div>

        {/* Overdue Titles */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm hover:border-rose-300 transition">
          <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center mb-3">
            <Clock size={20} />
          </div>
          <div className="text-3xl font-extrabold text-rose-600 font-mono tracking-tight">
            {stats.overdue_books || 0}
          </div>
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mt-1">
            Overdue Loans
          </div>
        </div>

        {/* Live Study Radar */}
        <div className="bg-gradient-to-br from-indigo-950 to-slate-900 rounded-2xl p-5 text-white shadow-sm border border-white/10 flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs mb-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Turing Quiet Wing</span>
            <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-[10px] font-bold border border-emerald-500/30">
              Open Now
            </span>
          </div>
          <div>
            <div className="flex justify-between text-xs text-slate-300 mb-1">
              <span>Occupancy Radar</span>
              <span className="font-mono font-bold text-cyan-400">54% Filled</span>
            </div>
            <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-cyan-400 to-indigo-400 rounded-full" style={{ width: '54%' }}></div>
            </div>
          </div>
          <span className="text-[10px] text-slate-400 mt-2">Peak academic hours &bull; 38 desks open</span>
        </div>
      </div>

      {/* 3. Navigation Tabs */}
      <div className="flex border-b border-slate-200 overflow-x-auto scrollbar-none gap-2">
        {[
          { id: 'notes', label: 'Courseware & Notes Vault', icon: FileText, count: notes.length, highlight: true },
          { id: 'catalog', label: 'Library Catalog & Shelves', icon: BookOpen, count: books.length },
          { id: 'marketplace', label: 'Peer Textbook Market', icon: Store, count: offers.length },
          { id: 'issues', label: 'My Borrowed Books', icon: BookMarked, count: myIssues.length },
          { id: 'badges', label: 'Badges & Achievements', icon: Award, count: gamification.badges?.length || 1 }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-3 text-sm font-bold border-b-2 whitespace-nowrap transition cursor-pointer ${
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
                    isActive
                      ? 'bg-indigo-100 text-indigo-700'
                      : tab.highlight
                      ? 'bg-amber-100 text-amber-800 font-bold'
                      : 'bg-slate-100 text-slate-600'
                  }`}
                >
                  {tab.count}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* ======================================================== */}
      {/* TAB: COURSEWARE & NOTES VAULT (WITH INTEGRATED UPLOADER) */}
      {/* ======================================================== */}
      {activeTab === 'notes' && (
        <div className="space-y-6">
          {/* Hero Upload Callout & Toggle */}
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-amber-500 via-amber-600 to-indigo-900 p-6 md:p-8 text-white shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="relative z-10 max-w-xl">
              <span className="px-3 py-1 rounded-full bg-white/20 text-white text-[10px] font-extrabold uppercase tracking-wider inline-flex items-center gap-1.5 backdrop-blur-md mb-2">
                <Sparkles size={12} className="text-amber-200" /> Peer Study Commons
              </span>
              <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight font-heading">
                Upload &amp; Access Handwritten Lecture Decks
              </h2>
              <p className="text-amber-100 text-xs md:text-sm mt-1 leading-relaxed">
                Contribute verified class summaries, formula cheat sheets, and exam prep decks. Earn <span className="font-bold underline">+50 Scholar Points</span> per upload and rank up your student pass!
              </p>
            </div>

            <div className="relative z-10 flex flex-wrap items-center gap-3">
              <button
                onClick={() => setShowInlineUploader((prev) => !prev)}
                className="px-5 py-3 rounded-2xl bg-white text-slate-950 font-extrabold text-xs shadow-xl hover:bg-amber-50 hover:scale-105 transition flex items-center gap-2 cursor-pointer"
              >
                <Upload size={16} className="text-amber-600" />
                <span>{showInlineUploader ? 'Hide Upload Section' : 'Open Upload Section'}</span>
              </button>
            </div>
          </div>

          {/* DEDICATED INLINE UPLOAD SECTION (DIRECTLY ON PAGE) */}
          {showInlineUploader && (
            <div className="bg-white rounded-3xl p-6 md:p-8 border-2 border-amber-200 shadow-xl transition-all">
              <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-6">
                <div>
                  <div className="inline-flex items-center gap-2 px-3 py-0.5 rounded-full bg-amber-50 text-amber-800 text-[10px] font-extrabold uppercase">
                    <FileUp size={12} /> Live Notes Uploader
                  </div>
                  <h3 className="text-xl font-extrabold text-slate-900 font-heading mt-1">
                    Contribute Courseware Notes to Vault
                  </h3>
                  <p className="text-xs text-slate-500">
                    Upload your handwritten summaries, slides, or formula sheets. Verified documents appear in the student vault instantly.
                  </p>
                </div>
                <button
                  onClick={() => setShowInlineUploader(false)}
                  className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100"
                  title="Close Section"
                >
                  <X size={18} />
                </button>
              </div>

              <form onSubmit={handleNoteSubmit} className="space-y-5">
                {/* Drag and Drop Zone with Real File Input Trigger */}
                <div
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => fileInputInlineRef.current?.click()}
                  className={`border-2 border-dashed rounded-2xl p-8 text-center transition cursor-pointer select-none group ${
                    isDragging
                      ? 'border-amber-500 bg-amber-100/50 scale-[1.01]'
                      : uploadedFileDetails
                      ? 'border-emerald-400 bg-emerald-50/40'
                      : 'border-amber-300 hover:border-amber-500 bg-amber-50/40 hover:bg-amber-50'
                  }`}
                >
                  <div className="w-14 h-14 rounded-2xl bg-amber-100 text-amber-700 mx-auto flex items-center justify-center mb-3 group-hover:scale-110 transition shadow-sm">
                    {uploadedFileDetails ? <FileCheck size={28} className="text-emerald-600" /> : <Upload size={28} />}
                  </div>

                  {uploadedFileDetails ? (
                    <div>
                      <div className="text-sm font-extrabold text-emerald-800 flex items-center justify-center gap-2">
                        <CheckCircle2 size={16} className="text-emerald-600" />
                        <span>File Attached: {uploadedFileDetails.name}</span>
                      </div>
                      <div className="text-xs font-mono text-slate-500 mt-1">
                        Size: {uploadedFileDetails.size} &bull; {uploadedFileDetails.type}
                      </div>
                      <div className="mt-2 text-[11px] text-indigo-600 font-bold underline">
                        Click to change document
                      </div>
                    </div>
                  ) : (
                    <div>
                      <div className="text-sm font-extrabold text-slate-900">
                        Click to browse notes file from your computer or drag &amp; drop
                      </div>
                      <p className="text-xs text-slate-500 mt-1">
                        Supports PDF documents, Word DOCX, handwritten scan images (PNG, JPG)
                      </p>
                    </div>
                  )}
                </div>

                {/* Upload Progress Bar (when active) */}
                {isUploading && (
                  <div className="space-y-1.5 p-4 rounded-2xl bg-slate-50 border border-slate-200">
                    <div className="flex justify-between text-xs font-extrabold text-slate-700">
                      <span>Publishing notes deck to university vault...</span>
                      <span>{uploadProgress}%</span>
                    </div>
                    <div className="w-full h-2.5 bg-slate-200 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-amber-500 via-amber-600 to-indigo-600 transition-all duration-200 rounded-full"
                        style={{ width: `${uploadProgress}%` }}
                      ></div>
                    </div>
                  </div>
                )}

                {/* Form Fields Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Title */}
                  <div className="md:col-span-2">
                    <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                      Document Title *
                    </label>
                    <input
                      type="text"
                      required
                      placeholder="e.g. Operating Systems: Virtual Memory & Page Replacement Cheat Sheet"
                      value={noteForm.title}
                      onChange={(e) => setNoteForm({ ...noteForm, title: e.target.value })}
                      className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                    />
                  </div>

                  {/* Subject */}
                  <div>
                    <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                      Subject / Course Discipline *
                    </label>
                    <select
                      value={noteForm.subject}
                      onChange={(e) => setNoteForm({ ...noteForm, subject: e.target.value })}
                      className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                    >
                      <option value="Computer Science">Computer Science</option>
                      <option value="Operating Systems">Operating Systems</option>
                      <option value="Artificial Intelligence">Artificial Intelligence</option>
                      <option value="Data Structures & Algorithms">Data Structures &amp; Algorithms</option>
                      <option value="Mathematics">Mathematics</option>
                      <option value="Computer Networks">Computer Networks</option>
                      <option value="Database Systems">Database Systems</option>
                    </select>
                  </div>

                  {/* Semester */}
                  <div>
                    <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                      Academic Term / Semester *
                    </label>
                    <select
                      value={noteForm.semester}
                      onChange={(e) => setNoteForm({ ...noteForm, semester: e.target.value })}
                      className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                    >
                      <option value="Semester 1">Semester 1</option>
                      <option value="Semester 2">Semester 2</option>
                      <option value="Semester 3">Semester 3</option>
                      <option value="Semester 4">Semester 4</option>
                      <option value="Semester 5">Semester 5</option>
                      <option value="Semester 6">Semester 6</option>
                      <option value="Semester 7">Semester 7</option>
                      <option value="Semester 8">Semester 8</option>
                    </select>
                  </div>

                  {/* Description / Topics */}
                  <div className="md:col-span-2">
                    <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                      Key Highlights, Topics &amp; Formulas Covered
                    </label>
                    <textarea
                      rows="3"
                      placeholder="Outline core definitions, formulas, or practice problems in this deck..."
                      value={noteForm.description}
                      onChange={(e) => setNoteForm({ ...noteForm, description: e.target.value })}
                      className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                    ></textarea>
                  </div>
                </div>

                {/* Submitter Pill & Action Button */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-3 border-t border-slate-100">
                  <div className="text-xs text-slate-500">
                    Publishing as: <strong className="text-slate-900">{profile.full_name || user?.full_name || 'Scholar'}</strong> ({profile.student_id || 'STU-0004'})
                  </div>
                  <div className="flex items-center gap-3">
                    <button
                      type="button"
                      onClick={() => setShowInlineUploader(false)}
                      className="px-4 py-2.5 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-xl"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={isUploading}
                      className="px-6 py-2.5 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-extrabold text-xs rounded-xl shadow-lg transition flex items-center gap-2 cursor-pointer"
                    >
                      <Upload size={15} />
                      <span>{isUploading ? 'Uploading to Vault...' : 'Publish Notes Deck (+50 Pts)'}</span>
                    </button>
                  </div>
                </div>
              </form>
            </div>
          )}

          {/* Filtering & Sorting Toolbar */}
          <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            {/* Search Input */}
            <div className="relative w-full lg:w-80">
              <Search size={16} className="absolute left-3.5 top-3 text-slate-400" />
              <input
                type="text"
                value={notesSearch}
                onChange={(e) => setNotesSearch(e.target.value)}
                placeholder="Search notes by subject, topic, or scholar..."
                className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
              {notesSearch && (
                <button
                  onClick={() => setNotesSearch('')}
                  className="absolute right-3 top-2.5 text-xs text-slate-400 hover:text-slate-600"
                >
                  Clear
                </button>
              )}
            </div>

            {/* Subject Filters */}
            <div className="flex items-center gap-2 overflow-x-auto scrollbar-none pb-1">
              {[
                { id: 'all', label: 'All Subjects' },
                { id: 'Computer Science', label: 'Computer Science' },
                { id: 'Operating Systems', label: 'Operating Systems' },
                { id: 'Artificial Intelligence', label: 'AI & ML' },
                { id: 'Mathematics', label: 'Mathematics' },
                { id: 'Data Structures', label: 'Data Structures' }
              ].map((subj) => (
                <button
                  key={subj.id}
                  onClick={() => setNotesSubjectFilter(subj.id)}
                  className={`px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition cursor-pointer ${
                    notesSubjectFilter === subj.id
                      ? 'bg-amber-500 text-slate-950 shadow-sm'
                      : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                  }`}
                >
                  {subj.label}
                </button>
              ))}
            </div>

            {/* Semester & Sort Controls */}
            <div className="flex items-center gap-2">
              <select
                value={notesSemesterFilter}
                onChange={(e) => setNotesSemesterFilter(e.target.value)}
                className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-bold text-slate-700 focus:outline-none focus:ring-2 focus:ring-amber-500"
              >
                <option value="all">All Semesters</option>
                <option value="Semester 1">Semester 1</option>
                <option value="Semester 2">Semester 2</option>
                <option value="Semester 3">Semester 3</option>
                <option value="Semester 4">Semester 4</option>
                <option value="Semester 5">Semester 5</option>
                <option value="Semester 6">Semester 6</option>
                <option value="Semester 7">Semester 7</option>
                <option value="Semester 8">Semester 8</option>
              </select>

              <select
                value={notesSortBy}
                onChange={(e) => setNotesSortBy(e.target.value)}
                className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-bold text-slate-700 focus:outline-none focus:ring-2 focus:ring-amber-500"
              >
                <option value="popular">🔥 Most Upvoted</option>
                <option value="newest">⚡ Newest First</option>
                <option value="title">🔤 Title (A-Z)</option>
              </select>
            </div>
          </div>

          {/* Notes Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredNotes.map((note) => {
              const likesCount = (note.likes_count || 10) + (likedNotes[note.id] || 0);
              const isLiked = Boolean(likedNotes[note.id]);

              return (
                <div
                  key={note.id}
                  className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-sm hover:shadow-xl hover:-translate-y-1 transition duration-200 flex flex-col justify-between group"
                >
                  <div>
                    {/* Header Chips */}
                    <div className="flex items-center justify-between gap-2 mb-3">
                      <span className="px-3 py-1 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-[11px] font-extrabold">
                        {note.subject || 'Computer Science'}
                      </span>
                      <span className="text-[11px] font-mono font-bold text-slate-500 bg-slate-100 px-2.5 py-0.5 rounded-full">
                        {note.semester || 'Semester 4'}
                      </span>
                    </div>

                    {/* Note Title */}
                    <h4
                      onClick={() => {
                        setSelectedNote(note);
                        setPreviewPageIndex(1);
                      }}
                      className="font-bold text-slate-900 text-lg group-hover:text-amber-600 transition cursor-pointer line-clamp-2 leading-snug"
                    >
                      {note.title}
                    </h4>

                    {/* Description */}
                    <p className="text-xs text-slate-600 mt-2 line-clamp-2 leading-relaxed">
                      {note.description || 'Verified student revision deck with formulas, diagrams, and solved exam problems.'}
                    </p>

                    {/* Document Meta Pill */}
                    <div className="mt-4 p-3 rounded-2xl bg-slate-50 border border-slate-100 flex items-center justify-between text-xs text-slate-600">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold text-xs">
                          PDF
                        </div>
                        <div>
                          <div className="font-bold text-slate-800 text-[11px]">Handwritten Deck</div>
                          <div className="text-[10px] text-slate-400">Verified &bull; 18 Pages</div>
                        </div>
                      </div>
                      <span className="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-md">
                        Exam Ready
                      </span>
                    </div>

                    <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400">
                      <span>Shared by: <strong className="text-slate-700">{note.author_name || note.uploader_name || 'Scholar Contributor'}</strong></span>
                    </div>
                  </div>

                  {/* Action Buttons: Like, Preview, Download */}
                  <div className="mt-5 pt-4 border-t border-slate-100 flex items-center justify-between gap-2">
                    <button
                      onClick={() => handleLikeNote(note.id)}
                      className={`inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold transition cursor-pointer ${
                        isLiked
                          ? 'bg-rose-50 text-rose-600 border border-rose-200 shadow-sm'
                          : 'bg-slate-50 hover:bg-rose-50 text-slate-700 hover:text-rose-600 border border-slate-200'
                      }`}
                      title="Upvote Note (+1 Scholar Point)"
                    >
                      <ThumbsUp size={14} className={isLiked ? 'fill-rose-600 text-rose-600' : ''} />
                      <span>{likesCount}</span>
                    </button>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => {
                          setSelectedNote(note);
                          setPreviewPageIndex(1);
                        }}
                        className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold transition cursor-pointer"
                        title="Preview Document Deck"
                      >
                        <Eye size={14} />
                        <span>Preview</span>
                      </button>

                      <button
                        onClick={() => handleDownloadDeck(note)}
                        className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition shadow-sm cursor-pointer"
                        title="Download PDF"
                      >
                        <Download size={14} />
                        <span>Download</span>
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {filteredNotes.length === 0 && (
            <div className="bg-white rounded-3xl p-12 text-center border border-slate-200">
              <FileText size={40} className="text-slate-300 mx-auto mb-3" />
              <h4 className="font-bold text-slate-900">No courseware notes match your criteria</h4>
              <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                Be the first to upload lecture notes or formula sheets for this discipline!
              </p>
              <button
                onClick={() => setShowInlineUploader(true)}
                className="mt-4 px-5 py-2.5 rounded-xl bg-amber-500 text-slate-950 font-bold text-xs shadow-md transition"
              >
                Upload First Note Deck
              </button>
            </div>
          )}
        </div>
      )}

      {/* TAB: CATALOG & 3D VIRTUAL SPINE SHELF */}
      {activeTab === 'catalog' && (
        <div className="space-y-6">
          {/* Controls Bar: Search, Category Filter & View Mode Toggle */}
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 bg-white p-4 rounded-2xl border border-slate-200/80 shadow-sm">
            {/* Search */}
            <div className="relative w-full lg:w-96">
              <Search size={16} className="absolute left-3.5 top-3 text-slate-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by title, author, or rack coordinates..."
                className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-3 top-2.5 text-xs text-slate-400 hover:text-slate-600"
                >
                  Clear
                </button>
              )}
            </div>

            {/* View Mode Toggle & Wishlist Button */}
            <div className="flex items-center gap-3">
              <div className="flex items-center p-1 rounded-xl bg-slate-100 border border-slate-200 text-xs font-bold">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`flex items-center gap-1 px-3 py-1.5 rounded-lg transition ${
                    viewMode === 'grid' ? 'bg-white text-indigo-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <Grid size={14} /> <span>Grid</span>
                </button>
                <button
                  onClick={() => setViewMode('spines')}
                  className={`flex items-center gap-1 px-3 py-1.5 rounded-lg transition ${
                    viewMode === 'spines' ? 'bg-white text-indigo-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <Columns size={14} /> <span>3D Spines</span>
                </button>
              </div>

              <button
                onClick={() => setShowWishlistModal(true)}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-50 text-indigo-700 border border-indigo-200 hover:bg-indigo-100 text-xs font-bold transition shadow-sm"
              >
                <Heart size={14} className="text-rose-500 fill-rose-500" />
                <span>Request Title</span>
              </button>
            </div>
          </div>

          {/* Category Filter Pills */}
          <div className="flex items-center gap-2 overflow-x-auto scrollbar-none pb-2">
            {categories.slice(0, 10).map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition cursor-pointer ${
                  selectedCategory.toLowerCase() === cat.toLowerCase()
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </button>
            ))}
          </div>

          {/* VIEW: 3D VIRTUAL SPINE SHELF */}
          {viewMode === 'spines' ? (
            <div className="p-6 md:p-8 rounded-3xl bg-gradient-to-b from-slate-900 to-indigo-950 border border-white/10 shadow-2xl overflow-hidden">
              <div className="flex items-center justify-between text-white mb-6">
                <div>
                  <h3 className="font-extrabold text-lg flex items-center gap-2 font-heading">
                    <Sparkles size={16} className="text-amber-400" />
                    Interactive 3D Virtual Spine Rack
                  </h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Click any volume spine to inspect academic takeaways, shelf coordinates, or checkout.
                  </p>
                </div>
                <span className="text-xs font-mono text-cyan-300 bg-cyan-900/40 px-3 py-1 rounded-full border border-cyan-500/30">
                  {filteredBooks.length} Volumes On Shelf
                </span>
              </div>

              {/* Wooden Shelf Simulation */}
              <div className="relative pt-4 pb-2 border-b-8 border-amber-900/80 bg-slate-950/40 rounded-xl p-4 shadow-inner">
                <div className="flex items-end gap-2 overflow-x-auto scrollbar-none py-4 px-2 min-h-[220px]">
                  {filteredBooks.map((book) => {
                    const color = book.accent_color || '#4f46e5';
                    return (
                      <div
                        key={book.id}
                        onClick={() => setSelectedBook(book)}
                        className="book-spine-item flex-shrink-0 cursor-pointer rounded-t-md p-2 flex flex-col justify-between select-none relative group"
                        style={{
                          backgroundColor: color,
                          width: '44px',
                          height: `${175 + (book.id % 5) * 8}px`,
                          boxShadow: 'inset 0 0 10px rgba(0,0,0,0.4), 0 8px 16px rgba(0,0,0,0.4)',
                          borderLeft: '2px solid rgba(255,255,255,0.25)',
                          borderRight: '2px solid rgba(0,0,0,0.3)'
                        }}
                        title={book.title}
                      >
                        <div className="text-[9px] font-mono font-bold text-white/80 uppercase tracking-tighter truncate text-center">
                          {book.difficulty_level?.[0] || 'I'}
                        </div>

                        {/* Rotated Vertical Title */}
                        <div className="h-full flex items-center justify-center overflow-hidden my-1">
                          <span
                            className="text-[11px] font-bold text-white tracking-tight truncate whitespace-nowrap"
                            style={{
                              writingMode: 'vertical-rl',
                              transform: 'rotate(180deg)',
                              textShadow: '0 1px 2px rgba(0,0,0,0.6)'
                            }}
                          >
                            {book.title}
                          </span>
                        </div>

                        <div className="w-full text-center border-t border-white/20 pt-1">
                          <span className="text-[8px] font-mono text-white/90 font-bold block truncate">
                            #{book.id}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          ) : (
            /* VIEW: MODERN CARD GRID */
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
              {filteredBooks.map((book) => {
                const authorName = typeof book.author === 'string' ? book.author : book.author?.name || 'Unknown Author';
                const categoryName = typeof book.category === 'string' ? book.category : book.category?.name || 'General';
                const isAvailable = (book.available_quantity ?? 1) > 0;

                return (
                  <div
                    key={book.id}
                    className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm hover:shadow-lg hover:-translate-y-1 transition duration-200 flex flex-col justify-between group"
                  >
                    <div>
                      {/* Top Badges */}
                      <div className="flex items-center justify-between text-xs mb-3">
                        <span className="px-2.5 py-0.5 rounded-md bg-slate-100 text-slate-700 text-[11px] font-bold">
                          {categoryName}
                        </span>
                        <span
                          className={`px-2 py-0.5 rounded-full text-[10px] font-bold font-mono ${
                            isAvailable ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'
                          }`}
                        >
                          {isAvailable ? `${book.available_quantity ?? 1} in stock` : 'Checked Out'}
                        </span>
                      </div>

                      {/* Title & Author */}
                      <h4
                        onClick={() => setSelectedBook(book)}
                        className="font-bold text-slate-900 group-hover:text-indigo-600 transition cursor-pointer line-clamp-2 leading-snug"
                      >
                        {book.title}
                      </h4>
                      <p className="text-xs text-slate-500 mt-1 line-clamp-1">by {authorName}</p>

                      {/* Shelf Coordinates Pill */}
                      <div className="mt-3 flex items-center gap-1.5 text-[11px] font-mono text-slate-600 bg-slate-50 p-2 rounded-xl border border-slate-100">
                        <Library size={12} className="text-indigo-500" />
                        <span className="truncate">{book.shelf_location || 'Zone A · Rack 01'}</span>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="mt-4 pt-3 border-t border-slate-100 flex items-center gap-2">
                      <button
                        onClick={() => setSelectedBook(book)}
                        className="flex-1 py-2 px-3 rounded-xl border border-slate-200 text-slate-700 hover:bg-slate-50 text-xs font-bold transition flex items-center justify-center gap-1 cursor-pointer"
                      >
                        <Eye size={14} /> <span>Inspect</span>
                      </button>
                      <button
                        onClick={() => handleBorrow(book.id)}
                        disabled={!isAvailable}
                        className={`flex-1 py-2 px-3 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1 shadow-sm cursor-pointer ${
                          isAvailable
                            ? 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-indigo-200'
                            : 'bg-slate-100 text-slate-400 cursor-not-allowed'
                        }`}
                      >
                        <BookOpen size={14} /> <span>Borrow</span>
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* TAB: PEER TEXTBOOK MARKETPLACE (BUY, SELL & EXCHANGE) */}
      {activeTab === 'marketplace' && (
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm">
            <div>
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-mono font-bold uppercase tracking-wider mb-2">
                <span>📚 Campus Student Hub</span>
              </div>
              <h3 className="text-xl font-extrabold text-slate-900 font-heading">
                Peer Textbook Market: Buy, Sell &amp; Exchange
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Direct student-to-student textbook handoffs with verified mobile &amp; WhatsApp contacts.
              </p>
            </div>
            <button
              onClick={() => setShowPostOfferModal(true)}
              className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs shadow-md shadow-emerald-600/20 transition cursor-pointer"
            >
              <Plus size={16} /> <span>List Book (Sell / Buy / Exchange)</span>
            </button>
          </div>

          {/* Filter Bar */}
          <div className="flex flex-wrap gap-2 items-center bg-slate-50 p-2 rounded-xl border border-slate-200/60">
            {[
              { id: 'all', label: 'All Listings' },
              { id: 'sell', label: '🏷️ For Sale' },
              { id: 'exchange', label: '🔄 For Exchange' },
              { id: 'buy', label: '🔍 Looking to Buy' },
              { id: 'free_giveaway', label: '🎁 Free Giveaway' },
            ].map((f) => (
              <button
                key={f.id}
                onClick={() => setMarketFilter(f.id)}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition cursor-pointer ${
                  marketFilter === f.id
                    ? 'bg-white text-slate-900 shadow-sm border border-slate-200'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>

          {/* Listings Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {offers
              .filter((o) => marketFilter === 'all' || o.offer_type === marketFilter)
              .map((offer) => {
                const isSell = offer.offer_type === 'sell';
                const isExchange = offer.offer_type === 'exchange';
                const isBuy = offer.offer_type === 'buy';
                const isFree = offer.offer_type === 'free_giveaway' || (!isSell && !isExchange && !isBuy && !offer.price);
                const phone = offer.contact_phone || '';
                const cleanPhone = phone.replace(/\D/g, '');

                return (
                  <div
                    key={offer.id}
                    className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm flex flex-col justify-between hover:shadow-md transition"
                  >
                    <div>
                      {/* Top Type Badge */}
                      <div className="flex items-center justify-between mb-3">
                        {isSell && (
                          <span className="px-2.5 py-1 rounded-lg bg-emerald-50 border border-emerald-200/60 text-emerald-700 font-mono font-extrabold text-xs">
                            🏷️ FOR SALE · ₹{offer.price || '0'}
                          </span>
                        )}
                        {isExchange && (
                          <span className="px-2.5 py-1 rounded-lg bg-cyan-50 border border-cyan-200/60 text-cyan-700 font-mono font-extrabold text-xs">
                            🔄 BOOK EXCHANGE
                          </span>
                        )}
                        {isBuy && (
                          <span className="px-2.5 py-1 rounded-lg bg-purple-50 border border-purple-200/60 text-purple-700 font-mono font-extrabold text-xs">
                            🔍 LOOKING TO BUY
                          </span>
                        )}
                        {isFree && (
                          <span className="px-2.5 py-1 rounded-lg bg-amber-50 border border-amber-200/60 text-amber-700 font-mono font-extrabold text-xs">
                            🎁 FREE GIVEAWAY
                          </span>
                        )}

                        <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-slate-100 text-slate-600">
                          {offer.condition || 'Good'}
                        </span>
                      </div>

                      <h4 className="font-bold text-slate-900 text-base leading-snug">{offer.title}</h4>
                      <p className="text-xs text-slate-500 mt-0.5">by {offer.author}</p>

                      {offer.description && (
                        <p className="text-xs text-slate-600 italic mt-2.5 bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                          "{offer.description}"
                        </p>
                      )}

                      <div className="mt-3 text-[11px] text-slate-500 flex items-center gap-1 font-medium">
                        <span>📍 Location:</span>
                        <span className="text-slate-700 font-semibold">{offer.pickup_location || 'Campus / Library'}</span>
                      </div>
                    </div>

                    {/* Contact Section: Active in ALL Conditions & Types */}
                    <div className="mt-4 pt-3.5 border-t border-slate-100">
                      <div className="flex items-center justify-between text-xs mb-2.5">
                        <span className="text-slate-600 font-medium">
                          {isSell ? 'Seller: ' : isExchange ? 'Swap Partner: ' : isBuy ? 'Buyer: ' : 'Donor: '}
                          <strong className="text-slate-900">{offer.donor_name || offer.seller_name || 'Classmate'}</strong>
                        </span>
                        {phone && (
                          <span className="font-mono text-xs font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded-md border border-indigo-200/60">
                            📞 {phone}
                          </span>
                        )}
                      </div>

                      {/* Direct Action Contact Buttons in ALL Conditions */}
                      <div className="grid grid-cols-2 gap-2">
                        {phone ? (
                          <>
                            <a
                              href={`tel:${phone}`}
                              className="inline-flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition shadow-sm cursor-pointer"
                              title={`Call ${phone}`}
                            >
                              <Phone size={13} />
                              <span>{isSell ? 'Call Seller' : isExchange ? 'Call Partner' : isBuy ? 'Call Buyer' : 'Call Donor'}</span>
                            </a>
                            <a
                              href={`https://wa.me/${cleanPhone}?text=Hi%20${encodeURIComponent(offer.donor_name || 'Peer')},%20I%20saw%20your%20book%20listing%20"${encodeURIComponent(offer.title)}"%20(${offer.offer_type || 'listing'})%20on%20NexShelf.`}
                              target="_blank"
                              rel="noreferrer"
                              className="inline-flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold transition shadow-sm cursor-pointer"
                              title="Chat on WhatsApp"
                            >
                              <span>💬 WhatsApp</span>
                            </a>
                          </>
                        ) : (
                          <a
                            href={`mailto:${offer.contact_email || 'student@nexshelf.edu'}?subject=Regarding your listing: ${encodeURIComponent(offer.title)}`}
                            className="col-span-2 inline-flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition cursor-pointer"
                          >
                            <Phone size={13} />
                            <span>Contact via Email</span>
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
          </div>
        </div>
      )}

      {/* TAB: MY ACTIVE LOANS */}
      {activeTab === 'issues' && (
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
          <div className="p-5 border-b border-slate-100 flex items-center justify-between">
            <h3 className="font-extrabold text-slate-900 font-heading text-lg">My Circulation Records</h3>
            <span className="text-xs text-slate-500 font-mono">{myIssues.length} Total Loans on Record</span>
          </div>

          <div className="divide-y divide-slate-100">
            {myIssues.map((issue) => (
              <div key={issue.id} className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-slate-50/60 transition">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-bold text-slate-900">{issue.book_title || 'Institutional Textbook'}</span>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider ${
                        issue.status === 'issued'
                          ? 'bg-indigo-100 text-indigo-700'
                          : 'bg-emerald-100 text-emerald-700'
                      }`}
                    >
                      {issue.status}
                    </span>
                  </div>
                  <div className="text-xs text-slate-500 font-mono">
                    Shelf Location: {issue.shelf_location || 'Zone A · Rack 01'} &bull; Due Date: {issue.due_date ? new Date(issue.due_date).toLocaleDateString() : 'N/A'}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-3 py-1.5 rounded-xl">
                    Active Loan
                  </span>
                </div>
              </div>
            ))}
            {myIssues.length === 0 && (
              <div className="p-12 text-center text-slate-400">
                <BookOpen size={36} className="mx-auto mb-2 opacity-50" />
                <p className="text-sm font-semibold">No active borrowings recorded.</p>
                <button
                  onClick={() => setActiveTab('catalog')}
                  className="mt-3 px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-bold shadow transition"
                >
                  Explore Catalog
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB: BADGES & ACHIEVEMENTS */}
      {activeTab === 'badges' && (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
            <h3 className="text-xl font-extrabold text-slate-900 font-heading">Scholar Milestones &amp; Badges</h3>
            <p className="text-xs text-slate-500 mt-1">Unlock badges by borrowing books, writing peer reviews, and maintaining punctual returns.</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {(gamification.all_available_badges?.length > 0
              ? gamification.all_available_badges
              : [
                  { title: "Scholar's First Step", description: 'Issued your very first library volume.', unlocked: true },
                  { title: 'Bibliophile Master', description: 'Read and borrowed 5 or more titles.', unlocked: false },
                  { title: 'Punctual Scholar', description: 'Returned books promptly on time without fines.', unlocked: true },
                  { title: 'Literary Critic', description: 'Submitted a verified reader review and rating.', unlocked: true },
                  { title: 'Knowledge Explorer', description: 'Explored books across multiple academic disciplines.', unlocked: false }
                ]
            ).map((badge, idx) => (
              <div
                key={idx}
                className={`p-5 rounded-2xl border transition flex items-start gap-4 ${
                  badge.unlocked
                    ? 'bg-white border-indigo-200 shadow-sm'
                    : 'bg-slate-50/70 border-slate-200 opacity-60'
                }`}
              >
                <div
                  className={`w-12 h-12 rounded-2xl flex items-center justify-center flex-shrink-0 ${
                    badge.unlocked ? 'bg-gradient-to-tr from-amber-400 to-amber-500 text-slate-900 shadow-md' : 'bg-slate-200 text-slate-400'
                  }`}
                >
                  <Award size={24} />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="font-bold text-slate-900 text-sm">{badge.title}</h4>
                    {badge.unlocked && (
                      <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">
                        Unlocked
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-500 mt-1 leading-relaxed">{badge.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* MODAL: INTERACTIVE STUDY NOTE DECK VIEWER & PREVIEW */}
      {/* ======================================================== */}
      {selectedNote && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-md">
          <div className="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-100 max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="flex items-start justify-between pb-4 border-b border-slate-100">
              <div>
                <div className="flex items-center gap-2 mb-1.5">
                  <span className="px-3 py-0.5 rounded-md bg-amber-50 text-amber-800 text-xs font-extrabold border border-amber-200">
                    {selectedNote.subject || 'Courseware'}
                  </span>
                  <span className="text-xs font-mono text-slate-500 bg-slate-100 px-2.5 py-0.5 rounded-full">
                    {selectedNote.semester || 'Semester 4'}
                  </span>
                </div>
                <h3 className="font-extrabold text-xl text-slate-900 font-heading">{selectedNote.title}</h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Contributed by <strong className="text-slate-700">{selectedNote.author_name || selectedNote.uploader_name || 'Scholar Contributor'}</strong>
                </p>
              </div>
              <button
                onClick={() => setSelectedNote(null)}
                className="p-1.5 text-slate-400 hover:text-slate-600 rounded-full hover:bg-slate-100 transition"
              >
                <X size={20} />
              </button>
            </div>

            {/* Document Deck Preview Carousel */}
            <div className="my-5 space-y-4">
              <div className="relative rounded-2xl bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-6 shadow-inner border border-slate-800 min-h-[240px] flex flex-col justify-between">
                <div className="flex items-center justify-between text-xs text-slate-400 pb-2 border-b border-white/10">
                  <span className="font-mono flex items-center gap-1.5">
                    <FileText size={14} className="text-amber-400" />
                    Page {previewPageIndex} of 3 &bull; Courseware Deck
                  </span>
                  <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold text-[10px]">
                    Verified by Academic Peer
                  </span>
                </div>

                {/* Page Content Simulation */}
                <div className="my-4 space-y-2">
                  {previewPageIndex === 1 && (
                    <div>
                      <h5 className="font-extrabold text-amber-300 text-sm mb-1">Section 1: Executive Theory &amp; Scope</h5>
                      <p className="text-xs text-slate-300 leading-relaxed">
                        {selectedNote.description || 'Comprehensive conceptual notes covering fundamental definitions, proofs, architecture models, and algorithm design paradigms.'}
                      </p>
                      <div className="mt-3 p-3 rounded-xl bg-white/5 border border-white/10 text-[11px] font-mono text-cyan-200">
                        &bull; Axioms &amp; Prerequisites verified<br />
                        &bull; Covers Core Syllabus Units 1 &ndash; 3
                      </div>
                    </div>
                  )}

                  {previewPageIndex === 2 && (
                    <div>
                      <h5 className="font-extrabold text-amber-300 text-sm mb-1">Section 2: Essential Formulas &amp; Equations</h5>
                      <div className="p-3 rounded-xl bg-white/5 border border-white/10 text-xs font-mono text-amber-200 space-y-1">
                        <div>&bull; Complexity: T(n) = 2T(n/2) + O(n) &rArr; O(n log n)</div>
                        <div>&bull; Memory Latency: Effective_Access = Hit_Time + (Miss_Rate &times; Penalty)</div>
                        <div>&bull; Nyquist Theorem: Sampling_Rate &ge; 2 &times; Frequency_Max</div>
                      </div>
                      <p className="text-[11px] text-slate-400 mt-2">Diagrams and hand-drawn schema included in full PDF download.</p>
                    </div>
                  )}

                  {previewPageIndex === 3 && (
                    <div>
                      <h5 className="font-extrabold text-amber-300 text-sm mb-1">Section 3: Solved Past Exam Problems</h5>
                      <p className="text-xs text-slate-300 leading-relaxed">
                        Step-by-step walkthroughs of 10 recurring university mid-term and semester final problems with verified solutions.
                      </p>
                      <div className="mt-2 text-xs font-mono text-emerald-300">
                        &bull; Includes 2024 &amp; 2025 question bank solutions
                      </div>
                    </div>
                  )}
                </div>

                {/* Deck Page Navigation */}
                <div className="flex items-center justify-between pt-2 border-t border-white/10 text-xs">
                  <button
                    disabled={previewPageIndex <= 1}
                    onClick={() => setPreviewPageIndex((p) => Math.max(1, p - 1))}
                    className="px-3 py-1 rounded-lg bg-white/10 hover:bg-white/20 disabled:opacity-30 disabled:cursor-not-allowed transition flex items-center gap-1 font-bold cursor-pointer"
                  >
                    <ChevronLeft size={14} /> Prev Page
                  </button>
                  <span className="text-[11px] font-mono text-slate-400">Page {previewPageIndex} of 3</span>
                  <button
                    disabled={previewPageIndex >= 3}
                    onClick={() => setPreviewPageIndex((p) => Math.min(3, p + 1))}
                    className="px-3 py-1 rounded-lg bg-white/10 hover:bg-white/20 disabled:opacity-30 disabled:cursor-not-allowed transition flex items-center gap-1 font-bold cursor-pointer"
                  >
                    Next Page <ChevronRight size={14} />
                  </button>
                </div>
              </div>
            </div>

            {/* Modal Footer Actions */}
            <div className="flex items-center justify-between pt-4 border-t border-slate-100">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(window.location.href);
                  showToast('Note deck link copied to clipboard!');
                }}
                className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl border border-slate-200 text-xs font-bold text-slate-700 hover:bg-slate-50 transition cursor-pointer"
              >
                <Share2 size={14} />
                <span>Share Deck</span>
              </button>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => setSelectedNote(null)}
                  className="px-4 py-2 rounded-xl text-xs font-bold text-slate-600 hover:bg-slate-100 transition"
                >
                  Close
                </button>
                <button
                  onClick={() => handleDownloadDeck(selectedNote)}
                  className="px-5 py-2 rounded-xl bg-amber-500 hover:bg-amber-600 text-slate-950 text-xs font-extrabold shadow-md transition flex items-center gap-1.5 cursor-pointer"
                >
                  <Download size={14} />
                  <span>Download Full PDF Deck</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: POPUP UPLOAD STUDY NOTE MODAL (WITH REAL FILE INPUT) */}
      {showUploadNoteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-md">
          <div className="bg-white rounded-3xl max-w-xl w-full p-6 sm:p-8 shadow-2xl border border-slate-100 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div>
                <span className="px-3 py-0.5 rounded-full bg-amber-50 text-amber-800 text-[10px] font-extrabold uppercase">
                  Contribute &bull; +50 Points
                </span>
                <h3 className="font-extrabold text-xl text-slate-900 font-heading mt-1">Upload Courseware Notes</h3>
              </div>
              <button onClick={() => setShowUploadNoteModal(false)} className="text-slate-400 hover:text-slate-600">
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleNoteSubmit} className="mt-5 space-y-4">
              {/* Working Real File Dropzone */}
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputModalRef.current?.click()}
                className={`border-2 border-dashed rounded-2xl p-6 text-center transition cursor-pointer select-none group ${
                  isDragging
                    ? 'border-amber-500 bg-amber-100/50'
                    : uploadedFileDetails
                    ? 'border-emerald-400 bg-emerald-50/40'
                    : 'border-amber-300 hover:border-amber-500 bg-amber-50/40 hover:bg-amber-50'
                }`}
              >
                <div className="w-12 h-12 rounded-2xl bg-amber-100 text-amber-700 mx-auto flex items-center justify-center mb-2 group-hover:scale-110 transition">
                  {uploadedFileDetails ? <FileCheck size={24} className="text-emerald-600" /> : <Upload size={22} />}
                </div>

                {uploadedFileDetails ? (
                  <div>
                    <div className="text-xs font-extrabold text-emerald-800 flex items-center justify-center gap-1.5">
                      <CheckCircle2 size={14} className="text-emerald-600" />
                      <span>{uploadedFileDetails.name}</span>
                    </div>
                    <div className="text-[11px] font-mono text-slate-500 mt-0.5">
                      {uploadedFileDetails.size} &bull; Click to change file
                    </div>
                  </div>
                ) : (
                  <div>
                    <div className="text-xs font-bold text-slate-800">
                      Click to choose document or drag &amp; drop
                    </div>
                    <div className="text-[11px] text-slate-500 mt-1">
                      Accepts PDF, DOCX, DOC, PNG, or JPG (up to 25 MB)
                    </div>
                  </div>
                )}
              </div>

              {/* Upload Progress Bar */}
              {isUploading && (
                <div className="space-y-1.5 p-3 rounded-xl bg-slate-50 border border-slate-200">
                  <div className="flex justify-between text-xs font-bold text-slate-700">
                    <span>Uploading Deck to Vault...</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-amber-500 to-indigo-600 transition-all duration-200 rounded-full"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                </div>
              )}

              {/* Title Input */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                  Document Title *
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Operating Systems: Virtual Memory & Paging Cheat Sheet"
                  value={noteForm.title}
                  onChange={(e) => setNoteForm({ ...noteForm, title: e.target.value })}
                  className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>

              {/* Subject & Semester */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Subject / Discipline *
                  </label>
                  <select
                    value={noteForm.subject}
                    onChange={(e) => setNoteForm({ ...noteForm, subject: e.target.value })}
                    className="w-full px-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
                  >
                    <option value="Computer Science">Computer Science</option>
                    <option value="Operating Systems">Operating Systems</option>
                    <option value="Artificial Intelligence">Artificial Intelligence</option>
                    <option value="Data Structures & Algorithms">Data Structures &amp; Algorithms</option>
                    <option value="Mathematics">Mathematics</option>
                    <option value="Computer Networks">Computer Networks</option>
                    <option value="Database Systems">Database Systems</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Academic Semester *
                  </label>
                  <select
                    value={noteForm.semester}
                    onChange={(e) => setNoteForm({ ...noteForm, semester: e.target.value })}
                    className="w-full px-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
                  >
                    <option value="Semester 1">Semester 1</option>
                    <option value="Semester 2">Semester 2</option>
                    <option value="Semester 3">Semester 3</option>
                    <option value="Semester 4">Semester 4</option>
                    <option value="Semester 5">Semester 5</option>
                    <option value="Semester 6">Semester 6</option>
                    <option value="Semester 7">Semester 7</option>
                    <option value="Semester 8">Semester 8</option>
                  </select>
                </div>
              </div>

              {/* Description */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                  Key Topics &amp; Formulas Covered
                </label>
                <textarea
                  rows="3"
                  placeholder="Outline core definitions, formulas, or practice problems in this deck..."
                  value={noteForm.description}
                  onChange={(e) => setNoteForm({ ...noteForm, description: e.target.value })}
                  className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
                ></textarea>
              </div>

              {/* Submit Actions */}
              <div className="flex justify-end gap-3 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowUploadNoteModal(false)}
                  className="px-4 py-2.5 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isUploading}
                  className="px-6 py-2.5 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-extrabold text-xs rounded-xl shadow-md transition flex items-center gap-1.5 cursor-pointer"
                >
                  <Upload size={14} />
                  <span>{isUploading ? 'Uploading...' : 'Publish to Notes Vault'}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL: BOOK DETAILS / SYNOPSIS & AUDIO MODAL */}
      {selectedBook && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white rounded-3xl max-w-xl w-full p-6 sm:p-8 shadow-2xl border border-slate-100 max-h-[90vh] overflow-y-auto">
            <div className="flex items-start justify-between pb-4 border-b border-slate-100">
              <div>
                <span className="px-2.5 py-1 rounded-md bg-indigo-50 text-indigo-700 text-xs font-bold">
                  {typeof selectedBook.category === 'string' ? selectedBook.category : selectedBook.category?.name || 'Computer Science'}
                </span>
                <h3 className="font-extrabold text-xl text-slate-900 mt-2 font-heading leading-tight">{selectedBook.title}</h3>
                <p className="text-xs text-slate-500 mt-1">
                  by {typeof selectedBook.author === 'string' ? selectedBook.author : selectedBook.author?.name || 'Author'}
                </p>
              </div>
              <button
                onClick={() => {
                  if (isSpeaking) window.speechSynthesis.cancel();
                  setIsSpeaking(false);
                  setSelectedBook(null);
                }}
                className="p-1.5 text-slate-400 hover:text-slate-600 rounded-full hover:bg-slate-100 transition"
              >
                <X size={20} />
              </button>
            </div>

            <div className="my-5 space-y-4">
              <div className="p-4 rounded-2xl bg-indigo-50/70 border border-indigo-100 flex items-center justify-between">
                <div>
                  <div className="text-[10px] uppercase font-bold text-indigo-500 tracking-wider">Physical Coordinates</div>
                  <div className="text-sm font-mono font-bold text-slate-900 mt-0.5">
                    {selectedBook.shelf_location || 'Zone A · Rack 01 · Shelf 1'}
                  </div>
                </div>
                <span className="px-3 py-1 rounded-full bg-white text-indigo-700 text-xs font-bold border border-indigo-200">
                  {selectedBook.difficulty_level || 'Intermediate'} Level
                </span>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <h5 className="font-bold text-xs uppercase tracking-wider text-slate-500">Executive Summary</h5>
                  <button
                    onClick={() => handleSpeakSummary(selectedBook.summary || selectedBook.description || selectedBook.title)}
                    className="inline-flex items-center gap-1 text-xs font-bold text-indigo-600 hover:text-indigo-800 cursor-pointer"
                  >
                    <Volume2 size={14} className={isSpeaking ? 'animate-pulse text-amber-500' : ''} />
                    <span>{isSpeaking ? 'Stop Audio' : 'Listen'}</span>
                  </button>
                </div>
                <p className="text-sm text-slate-600 leading-relaxed bg-slate-50 p-4 rounded-2xl border border-slate-100">
                  {selectedBook.summary || selectedBook.description || 'Standard institutional reference textbook. Covers fundamental theory, proofs, algorithms, and practical applications.'}
                </p>
              </div>

              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-xs text-slate-600 font-medium">Academic Citation (APA &bull; IEEE)</span>
                <button
                  onClick={() => handleCopyCitation(selectedBook)}
                  className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-xs font-bold text-slate-700 hover:bg-slate-50 transition cursor-pointer"
                >
                  {copiedCitation ? <Check size={13} className="text-emerald-600" /> : <Copy size={13} />}
                  <span>{copiedCitation ? 'Copied' : 'Copy Citation'}</span>
                </button>
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
              <button
                onClick={() => {
                  if (isSpeaking) window.speechSynthesis.cancel();
                  setIsSpeaking(false);
                  setSelectedBook(null);
                }}
                className="px-4 py-2.5 rounded-xl border border-slate-200 text-xs font-bold text-slate-600 hover:bg-slate-50 transition"
              >
                Close
              </button>
              <button
                onClick={() => {
                  handleBorrow(selectedBook.id);
                  setSelectedBook(null);
                }}
                disabled={(selectedBook.available_quantity ?? 1) <= 0}
                className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold shadow-md shadow-indigo-200 transition flex items-center gap-2 cursor-pointer"
              >
                <BookOpen size={14} />
                <span>Confirm Borrow Record</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: HOLOGRAPHIC DIGITAL STUDENT ID PASS */}
      {showPassModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-md">
          <div className="bg-gradient-to-br from-indigo-950 via-slate-900 to-indigo-900 text-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-white/20 relative overflow-hidden">
            <div className="absolute top-0 right-0 -mr-12 -mt-12 w-48 h-48 rounded-full bg-cyan-500/20 blur-3xl pointer-events-none"></div>

            <div className="flex items-center justify-between pb-4 border-b border-white/10">
              <div>
                <span className="text-[10px] font-mono tracking-widest uppercase text-cyan-300 font-bold">NEXSHELF UNIVERSITY LIBRARY</span>
                <h4 className="text-lg font-extrabold tracking-tight font-heading">Digital Student Access Pass</h4>
              </div>
              <button onClick={() => setShowPassModal(false)} className="text-white/60 hover:text-white">
                <X size={20} />
              </button>
            </div>

            <div className="my-6 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Scholar Name</div>
                  <div className="text-lg font-bold font-heading">{profile.full_name || user?.full_name || 'Scholar'}</div>
                  <div className="text-xs font-mono text-indigo-300">{profile.email || user?.email}</div>
                </div>
                <div className="w-20 h-20 bg-white p-2 rounded-xl flex items-center justify-center shadow-lg">
                  <QrCode size={64} className="text-slate-900" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3 pt-3 border-t border-white/10 text-xs">
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-bold">Student ID</span>
                  <span className="font-mono font-bold text-white text-sm">{profile.student_id || 'STU-0004'}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-bold">Department</span>
                  <span className="font-semibold text-white">{profile.department || 'Computer Science'}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-bold">Academic Standing</span>
                  <span className="text-emerald-400 font-bold flex items-center gap-1">
                    <CheckCircle2 size={12} /> Active &bull; Good Standing
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-bold">Expiration</span>
                  <span className="font-mono text-white">Spring 2027</span>
                </div>
              </div>
            </div>

            <button
              onClick={() => setShowPassModal(false)}
              className="w-full py-2.5 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 text-xs font-bold text-white transition"
            >
              Dismiss Pass
            </button>
          </div>
        </div>
      )}

      {/* MODAL: ACQUISITION WISHLIST */}
      {showWishlistModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <h3 className="font-bold text-lg text-slate-900">Request a Book for Library Acquisition</h3>
              <button onClick={() => setShowWishlistModal(false)} className="text-slate-400 hover:text-slate-600">
                <X size={20} />
              </button>
            </div>
            <form onSubmit={handleWishlistSubmit} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase text-slate-600 mb-1">Book Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Concrete Mathematics"
                  value={wishlistForm.title}
                  onChange={(e) => setWishlistForm({ ...wishlistForm, title: e.target.value })}
                  className="w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase text-slate-600 mb-1">Author</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Ronald L. Graham, Donald E. Knuth"
                  value={wishlistForm.author}
                  onChange={(e) => setWishlistForm({ ...wishlistForm, author: e.target.value })}
                  className="w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase text-slate-600 mb-1">Academic Reason</label>
                <textarea
                  rows="3"
                  required
                  placeholder="Why is this textbook essential for your coursework or research?"
                  value={wishlistForm.reason}
                  onChange={(e) => setWishlistForm({ ...wishlistForm, reason: e.target.value })}
                  className="w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                ></textarea>
              </div>
              <div className="flex justify-end gap-3 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowWishlistModal(false)}
                  className="px-4 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm rounded-xl shadow"
                >
                  Submit Acquisition Request
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL: POST PEER OFFER (SELL / BUY / EXCHANGE) */}
      {showPostOfferModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-7 shadow-2xl border border-slate-100 my-8">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div>
                <h3 className="font-bold text-lg text-slate-900">List Book on Peer Marketplace</h3>
                <p className="text-xs text-slate-500">Sell, exchange, request to buy, or donate textbooks to classmates.</p>
              </div>
              <button
                onClick={() => setShowPostOfferModal(false)}
                className="text-slate-400 hover:text-slate-600 p-1 rounded-lg"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleOfferSubmit} className="mt-4 space-y-4">
              {/* Listing Purpose / Type */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                  What would you like to do?
                </label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {[
                    { id: 'sell', label: '🏷️ Sell Book' },
                    { id: 'exchange', label: '🔄 Exchange' },
                    { id: 'buy', label: '🔍 Want to Buy' },
                    { id: 'free_giveaway', label: '🎁 Free Gift' },
                  ].map((t) => (
                    <button
                      key={t.id}
                      type="button"
                      onClick={() => setOfferForm({ ...offerForm, offer_type: t.id })}
                      className={`p-2.5 rounded-xl text-xs font-bold border transition text-center cursor-pointer ${
                        offerForm.offer_type === t.id
                          ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm'
                          : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                      }`}
                    >
                      {t.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Title & Author */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                  Book Title *
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Database System Concepts, 7th Edition"
                  value={offerForm.title}
                  onChange={(e) => setOfferForm({ ...offerForm, title: e.target.value })}
                  className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Author / Publication *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Silberschatz & Korth"
                    value={offerForm.author}
                    onChange={(e) => setOfferForm({ ...offerForm, author: e.target.value })}
                    className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Condition
                  </label>
                  <select
                    value={offerForm.condition}
                    onChange={(e) => setOfferForm({ ...offerForm, condition: e.target.value })}
                    className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
                  >
                    <option value="Brand New">Brand New (Unopened)</option>
                    <option value="Like New">Like New (Highlighted)</option>
                    <option value="Good">Good (Readable)</option>
                    <option value="Fair">Fair (Handwritten notes)</option>
                  </select>
                </div>
              </div>

              {/* Price (if sell or buy) */}
              {(offerForm.offer_type === 'sell' || offerForm.offer_type === 'buy') && (
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    {offerForm.offer_type === 'sell' ? 'Selling Price (₹) *' : 'Offered Budget (₹) *'}
                  </label>
                  <input
                    type="number"
                    step="1"
                    min="0"
                    required
                    placeholder="e.g. 250"
                    value={offerForm.price}
                    onChange={(e) => setOfferForm({ ...offerForm, price: e.target.value })}
                    className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              )}

              {/* Contact Information - IN ALL CONDITIONS & LISTING TYPES */}
              <div className="p-4 rounded-2xl bg-indigo-50/70 border border-indigo-100 space-y-3">
                <div className="flex items-center gap-2 text-indigo-900 font-bold text-xs uppercase tracking-wider">
                  <Phone size={14} className="text-indigo-600" />
                  <span>Contact Information (Active For All Conditions &amp; Options)</span>
                </div>
                <p className="text-[11px] text-slate-600">
                  Classmates will use this mobile number or WhatsApp to call you directly to arrange book inspection and campus handover.
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-[11px] font-bold uppercase text-slate-700 mb-1">
                      Mobile / Phone Number (Call / SMS) *
                    </label>
                    <input
                      type="tel"
                      required
                      placeholder="+91 98765 43210"
                      value={offerForm.contact_phone}
                      onChange={(e) => setOfferForm({ ...offerForm, contact_phone: e.target.value })}
                      className="w-full px-3.5 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono"
                    />
                  </div>

                  <div>
                    <label className="block text-[11px] font-bold uppercase text-slate-700 mb-1">
                      WhatsApp Number (Optional)
                    </label>
                    <input
                      type="tel"
                      placeholder="+91 98765 43210"
                      value={offerForm.contact_whatsapp}
                      onChange={(e) => setOfferForm({ ...offerForm, contact_whatsapp: e.target.value })}
                      className="w-full px-3.5 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-[11px] font-bold uppercase text-slate-700 mb-1">
                    Campus Handover / Meeting Point
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. Central Library 1st Floor, Hostel 4, Main Cafeteria"
                    value={offerForm.pickup_location}
                    onChange={(e) => setOfferForm({ ...offerForm, pickup_location: e.target.value })}
                    className="w-full px-3.5 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              {/* Notes */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                  Additional Notes (Edition, Condition, Exchange wishes)
                </label>
                <textarea
                  rows="2"
                  placeholder="e.g. 7th Edition in clean condition. Willing to exchange for Computer Networks (Tanenbaum)."
                  value={offerForm.description}
                  onChange={(e) => setOfferForm({ ...offerForm, description: e.target.value })}
                  className="w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                ></textarea>
              </div>

              {/* Form Action Buttons */}
              <div className="flex justify-end gap-3 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowPostOfferModal(false)}
                  className="px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-100 rounded-xl transition cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-sm rounded-xl shadow-md transition cursor-pointer"
                >
                  Publish Listing
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

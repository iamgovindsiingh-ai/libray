# NexShelf · Modern React Single-Page Application (SPA)

This directory contains the modern **React 18 + Vite + Tailwind CSS** frontend client for **NexShelf Ultra**.

---

## 📁 Directory Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.js             # Centralized Axios/fetch REST client with JWT Bearer auth
│   ├── components/
│   │   ├── Navbar.jsx            # Frosted glass dynamic navigation bar
│   │   └── ProtectedRoute.jsx    # React Router role & session guard
│   ├── context/
│   │   └── AuthContext.jsx       # Global authentication state, session storage, and login/logout
│   ├── pages/
│   │   ├── Login.jsx             # Glassmorphic auth with 1-click Demo Student & Admin chips
│   │   ├── Register.jsx          # Digital student card issuance form
│   │   ├── StudentDashboard.jsx  # Scholar Dashboard (5 Portals, 3D Spine Bookshelf, Swaps & Notes)
│   │   ├── AdminDashboard.jsx    # Executive Control Console (KPI reels, Catalog, Issues & Moderation)
│   │   └── Contact.jsx           # Public help desk ticket dispatch
│   ├── App.jsx                   # Application routing and route guards
│   ├── main.jsx                  # React DOM root entry point
│   └── index.css                 # Custom styling, Aurora background canvas, 3D spine styles
├── index.html                    # Root HTML mount with Plus Jakarta Sans & Space Grotesk fonts
├── package.json                  # Dependencies (React 18, React Router 6, Lucide React, Tailwind)
├── tailwind.config.js            # Tailwind theme tokens & color palettes
└── vite.config.js                # Vite bundler configuration & backend API reverse proxy
```

---

## 🚀 How to Run the Frontend

1. Open a terminal in this directory:
   ```powershell
   cd frontend
   ```

2. Start the Vite development server:
   ```powershell
   npm run dev
   ```

3. Open your browser:
   👉 **`http://localhost:3000`** (or `http://localhost:5173`)

---

## 📦 How to Build for Production

```powershell
npm run build
```
This compiles the application into static HTML/CSS/JS bundles in `frontend/dist/`.


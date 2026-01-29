# ⚡ HustleReport - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Set Up Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Supabase credentials
VITE_SUPABASE_URL=your-project-url.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

**Where to find Supabase credentials:**
- Already configured in this project! Check your `.env` file

### Step 2: Start the Development Server
```bash
npm run dev
```

The app will open at: **http://localhost:3000**

### Step 3: Explore the App
- **Dashboard** (`/`) - Overview of all metrics
- **Schedule** (`/schedule`) - Optimized work schedule
- **Expenses** (`/expenses`) - Spending analysis
- **Performance** (`/performance`) - Grade and comparison
- **Reports** (`/reports`) - All documentation

---

## 📱 What You'll See

### Navigation
- Modern top navigation bar with HustleReport branding
- 5 main sections with icons
- Responsive mobile menu

### Dashboard Features
- 4 key metric cards (trips, target, earnings, net income)
- Data correction alerts (Phase 9 updates)
- Peak earning hours (10 PM - 11 PM is highest)
- Top 3 revenue zones (TX 75206, 75204, 75219)
- Monthly earnings breakdown

### Design Aesthetic
- Purple gradient background (#667eea → #764ba2)
- White content cards with shadows
- Smooth hover animations
- Clean typography
- Professional color-coded badges

---

## 🛠️ Development Commands

```bash
npm run dev      # Start development server (port 3000)
npm run build    # Build for production (creates dist/)
npm run preview  # Preview production build
npm run lint     # Check code quality
```

---

## 📊 Data Source

Currently displays **static data** from your actual analysis:
- **1,077 trips** (Aug-Dec 2025)
- **$1,985/month** actual earnings
- **$3,050/month** target
- **33.3% schedule adherence** (Grade F)

### To Connect Live Data
The database schema is ready. Run the migration script:
```bash
# Coming soon - CSV to Supabase migration
python scripts/migrate_to_supabase.py
```

---

## 🎨 Customization

### Change Colors
Edit `tailwind.config.js`:
```js
colors: {
  primary: {
    DEFAULT: '#667eea',  // Your main purple
    dark: '#764ba2',     // Darker shade
  },
}
```

### Add New Page
1. Create `src/pages/YourPage.tsx`
2. Add route in `src/App.tsx`
3. Add nav item in `src/components/Layout.tsx`

### Modify Components
All reusable components in `src/components/`:
- `StatCard.tsx` - Metric cards
- `SectionCard.tsx` - Content sections
- `GradientCard.tsx` - Feature cards
- `Alert.tsx` - Messages
- `Badge.tsx` - Status labels

---

## 🚀 Deployment

### Deploy to Netlify (Recommended)
1. Push to GitHub
2. Connect repo to Netlify
3. Settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
4. Add environment variables in Netlify UI
5. Deploy!

### Deploy to Vercel
1. Import project in Vercel
2. Auto-detects Vite settings
3. Add environment variables
4. Deploy!

---

## 🔥 Pro Tips

1. **Mobile First**: The app is fully responsive. Test on your phone!

2. **Fast Reload**: Vite's HMR means instant updates as you code

3. **TypeScript**: Hover over components to see available props

4. **Icons**: Using Lucide React. Browse icons at [lucide.dev](https://lucide.dev)

5. **Charts**: Recharts is ready. Add more visualizations easily

6. **Search**: The Reports page has search functionality (press "/" key)

---

## 📖 Key Files

| File | Purpose |
|------|---------|
| `src/main.tsx` | App entry point |
| `src/App.tsx` | Route definitions |
| `src/components/Layout.tsx` | Navigation shell |
| `src/pages/Dashboard.tsx` | Main overview page |
| `src/lib/supabase.ts` | Database client |
| `tailwind.config.js` | Design tokens |
| `vite.config.ts` | Build config |

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
npx kill-port 3000
npm run dev
```

### Module Not Found
```bash
# Reinstall dependencies
rm -rf node_modules
npm install
```

### Build Errors
```bash
# Clear cache and rebuild
rm -rf dist
npm run build
```

### Supabase Connection Issues
- Check `.env` file has correct credentials
- Verify Supabase project is active
- Check browser console for errors

---

## ✅ Success Checklist

After running `npm run dev`, you should see:

- ✅ Purple gradient background
- ✅ White navigation bar at top
- ✅ "HustleReport" branding with logo
- ✅ 4 metric cards showing trip/earnings data
- ✅ Alert banners about Phase 9 corrections
- ✅ Peak hours section with purple cards
- ✅ Top revenue zones section
- ✅ Smooth animations on hover
- ✅ Mobile responsive (test by resizing browser)

---

## 🎯 Next Actions

### Today
- [x] Build complete
- [x] Design system implemented
- [ ] Run `npm run dev` and explore
- [ ] Test on mobile device
- [ ] Review all 5 pages

### This Week
- [ ] Add your Supabase credentials
- [ ] Deploy to Netlify/Vercel
- [ ] Create data migration script
- [ ] Add authentication

### This Month
- [ ] Real-time data updates
- [ ] User accounts
- [ ] Advanced filtering
- [ ] Export to PDF
- [ ] Share with team

---

**Need Help?**
- Full docs: `HUSTLEREPORT_REACT_BUILD_COMPLETE.md`
- Component architecture: `docs/COMPONENT_ARCHITECTURE.md`
- Original Python docs: `docs/START_HERE.md`

**Ready to launch!** 🚀

Run `npm run dev` now to see your supreme UI/UX courier analytics platform.

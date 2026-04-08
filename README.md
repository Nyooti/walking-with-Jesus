# Walking with Jesus Christ Website

A modern church website with auto-playing carousels for sermons and blog articles.

##  Features

- **15 Sermons** with auto-playing carousel (6-second intervals)
- **15 Blog Articles** with auto-playing carousel (5-second intervals)
- **Admin Panel** for content management
- **Responsive Design** for all devices
- **Smooth Animations** and transitions
- **Local Network Support** for multi-device access

##  Quick Start

### Method 1: Python Server (Recommended)

1. **Start the server:**
   ```bash
   python server.py
   ```

2. **Access the website:**
   - **Local:** http://localhost:8000
   - **Admin Panel:** http://localhost:8000/admin.html
   - **Network:** Check server output for your local IP

### Method 2: Using start.bat (Windows)

1. **Double-click** the `start.bat` file
2. **Wait** for the server to start
3. **Open** your browser to the shown URL

### Method 3: Manual Python

```bash
cd /path/to/walking-with-jesus-christ-main
python -m http.server 8000
```

## 🌐 Local Network Access

When you run the server, it will show:

```
🌍 Walking with Jesus Christ Website Server
============================================================
📁 Serving directory: /path/to/your/project
🌐 Local access: http://localhost:8000
🏠 Network access: http://192.168.1.100:8000
📱 Admin panel: http://192.168.1.100:8000/admin.html
============================================================
```

**Other devices on your network can access using the Network URL!**

##  Mobile Access

1. **Connect** all devices to the same WiFi network
2. **Start the server** on your main computer
3. **Open** the Network URL on mobile devices
4. **Enjoy** the full website experience on any device

##  Carousel Features

### Sermons Carousel
- **Auto-play:** Starts automatically (6 seconds per slide)
- **15 Sermons:** 5 pages with 3 sermons each
- **Hover Pause:** Pauses when you hover over sermons
- **Manual Navigation:** Arrow buttons and dot indicators
- **Background Images:** Theme-matching visuals for each sermon

### Blog Carousel
- **Auto-play:** Starts automatically (5 seconds per slide)
- **15 Articles:** 5 pages with 3 articles each
- **Categories:** Theology, Culture, Biblical Interpretation
- **Hover Pause:** Pauses when you hover over articles
- **Manual Navigation:** Arrow buttons and dot indicators

## 🔧 Admin Panel

Access the admin panel at `/admin.html` to:
- **Update Sermon Content** (titles, dates, videos, notes)
- **Change Background Images**
- **Manage All 15 Sermons**
- **Real-time Updates** to main website

##  Content Structure

### Sermons (March-June 2026)
- **Page 1:** Grace, Faith, Fruit of Spirit
- **Page 2:** Healing, Prayer, Blood of Jesus
- **Page 3:** Kingdom, Victory, Holy Spirit
- **Page 4:** Fear, Name of Jesus, Protection
- **Page 5:** Word of God, Worship, End Times

### Blog Articles
- **Christian Theology:** 5 articles
- **Cultural Commentary:** 5 articles
- **Biblical Interpretation:** 5 articles

##  Customization

### Change Port
```bash
python server.py --port 8080
```

### Stop Server
Press `Ctrl+C` in the terminal

### Update Content
1. Open `/admin.html`
2. Make changes
3. Click "Update Sermons"
4. Changes appear immediately on main site

##  Browser Support

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## 🔒 Security Note

This is a local development server. For production deployment, consider using a proper web server like Apache or Nginx.

##  Support

If you encounter issues:
1. Check that Python is installed
2. Ensure port 8000 is not in use
3. Verify all devices are on the same network
4. Check firewall settings if network access fails
<p align="center">
  <img src="logo.png" alt="Sentiment Engine Logo" width="120" />
</p>

<h1 align="center">Sentiment Engine</h1>

<p align="center">
  <strong>AI-Driven, Multi-Language Political Sentiment Analysis Platform for India</strong>
</p>

<p align="center">
  <em>Built for India Innovates 2026 Hackathon</em>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#api-reference">API Reference</a> •
  <a href="#project-structure">Project Structure</a>
</p>

---

## Overview

**Sentiment Engine** is a real-time political sentiment analysis platform designed for India. It scrapes data from multiple sources (YouTube, Reddit, News, Twitter), performs multilingual NLP analysis across **11 Indian languages**, maps sentiments to parliamentary constituencies, and delivers actionable intelligence through an interactive dashboard with live heatmaps, charts, and Telegram alerts.

---

## Features

- **Multi-Source Data Ingestion** — Scrapes YouTube comments, Reddit posts, news articles, and tweets in parallel
- **11 Indian Languages** — Supports Hindi, English, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, and Urdu — plus Hinglish (Roman Hindi) detection
- **XLM-RoBERTa Sentiment Analysis** — Transformer-based multilingual sentiment classification with confidence scores
- **Topic Extraction** — KeyBERT-powered keyphrase extraction with political keyword fallback
- **Constituency Mapping** — Maps content to 10 Indian parliamentary constituencies with booth-level granularity
- **AI-Powered Reports** — LLaMA 3.1 / Gemini 2.0 Flash generate constituency intelligence reports and daily briefings
- **Negative Sentiment Spike Detection** — Automatic detection of sentiment spikes with severity classification
- **Telegram Alerts** — Real-time notifications for sentiment spikes, daily summaries, and system events
- **Interactive Dashboard** — Live charts, sentiment timeline, topic trends, source breakdown, and language distribution
- **Constituency Heatmap** — Leaflet-based map with color-coded sentiment scores per constituency
- **In-Memory Caching** — TTL-based cache for fast dashboard responses

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10, FastAPI, Uvicorn |
| **Frontend** | React 19, TypeScript, Vite 7, Tailwind CSS 4 |
| **NLP / ML** | HuggingFace Transformers (XLM-RoBERTa), spaCy, KeyBERT, PyTorch |
| **LLMs** | Groq (LLaMA 3.1 8B Instant), Google Gemini 2.0 Flash |
| **Translation** | deep-translator (Google Translate) |
| **Database** | MongoDB Atlas |
| **Scraping** | YouTube Data API v3, NewsAPI, Google News RSS, Arctic Shift / PullPush (Reddit), snscrape (Twitter) |
| **Alerts** | Telegram Bot API |
| **Charts** | Recharts |
| **Maps** | Leaflet + React-Leaflet |
| **Animations** | Framer Motion |
| **Data Fetching** | TanStack React Query, Axios |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                          │
│  Dashboard │ Sentiment Analyzer │ Heatmap │ Alerts │ About  │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API (Axios + React Query)
┌──────────────────────▼──────────────────────────────────────┐
│                   FastAPI Backend                           │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │  Scrapers   │  │   NLP Engine │  │   Alert System    │   │
│  │ ─────────── │  │ ──────────── │  │ ───────────────── │   │
│  │ • YouTube   │  │ • Sentiment  │  │ • Spike Detector  │   │
│  │ • Reddit    │→ │ • Topics     │→ │ • Telegram Alerts │   │
│  │ • News      │  │ • Translator │  │                   │   │
│  │ • Twitter   │  │ • Summarizer │  └───────────────────┘   │
│  └─────────────┘  │ • Entities   │                          │
│                   └──────┬───────┘                          │
│  ┌─────────────┐         │         ┌───────────────────┐    │
│  │  Geo Mapper │◄────────┘         │   TTL Cache       │    │
│  │ • Constit.  │                   │   (In-Memory)     │    │
│  │ • Booths    │                   └───────────────────┘    │
│  └──────┬──────┘                                            │
└─────────┼───────────────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────────────────────┐
│              MongoDB Atlas (sentimentdb)                    │
│  raw_data │ sentiments │ topics │ alerts │ constituencies   │
└─────────────────────────────────────────────────────────────┘
```

### Data Pipeline

```
Scrape → Strip HTML → Detect Language → Batch Sentiment Analysis
→ Topic Extraction → Constituency Mapping → Booth Mapping
→ Batch Save to MongoDB → Cache Invalidation
→ Spike Detection → AI Summary → Telegram Notification
```

---

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **MongoDB Atlas** account (free tier works)
- API keys for: YouTube Data API, NewsAPI, Groq, Telegram Bot

### 1. Clone the Repository

```bash
git clone https://github.com/ParthChauhan1658/Sentiment-Engine.git
cd Sentiment-Engine
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Environment Variables

Create a `.env` file in the project root:

```env
# Required
YOUTUBE_API_KEY=your_youtube_api_key
NEWS_API_KEY=your_newsapi_key
GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_connection_string
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Optional
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Start the Backend

```bash
cd backend
python main.py
```

The API server starts at `http://localhost:8000`.

### 5. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend starts at `http://localhost:3000` and proxies API requests to the backend.

### 6. Verify

- Open `http://localhost:3000` — Landing page
- Open `http://localhost:8000/health` — Backend health check
- Open `http://localhost:8000/docs` — FastAPI interactive API docs

---

## API Reference

### Core Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root info |
| `GET` | `/health` | Health check with DB status and service readiness |
| `GET` | `/api/scrape-and-analyze?keywords=` | Full pipeline: scrape all sources → analyze → save → alert |
| `GET` | `/api/scrape-source?source=&keywords=` | Scrape a single source (`youtube`, `reddit`, `news`, `twitter`) |
| `GET` | `/api/generate-report?constituency=` | AI-generated constituency or overall report |
| `GET` | `/api/clear-data` | Clear all data (testing only) |
| `GET` | `/api/clean-html` | Strip HTML artifacts from stored text |

### Dashboard — `/api/dashboard`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/summary?hours=24` | Sentiment counts (positive / negative / neutral) |
| `GET` | `/timeline?hours=24` | Hourly sentiment breakdown |
| `GET` | `/topics?limit=20&hours=24` | Trending topics |
| `GET` | `/sources?hours=24` | Data count by source |
| `GET` | `/languages?hours=24` | Data count by language |
| `GET` | `/recent?limit=50&page=1` | Recent results (paginated) |
| `GET` | `/stats` | Database statistics |

### Sentiment Analysis — `/api/sentiment`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/analyze` | Analyze a single text (`{text, translate_first?}`) |
| `POST` | `/analyze-batch` | Analyze multiple texts (`{texts[]}`) |
| `GET` | `/test` | Test with 5 sample texts (English + Hindi) |

### Alerts — `/api/alerts`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/recent?limit=10` | Recent alerts |
| `POST` | `/test` | Send a test alert to Telegram |

### Map — `/api/map`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/constituencies` | All constituencies with coordinates |
| `GET` | `/heatmap?hours=24` | Sentiment heatmap data (score, lat/lng, mentions) |
| `GET` | `/constituency/{name}?hours=24` | Detailed data for a specific constituency |

---

## Project Structure

```
sentiment-engine/
├── backend/
│   ├── main.py                 # FastAPI app, pipeline orchestration
│   ├── config.py               # Environment config, constants
│   ├── services.py             # Service registry (singleton init)
│   ├── cache.py                # In-memory TTL cache
│   ├── requirements.txt        # Python dependencies
│   ├── api/
│   │   ├── dashboard_routes.py # Dashboard data endpoints
│   │   ├── sentiment_routes.py # Text analysis endpoints
│   │   ├── alert_routes.py     # Alert endpoints
│   │   └── map_routes.py       # Map & constituency endpoints
│   ├── nlp/
│   │   ├── sentiment.py        # XLM-RoBERTa sentiment analyzer
│   │   ├── topics.py           # KeyBERT topic extraction
│   │   ├── summarizer.py       # Groq/Gemini AI summarizer
│   │   ├── entities.py         # spaCy named entity extraction
│   │   └── translator.py       # Multi-language translation & detection
│   ├── scrapers/
│   │   ├── scraper_manager.py  # Parallel scraper orchestrator
│   │   ├── youtube_scraper.py  # YouTube Data API v3
│   │   ├── news_scraper.py     # NewsAPI + Google News RSS
│   │   ├── reddit_scraper.py   # Arctic Shift / PullPush / Reddit JSON
│   │   └── twitter_scraper.py  # snscrape (best-effort)
│   ├── database/
│   │   ├── models.py           # MongoDB document schemas
│   │   └── mongo_client.py     # MongoDB Atlas client (singleton)
│   ├── alerts/
│   │   ├── spike_detector.py   # Negative sentiment spike detection
│   │   └── telegram_alert.py   # Telegram Bot notifications
│   └── geo/
│       ├── constituency_mapper.py  # Text → constituency mapping
│       └── booth_mapper.py         # Constituency → booth mapping
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts          # Vite 7 + proxy + chunk splitting
│   ├── tsconfig.json
│   └── src/
│       ├── App.tsx             # Router + layout
│       ├── main.tsx            # Entry point
│       ├── index.css           # Tailwind + global styles
│       ├── api/                # Axios API clients
│       ├── components/         # Reusable UI components
│       ├── hooks/              # React Query hooks
│       ├── layouts/            # MainLayout (Navbar + Footer)
│       ├── pages/              # Route pages
│       └── utils/              # Constants + formatters
├── data/
│   └── constituencies.json     # Constituency data
├── scripts/
│   └── verify_keys.py          # API key verification script
├── .env                        # Environment variables (not committed)
├── .gitignore
├── ABOUT.md
└── README.md
```

---

## NLP Models

| Component | Model | Purpose |
|---|---|---|
| **Sentiment Analysis** | `cardiffnlp/twitter-xlm-roberta-base-sentiment` | Multilingual sentiment (100+ languages) |
| **Topic Extraction** | KeyBERT + `all-MiniLM-L6-v2` | Keyphrase extraction with MMR diversity |
| **Entity Recognition** | spaCy `en_core_web_sm` | Person, Org, Location extraction |
| **Translation** | Google Translate (via deep-translator) | Indian language → English |
| **Summarization** | Groq LLaMA 3.1 8B / Gemini 2.0 Flash | AI reports and briefings |

---

## Supported Languages

| Language | Script | Code |
|---|---|---|
| English | Latin | `en` |
| Hindi | Devanagari | `hi` |
| Hinglish | Latin (Roman Hindi) | `hi-Latn` |
| Tamil | Tamil | `ta` |
| Telugu | Telugu | `te` |
| Bengali | Bengali | `bn` |
| Marathi | Devanagari | `mr` |
| Gujarati | Gujarati | `gu` |
| Kannada | Kannada | `kn` |
| Malayalam | Malayalam | `ml` |
| Punjabi | Gurmukhi | `pa` |
| Urdu | Arabic | `ur` |

---

## Monitored Constituencies

| Constituency | State |
|---|---|
| Varanasi | Uttar Pradesh |
| New Delhi | Delhi |
| Mumbai North | Maharashtra |
| Chennai South | Tamil Nadu |
| Kolkata North | West Bengal |
| Lucknow | Uttar Pradesh |
| Patna Sahib | Bihar |
| Gandhinagar | Gujarat |
| Bangalore South | Karnataka |
| Hyderabad | Telangana |

---

## Alert System

- **Spike Threshold:** > 60% negative sentiment triggers an alert
- **Change Threshold:** > 50% shift from baseline
- **Minimum Data Points:** 10 posts required before evaluation
- **Severity Levels:**
  - 🔴 **HIGH** — > 80% negative sentiment
  - 🟡 **MEDIUM** — > 60% negative sentiment
- **Delivery:** Telegram Bot with rich HTML formatting

---

## License

This project was built for the **India Innovates 2026 Hackathon**.

---

<p align="center">
  Made with ❤️ for Indian Democracy
</p>

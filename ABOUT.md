# Sentiment Engine — Detailed Project Overview

> **AI-Driven, Multi-Language Political Sentiment Analysis Platform for India**
> Built for **India Innovates 2026 Hackathon**

---

## Table of Contents

1. [What Is Sentiment Engine?](#1-what-is-sentiment-engine)
2. [Who Are the Users?](#2-who-are-the-users)
3. [Tonality & Sentiment Classification](#3-tonality--sentiment-classification)
4. [Data Sources & Scraping](#4-data-sources--scraping)
5. [Language Support & Translation](#5-language-support--translation)
6. [NLP Pipeline — How It Works](#6-nlp-pipeline--how-it-works)
7. [Geo-Mapping — Constituencies & Booths](#7-geo-mapping--constituencies--booths)
8. [Alerting & Spike Detection](#8-alerting--spike-detection)
9. [AI Summarization & Report Generation](#9-ai-summarization--report-generation)
10. [Frontend — The Dashboard Experience](#10-frontend--the-dashboard-experience)
11. [Backend — API Architecture](#11-backend--api-architecture)
12. [Database & Storage](#12-database--storage)
13. [Tech Stack](#13-tech-stack)
14. [End-to-End Data Flow](#14-end-to-end-data-flow)
15. [Project Structure](#15-project-structure)
16. [Authentication & Access](#16-authentication--access)
17. [Getting Started](#17-getting-started)

---

## 1. What Is Sentiment Engine?

Sentiment Engine is a **real-time political sentiment analysis platform** designed specifically for the Indian political landscape. It continuously scrapes public discourse from four major social and news platforms (YouTube, Reddit, News outlets, and Twitter/X), processes the text through a multi-stage NLP pipeline, and presents actionable insights through a premium interactive dashboard.

### Core Capabilities

- **Multi-platform scraping** — Collects public political discourse from YouTube comments, Reddit posts, news articles, and Twitter/X posts in real time.
- **Multi-language sentiment analysis** — Classifies text as positive, negative, or neutral across 11+ Indian languages using a cross-lingual transformer model.
- **Constituency-level geo-mapping** — Maps every piece of analyzed content to Indian parliamentary constituencies (down to booth-level granularity) for geographic sentiment visualization.
- **Spike detection & alerting** — Automatically detects sudden surges in negative sentiment within any constituency and sends real-time alerts via Telegram.
- **AI-powered reporting** — Generates narrative summaries and constituency-specific reports using large language models (Groq LLaMA 3.1 / Google Gemini).
- **Interactive dashboard** — Presents all data through rich charts, maps, timelines, and feeds with auto-refreshing live data.

### The Problem It Solves

Political analysts, journalists, campaign strategists, and governance bodies need to understand public sentiment across India's diverse, multilingual population. Manually tracking opinions across platforms and languages is impossible at scale. Sentiment Engine automates this entire workflow — from data collection to insight delivery — providing a single pane of glass into the political mood of the nation.

---

## 2. Who Are the Users?

Sentiment Engine is designed for the following user personas:

### Political Analysts & Strategists
- Monitor constituency-level sentiment trends to gauge public opinion on policies, candidates, and events.
- Receive spike alerts when negative sentiment surges in specific regions.
- Use AI-generated reports for quick briefings.

### Journalists & Media Houses
- Track trending political topics across platforms.
- Identify breaking sentiment shifts before they become mainstream news.
- Analyze public reaction to specific events or announcements.

### Government & Policy Makers
- Understand public perception of policies and governance actions across regions.
- Identify areas of public dissatisfaction (water, roads, corruption, healthcare, etc.).
- Geo-targeted insights help prioritize constituency-level intervention.

### Researchers & Academics
- Study political discourse patterns across languages and platforms.
- Analyze sentiment distribution across demographic and geographic dimensions.
- Use the interactive analyzer for ad-hoc sentiment classification of any text.

### General Public / Civic Tech Enthusiasts
- Explore how political sentiment varies across India via the interactive map.
- Use the single-text analyzer to classify the tonality of any political statement.
- Browse trending topics and recent discourse.

---

## 3. Tonality & Sentiment Classification

"Tonality" in Sentiment Engine refers to the **emotional tone or sentiment** expressed in a piece of political text. Every scraped item is classified into one of three sentiment categories:

### The Three Sentiment Classes

| Sentiment | Meaning | Examples | Color |
|-----------|---------|----------|-------|
| **Positive** | Favorable, supportive, optimistic, appreciative tone | *"Great initiative by the government for rural development"* | 🟢 Green (`#22c55e`) |
| **Negative** | Critical, dissatisfied, hostile, frustrated tone | *"Terrible roads in my constituency, no one cares"* | 🔴 Red (`#ef4444`) |
| **Neutral** | Factual, objective, balanced, or ambiguous tone | *"The parliament session begins on Monday"* | 🟡 Yellow (`#eab308`) |

### How Tonality Is Measured

Each classification includes three dimensions of information:

1. **Sentiment Label** — The dominant sentiment class (positive / negative / neutral).
2. **Confidence Score** (0.0 to 1.0) — How certain the model is in its classification. A score of 0.92 means the model is 92% confident.
3. **Full Score Distribution** — The probability assigned to each of the three classes. For example:
   ```
   { "positive": 0.82, "negative": 0.10, "neutral": 0.08 }
   ```
   This means the text is predominantly positive (82%), with minor negative (10%) and neutral (8%) undertones.

### Constituency-Level Sentiment Score

For geographic aggregation (the map view), a **composite sentiment score** is calculated per constituency on a scale of **-1.0 to +1.0**:

```
score = (positive_count - negative_count) / total_count
```

| Score Range | Interpretation | Map Color |
|-------------|---------------|-----------|
| **> +0.2** | Positive-leaning constituency | Green |
| **-0.2 to +0.2** | Neutral / Mixed sentiment | Yellow |
| **< -0.2** | Negative-leaning constituency | Red |

### The Model Behind Tonality

Sentiment Engine uses **`cardiffnlp/twitter-xlm-roberta-base-sentiment`** from HuggingFace — a cross-lingual RoBERTa model pre-trained on 100+ languages and fine-tuned on Twitter sentiment data. This makes it particularly well-suited for:

- **Short, informal text** typical of social media and comments
- **Multilingual content** without needing separate models per language
- **Political discourse** which often contains strong opinions, sarcasm, and mixed-code text

The model internally maps its output labels (`LABEL_0` → negative, `LABEL_1` → neutral, `LABEL_2` → positive) and returns top-k scores for all three classes with every prediction.

### Batch Processing

For efficiency, sentiment analysis runs in batches of 32 texts at a time. Each batch is processed through the transformer pipeline in a single forward pass, significantly reducing inference time when analyzing hundreds of scraped items.

---

## 4. Data Sources & Scraping

Sentiment Engine collects data from **four platforms** simultaneously using a parallel scraping architecture:

### YouTube
- **API**: Google YouTube Data API v3
- **What it scrapes**: Political video comments with like counts
- **Strategy**: Searches for political videos in the India region with Hindi relevance keywords, then extracts top-level comments from the most relevant results.
- **Data captured**: Comment text, author, like count, video title, video ID, published date.

### Reddit
- **API**: Three-tier fallback system (no API key required):
  1. **Arctic Shift API** (primary) — Historical Reddit data archive
  2. **PullPush API** (fallback) — Community-maintained Pushshift replacement
  3. **Reddit JSON endpoint** (last resort) — Direct Reddit `.json` suffix scraping
- **Subreddits monitored**: 9 India-focused political subreddits including `r/india`, `r/IndiaSpeaks`, `r/IndianPolitics`, `r/delhi`, `r/mumbai`, `r/bangalore`, `r/chennai`, `r/kolkata`, `r/hyderabad`
- **Data captured**: Post/comment text, author, score, subreddit, post URL, created date.

### News
- **APIs**: Dual-source approach:
  1. **NewsAPI** (paid tier) — Structured news article search
  2. **Google News RSS** (free) — RSS feed parsing for Indian headlines
- **Strategy**: Fetches top Indian political headlines plus keyword-specific searches in both English and Hindi.
- **Data captured**: Article title, description, source name, URL, published date.

### Twitter / X
- **Tool**: `snscrape` (Python-based Twitter scraper)
- **Status**: Best-effort — snscrape may not work reliably with X's latest API changes. The scraper gracefully degrades if unavailable (returns empty results without crashing).
- **Data captured**: Tweet text, author, likes, retweets, date.

### Parallel Scraping

All four scrapers run simultaneously via `ThreadPoolExecutor` with 4 worker threads, managed by the `ScraperManager`. Results are merged into a unified list of raw data items, each tagged with its source platform.

### Political Keywords

The system searches for content related to **24 predefined political keywords**:
> BJP, Congress, Modi, Rahul Gandhi, Parliament, Lok Sabha, Rajya Sabha, Election, CAA, NRC, Farm Laws, Budget, GST, Infrastructure, Development, Corruption, Unemployment, Inflation, Healthcare, Education, Water, Roads, Digital India, Make in India

---

## 5. Language Support & Translation

India's linguistic diversity is a core challenge. Sentiment Engine handles **11+ languages** through a multi-layered detection and translation system.

### Supported Languages

| Language | Script | Detection Method |
|----------|--------|-----------------|
| **English** | Latin | Default (>80% ASCII characters) |
| **Hindi** | Devanagari | Unicode range U+0900–U+097F |
| **Hinglish** | Latin | Custom word-matching against 80+ Hinglish words |
| **Tamil** | Tamil | Unicode range U+0B80–U+0BFF |
| **Telugu** | Telugu | Unicode range U+0C00–U+0C7F |
| **Bengali** | Bengali | Unicode range U+0980–U+09FF |
| **Gujarati** | Gujarati | Unicode range U+0A80–U+0AFF |
| **Kannada** | Kannada | Unicode range U+0C80–U+0CFF |
| **Malayalam** | Malayalam | Unicode range U+0D00–U+0D7F |
| **Punjabi** | Gurmukhi | Unicode range U+0A00–U+0A7F |
| **Urdu** | Arabic | Unicode range U+0600–U+06FF |

### Language Detection

The `TranslatorService` performs detection in this order:

1. **Script-based detection** — Checks if the text contains characters from any of 9 Indian scripts by scanning Unicode ranges. The first matching script determines the language.
2. **Hinglish detection** — If the text is primarily Latin script, it checks against a curated list of 80+ common Hinglish words (e.g., "accha", "kya", "hai", "bohot", "paisa", "sarkaar"). If >20% of words match and at least 2 Hinglish words are found, it's classified as `hi-Latn` (romanized Hindi).
3. **English fallback** — If >80% of characters are ASCII and no Hinglish is detected, the text is classified as English.

### Translation Pipeline

Non-English text is translated to English using **Google Translate** (via the `deep-translator` library) before being passed to downstream NLP tasks like topic extraction. The sentiment model itself is multilingual and can handle most Indian languages directly, but translation ensures consistent topic extraction and constituency mapping.

---

## 6. NLP Pipeline — How It Works

Every scraped text item passes through a **five-stage NLP pipeline**:

### Stage 1: Language Detection
```
Input: Raw text → Output: Language code (e.g., "en", "hi", "ta", "hi-Latn")
```
Uses the `TranslatorService` to identify the language via script detection and Hinglish heuristics.

### Stage 2: Sentiment Analysis
```
Input: Text + Language → Output: {sentiment, confidence, scores}
```
The `SentimentAnalyzer` processes texts through the **XLM-RoBERTa** model in batches of 32. Each text receives:
- A **sentiment label** (positive / negative / neutral)
- A **confidence score** (0.0–1.0)
- A **full score distribution** across all three classes

### Stage 3: Topic Extraction
```
Input: Text + Language → Output: ["water infrastructure", "corruption", ...]
```
The `TopicExtractor` uses two approaches:
- **Primary — KeyBERT**: BERT sentence-embeddings with cosine similarity and Maximal Marginal Relevance (MMR) for diversity. Extracts 1–2 word keyphrases.
- **Fallback — Keyword matching**: Scans text against 60+ predefined political terms organized by category (governance, economy, social issues, infrastructure, etc.).

For non-English text, the text is first translated to English before topic extraction.

### Stage 4: Constituency Mapping
```
Input: Text → Output: "Varanasi" | "New Delhi" | "Mumbai North" | ...
```
The `ConstituencyMapper` scans the text for location keywords (in English, Hindi, and Devanagari) and maps them to one of 10 sample parliamentary constituencies. Texts mentioning national political figures or institutions default to "New Delhi". Unknown locations remain tagged as "unknown".

### Stage 5: Booth-Level Mapping
```
Input: Constituency → Output: "VNS-003" | "DLH-001" | ...
```
The `BoothMapper` assigns texts to sample polling booth IDs within the mapped constituency. For the demo, 15 sample booths are defined across Varanasi (5), New Delhi (5), and Mumbai North (5). Assignment is randomized for demonstration purposes.

### Pipeline Output

After all five stages, each text item becomes a fully enriched document:
```json
{
  "text": "Modi government's water scheme is excellent for villages",
  "source": "youtube",
  "sentiment": "positive",
  "confidence": 0.94,
  "scores": { "positive": 0.94, "negative": 0.03, "neutral": 0.03 },
  "language": "en",
  "topics": ["water infrastructure", "modi"],
  "entities": [],
  "constituency": "Varanasi",
  "booth": "VNS-002",
  "analyzed_at": "2026-03-03T14:30:00Z"
}
```

---

## 7. Geo-Mapping — Constituencies & Booths

### Parliamentary Constituencies

Sentiment Engine maps analyzed data to **10 sample Indian parliamentary constituencies**, each with latitude/longitude coordinates for map visualization:

| Constituency | State | Coordinates |
|-------------|-------|-------------|
| Varanasi | Uttar Pradesh | 25.32°N, 82.99°E |
| New Delhi | Delhi | 28.63°N, 77.22°E |
| Mumbai North | Maharashtra | 19.18°N, 72.85°E |
| Chennai Central | Tamil Nadu | 13.08°N, 80.27°E |
| Kolkata Dakshin | West Bengal | 22.57°N, 88.36°E |
| Bangalore South | Karnataka | 12.97°N, 77.59°E |
| Hyderabad | Telangana | 17.38°N, 78.49°E |
| Ahmedabad East | Gujarat | 23.02°N, 72.58°E |
| Lucknow | Uttar Pradesh | 26.85°N, 80.95°E |
| Amritsar | Punjab | 31.63°N, 74.87°E |

### Keyword-to-Constituency Mapping

The system maintains **70+ keyword mappings** across English, Hindi, and Devanagari script. Examples:
- "varanasi", "banaras", "kashi", "वाराणसी" → **Varanasi**
- "mumbai", "bombay", "मुंबई" → **Mumbai North**
- "modi", "parliament", "lok sabha", "bjp", "congress" → **New Delhi** (national politics default)

### Booth-Level Granularity

Within each constituency, data is further mapped to sample polling booths:
- **Varanasi**: VNS-001 through VNS-005 (e.g., Dashashwamedh, Lanka, Ramnagar, Sarnath, Cantonment)
- **New Delhi**: DLH-001 through DLH-005 (e.g., Connaught Place, Karol Bagh, Patel Nagar, Rajender Nagar, Chanakyapuri)
- **Mumbai North**: MBN-001 through MBN-005 (e.g., Borivali, Kandivali, Malad, Goregaon, Dahisar)

### Map Visualization

The frontend renders an interactive **Leaflet.js** map centered on India (22.5°N, 82°E) with dark CartoDB tiles. Each constituency appears as a `CircleMarker` that is:
- **Color-coded** by sentiment score (green/yellow/red)
- **Size-scaled** by the amount of data collected
- **Clickable** — shows a popup with the full sentiment breakdown, top topics, and recent sample texts
- **Accompanied** by a ranked side panel listing all constituencies by sentiment score

---

## 8. Alerting & Spike Detection

### How Spikes Are Detected

The `SpikeDetector` runs after every scrape-and-analyze cycle and checks each constituency for sentiment anomalies:

1. **Time window**: Looks at data from the last **4 hours**.
2. **Minimum threshold**: Requires at least **10 data points** in the window (to avoid false alarms from low-volume constituencies).
3. **Spike condition**: If **>60% of sentiment** in a constituency is **negative**, a spike alert is triggered.

### Severity Levels

| Severity | Condition | Action |
|----------|-----------|--------|
| **HIGH** | >80% negative sentiment | Immediate Telegram alert with 🔴 indicator |
| **MEDIUM** | 60–80% negative sentiment | Telegram alert with 🟡 indicator |
| **LOW** | Stored but no push notification | Viewable in dashboard only |

### Telegram Alerts

When a spike is detected, the `TelegramAlerter` sends a formatted HTML message to a configured Telegram chat containing:
- Constituency name
- Severity badge (HIGH / MEDIUM)
- Negative sentiment percentage and change rate
- Top negative topics
- Timestamp

Additional Telegram notifications:
- **Daily summary** — Scheduled summary of overall sentiment trends
- **Startup notification** — Sent when the system boots up to confirm it's running

### Alert Storage

All triggered alerts are stored in MongoDB's `alerts` collection with an index on `triggered_at` for efficient retrieval. The frontend's Alerts page displays recent alerts with color-coded severity badges.

---

## 9. AI Summarization & Report Generation

### Dual-LLM Architecture

Sentiment Engine uses two large language models for generating human-readable summaries:

| Role | Model | Provider | Parameters |
|------|-------|----------|------------|
| **Primary** | LLaMA 3.1 8B Instant | Groq | temperature=0.3, max_tokens=500 |
| **Backup** | Gemini 2.0 Flash | Google | Fallback if Groq fails |

### Types of Generated Content

1. **Sentiment Summaries** — Given aggregated sentiment data, the LLM generates a narrative summary highlighting key insights, dominant sentiment, and notable trends.

2. **Constituency Reports** — Focused reports for a specific constituency, accessible via `GET /api/generate-report?constituency=Varanasi`. Includes sentiment distribution, top topics, recent trends, and AI-generated analysis.

3. **Daily Briefings** — Scheduled comprehensive summaries covering all constituencies, trending topics, and significant sentiment shifts over the past 24 hours.

### How It Works

The `Summarizer` class constructs detailed prompts containing structured data (sentiment counts, top topics, source breakdown) and instructs the LLM to produce concise, politically neutral analysis in a professional briefing style.

---

## 10. Frontend — The Dashboard Experience

The frontend is a **React 19 + TypeScript** single-page application built with **Vite**, styled with **Tailwind CSS 4**, and featuring a distinctive **"Deep Forest + Champagne"** design theme.

### Visual Design

- **Primary background**: Deep forest green (`#102C26`)
- **Accent color**: Champagne gold (`#F7E7CE`)
- **Style**: Glassmorphism (frosted glass cards with backdrop blur)
- **Typography**: Inter (body) + Space Grotesk (headings) from Google Fonts
- **Animations**: Framer Motion page transitions, scroll-triggered counters, shimmer loading states

### Pages

#### Landing Page (`/`)
The entry point featuring:
- A hero section with an India Parliament background image
- Animated stat counters (543+ constituencies, 4 platforms, 11+ languages, real-time analysis)
- Feature breakdown cards (Multilingual NLP, Constituency Mapping, Live Alerts, AI Reports)
- Data source showcase (YouTube, Reddit, News, Twitter)

#### Dashboard (`/dashboard`)
The primary analytics hub with auto-refreshing data (every 30–60 seconds):
- **Stat Cards**: Total analyzed, positive count, negative count, neutral count — each with an `AnimatedCounter`
- **Sentiment Timeline**: Stacked area chart (Recharts) showing positive/negative/neutral volume over the last 24 hours
- **Sentiment Distribution**: Pie chart showing overall positive/negative/neutral split
- **Trending Topics**: Horizontal bar chart of the top 10 extracted topics
- **Source Breakdown**: Pie chart showing data volume by platform (YouTube / Reddit / News / Twitter)
- **Language Distribution**: Bar chart showing analyzed content by language
- **Recent Analysis Feed**: Live-updating list of the most recently analyzed items with sentiment badges

#### Sentiment Analyzer (`/analyze`)
An interactive tool for manual text analysis:
- **Single mode**: Paste any text and get instant sentiment classification with a confidence bar and full score breakdown
- **Batch mode**: Analyze multiple texts separated by newlines
- Results show: sentiment badge, confidence percentage, score distribution visualization, detected language

#### Constituency Map (`/map`)
An interactive geographic view:
- **Leaflet.js** map centered on India with dark CartoDB basemap tiles
- **Circle markers** per constituency, colored by sentiment score
- **Click popups** with detailed sentiment breakdown
- **Side panel** with a color legend and ranked constituency list

#### Alerts (`/alerts`)
A real-time alert dashboard:
- Lists all triggered sentiment spike alerts
- Color-coded by severity (red for HIGH, yellow for MEDIUM, gray for LOW)
- Shows constituency name, negative percentage, change rate, and timestamps
- Auto-refreshes every 30 seconds

#### About (`/about`)
Project documentation page:
- Project description and mission statement
- Technology stack grid
- Data source descriptions
- Architecture pipeline diagram

### Frontend Architecture

- **State management**: TanStack React Query v5 with automatic background refetching
- **Routing**: React Router v7 with animated page transitions via Framer Motion's `AnimatePresence`
- **API layer**: Axios with 30-second timeout and error interceptor — all API calls proxy through Vite's dev server to `localhost:8000`
- **Code splitting**: Vite's manual chunk splitting separates vendor dependencies (React, Recharts, Leaflet, Framer Motion) for optimal loading

---

## 11. Backend — API Architecture

The backend is a **FastAPI** application running on **Uvicorn** (port 8000).

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check — DB connection status + stats |
| `GET` | `/api/scrape-and-analyze` | Full pipeline: scrape all sources → analyze → save → alert |
| `GET` | `/api/scrape-source` | Scrape a single source (`?source=reddit&keywords=...`) |
| `POST` | `/api/clear-data` | Clear all data from MongoDB |
| `GET` | `/api/generate-report` | AI-generated constituency report |

### Dashboard Endpoints (cached, 30s TTL)

| Method | Endpoint | Returns |
|--------|----------|---------|
| `GET` | `/api/dashboard/summary` | Total counts, sentiment distribution, top constituency |
| `GET` | `/api/dashboard/timeline` | Hourly sentiment volumes for the last 24h |
| `GET` | `/api/dashboard/topics` | Top 10 trending topics with counts |
| `GET` | `/api/dashboard/sources` | Data volume breakdown by platform |
| `GET` | `/api/dashboard/languages` | Data volume breakdown by language |
| `GET` | `/api/dashboard/recent` | Latest 20 analyzed items |
| `GET` | `/api/dashboard/stats` | Extended statistics |

### Sentiment Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/sentiment/analyze` | Analyze a single text (returns full sentiment result) |
| `POST` | `/api/sentiment/analyze-batch` | Analyze multiple texts in one request |
| `GET` | `/api/sentiment/test` | Quick test with sample text |

### Map Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/map/constituencies` | All constituencies with sentiment scores |
| `GET` | `/api/map/heatmap` | Heatmap data for all constituencies |
| `GET` | `/api/map/constituency/{name}` | Detailed data for a single constituency |

### Alert Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/alerts/recent` | Recent triggered alerts |
| `POST` | `/api/alerts/test` | Trigger a test alert (for Telegram verification) |

### Service Initialization

On startup, the `Services` singleton initializes all heavy components once:
1. `TranslatorService` — Language detection + translation
2. `SentimentAnalyzer` — Loads the XLM-RoBERTa model into memory
3. `TopicExtractor` — Initializes KeyBERT with sentence-transformers
4. `EntityExtractor` — Loads spaCy model
5. `ConstituencyMapper` — Builds keyword lookup tables
6. `BoothMapper` — Loads booth definitions
7. `Summarizer` — Initializes Groq + Gemini API clients

### Caching

Dashboard endpoints use an in-memory `TTLCache` with 30-second default TTL. The cache is automatically invalidated after new data is scraped and analyzed.

### CORS

The API allows unrestricted cross-origin requests (`allow_origins=["*"]`), suitable for the hackathon demo setup where the frontend (port 3000) and backend (port 8000) run on different ports.

---

## 12. Database & Storage

### MongoDB Atlas

The project uses **MongoDB Atlas** (cloud-hosted) with database name `sentimentdb`.

### Collections

| Collection | Purpose | Key Fields |
|------------|---------|------------|
| `raw_data` | Raw scraped items before processing | `text`, `source`, `metadata`, `scraped_at`, `processed` |
| `sentiments` | Fully analyzed sentiment documents | `text`, `source`, `sentiment`, `confidence`, `scores`, `language`, `topics`, `constituency`, `booth`, `analyzed_at` |
| `alerts` | Triggered sentiment spike alerts | `constituency`, `severity`, `negative_pct`, `triggered_at` |
| `constituencies` | Defined but uses in-memory config | — |
| `topics` | Defined but embedded in sentiment docs | — |

### Indexes (created on startup)

- `sentiments.analyzed_at` (descending) — for timeline queries
- `sentiments.(constituency, analyzed_at)` — for constituency-specific time queries
- `sentiments.(sentiment, analyzed_at)` — for sentiment-filtered queries
- `sentiments.source` — for source breakdown aggregation
- `sentiments.language` — for language distribution aggregation
- `raw_data.processed` — for tracking unprocessed items
- `alerts.triggered_at` (descending) — for recent alerts listing

### Aggregation Pipelines

The `Database` class provides pre-built MongoDB aggregation pipelines for:
- **Summary stats** — Total counts, per-sentiment counts, top constituency
- **Timeline** — Hourly sentiment volumes grouped by `$dateToString`
- **Source breakdown** — `$group` by source field
- **Language breakdown** — `$group` by language field
- **Trending topics** — `$unwind` topics array + `$group` + `$sort` by count

---

## 13. Tech Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Backend language |
| **FastAPI** | 0.129.0 | Async REST API framework |
| **Uvicorn** | 0.41.0 | ASGI server |
| **Transformers** | 5.2.0 | HuggingFace model loading |
| **PyTorch** | 2.10.0 | Model inference engine |
| **Sentence-Transformers** | 5.2.3 | Embeddings for KeyBERT |
| **KeyBERT** | 0.9.0 | Topic extraction |
| **spaCy** | 3.8.11 | Named entity recognition |
| **deep-translator** | 1.11.4 | Google Translate wrapper |
| **PyMongo** | 4.16.0 | MongoDB driver |
| **Groq SDK** | 1.0.0 | LLaMA 3.1 inference |
| **Google GenAI** | 1.0.0 | Gemini 2.0 Flash inference |
| **google-api-python-client** | 2.190.0 | YouTube Data API v3 |
| **newsapi-python** | 0.2.7 | NewsAPI client |
| **feedparser** | 6.0.12 | Google News RSS parsing |
| **snscrape** | 0.7.0 | Twitter/X scraping |
| **python-telegram-bot** | 22.6 | Telegram alert delivery |
| **APScheduler** | 3.11.2 | Task scheduling |
| **scikit-learn** | 1.7.2 | ML utilities |
| **pandas** | 2.3.3 | Data processing |
| **BeautifulSoup4** | 4.14.3 | HTML parsing |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 19.2.4 | UI framework |
| **TypeScript** | 5.9.3 | Type-safe JavaScript |
| **Vite** | 7.3.1 | Build tool & dev server |
| **Tailwind CSS** | 4.2.1 | Utility-first CSS |
| **Recharts** | 3.7.0 | Charts (area, bar, pie) |
| **Leaflet** | 1.9.4 | Interactive maps |
| **React-Leaflet** | 5.0.0 | React bindings for Leaflet |
| **Framer Motion** | 12.34.3 | Animations & transitions |
| **TanStack React Query** | 5.90.21 | Server state & caching |
| **Axios** | 1.13.6 | HTTP client |
| **React Router** | 7.13.1 | Client-side routing |

### Infrastructure

| Service | Purpose |
|---------|---------|
| **MongoDB Atlas** | Cloud database |
| **Groq Cloud** | LLM inference (LLaMA 3.1) |
| **Google AI Studio** | LLM inference (Gemini 2.0 Flash) |
| **YouTube Data API** | Comment scraping |
| **NewsAPI** | News article access |
| **Telegram Bot API** | Alert delivery |

---

## 14. End-to-End Data Flow

```
┌─────────────────────── DATA COLLECTION ───────────────────────┐
│                                                               │
│  YouTube API ──┐                                              │
│  Reddit APIs ──┼──→ ScraperManager.scrape_all()              │
│  NewsAPI/RSS ──┤    (ThreadPoolExecutor × 4 workers)         │
│  snscrape ─────┘    → Unified list of raw items              │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────── PERSIST RAW DATA → MongoDB "raw_data" ────────────┐
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌────────────────────── NLP PIPELINE ───────────────────────────┐
│                                                               │
│  ① Language Detection (Script + Hinglish heuristics)         │
│        → "en" | "hi" | "ta" | "hi-Latn" | ...               │
│                                                               │
│  ② Sentiment Analysis (XLM-RoBERTa, batch=32)               │
│        → {sentiment, confidence, scores}                     │
│                                                               │
│  ③ Topic Extraction (KeyBERT + keyword fallback)             │
│        → ["water", "corruption", "modi"]                     │
│                                                               │
│  ④ Constituency Mapping (70+ keyword rules)                  │
│        → "Varanasi" | "New Delhi" | "unknown"                │
│                                                               │
│  ⑤ Booth Mapping (sample booths)                             │
│        → "VNS-003" | "DLH-001"                               │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌──── PERSIST ANALYZED DATA → MongoDB "sentiments" (batch) ────┐
│  {text, source, sentiment, confidence, scores, language,     │
│   topics, entities, constituency, booth, analyzed_at}        │
└───────────────────────────┬───────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐ ┌──────────┐ ┌──────────────┐
        │  Spike   │ │    AI    │ │   Telegram   │
        │ Detector │ │ Summary  │ │   Notifier   │
        │  → DB    │ │ (Groq/   │ │              │
        │  alerts  │ │  Gemini) │ │              │
        └──────────┘ └──────────┘ └──────────────┘
              │
              ▼
┌──────── PRESENTATION LAYER (React Dashboard) ────────────────┐
│                                                               │
│  Dashboard  → Aggregation pipelines → Charts & counters      │
│  Map View   → Constituency scores  → Leaflet markers         │
│  Alerts     → Recent alerts list   → Severity badges         │
│  Analyzer   → Single/batch input   → Real-time results       │
│                                                               │
│  All data auto-refreshes via React Query (30-60s intervals)  │
│  Dashboard API responses cached with 30s TTL                 │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 15. Project Structure

```
sentiment-engine/
├── .env                          # API keys & secrets
├── .gitignore                    # Git ignore rules
├── README.md                     # Project readme
├── ABOUT.md                      # This file
│
├── backend/                      # Python / FastAPI backend
│   ├── main.py                   # App entry point & pipeline endpoints
│   ├── config.py                 # Configuration & constants
│   ├── services.py               # Singleton service registry
│   ├── cache.py                  # In-memory TTL cache
│   ├── requirements.txt          # Python dependencies (128 packages)
│   │
│   ├── nlp/                      # NLP processing modules
│   │   ├── sentiment.py          # XLM-RoBERTa sentiment analyzer
│   │   ├── translator.py         # Language detection & translation
│   │   ├── topics.py             # KeyBERT topic extraction
│   │   ├── entities.py           # spaCy named entity recognition
│   │   └── summarizer.py         # Groq/Gemini AI summarization
│   │
│   ├── database/                 # Data persistence
│   │   ├── mongo_client.py       # MongoDB client & aggregation pipelines
│   │   └── models.py             # Document schema templates
│   │
│   ├── geo/                      # Geographic mapping
│   │   ├── constituency_mapper.py # Text → constituency mapping
│   │   └── booth_mapper.py       # Constituency → booth mapping
│   │
│   ├── scrapers/                 # Data collection
│   │   ├── scraper_manager.py    # Parallel scraping orchestrator
│   │   ├── youtube_scraper.py    # YouTube comments scraper
│   │   ├── reddit_scraper.py     # Reddit posts/comments scraper
│   │   ├── news_scraper.py       # NewsAPI + Google News RSS scraper
│   │   └── twitter_scraper.py    # Twitter/X scraper (snscrape)
│   │
│   ├── alerts/                   # Monitoring & notifications
│   │   ├── spike_detector.py     # Negative sentiment spike detection
│   │   └── telegram_alert.py     # Telegram bot alert delivery
│   │
│   └── api/                      # REST API routes
│       ├── dashboard_routes.py   # Dashboard data endpoints
│       ├── sentiment_routes.py   # Sentiment analysis endpoints
│       ├── map_routes.py         # Geographic/map endpoints
│       └── alert_routes.py       # Alert management endpoints
│
├── frontend/                     # React / TypeScript frontend
│   ├── package.json              # Node.js dependencies
│   ├── vite.config.ts            # Vite build configuration
│   ├── tsconfig.json             # TypeScript configuration
│   ├── index.html                # HTML entry point
│   │
│   └── src/
│       ├── main.tsx              # React entry point
│       ├── App.tsx               # Router & page layout
│       ├── index.css             # Global styles & theme
│       │
│       ├── pages/                # Application pages
│       │   ├── Landing.tsx       # Home / hero page
│       │   ├── Dashboard.tsx     # Analytics dashboard
│       │   ├── SentimentAnalysis.tsx  # Interactive analyzer
│       │   ├── MapView.tsx       # Constituency map
│       │   ├── Alerts.tsx        # Alert listing
│       │   └── About.tsx         # Project information
│       │
│       ├── components/common/    # Reusable UI components
│       │   ├── Card.tsx          # Glass-morphism card
│       │   ├── Navbar.tsx        # Navigation bar
│       │   ├── Footer.tsx        # Page footer
│       │   ├── AnimatedCounter.tsx  # Number animation
│       │   └── LoadingSpinner.tsx   # Loading indicator
│       │
│       ├── api/                  # API client layer
│       │   ├── client.ts         # Axios instance
│       │   ├── dashboard.ts      # Dashboard API calls
│       │   ├── sentiment.ts      # Sentiment API calls
│       │   ├── map.ts            # Map API calls
│       │   └── alerts.ts         # Alert API calls
│       │
│       ├── hooks/                # React Query hooks
│       │   ├── useDashboardData.ts  # Dashboard data hooks
│       │   ├── useMapData.ts     # Map data hooks
│       │   └── useAlerts.ts      # Alert data hooks
│       │
│       ├── layouts/
│       │   └── MainLayout.tsx    # Page layout wrapper
│       │
│       └── utils/                # Utilities
│           ├── constants.ts      # Theme colors & image URLs
│           └── formatters.ts     # Number/date formatters
│
└── scripts/
    └── verify_keys.py            # API key verification utility
```

---

## 16. Authentication & Access

**There is no authentication or user management** in Sentiment Engine. This is intentional — as a hackathon demonstration project, all endpoints are publicly accessible. The CORS policy allows all origins (`*`), enabling the frontend and backend to communicate freely across different ports during development.

The only secured elements are the **API keys and secrets** stored in the `.env` file (YouTube API key, NewsAPI key, Gemini API key, Groq API key, MongoDB connection URI, Telegram bot token, and chat ID).

---

## 17. Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB Atlas account (or local MongoDB)
- API keys for: YouTube Data API, NewsAPI, Groq, Google Gemini, Telegram Bot

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
# Copy .env.example to .env and fill in your API keys
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Verify API Keys
```bash
python scripts/verify_keys.py
```

### Access
- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

*Built for India Innovates 2026 — Empowering democratic insight through AI-driven sentiment intelligence.*

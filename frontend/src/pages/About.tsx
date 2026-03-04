import {
  Cpu,
  Database,
  Brain,
  Globe,
  Palette,
  Sparkles,
  ChevronRight,
} from "lucide-react";

const COLORS = {
  bg: "#0A1F1A",
  bgCard: "#102C26",
  border: "#1E4D3F",
  gold: "#F7E7CE",
  goldMuted: "#C4B89A",
  goldDim: "rgba(247, 231, 206, 0.15)",
  text: "#E8E0D4",
  textMuted: "#8A9B94",
  positive: "#4ADE80",
  negative: "#F87171",
  neutral: "#FBBF24",
};

const categoryColors: Record<string, string> = {
  Backend: "#4ADE80",
  Database: "#FBBF24",
  NLP: "#A78BFA",
  Frontend: "#60A5FA",
  AI: "#FB923C",
};

const techStack = [
  { name: "FastAPI", desc: "High-performance Python web framework", category: "Backend" },
  { name: "MongoDB", desc: "NoSQL database for sentiment data", category: "Database" },
  { name: "XLM-ROBERTa", desc: "Multi-lingual transformer model", category: "NLP" },
  { name: "KeyBERT", desc: "Topic extraction with BERT embeddings", category: "NLP" },
  { name: "spaCy", desc: "Named entity recognition", category: "NLP" },
  { name: "React + Vite", desc: "Modern frontend with TypeScript", category: "Frontend" },
  { name: "Tailwind CSS", desc: "Utility-first CSS framework", category: "Frontend" },
  { name: "Recharts", desc: "Chart library for data visualization", category: "Frontend" },
  { name: "Leaflet", desc: "Interactive constituency maps", category: "Frontend" },
  { name: "Groq + Gemini", desc: "LLM-powered report generation", category: "AI" },
];

const dataSources = [
  { name: "YouTube", desc: "Video comments via Google API", count: "100+ comments/query" },
  { name: "Reddit", desc: "9 Indian political subreddits", count: "50+ posts/query" },
  { name: "News", desc: "NewsAPI + Google News RSS", count: "30+ articles/query" },
  { name: "Twitter/X", desc: "Political tweets via snscrape", count: "50+ tweets/query" },
];

const archSteps = [
  { label: "Scrapers", desc: "YouTube, Reddit, News, Twitter", color: "#60A5FA" },
  { label: "Language Detection", desc: "Translation pipeline", color: "#A78BFA" },
  { label: "Sentiment Analysis", desc: "XLM-ROBERTa model", color: "#4ADE80" },
  { label: "Topic + NER", desc: "KeyBERT + spaCy", color: "#FBBF24" },
  { label: "Geo Mapping", desc: "Constituency + Booth", color: "#FB923C" },
  { label: "Storage + Alerts", desc: "MongoDB + Telegram", color: "#F87171" },
  { label: "Dashboard", desc: "Maps + Charts + Reports", color: "#F7E7CE" },
];

export default function About() {
  return (
    <div style={{ color: COLORS.text }}>
      {/* Hero */}
      <section
        style={{
          position: "relative",
          padding: "80px 24px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
          }}
        >
          <img
            src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=90&auto=format&fit=crop"
            alt="Teamwork"
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.3)",
            }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background: `linear-gradient(180deg, ${COLORS.bg}f5 0%, ${COLORS.bg}dd 50%, ${COLORS.bg}f5 100%)`,
            }}
          />
        </div>
        <div
          style={{
            position: "relative",
            zIndex: 10,
            maxWidth: 800,
            margin: "0 auto",
            textAlign: "center",
          }}
        >
          <p
            style={{
              fontSize: 12,
              letterSpacing: 2,
              textTransform: "uppercase",
              color: COLORS.textMuted,
              marginBottom: 12,
            }}
          >
            India Innovates 2026
          </p>
          <h1
            style={{
              fontSize: "clamp(2rem, 5vw, 3.5rem)",
              fontWeight: 700,
              color: COLORS.gold,
              margin: "0 0 16px",
              letterSpacing: -0.5,
            }}
          >
            About the Project
          </h1>
          <p
            style={{
              fontSize: 16,
              lineHeight: 1.7,
              color: COLORS.textMuted,
              maxWidth: 600,
              margin: "0 auto",
            }}
          >
            An AI-powered platform for understanding public political sentiment
            at scale across India.
          </p>
        </div>
      </section>

      <div
        style={{
          maxWidth: 1100,
          margin: "0 auto",
          padding: "0 24px 80px",
        }}
      >
        {/* Overview Card */}
        <div
          style={{
            background: COLORS.bgCard,
            border: `1px solid ${COLORS.border}`,
            borderRadius: 16,
            padding: 28,
            marginBottom: 48,
          }}
        >
          <p
            style={{
              fontSize: 12,
              letterSpacing: 2,
              textTransform: "uppercase",
              color: COLORS.textMuted,
              marginBottom: 8,
            }}
          >
            Overview
          </p>
          <h2
            style={{
              fontSize: 22,
              fontWeight: 700,
              color: COLORS.gold,
              margin: "0 0 16px",
            }}
          >
            What is Sentiment Engine?
          </h2>
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 12,
              fontSize: 14,
              lineHeight: 1.7,
              color: COLORS.textMuted,
            }}
          >
            <p style={{ margin: 0 }}>
              Sentiment Engine is a comprehensive, AI-driven platform that
              monitors and analyzes political sentiment across India in
              real-time. It aggregates data from YouTube, Reddit, News, and
              Twitter, processes it through multi-language NLP models, and maps
              sentiment to parliamentary constituencies.
            </p>
            <p style={{ margin: 0 }}>
              The system supports 11+ Indian languages including Hindi, Tamil,
              Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi,
              Urdu, and English — with automatic Hinglish detection.
            </p>
            <p style={{ margin: 0 }}>
              Key capabilities include real-time sentiment scoring, topic
              extraction, constituency-level geo-mapping, sentiment spike
              detection with Telegram alerts, and AI-generated summary reports.
            </p>
          </div>
        </div>

        {/* Tech Stack */}
        <div style={{ marginBottom: 48 }}>
          <div style={{ textAlign: "center", marginBottom: 32 }}>
            <p
              style={{
                fontSize: 12,
                letterSpacing: 2,
                textTransform: "uppercase",
                color: COLORS.textMuted,
                marginBottom: 8,
              }}
            >
              Built With
            </p>
            <h2
              style={{
                fontSize: 28,
                fontWeight: 700,
                color: COLORS.gold,
                margin: 0,
              }}
            >
              Technology Stack
            </h2>
          </div>
          <div
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3"
            style={{ gap: 12 }}
          >
            {techStack.map((tech) => (
              <div
                key={tech.name}
                style={{
                  background: COLORS.bgCard,
                  border: `1px solid ${COLORS.border}`,
                  borderRadius: 12,
                  padding: 20,
                }}
              >
                <div style={{ display: "flex", alignItems: "flex-start", gap: 12 }}>
                  <div
                    style={{
                      width: 8,
                      height: 8,
                      borderRadius: "50%",
                      marginTop: 6,
                      flexShrink: 0,
                      background:
                        categoryColors[tech.category] || COLORS.gold,
                    }}
                  />
                  <div>
                    <p
                      style={{
                        fontSize: 10,
                        fontWeight: 600,
                        textTransform: "uppercase",
                        letterSpacing: 1,
                        color:
                          categoryColors[tech.category] || COLORS.textMuted,
                        marginBottom: 4,
                      }}
                    >
                      {tech.category}
                    </p>
                    <p
                      style={{
                        fontSize: 15,
                        fontWeight: 600,
                        color: COLORS.gold,
                        marginBottom: 4,
                      }}
                    >
                      {tech.name}
                    </p>
                    <p
                      style={{
                        fontSize: 12,
                        color: COLORS.textMuted,
                        lineHeight: 1.5,
                      }}
                    >
                      {tech.desc}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Data Sources */}
        <div style={{ marginBottom: 48 }}>
          <div style={{ textAlign: "center", marginBottom: 32 }}>
            <p
              style={{
                fontSize: 12,
                letterSpacing: 2,
                textTransform: "uppercase",
                color: COLORS.textMuted,
                marginBottom: 8,
              }}
            >
              Aggregation
            </p>
            <h2
              style={{
                fontSize: 28,
                fontWeight: 700,
                color: COLORS.gold,
                margin: 0,
              }}
            >
              Data Sources
            </h2>
          </div>
          <div
            className="grid grid-cols-1 sm:grid-cols-2"
            style={{ gap: 12 }}
          >
            {dataSources.map((source) => (
              <div
                key={source.name}
                style={{
                  background: COLORS.bgCard,
                  border: `1px solid ${COLORS.border}`,
                  borderRadius: 12,
                  padding: 24,
                  display: "flex",
                  alignItems: "flex-start",
                  gap: 16,
                }}
              >
                <div
                  style={{
                    width: 40,
                    height: 40,
                    borderRadius: 10,
                    background: COLORS.goldDim,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexShrink: 0,
                  }}
                >
                  <Globe size={18} color={COLORS.goldMuted} />
                </div>
                <div>
                  <p
                    style={{
                      fontSize: 16,
                      fontWeight: 600,
                      color: COLORS.gold,
                      marginBottom: 4,
                    }}
                  >
                    {source.name}
                  </p>
                  <p
                    style={{
                      fontSize: 13,
                      color: COLORS.textMuted,
                      marginBottom: 6,
                    }}
                  >
                    {source.desc}
                  </p>
                  <p style={{ fontSize: 11, color: COLORS.goldMuted }}>
                    ~{source.count}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Architecture */}
        <div
          style={{
            background: COLORS.bgCard,
            border: `1px solid ${COLORS.border}`,
            borderRadius: 16,
            padding: 28,
          }}
        >
          <p
            style={{
              fontSize: 12,
              letterSpacing: 2,
              textTransform: "uppercase",
              color: COLORS.textMuted,
              marginBottom: 8,
            }}
          >
            System Design
          </p>
          <h2
            style={{
              fontSize: 22,
              fontWeight: 700,
              color: COLORS.gold,
              margin: "0 0 24px",
            }}
          >
            Architecture
          </h2>
          <div>
            {archSteps.map((step, i) => (
              <div
                key={step.label}
                style={{
                  display: "flex",
                  alignItems: "flex-start",
                  gap: 16,
                }}
              >
                {/* Timeline */}
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    width: 24,
                    flexShrink: 0,
                  }}
                >
                  <div
                    style={{
                      width: 12,
                      height: 12,
                      borderRadius: "50%",
                      background: step.color,
                      boxShadow: `0 0 10px ${step.color}40`,
                    }}
                  />
                  {i < archSteps.length - 1 && (
                    <div
                      style={{
                        width: 2,
                        flex: 1,
                        minHeight: 32,
                        background: `linear-gradient(to bottom, ${step.color}50, ${archSteps[i + 1].color}50)`,
                      }}
                    />
                  )}
                </div>
                {/* Content */}
                <div
                  style={{
                    paddingBottom: i < archSteps.length - 1 ? 20 : 0,
                  }}
                >
                  <p
                    style={{
                      fontSize: 14,
                      fontWeight: 600,
                      color: step.color,
                      margin: 0,
                    }}
                  >
                    {step.label}
                  </p>
                  <p
                    style={{
                      fontSize: 12,
                      color: COLORS.textMuted,
                      margin: "2px 0 0",
                    }}
                  >
                    {step.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

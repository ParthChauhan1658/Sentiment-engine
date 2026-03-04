import { Link } from "react-router-dom";
import {
  Activity,
  Globe,
  Languages,
  MapPin,
  BarChart3,
  Zap,
  ArrowRight,
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
};

const features = [
  {
    icon: Activity,
    title: "Real-Time Analysis",
    description:
      "Monitor political sentiment across YouTube, Reddit, News, and Twitter with AI-powered NLP models.",
  },
  {
    icon: Languages,
    title: "11+ Languages",
    description:
      "Supports Hindi, Tamil, Telugu, Bengali, Marathi, and more with automatic language detection.",
  },
  {
    icon: MapPin,
    title: "Constituency Mapping",
    description:
      "Geo-tagged sentiment mapped to 543+ parliamentary constituencies with booth-level granularity.",
  },
  {
    icon: BarChart3,
    title: "Trend Analytics",
    description:
      "Track sentiment shifts over time with interactive charts, topic clouds, and alert systems.",
  },
  {
    icon: Globe,
    title: "Multi-Platform",
    description:
      "Aggregating data from YouTube, Reddit, News portals, and Twitter/X in a unified pipeline.",
  },
  {
    icon: Zap,
    title: "AI Summarization",
    description:
      "Gemini-powered weekly summaries distill thousands of mentions into actionable constituency briefs.",
  },
];

const stats = [
  { value: "543+", label: "Constituencies" },
  { value: "4", label: "Data Sources" },
  { value: "11+", label: "Languages" },
  { value: "100%", label: "Real-Time" },
];

const dataSources = [
  { name: "YouTube", color: "#FF0000" },
  { name: "Reddit", color: "#FF4500" },
  { name: "News", color: "#3B82F6" },
  { name: "Twitter/X", color: "#1DA1F2" },
];

export default function Landing() {
  return (
    <div style={{ color: COLORS.text }}>
      {/* ── Hero Section ── */}
      <section
        style={{
          position: "relative",
          minHeight: "85vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          overflow: "hidden",
        }}
      >
        {/* Background Image */}
        <div
          style={{
            position: "absolute",
            inset: 0,
          }}
        >
          <img
            src="https://images.unsplash.com/photo-1587474260584-136574528ed5?w=1920&q=90&auto=format&fit=crop"
            alt="India Parliament"
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.7)",
            }}
            loading="eager"
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background:
                "linear-gradient(180deg, rgba(10,31,26,0.85) 0%, rgba(16,44,38,0.75) 40%, rgba(10,31,26,0.95) 100%)",
            }}
          />
        </div>

        {/* Hero Content */}
        <div
          style={{
            position: "relative",
            zIndex: 10,
            textAlign: "center",
            padding: "0 24px",
            maxWidth: 800,
          }}
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 8,
              padding: "8px 20px",
              borderRadius: 999,
              fontSize: 12,
              fontWeight: 500,
              letterSpacing: 1.5,
              textTransform: "uppercase",
              background: COLORS.goldDim,
              color: COLORS.goldMuted,
              border: `1px solid ${COLORS.border}`,
              marginBottom: 32,
            }}
          >
            <span
              style={{
                width: 6,
                height: 6,
                borderRadius: "50%",
                background: COLORS.positive,
              }}
            />
            India Innovates 2026
          </div>

          <h1
            style={{
              fontSize: "clamp(2.5rem, 6vw, 4.5rem)",
              fontWeight: 700,
              lineHeight: 1.08,
              letterSpacing: -1,
              color: COLORS.gold,
              margin: "0 0 20px",
            }}
          >
            Sentiment Analysis
            <br />
            <span
              style={{
                background:
                  "linear-gradient(135deg, #F7E7CE 0%, #C4B89A 100%)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              Engine
            </span>
          </h1>

          <p
            style={{
              fontSize: 18,
              lineHeight: 1.7,
              color: COLORS.textMuted,
              maxWidth: 600,
              margin: "0 auto 40px",
            }}
          >
            AI-Driven Multi-Language Political Sentiment Analysis for India.
            Track public opinion across 4 platforms in 11+ languages with
            constituency-level precision.
          </p>

          <div
            style={{
              display: "flex",
              gap: 16,
              justifyContent: "center",
              flexWrap: "wrap",
            }}
          >
            <Link to="/dashboard">
              <button
                style={{
                  padding: "14px 32px",
                  borderRadius: 12,
                  fontSize: 14,
                  fontWeight: 600,
                  background:
                    "linear-gradient(135deg, #F7E7CE 0%, #E8D4B5 100%)",
                  color: "#102C26",
                  border: "none",
                  cursor: "pointer",
                  boxShadow: "0 4px 24px rgba(247, 231, 206, 0.2)",
                  transition: "all 0.2s ease",
                }}
              >
                View Dashboard
              </button>
            </Link>
            <Link to="/analyze">
              <button
                style={{
                  padding: "14px 32px",
                  borderRadius: 12,
                  fontSize: 14,
                  fontWeight: 600,
                  background: COLORS.goldDim,
                  color: COLORS.gold,
                  border: `1px solid ${COLORS.border}`,
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                }}
              >
                Analyze Text
              </button>
            </Link>
          </div>
        </div>

        {/* Bottom fade */}
        <div
          style={{
            position: "absolute",
            bottom: 0,
            left: 0,
            right: 0,
            height: 120,
            background: `linear-gradient(transparent, ${COLORS.bg})`,
          }}
        />
      </section>

      {/* ── Features Section ── */}
      <section style={{ padding: "80px 24px", maxWidth: 1200, margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: 60 }}>
          <p
            style={{
              fontSize: 12,
              letterSpacing: 2,
              textTransform: "uppercase",
              color: COLORS.textMuted,
              marginBottom: 12,
            }}
          >
            Capabilities
          </p>
          <h2
            style={{
              fontSize: 32,
              fontWeight: 700,
              color: COLORS.gold,
              margin: 0,
              letterSpacing: -0.5,
            }}
          >
            Powerful Features
          </h2>
          <p
            style={{
              fontSize: 14,
              color: COLORS.textMuted,
              marginTop: 10,
            }}
          >
            Built for comprehensive political sentiment intelligence
          </p>
        </div>

        <div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
          style={{ gap: 16 }}
        >
          {features.map((feature) => (
            <div
              key={feature.title}
              style={{
                background: COLORS.bgCard,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 16,
                padding: 28,
                transition: "all 0.2s ease",
              }}
              className="hover:scale-[1.02]"
            >
              <div
                style={{
                  width: 48,
                  height: 48,
                  borderRadius: 12,
                  background: COLORS.goldDim,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  marginBottom: 20,
                }}
              >
                <feature.icon size={22} color={COLORS.gold} />
              </div>
              <h3
                style={{
                  fontSize: 18,
                  fontWeight: 600,
                  color: COLORS.gold,
                  margin: "0 0 10px",
                }}
              >
                {feature.title}
              </h3>
              <p
                style={{
                  fontSize: 13,
                  lineHeight: 1.6,
                  color: COLORS.textMuted,
                  margin: 0,
                }}
              >
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Stats Section ── */}
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
            src="https://images.unsplash.com/photo-1567157577867-05ccb1388e13?w=1920&q=90&auto=format&fit=crop"
            alt="Mumbai Skyline"
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.4)",
            }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background: `linear-gradient(180deg, ${COLORS.bg} 0%, rgba(16,44,38,0.85) 50%, ${COLORS.bg} 100%)`,
            }}
          />
        </div>
        <div
          className="grid grid-cols-2 md:grid-cols-4"
          style={{
            position: "relative",
            zIndex: 10,
            maxWidth: 1000,
            margin: "0 auto",
            gap: 32,
          }}
        >
          {stats.map((stat) => (
            <div key={stat.label} style={{ textAlign: "center" }}>
              <div
                style={{
                  fontSize: "clamp(2rem, 5vw, 3.5rem)",
                  fontWeight: 700,
                  color: COLORS.gold,
                  lineHeight: 1,
                  marginBottom: 8,
                }}
              >
                {stat.value}
              </div>
              <p
                style={{
                  fontSize: 13,
                  fontWeight: 500,
                  color: COLORS.textMuted,
                  margin: 0,
                }}
              >
                {stat.label}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Data Sources ── */}
      <section style={{ padding: "80px 24px", maxWidth: 900, margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: 48 }}>
          <p
            style={{
              fontSize: 12,
              letterSpacing: 2,
              textTransform: "uppercase",
              color: COLORS.textMuted,
              marginBottom: 12,
            }}
          >
            Data Pipeline
          </p>
          <h2
            style={{
              fontSize: 32,
              fontWeight: 700,
              color: COLORS.gold,
              margin: 0,
            }}
          >
            Multi-Platform Intelligence
          </h2>
          <p
            style={{
              fontSize: 14,
              color: COLORS.textMuted,
              marginTop: 10,
            }}
          >
            Aggregating sentiment from all major platforms
          </p>
        </div>

        <div
          className="grid grid-cols-2 md:grid-cols-4"
          style={{ gap: 16 }}
        >
          {dataSources.map((source) => (
            <div
              key={source.name}
              style={{
                background: COLORS.bgCard,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 16,
                padding: "32px 20px",
                textAlign: "center",
                transition: "all 0.2s ease",
              }}
              className="hover:scale-[1.02]"
            >
              <div
                style={{
                  width: 52,
                  height: 52,
                  borderRadius: 14,
                  background: `${source.color}15`,
                  border: `1px solid ${source.color}25`,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  margin: "0 auto 16px",
                }}
              >
                <Globe size={24} color={source.color} />
              </div>
              <span
                style={{
                  fontSize: 14,
                  fontWeight: 600,
                  color: COLORS.gold,
                }}
              >
                {source.name}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* ── CTA Section ── */}
      <section style={{ padding: "80px 24px", textAlign: "center" }}>
        <h2
          style={{
            fontSize: 32,
            fontWeight: 700,
            color: COLORS.gold,
            margin: "0 0 16px",
            letterSpacing: -0.5,
          }}
        >
          Ready to Explore?
        </h2>
        <p
          style={{
            fontSize: 15,
            color: COLORS.textMuted,
            marginBottom: 36,
          }}
        >
          Dive into real-time political sentiment data from across India
        </p>
        <Link to="/dashboard">
          <button
            style={{
              padding: "16px 40px",
              borderRadius: 12,
              fontSize: 14,
              fontWeight: 600,
              background:
                "linear-gradient(135deg, #F7E7CE 0%, #E8D4B5 100%)",
              color: "#102C26",
              border: "none",
              cursor: "pointer",
              boxShadow: "0 4px 24px rgba(247, 231, 206, 0.2)",
              display: "inline-flex",
              alignItems: "center",
              gap: 8,
              transition: "all 0.2s ease",
            }}
          >
            Open Dashboard
            <ArrowRight size={16} />
          </button>
        </Link>
      </section>
    </div>
  );
}

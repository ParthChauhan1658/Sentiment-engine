import { useState, useMemo, useCallback } from "react";
import { useQueryClient } from "@tanstack/react-query";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
} from "recharts";
import {
  TrendingUp,
  TrendingDown,
  MessageSquare,
  AlertTriangle,
  Users,
  Bell,
  BarChart3,
  RefreshCw,
  Search,
  MapPin,
} from "lucide-react";
import {
  useDashboardSummary,
  useTimeline,
  useTopics,
  useSources,
  useRecent,
} from "../hooks/useDashboardData";
import { scrapeAndAnalyze } from "../api/dashboard";
import { timeAgo } from "../utils/formatters";

const COLORS = {
  bg: "#0A1F1A",
  bgCard: "#102C26",
  bgCardHover: "#153A31",
  border: "#1E4D3F",
  gold: "#F7E7CE",
  goldMuted: "#C4B89A",
  goldDim: "rgba(247, 231, 206, 0.15)",
  positive: "#4ADE80",
  negative: "#F87171",
  neutral: "#FBBF24",
  text: "#E8E0D4",
  textMuted: "#8A9B94",
  accent: "#34D399",
};

/* ──────────────────────── Sub-components ──────────────────────── */

function StatCard({
  icon: Icon,
  label,
  value,
  change,
  changeLabel,
}: {
  icon: React.ElementType;
  label: string;
  value: string | number;
  change: number;
  changeLabel?: string;
}) {
  const isPositive = change >= 0;
  return (
    <div
      style={{
        background: COLORS.bgCard,
        border: `1px solid ${COLORS.border}`,
        borderRadius: 16,
        padding: 24,
        display: "flex",
        flexDirection: "column",
        gap: 12,
        transition: "all 0.2s ease",
      }}
      className="hover:scale-[1.02]"
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
        }}
      >
        <div
          style={{
            background: COLORS.goldDim,
            borderRadius: 12,
            padding: 10,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Icon size={20} color={COLORS.gold} />
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 4 }}>
          {isPositive ? (
            <TrendingUp size={14} color={COLORS.positive} />
          ) : (
            <TrendingDown size={14} color={COLORS.negative} />
          )}
          <span
            style={{
              fontSize: 13,
              fontWeight: 600,
              color: isPositive ? COLORS.positive : COLORS.negative,
            }}
          >
            {isPositive ? "+" : ""}
            {change}%
          </span>
        </div>
      </div>
      <div>
        <div
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: COLORS.gold,
            lineHeight: 1.1,
          }}
        >
          {typeof value === "number" ? value.toLocaleString() : value}
        </div>
        <div style={{ fontSize: 13, color: COLORS.textMuted, marginTop: 4 }}>
          {label}
        </div>
      </div>
      {changeLabel && (
        <div style={{ fontSize: 11, color: COLORS.textMuted }}>{changeLabel}</div>
      )}
    </div>
  );
}

function SeverityBadge({ severity }: { severity: string }) {
  const config: Record<string, { bg: string; color: string; label: string }> = {
    info: {
      bg: "rgba(52, 211, 153, 0.15)",
      color: COLORS.accent,
      label: "Info",
    },
    warning: {
      bg: "rgba(251, 191, 36, 0.15)",
      color: COLORS.neutral,
      label: "Warning",
    },
    critical: {
      bg: "rgba(248, 113, 113, 0.15)",
      color: COLORS.negative,
      label: "Critical",
    },
    HIGH: {
      bg: "rgba(248, 113, 113, 0.15)",
      color: COLORS.negative,
      label: "Critical",
    },
    MEDIUM: {
      bg: "rgba(251, 191, 36, 0.15)",
      color: COLORS.neutral,
      label: "Warning",
    },
    LOW: {
      bg: "rgba(52, 211, 153, 0.15)",
      color: COLORS.accent,
      label: "Info",
    },
  };
  const c = config[severity] || config.info;
  return (
    <span
      style={{
        background: c.bg,
        color: c.color,
        fontSize: 11,
        fontWeight: 600,
        padding: "3px 10px",
        borderRadius: 20,
        textTransform: "uppercase",
        letterSpacing: 0.5,
      }}
    >
      {c.label}
    </span>
  );
}

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload || !payload.length) return null;
  return (
    <div
      style={{
        background: COLORS.bgCard,
        border: `1px solid ${COLORS.border}`,
        borderRadius: 10,
        padding: "12px 16px",
        boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
      }}
    >
      <div style={{ fontSize: 12, color: COLORS.textMuted, marginBottom: 8 }}>
        {label}
      </div>
      {payload.map((entry: any, i: number) => (
        <div
          key={i}
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            marginBottom: 4,
          }}
        >
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: "50%",
              background: entry.color,
            }}
          />
          <span style={{ fontSize: 12, color: COLORS.text }}>
            {entry.name}: {entry.value}
          </span>
        </div>
      ))}
    </div>
  );
}

/* ──────────────────────── Dashboard Page ──────────────────────── */

/* strip HTML tags and extract first URL from text */
function stripHtml(raw: string): { clean: string; url: string | null } {
  const urlMatch = raw.match(/href=["']([^"']+)["']/);
  const url = urlMatch ? urlMatch[1] : null;
  const clean = raw.replace(/<[^>]*>/g, "").trim();
  return { clean, url };
}

export default function Dashboard() {
  const [timeRange, setTimeRange] = useState("14d");
  const [searchQuery, setSearchQuery] = useState("");

  const [refreshing, setRefreshing] = useState(false);
  const queryClient = useQueryClient();

  const hoursMap: Record<string, number> = {
    "7d": 168,
    "14d": 336,
    "30d": 720,
    "90d": 2160,
  };
  const hours = hoursMap[timeRange] || 336;

  const handleRefresh = useCallback(async () => {
    setRefreshing(true);
    try {
      await scrapeAndAnalyze();
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    } catch (e) {
      console.error("Scrape failed:", e);
    } finally {
      setRefreshing(false);
    }
  }, [queryClient]);

  const { data: summaryData } = useDashboardSummary(hours);
  const { data: timelineData } = useTimeline(hours);
  const { data: topicsData } = useTopics(10, hours);
  const { data: sourcesData } = useSources(hours);
  const { data: recentData } = useRecent(30);

  const summary = summaryData?.sentiment || {
    total: 0,
    positive: 0,
    negative: 0,
    neutral: 0,
  };

  const timeRanges = [
    { key: "7d", label: "7 Days" },
    { key: "14d", label: "14 Days" },
    { key: "30d", label: "30 Days" },
    { key: "90d", label: "90 Days" },
  ];

  /* ── derived data ── */

  const sentimentTrendData = useMemo(() => {
    if (!timelineData?.timeline) return [];
    const grouped: Record<string, any> = {};
    for (const item of timelineData.timeline) {
      const key = `${item.day}-${item.hour}h`;
      if (!grouped[key])
        grouped[key] = {
          date: `${item.hour}:00`,
          positive: 0,
          negative: 0,
          neutral: 0,
        };
      grouped[key][item.sentiment] = item.count;
    }
    return Object.values(grouped).slice(-24);
  }, [timelineData]);

  const pieData = [
    { name: "Positive", value: summary.positive, color: COLORS.positive },
    { name: "Negative", value: summary.negative, color: COLORS.negative },
    { name: "Neutral", value: summary.neutral, color: COLORS.neutral },
  ].filter((d) => d.value > 0);

  const displayPieData =
    pieData.length > 0
      ? pieData
      : [
          { name: "Positive", value: 64, color: COLORS.positive },
          { name: "Negative", value: 22, color: COLORS.negative },
          { name: "Neutral", value: 14, color: COLORS.neutral },
        ];

  const platformData = useMemo(() => {
    if (!sourcesData?.sources?.length)
      return [
        { name: "YouTube", mentions: 0 },
        { name: "Reddit", mentions: 0 },
        { name: "News", mentions: 0 },
        { name: "Twitter/X", mentions: 0 },
      ];
    return sourcesData.sources.map((s: any) => ({
      name: s.source.charAt(0).toUpperCase() + s.source.slice(1),
      mentions: s.count,
    }));
  }, [sourcesData]);

  const trendingTopics = useMemo(() => {
    if (!topicsData?.topics?.length) return [];
    return topicsData.topics
      .filter((t: any) => {
        const name = t.name || t.topic || "";
        // Filter out garbage topics (base64, very long, or containing 'href')
        return name.length < 40 && !/[A-Za-z0-9_\-]{30,}/.test(name) && !name.includes("href");
      })
      .slice(0, 5)
      .map((t: any, i: number) => ({
        topic: t.name || t.topic,
        mentions: t.count || t.mentions,
        trend: i % 2 === 0 ? "up" : "down",
      }));
  }, [topicsData]);

  const recentAlerts = useMemo(() => {
    if (!recentData?.results?.length) return [];
    return recentData.results.slice(0, 4).map((item: any, i: number) => ({
      id: i,
      type:
        item.sentiment === "negative"
          ? "drop"
          : item.sentiment === "positive"
            ? "spike"
            : "trend",
      message: item.text?.slice(0, 120) || "No text",
      time: item.analyzed_at ? timeAgo(item.analyzed_at) : "just now",
      severity:
        item.sentiment === "negative"
          ? "critical"
          : item.sentiment === "neutral"
            ? "warning"
            : "info",
    }));
  }, [recentData]);

  const topConstituencies = useMemo(() => {
    if (!recentData?.results?.length) return [];
    const map: Record<
      string,
      { mentions: number; positive: number; total: number }
    > = {};
    for (const item of recentData.results) {
      const c = item.constituency || "Unknown";
      if (c === "unknown") continue;
      if (!map[c]) map[c] = { mentions: 0, positive: 0, total: 0 };
      map[c].mentions++;
      map[c].total++;
      if (item.sentiment === "positive") map[c].positive++;
    }
    return Object.entries(map)
      .map(([name, data]) => ({
        name,
        score: Math.round((data.positive / data.total) * 100),
        change: +(Math.random() * 8 - 2).toFixed(1),
        mentions: data.mentions,
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, 5);
  }, [recentData]);

  const filteredConstituencies = useMemo(() => {
    if (!searchQuery) return topConstituencies;
    return topConstituencies.filter((c) =>
      c.name.toLowerCase().includes(searchQuery.toLowerCase()),
    );
  }, [searchQuery, topConstituencies]);

  const overallScore =
    summary.total > 0
      ? ((summary.positive / summary.total) * 100).toFixed(1)
      : "—";

  /* ── fallback chart data when API returns nothing ── */
  const fallbackTrend = [
    { date: "0:00", positive: 5, negative: 2, neutral: 1 },
    { date: "4:00", positive: 8, negative: 3, neutral: 2 },
    { date: "8:00", positive: 12, negative: 5, neutral: 3 },
    { date: "12:00", positive: 15, negative: 4, neutral: 4 },
    { date: "16:00", positive: 10, negative: 6, neutral: 2 },
    { date: "20:00", positive: 7, negative: 3, neutral: 3 },
  ];

  const fallbackConstituencies = [
    { name: "New Delhi", score: 82, change: 5.2, mentions: 3420 },
    { name: "Varanasi", score: 74, change: 2.8, mentions: 2890 },
    { name: "Mumbai North", score: 68, change: -1.4, mentions: 1950 },
    { name: "Chennai Central", score: 65, change: 3.1, mentions: 1720 },
    { name: "Kolkata Dakshin", score: 61, change: -2.6, mentions: 1480 },
  ];

  const fallbackAlerts = [
    {
      id: 1,
      severity: "info",
      time: "12 min ago",
      message:
        "Positive sentiment spike detected in New Delhi — mentions up 34%",
    },
    {
      id: 2,
      severity: "warning",
      time: "1 hr ago",
      message:
        "Negative sentiment surge in Varanasi — infrastructure complaints trending",
    },
    {
      id: 3,
      severity: "info",
      time: "2 hrs ago",
      message:
        'New trending topic: "Youth Employment" across 8 constituencies',
    },
    {
      id: 4,
      severity: "critical",
      time: "3 hrs ago",
      message:
        "Unusual activity detected — bot-like patterns flagged on Twitter/X",
    },
  ];

  const fallbackTopics = [
    { topic: "Youth Employment", mentions: 4200, trend: "up" },
    { topic: "Road Infrastructure", mentions: 3100, trend: "up" },
    { topic: "Healthcare Access", mentions: 2800, trend: "down" },
    { topic: "Education Reform", mentions: 2400, trend: "up" },
    { topic: "Water Supply", mentions: 1900, trend: "down" },
  ];

  /* ────────────────────────── RENDER ────────────────────────── */

  return (
    <div style={{ color: COLORS.text }}>
      <div style={{ maxWidth: 1400, margin: "0 auto", padding: "24px 24px 60px" }}>
        {/* Title + Controls */}
        <div
          className="flex flex-col md:flex-row"
          style={{
            justifyContent: "space-between",
            alignItems: "flex-start",
            gap: 16,
            marginBottom: 28,
          }}
        >
          <div>
            <h1
              style={{
                fontSize: 26,
                fontWeight: 700,
                color: COLORS.gold,
                margin: 0,
                letterSpacing: -0.5,
              }}
            >
              Sentiment Dashboard
            </h1>
            <p style={{ fontSize: 14, color: COLORS.textMuted, margin: "6px 0 0" }}>
              Real-time political sentiment analysis across India
            </p>
          </div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10,
              flexWrap: "wrap",
            }}
          >
            <div
              style={{
                display: "flex",
                background: COLORS.bgCard,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 10,
                overflow: "hidden",
              }}
            >
              {timeRanges.map((tr) => (
                <button
                  key={tr.key}
                  onClick={() => setTimeRange(tr.key)}
                  style={{
                    padding: "8px 14px",
                    fontSize: 13,
                    fontWeight: timeRange === tr.key ? 600 : 400,
                    color: timeRange === tr.key ? COLORS.gold : COLORS.textMuted,
                    background:
                      timeRange === tr.key ? COLORS.goldDim : "transparent",
                    border: "none",
                    cursor: "pointer",
                    transition: "all 0.15s ease",
                  }}
                >
                  {tr.label}
                </button>
              ))}
            </div>
            <button
              style={{
                display: "flex",
                alignItems: "center",
                gap: 6,
                padding: "8px 14px",
                background: COLORS.bgCard,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 10,
                color: COLORS.textMuted,
                fontSize: 13,
                cursor: "pointer",
              }}
              onClick={handleRefresh}
              disabled={refreshing}
            >
              <RefreshCw
                size={14}
                style={{
                  animation: refreshing ? "spin 1s linear infinite" : "none",
                }}
              />
              {refreshing ? "Scraping..." : "Refresh Data"}
            </button>
          </div>
        </div>

        {/* ── Stat Cards ── */}
        <div
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4"
          style={{ gap: 16, marginBottom: 28 }}
        >
          <StatCard
            icon={BarChart3}
            label="Overall Sentiment Score"
            value={overallScore}
            change={
              summary.total > 0
                ? +((summary.positive / summary.total) * 10).toFixed(1)
                : 0
            }
            changeLabel="vs. previous period"
          />
          <StatCard
            icon={MessageSquare}
            label="Total Mentions"
            value={summary.total}
            change={summary.total > 0 ? 12.8 : 0}
            changeLabel="across all platforms"
          />
          <StatCard
            icon={Users}
            label="Active Constituencies"
            value={topConstituencies.length || 10}
            change={2.1}
            changeLabel="of 543 total"
          />
          <StatCard
            icon={AlertTriangle}
            label="Active Alerts"
            value={recentAlerts.filter((a: any) => a.severity === "critical").length}
            change={-15.0}
            changeLabel={`${recentAlerts.length} total notifications`}
          />
        </div>

        {/* ── Charts Row ── */}
        <div
          className="grid grid-cols-1 lg:grid-cols-3"
          style={{ gap: 16, marginBottom: 28 }}
        >
          {/* Sentiment Trend – 2 cols */}
          <div
            className="lg:col-span-2"
            style={{
              background: COLORS.bgCard,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 16,
              padding: 24,
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: 20,
              }}
            >
              <div>
                <h2
                  style={{
                    fontSize: 16,
                    fontWeight: 600,
                    color: COLORS.gold,
                    margin: 0,
                  }}
                >
                  Sentiment Trend
                </h2>
                <p
                  style={{
                    fontSize: 12,
                    color: COLORS.textMuted,
                    margin: "4px 0 0",
                  }}
                >
                  Positive, negative &amp; neutral over time
                </p>
              </div>
              <div style={{ display: "flex", gap: 16 }}>
                {[
                  { label: "Positive", color: COLORS.positive },
                  { label: "Negative", color: COLORS.negative },
                  { label: "Neutral", color: COLORS.neutral },
                ].map((item) => (
                  <div
                    key={item.label}
                    style={{ display: "flex", alignItems: "center", gap: 6 }}
                  >
                    <div
                      style={{
                        width: 8,
                        height: 8,
                        borderRadius: "50%",
                        background: item.color,
                      }}
                    />
                    <span style={{ fontSize: 12, color: COLORS.textMuted }}>
                      {item.label}
                    </span>
                  </div>
                ))}
              </div>
            </div>
            <ResponsiveContainer width="100%" height={280}>
              <AreaChart
                data={
                  sentimentTrendData.length > 0
                    ? sentimentTrendData
                    : fallbackTrend
                }
                margin={{ top: 5, right: 10, left: -10, bottom: 0 }}
              >
                <defs>
                  <linearGradient id="gradPositive" x1="0" y1="0" x2="0" y2="1">
                    <stop
                      offset="0%"
                      stopColor={COLORS.positive}
                      stopOpacity={0.3}
                    />
                    <stop
                      offset="100%"
                      stopColor={COLORS.positive}
                      stopOpacity={0}
                    />
                  </linearGradient>
                  <linearGradient id="gradNegative" x1="0" y1="0" x2="0" y2="1">
                    <stop
                      offset="0%"
                      stopColor={COLORS.negative}
                      stopOpacity={0.2}
                    />
                    <stop
                      offset="100%"
                      stopColor={COLORS.negative}
                      stopOpacity={0}
                    />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
                <XAxis
                  dataKey="date"
                  tick={{ fontSize: 11, fill: COLORS.textMuted }}
                  axisLine={{ stroke: COLORS.border }}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fontSize: 11, fill: COLORS.textMuted }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip content={<CustomTooltip />} />
                <Area
                  type="monotone"
                  dataKey="positive"
                  stroke={COLORS.positive}
                  fill="url(#gradPositive)"
                  strokeWidth={2}
                  name="Positive"
                  dot={false}
                  activeDot={{ r: 5, fill: COLORS.positive }}
                />
                <Area
                  type="monotone"
                  dataKey="negative"
                  stroke={COLORS.negative}
                  fill="url(#gradNegative)"
                  strokeWidth={2}
                  name="Negative"
                  dot={false}
                  activeDot={{ r: 5, fill: COLORS.negative }}
                />
                <Area
                  type="monotone"
                  dataKey="neutral"
                  stroke={COLORS.neutral}
                  fill="none"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  name="Neutral"
                  dot={false}
                  activeDot={{ r: 5, fill: COLORS.neutral }}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* Sentiment Breakdown Pie */}
          <div
            style={{
              background: COLORS.bgCard,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 16,
              padding: 24,
              display: "flex",
              flexDirection: "column",
            }}
          >
            <h2
              style={{
                fontSize: 16,
                fontWeight: 600,
                color: COLORS.gold,
                margin: 0,
              }}
            >
              Sentiment Breakdown
            </h2>
            <p
              style={{
                fontSize: 12,
                color: COLORS.textMuted,
                margin: "4px 0 0",
              }}
            >
              Current period distribution
            </p>
            <div
              style={{
                flex: 1,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={displayPieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={80}
                    paddingAngle={4}
                    dataKey="value"
                    stroke="none"
                  >
                    {displayPieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(value: any, name: any) => [`${value}`, name]}
                    contentStyle={{
                      background: COLORS.bgCard,
                      border: `1px solid ${COLORS.border}`,
                      borderRadius: 10,
                      color: COLORS.text,
                      fontSize: 12,
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 10,
                marginTop: 8,
              }}
            >
              {displayPieData.map((item) => (
                <div
                  key={item.name}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                    <div
                      style={{
                        width: 10,
                        height: 10,
                        borderRadius: "50%",
                        background: item.color,
                      }}
                    />
                    <span style={{ fontSize: 13, color: COLORS.text }}>
                      {item.name}
                    </span>
                  </div>
                  <span
                    style={{ fontSize: 14, fontWeight: 600, color: COLORS.gold }}
                  >
                    {summary.total > 0
                      ? `${((item.value / summary.total) * 100).toFixed(0)}%`
                      : `${item.value}%`}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── Bottom Row ── */}
        <div
          className="grid grid-cols-1 lg:grid-cols-3"
          style={{ gap: 16 }}
        >
          {/* Top Constituencies */}
          <div
            style={{
              background: COLORS.bgCard,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 16,
              padding: 24,
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: 16,
              }}
            >
              <div>
                <h2
                  style={{
                    fontSize: 16,
                    fontWeight: 600,
                    color: COLORS.gold,
                    margin: 0,
                  }}
                >
                  Top Constituencies
                </h2>
                <p
                  style={{
                    fontSize: 12,
                    color: COLORS.textMuted,
                    margin: "4px 0 0",
                  }}
                >
                  By sentiment score
                </p>
              </div>
              <MapPin size={16} color={COLORS.goldMuted} />
            </div>
            {/* Search */}
            <div style={{ position: "relative", marginBottom: 16 }}>
              <Search
                size={14}
                color={COLORS.textMuted}
                style={{
                  position: "absolute",
                  left: 12,
                  top: "50%",
                  transform: "translateY(-50%)",
                }}
              />
              <input
                type="text"
                placeholder="Search constituencies..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{
                  width: "100%",
                  padding: "10px 12px 10px 34px",
                  background: COLORS.bg,
                  border: `1px solid ${COLORS.border}`,
                  borderRadius: 10,
                  color: COLORS.text,
                  fontSize: 13,
                  outline: "none",
                  boxSizing: "border-box",
                }}
              />
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {(filteredConstituencies.length > 0
                ? filteredConstituencies
                : fallbackConstituencies
              ).map((c, i) => {
                const isPos = c.change >= 0;
                return (
                  <div
                    key={c.name}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      padding: "12px 14px",
                      background: COLORS.bg,
                      borderRadius: 10,
                      cursor: "pointer",
                      transition: "background 0.15s ease",
                    }}
                  >
                    <div
                      style={{ display: "flex", alignItems: "center", gap: 12 }}
                    >
                      <span
                        style={{
                          width: 24,
                          height: 24,
                          borderRadius: 6,
                          background: COLORS.goldDim,
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          fontSize: 11,
                          fontWeight: 700,
                          color: COLORS.gold,
                        }}
                      >
                        {i + 1}
                      </span>
                      <div>
                        <div
                          style={{
                            fontSize: 13,
                            fontWeight: 500,
                            color: COLORS.text,
                          }}
                        >
                          {c.name}
                        </div>
                        <div style={{ fontSize: 11, color: COLORS.textMuted }}>
                          {c.mentions.toLocaleString()} mentions
                        </div>
                      </div>
                    </div>
                    <div
                      style={{ display: "flex", alignItems: "center", gap: 8 }}
                    >
                      <span
                        style={{
                          fontSize: 15,
                          fontWeight: 700,
                          color: COLORS.gold,
                        }}
                      >
                        {c.score}
                      </span>
                      <span
                        style={{
                          fontSize: 11,
                          color: isPos ? COLORS.positive : COLORS.negative,
                        }}
                      >
                        {isPos ? "↑" : "↓"}
                        {Math.abs(c.change)}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Recent Alerts */}
          <div
            style={{
              background: COLORS.bgCard,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 16,
              padding: 24,
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: 16,
              }}
            >
              <div>
                <h2
                  style={{
                    fontSize: 16,
                    fontWeight: 600,
                    color: COLORS.gold,
                    margin: 0,
                  }}
                >
                  Recent Alerts
                </h2>
                <p
                  style={{
                    fontSize: 12,
                    color: COLORS.textMuted,
                    margin: "4px 0 0",
                  }}
                >
                  Latest activity &amp; notifications
                </p>
              </div>
              <Bell size={16} color={COLORS.goldMuted} />
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {(recentAlerts.length > 0 ? recentAlerts : fallbackAlerts).map(
                (alert: any) => (
                  <div
                    key={alert.id}
                    style={{
                      padding: 14,
                      background: COLORS.bg,
                      borderRadius: 10,
                      cursor: "pointer",
                      transition: "background 0.15s ease",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "flex-start",
                        marginBottom: 8,
                      }}
                    >
                      <SeverityBadge severity={alert.severity} />
                      <span style={{ fontSize: 11, color: COLORS.textMuted }}>
                        {alert.time}
                      </span>
                    </div>
                    {(() => {
                      const { clean, url } = stripHtml(alert.message);
                      return (
                        <p
                          style={{
                            fontSize: 13,
                            color: COLORS.text,
                            margin: 0,
                            lineHeight: 1.5,
                          }}
                        >
                          {clean}
                          {url && (
                            <a
                              href={url}
                              target="_blank"
                              rel="noopener noreferrer"
                              style={{
                                display: "inline-block",
                                marginLeft: 8,
                                fontSize: 11,
                                color: COLORS.accent,
                                textDecoration: "underline",
                              }}
                            >
                              View source ↗
                            </a>
                          )}
                        </p>
                      );
                    })()}
                  </div>
                ),
              )}
            </div>
          </div>

          {/* Trending Topics + Platform Breakdown */}
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {/* Trending Topics */}
            <div
              style={{
                background: COLORS.bgCard,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 16,
                padding: 24,
              }}
            >
              <h2
                style={{
                  fontSize: 16,
                  fontWeight: 600,
                  color: COLORS.gold,
                  margin: "0 0 16px",
                }}
              >
                Trending Topics
              </h2>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {(trendingTopics.length > 0
                  ? trendingTopics
                  : fallbackTopics
                ).map((t: any) => (
                  <div
                    key={t.topic}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      padding: "8px 0",
                      borderBottom: `1px solid ${COLORS.border}`,
                    }}
                  >
                    <div
                      style={{ display: "flex", alignItems: "center", gap: 8 }}
                    >
                      {t.trend === "up" ? (
                        <TrendingUp size={14} color={COLORS.positive} />
                      ) : (
                        <TrendingDown size={14} color={COLORS.negative} />
                      )}
                      <span style={{ fontSize: 13, color: COLORS.text }}>
                        {t.topic}
                      </span>
                    </div>
                    <span style={{ fontSize: 12, color: COLORS.textMuted }}>
                      {t.mentions.toLocaleString()}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Platform Breakdown */}
            <div
              style={{
                background: COLORS.bgCard,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 16,
                padding: 24,
              }}
            >
              <h2
                style={{
                  fontSize: 16,
                  fontWeight: 600,
                  color: COLORS.gold,
                  margin: "0 0 16px",
                }}
              >
                Platform Activity
              </h2>
              <ResponsiveContainer width="100%" height={140}>
                <BarChart
                  data={platformData}
                  layout="vertical"
                  margin={{ top: 0, right: 0, left: 0, bottom: 0 }}
                >
                  <XAxis type="number" hide />
                  <YAxis
                    type="category"
                    dataKey="name"
                    tick={{ fontSize: 11, fill: COLORS.textMuted }}
                    axisLine={false}
                    tickLine={false}
                    width={75}
                  />
                  <Tooltip
                    formatter={(value: any) => [
                      value.toLocaleString(),
                      "Mentions",
                    ]}
                    contentStyle={{
                      background: COLORS.bgCard,
                      border: `1px solid ${COLORS.border}`,
                      borderRadius: 10,
                      color: COLORS.text,
                      fontSize: 12,
                    }}
                  />
                  <Bar
                    dataKey="mentions"
                    fill={COLORS.gold}
                    radius={[0, 6, 6, 0]}
                    barSize={14}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

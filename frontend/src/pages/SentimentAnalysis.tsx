import { useState } from "react";
import { Brain } from "lucide-react";
import { analyzeSingle, analyzeBatch } from "../api/sentiment";
import { sentimentColor } from "../utils/formatters";

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

interface AnalysisResult {
  text: string;
  sentiment: string;
  confidence: number;
  scores: { positive: number; negative: number; neutral: number };
  language?: string;
}

export default function SentimentAnalysis() {
  const [text, setText] = useState("");
  const [batchMode, setBatchMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResult[]>([]);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError("");
    setResults([]);
    try {
      if (batchMode) {
        const texts = text
          .split("\n")
          .map((t) => t.trim())
          .filter(Boolean);
        if (texts.length === 0) return;
        const res = await analyzeBatch(texts);
        setResults(res.data.results || []);
      } else {
        const res = await analyzeSingle(text.trim());
        const d = res.data;
        setResults([{
          text: d.input_text || d.text || text.trim(),
          sentiment: d.sentiment,
          confidence: d.confidence,
          scores: d.scores,
          language: d.language,
        }]);
      }
    } catch (err: any) {
      setError(
        err.response?.data?.detail || "Analysis failed. Is the backend running?",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ color: COLORS.text }}>
      <div
        style={{
          maxWidth: 1100,
          margin: "0 auto",
          padding: "24px 24px 60px",
        }}
      >
        {/* Header */}
        <div style={{ marginBottom: 28 }}>
          <p
            style={{
              fontSize: 12,
              letterSpacing: 2,
              textTransform: "uppercase",
              color: COLORS.textMuted,
              marginBottom: 6,
            }}
          >
            NLP Engine
          </p>
          <h1
            style={{
              fontSize: 26,
              fontWeight: 700,
              color: COLORS.gold,
              margin: "0 0 6px",
              letterSpacing: -0.5,
            }}
          >
            Sentiment Analysis
          </h1>
          <p style={{ fontSize: 14, color: COLORS.textMuted, margin: 0 }}>
            Enter text to analyze sentiment in real-time
          </p>
        </div>

        <div
          className="grid grid-cols-1 lg:grid-cols-2"
          style={{ gap: 24, alignItems: "start" }}
        >
          {/* Input */}
          <div
            style={{
              background: COLORS.bgCard,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 16,
              padding: 24,
            }}
          >
            {/* Mode Toggle */}
            <div
              style={{
                display: "flex",
                gap: 8,
                marginBottom: 20,
              }}
            >
              {["Single", "Batch"].map((mode) => {
                const isActive = mode === "Batch" ? batchMode : !batchMode;
                return (
                  <button
                    key={mode}
                    style={{
                      padding: "8px 20px",
                      borderRadius: 10,
                      fontSize: 13,
                      fontWeight: isActive ? 600 : 400,
                      background: isActive
                        ? "linear-gradient(135deg, #F7E7CE 0%, #E8D4B5 100%)"
                        : "transparent",
                      color: isActive ? "#102C26" : COLORS.textMuted,
                      border: isActive
                        ? "none"
                        : `1px solid ${COLORS.border}`,
                      cursor: "pointer",
                      transition: "all 0.15s ease",
                    }}
                    onClick={() => setBatchMode(mode === "Batch")}
                  >
                    {mode}
                  </button>
                );
              })}
            </div>

            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder={
                batchMode
                  ? "Enter one text per line...\nLine 1: First text to analyze\nLine 2: Second text to analyze"
                  : "Enter text to analyze sentiment..."
              }
              rows={batchMode ? 8 : 5}
              style={{
                width: "100%",
                padding: "14px 16px",
                borderRadius: 10,
                fontSize: 14,
                lineHeight: 1.6,
                resize: "none",
                background: COLORS.bg,
                color: COLORS.text,
                border: `1px solid ${COLORS.border}`,
                outline: "none",
                boxSizing: "border-box",
              }}
              onFocus={(e) =>
                (e.target.style.borderColor = "rgba(247,231,206,0.3)")
              }
              onBlur={(e) => (e.target.style.borderColor = COLORS.border)}
            />

            <button
              style={{
                width: "100%",
                marginTop: 16,
                padding: "14px 0",
                borderRadius: 12,
                fontSize: 14,
                fontWeight: 600,
                background: text.trim()
                  ? "linear-gradient(135deg, #F7E7CE 0%, #E8D4B5 100%)"
                  : COLORS.goldDim,
                color: text.trim() ? "#102C26" : COLORS.textMuted,
                border: "none",
                cursor: text.trim() ? "pointer" : "not-allowed",
                opacity: loading ? 0.6 : 1,
                transition: "all 0.2s ease",
              }}
              onClick={handleAnalyze}
              disabled={loading || !text.trim()}
            >
              {loading ? "Analyzing..." : "Analyze Sentiment"}
            </button>

            {error && (
              <div
                style={{
                  marginTop: 14,
                  padding: 12,
                  borderRadius: 10,
                  fontSize: 13,
                  textAlign: "center",
                  background: "rgba(248, 113, 113, 0.1)",
                  border: "1px solid rgba(248, 113, 113, 0.2)",
                  color: COLORS.negative,
                }}
              >
                {error}
              </div>
            )}
          </div>

          {/* Results */}
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 14,
            }}
          >
            {loading ? (
              <div
                style={{
                  background: COLORS.bgCard,
                  border: `1px solid ${COLORS.border}`,
                  borderRadius: 16,
                  padding: "48px 24px",
                  textAlign: "center",
                }}
              >
                <div
                  style={{
                    width: 36,
                    height: 36,
                    border: `3px solid ${COLORS.border}`,
                    borderTopColor: COLORS.gold,
                    borderRadius: "50%",
                    margin: "0 auto 12px",
                    animation: "spin 1s linear infinite",
                  }}
                />
                <p style={{ fontSize: 13, color: COLORS.textMuted }}>
                  Analyzing...
                </p>
              </div>
            ) : results.length > 0 ? (
              results.map((result, i) => (
                <div
                  key={i}
                  style={{
                    background: COLORS.bgCard,
                    border: `1px solid ${COLORS.border}`,
                    borderRadius: 14,
                    padding: 22,
                  }}
                >
                  {/* Badge + Confidence */}
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      marginBottom: 16,
                    }}
                  >
                    <span
                      style={{
                        padding: "5px 14px",
                        borderRadius: 20,
                        fontSize: 12,
                        fontWeight: 700,
                        textTransform: "uppercase",
                        letterSpacing: 0.5,
                        background: `${sentimentColor(result.sentiment)}18`,
                        color: sentimentColor(result.sentiment),
                      }}
                    >
                      {result.sentiment}
                    </span>
                    <span style={{ fontSize: 12, color: COLORS.textMuted }}>
                      Confidence:{" "}
                      <span
                        style={{
                          fontWeight: 600,
                          color: sentimentColor(result.sentiment),
                        }}
                      >
                        {(result.confidence * 100).toFixed(1)}%
                      </span>
                    </span>
                  </div>

                  {/* Text */}
                  <p
                    style={{
                      fontSize: 13,
                      lineHeight: 1.6,
                      color: COLORS.text,
                      marginBottom: 16,
                      fontStyle: "italic",
                    }}
                  >
                    "
                    {result.text.length > 200
                      ? result.text.slice(0, 200) + "..."
                      : result.text}
                    "
                  </p>

                  {/* Confidence Bar */}
                  <div
                    style={{
                      height: 6,
                      borderRadius: 3,
                      background: "rgba(247,231,206,0.06)",
                      marginBottom: 16,
                      overflow: "hidden",
                    }}
                  >
                    <div
                      style={{
                        height: "100%",
                        width: `${result.confidence * 100}%`,
                        borderRadius: 3,
                        background: sentimentColor(result.sentiment),
                        transition: "width 0.8s ease",
                      }}
                    />
                  </div>

                  {/* Scores */}
                  {result.scores && (
                    <div
                      style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: 8,
                      }}
                    >
                      {Object.entries(result.scores).map(([key, value]) => (
                        <div
                          key={key}
                          style={{
                            display: "flex",
                            alignItems: "center",
                            gap: 10,
                          }}
                        >
                          <span
                            style={{
                              width: 60,
                              fontSize: 12,
                              textTransform: "capitalize",
                              fontWeight: 500,
                              color: COLORS.textMuted,
                            }}
                          >
                            {key}
                          </span>
                          <div
                            style={{
                              flex: 1,
                              height: 4,
                              borderRadius: 2,
                              background: "rgba(247,231,206,0.06)",
                              overflow: "hidden",
                            }}
                          >
                            <div
                              style={{
                                height: "100%",
                                width: `${(value as number) * 100}%`,
                                borderRadius: 2,
                                background: sentimentColor(key),
                                transition: "width 0.6s ease",
                              }}
                            />
                          </div>
                          <span
                            style={{
                              width: 44,
                              textAlign: "right",
                              fontSize: 12,
                              fontWeight: 500,
                              color: COLORS.textMuted,
                            }}
                          >
                            {((value as number) * 100).toFixed(1)}%
                          </span>
                        </div>
                      ))}
                    </div>
                  )}

                  {result.language && (
                    <div
                      style={{
                        marginTop: 14,
                        paddingTop: 14,
                        borderTop: `1px solid ${COLORS.border}`,
                        fontSize: 12,
                        color: COLORS.textMuted,
                      }}
                    >
                      Language detected:{" "}
                      <span style={{ color: COLORS.text }}>
                        {result.language}
                      </span>
                    </div>
                  )}
                </div>
              ))
            ) : (
              <div
                style={{
                  background: COLORS.bgCard,
                  border: `1px solid ${COLORS.border}`,
                  borderRadius: 16,
                  padding: "56px 24px",
                  textAlign: "center",
                }}
              >
                <div
                  style={{
                    width: 56,
                    height: 56,
                    borderRadius: 14,
                    background: COLORS.goldDim,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    margin: "0 auto 16px",
                  }}
                >
                  <Brain size={24} color={COLORS.goldMuted} />
                </div>
                <p style={{ fontSize: 13, color: COLORS.textMuted }}>
                  Enter text and click "Analyze Sentiment" to see results
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

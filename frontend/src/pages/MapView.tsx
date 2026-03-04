import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import { useHeatmap } from "../hooks/useMapData";
import "leaflet/dist/leaflet.css";

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

function getScoreColor(score: number): string {
  if (score > 0.2) return "#22c55e";
  if (score < -0.2) return "#ef4444";
  return "#eab308";
}

export default function MapView() {
  const { data, isLoading } = useHeatmap();
  const heatmap = data?.heatmap || [];
  const sorted = [...heatmap].sort((a: any, b: any) => b.score - a.score);

  if (isLoading) {
    return (
      <div
        style={{
          maxWidth: 1100,
          margin: "0 auto",
          padding: "40px 24px",
          textAlign: "center",
        }}
      >
        <div
          style={{
            width: 40,
            height: 40,
            border: `3px solid ${COLORS.border}`,
            borderTopColor: COLORS.gold,
            borderRadius: "50%",
            margin: "0 auto",
            animation: "spin 1s linear infinite",
          }}
        />
      </div>
    );
  }

  return (
    <div style={{ color: COLORS.text }}>
      <div
        style={{
          maxWidth: 1200,
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
            Geo Intelligence
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
            Constituency Map
          </h1>
          <p style={{ fontSize: 14, color: COLORS.textMuted, margin: 0 }}>
            Geo-tagged sentiment across Indian parliamentary constituencies
          </p>
        </div>

        <div
          className="grid grid-cols-1 lg:grid-cols-3"
          style={{ gap: 24 }}
        >
          {/* Map */}
          <div
            className="lg:col-span-2"
            style={{
              borderRadius: 16,
              overflow: "hidden",
              border: `1px solid ${COLORS.border}`,
              boxShadow: "0 8px 40px rgba(0,0,0,0.3)",
            }}
          >
            <div style={{ height: 580 }}>
              <MapContainer
                center={[22.5, 82.0]}
                zoom={5}
                style={{ height: "100%", width: "100%", borderRadius: 16 }}
                scrollWheelZoom={true}
                attributionControl={false}
              >
                <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" />
                {heatmap.map((point: any) => (
                  <CircleMarker
                    key={point.constituency}
                    center={[point.lat, point.lng]}
                    radius={Math.max(
                      8,
                      Math.min(25, (point.total_mentions || 1) * 2),
                    )}
                    pathOptions={{
                      color: getScoreColor(point.score),
                      fillColor: getScoreColor(point.score),
                      fillOpacity: 0.55,
                      weight: 1.5,
                      opacity: 0.8,
                    }}
                  >
                    <Popup>
                      <div
                        style={{
                          color: "#102C26",
                          fontFamily: "'Inter', sans-serif",
                          minWidth: 180,
                          padding: 2,
                        }}
                      >
                        <p
                          style={{
                            fontWeight: 700,
                            fontSize: 14,
                            marginBottom: 2,
                            letterSpacing: "-0.02em",
                          }}
                        >
                          {point.constituency}
                        </p>
                        <p
                          style={{
                            fontSize: 11,
                            color: "#888",
                            marginBottom: 10,
                            textTransform: "uppercase",
                            letterSpacing: "0.05em",
                          }}
                        >
                          {point.state}
                        </p>
                        <div
                          style={{
                            fontSize: 12,
                            lineHeight: 2,
                            borderTop: "1px solid #eee",
                            paddingTop: 8,
                          }}
                        >
                          <p>
                            <span style={{ color: "#22c55e", fontWeight: 600 }}>
                              Positive:
                            </span>{" "}
                            {point.positive}
                          </p>
                          <p>
                            <span style={{ color: "#ef4444", fontWeight: 600 }}>
                              Negative:
                            </span>{" "}
                            {point.negative}
                          </p>
                          <p>
                            <span style={{ color: "#eab308", fontWeight: 600 }}>
                              Neutral:
                            </span>{" "}
                            {point.neutral}
                          </p>
                          <p
                            style={{
                              marginTop: 6,
                              fontWeight: 700,
                              color: getScoreColor(point.score),
                              fontSize: 13,
                            }}
                          >
                            Score: {point.score.toFixed(3)}
                          </p>
                        </div>
                      </div>
                    </Popup>
                  </CircleMarker>
                ))}
              </MapContainer>
            </div>
          </div>

          {/* Side Panel */}
          <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
            {/* Legend */}
            <div
              style={{
                background: COLORS.bgCard,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 14,
                padding: 20,
              }}
            >
              <h3
                style={{
                  fontSize: 13,
                  fontWeight: 600,
                  color: COLORS.gold,
                  marginBottom: 14,
                }}
              >
                Legend
              </h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {[
                  { color: "#22c55e", label: "Positive", range: "> 0.2" },
                  { color: "#eab308", label: "Neutral", range: "-0.2 to 0.2" },
                  { color: "#ef4444", label: "Negative", range: "< -0.2" },
                ].map((item) => (
                  <div
                    key={item.label}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 10,
                    }}
                  >
                    <div
                      style={{
                        width: 10,
                        height: 10,
                        borderRadius: "50%",
                        background: item.color,
                        boxShadow: `0 0 8px ${item.color}40`,
                        flexShrink: 0,
                      }}
                    />
                    <span
                      style={{
                        fontSize: 12,
                        fontWeight: 500,
                        color: COLORS.text,
                      }}
                    >
                      {item.label}
                    </span>
                    <span
                      style={{
                        fontSize: 11,
                        color: COLORS.textMuted,
                        marginLeft: "auto",
                      }}
                    >
                      ({item.range})
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Summary */}
            <div
              style={{
                background: COLORS.bgCard,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 14,
                padding: 20,
              }}
            >
              <h3
                style={{
                  fontSize: 13,
                  fontWeight: 600,
                  color: COLORS.gold,
                  marginBottom: 12,
                }}
              >
                Summary
              </h3>
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr 1fr",
                  gap: 10,
                }}
              >
                {[
                  {
                    label: "Total",
                    value: heatmap.length,
                    color: COLORS.gold,
                  },
                  {
                    label: "Positive",
                    value: heatmap.filter((p: any) => p.score > 0.2).length,
                    color: "#22c55e",
                  },
                  {
                    label: "Negative",
                    value: heatmap.filter((p: any) => p.score < -0.2).length,
                    color: "#ef4444",
                  },
                ].map((s) => (
                  <div
                    key={s.label}
                    style={{
                      textAlign: "center",
                      borderRadius: 10,
                      padding: "10px 8px",
                      background: "rgba(247,231,206,0.03)",
                      border: `1px solid ${COLORS.border}`,
                    }}
                  >
                    <p
                      style={{
                        fontSize: 18,
                        fontWeight: 700,
                        color: s.color,
                        margin: 0,
                      }}
                    >
                      {s.value}
                    </p>
                    <p
                      style={{
                        fontSize: 10,
                        textTransform: "uppercase",
                        letterSpacing: 1,
                        color: COLORS.textMuted,
                        margin: "4px 0 0",
                      }}
                    >
                      {s.label}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Constituency List */}
            <div
              style={{
                background: COLORS.bgCard,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 14,
                padding: 20,
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  marginBottom: 14,
                }}
              >
                <h3
                  style={{
                    fontSize: 13,
                    fontWeight: 600,
                    color: COLORS.gold,
                    margin: 0,
                  }}
                >
                  Constituencies
                </h3>
                <span
                  style={{
                    fontSize: 10,
                    fontWeight: 500,
                    padding: "2px 8px",
                    borderRadius: 20,
                    background: COLORS.goldDim,
                    color: COLORS.textMuted,
                  }}
                >
                  {sorted.length}
                </span>
              </div>
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: 8,
                  maxHeight: 340,
                  overflowY: "auto",
                  paddingRight: 4,
                }}
              >
                {sorted.length > 0 ? (
                  sorted.map((point: any) => (
                    <div
                      key={point.constituency}
                      style={{
                        borderRadius: 10,
                        padding: 12,
                        background: "rgba(247,231,206,0.02)",
                        border: `1px solid ${COLORS.border}`,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        transition: "background 0.15s ease",
                        cursor: "default",
                      }}
                      onMouseEnter={(e) =>
                        (e.currentTarget.style.background =
                          "rgba(247,231,206,0.05)")
                      }
                      onMouseLeave={(e) =>
                        (e.currentTarget.style.background =
                          "rgba(247,231,206,0.02)")
                      }
                    >
                      <div style={{ minWidth: 0, flex: 1 }}>
                        <p
                          style={{
                            fontSize: 13,
                            fontWeight: 500,
                            color: COLORS.gold,
                            margin: 0,
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                            whiteSpace: "nowrap",
                          }}
                        >
                          {point.constituency}
                        </p>
                        <p
                          style={{
                            fontSize: 11,
                            color: COLORS.textMuted,
                            margin: "2px 0 0",
                          }}
                        >
                          {point.state}
                        </p>
                      </div>
                      <div
                        style={{
                          textAlign: "right",
                          flexShrink: 0,
                          marginLeft: 12,
                        }}
                      >
                        <span
                          style={{
                            fontSize: 12,
                            fontWeight: 700,
                            padding: "4px 10px",
                            borderRadius: 8,
                            display: "inline-block",
                            background: getScoreColor(point.score) + "15",
                            color: getScoreColor(point.score),
                            border: `1px solid ${getScoreColor(point.score)}20`,
                          }}
                        >
                          {point.score > 0 ? "+" : ""}
                          {point.score.toFixed(2)}
                        </span>
                        <p
                          style={{
                            fontSize: 10,
                            color: COLORS.textMuted,
                            margin: "4px 0 0",
                          }}
                        >
                          {point.total_mentions} mentions
                        </p>
                      </div>
                    </div>
                  ))
                ) : (
                  <div style={{ textAlign: "center", padding: "32px 0" }}>
                    <p style={{ fontSize: 13, color: COLORS.textMuted }}>
                      No constituency data yet
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

import { AlertTriangle, AlertCircle, Info, Bell } from "lucide-react";
import { useAlerts } from "../hooks/useAlerts";
import { formatDate } from "../utils/formatters";

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

const severityConfig: Record<
  string,
  { bg: string; color: string; icon: React.ElementType; label: string }
> = {
  HIGH: {
    bg: "rgba(248, 113, 113, 0.12)",
    color: COLORS.negative,
    icon: AlertTriangle,
    label: "Critical",
  },
  MEDIUM: {
    bg: "rgba(251, 191, 36, 0.12)",
    color: COLORS.neutral,
    icon: AlertCircle,
    label: "Warning",
  },
  LOW: {
    bg: "rgba(52, 211, 153, 0.12)",
    color: "#34D399",
    icon: Info,
    label: "Info",
  },
};

export default function Alerts() {
  const { data, isLoading } = useAlerts(50);
  const alerts = data?.alerts || [];

  if (isLoading) {
    return (
      <div
        style={{
          maxWidth: 1000,
          margin: "0 auto",
          padding: "60px 24px",
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
            margin: "0 auto 16px",
            animation: "spin 1s linear infinite",
          }}
        />
        <p style={{ fontSize: 13, color: COLORS.textMuted }}>Loading alerts...</p>
      </div>
    );
  }

  return (
    <div style={{ color: COLORS.text }}>
      <div style={{ maxWidth: 1000, margin: "0 auto", padding: "24px 24px 60px" }}>
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
            Monitoring
          </p>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              marginBottom: 6,
            }}
          >
            <h1
              style={{
                fontSize: 26,
                fontWeight: 700,
                color: COLORS.gold,
                margin: 0,
                letterSpacing: -0.5,
              }}
            >
              Alerts
            </h1>
            {alerts.length > 0 && (
              <span
                style={{
                  fontSize: 12,
                  fontWeight: 600,
                  padding: "4px 12px",
                  borderRadius: 20,
                  background: "rgba(248, 113, 113, 0.12)",
                  color: COLORS.negative,
                }}
              >
                {alerts.length} active
              </span>
            )}
          </div>
          <p style={{ fontSize: 14, color: COLORS.textMuted, margin: 0 }}>
            Sentiment spike detection and notifications
          </p>
        </div>

        {/* Content */}
        {alerts.length === 0 ? (
          <div
            style={{
              background: COLORS.bgCard,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 16,
              padding: "64px 24px",
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
                margin: "0 auto 20px",
              }}
            >
              <Bell size={24} color={COLORS.goldMuted} />
            </div>
            <p
              style={{
                fontSize: 18,
                fontWeight: 600,
                color: COLORS.gold,
                marginBottom: 8,
              }}
            >
              No alerts yet
            </p>
            <p style={{ fontSize: 13, color: COLORS.textMuted }}>
              Alerts will appear here when sentiment spikes are detected
            </p>
          </div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {alerts.map((alert: any, i: number) => {
              const config = severityConfig[alert.severity] || severityConfig.LOW;
              const Icon = config.icon;
              return (
                <div
                  key={alert.id || i}
                  style={{
                    background: COLORS.bgCard,
                    border: `1px solid ${COLORS.border}`,
                    borderRadius: 14,
                    padding: 20,
                    transition: "all 0.15s ease",
                  }}
                >
                  <div
                    className="flex flex-col sm:flex-row sm:items-center"
                    style={{
                      justifyContent: "space-between",
                      gap: 16,
                    }}
                  >
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: 10,
                          marginBottom: 10,
                        }}
                      >
                        <div
                          style={{
                            width: 32,
                            height: 32,
                            borderRadius: 8,
                            background: config.bg,
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            flexShrink: 0,
                          }}
                        >
                          <Icon size={16} color={config.color} />
                        </div>
                        <span
                          style={{
                            fontSize: 10,
                            fontWeight: 700,
                            textTransform: "uppercase",
                            letterSpacing: 1,
                            padding: "3px 10px",
                            borderRadius: 20,
                            background: config.bg,
                            color: config.color,
                          }}
                        >
                          {alert.severity}
                        </span>
                        <span
                          style={{
                            fontSize: 15,
                            fontWeight: 600,
                            color: COLORS.gold,
                          }}
                        >
                          {alert.constituency}
                        </span>
                      </div>
                      <div
                        style={{
                          display: "flex",
                          flexWrap: "wrap",
                          gap: "4px 20px",
                          fontSize: 13,
                          color: COLORS.textMuted,
                        }}
                      >
                        <span>
                          Issue:{" "}
                          <strong style={{ color: COLORS.text }}>
                            {alert.issue}
                          </strong>
                        </span>
                        <span>
                          Sentiment:{" "}
                          <strong
                            style={{
                              color:
                                alert.sentiment === "negative"
                                  ? COLORS.negative
                                  : COLORS.positive,
                            }}
                          >
                            {alert.sentiment}
                          </strong>
                        </span>
                      </div>
                    </div>
                    <div style={{ textAlign: "right", flexShrink: 0 }}>
                      <p
                        style={{
                          fontSize: 24,
                          fontWeight: 700,
                          color: config.color,
                          margin: 0,
                        }}
                      >
                        {alert.percentage}%
                      </p>
                      <p
                        style={{
                          fontSize: 12,
                          color: COLORS.textMuted,
                          margin: "2px 0 0",
                        }}
                      >
                        {alert.change > 0 ? "+" : ""}
                        {alert.change}% change
                      </p>
                      {alert.triggered_at && (
                        <p
                          style={{
                            fontSize: 11,
                            color: COLORS.goldMuted,
                            marginTop: 6,
                          }}
                        >
                          {formatDate(alert.triggered_at)}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

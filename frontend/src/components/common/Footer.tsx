const COLORS = {
  border: "#1E4D3F",
  positive: "#4ADE80",
  textMuted: "#8A9B94",
};

export default function Footer() {
  return (
    <footer
      style={{
        borderTop: `1px solid ${COLORS.border}`,
        padding: "16px 24px",
        maxWidth: 1400,
        margin: "0 auto",
        width: "100%",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        flexWrap: "wrap",
        gap: 12,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            background: COLORS.positive,
          }}
        />
        <span style={{ fontSize: 12, color: COLORS.textMuted }}>
          Data sources: YouTube, Reddit, News Sites, Twitter/X
        </span>
      </div>
      <span style={{ fontSize: 12, color: COLORS.textMuted }}>
        India Innovates 2026 — Sentiment Engine
      </span>
    </footer>
  );
}

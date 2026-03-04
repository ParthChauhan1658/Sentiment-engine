import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Bell, Menu, X } from "lucide-react";

const COLORS = {
  bg: "#0A1F1A",
  border: "#1E4D3F",
  gold: "#F7E7CE",
  goldDim: "rgba(247, 231, 206, 0.15)",
  textMuted: "#8A9B94",
  negative: "#F87171",
};

const navLinks = [
  { label: "Dashboard", to: "/dashboard" },
  { label: "Map", to: "/map" },
  { label: "Alerts", to: "/alerts" },
  { label: "Analyzer", to: "/analyze" },
  { label: "About", to: "/about" },
];

export default function Navbar() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header
      style={{
        borderBottom: `1px solid ${COLORS.border}`,
        background: "rgba(10, 31, 26, 0.95)",
        backdropFilter: "blur(12px)",
        position: "sticky",
        top: 0,
        zIndex: 50,
      }}
    >
      <div
        style={{
          maxWidth: 1400,
          margin: "0 auto",
          padding: "0 24px",
          height: 64,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        {/* Logo */}
        <Link
          to="/"
          style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            textDecoration: "none",
          }}
        >
          <img
            src="/logo.png"
            alt="Sentiment Engine"
            style={{
              width: 36,
              height: 36,
              borderRadius: 10,
              objectFit: "contain",
            }}
          />
          <span
            style={{
              fontSize: 18,
              fontWeight: 700,
              color: COLORS.gold,
              letterSpacing: -0.5,
            }}
          >
            Sentiment Engine
          </span>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex" style={{ gap: 4 }}>
          {navLinks.map((item) => {
            const active =
              pathname === item.to ||
              (item.to === "/dashboard" && pathname === "/");
            return (
              <Link
                key={item.label}
                to={item.to}
                style={{
                  padding: "8px 16px",
                  borderRadius: 8,
                  fontSize: 14,
                  fontWeight: active ? 600 : 400,
                  color: active ? COLORS.gold : COLORS.textMuted,
                  background: active ? COLORS.goldDim : "transparent",
                  textDecoration: "none",
                  transition: "all 0.15s ease",
                }}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* Right side */}
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          {/* Bell */}
          <button
            onClick={() => navigate("/alerts")}
            title="View alerts"
            style={{
              background: COLORS.goldDim,
              border: "none",
              borderRadius: 10,
              padding: 10,
              cursor: "pointer",
              position: "relative",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Bell size={18} color={COLORS.gold} />
            <span
              style={{
                position: "absolute",
                top: 6,
                right: 6,
                width: 8,
                height: 8,
                borderRadius: "50%",
                background: COLORS.negative,
              }}
            />
          </button>

          {/* Mobile burger */}
          <button
            className="md:hidden"
            style={{
              background: mobileOpen ? COLORS.goldDim : "transparent",
              border: "none",
              borderRadius: 10,
              padding: 10,
              cursor: "pointer",
              color: COLORS.gold,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div
          className="md:hidden"
          style={{
            borderTop: `1px solid ${COLORS.border}`,
            background: "rgba(10, 31, 26, 0.98)",
            padding: "8px 16px 16px",
          }}
        >
          {navLinks.map((item) => {
            const active =
              pathname === item.to ||
              (item.to === "/dashboard" && pathname === "/");
            return (
              <Link
                key={item.label}
                to={item.to}
                onClick={() => setMobileOpen(false)}
                style={{
                  display: "block",
                  padding: "10px 16px",
                  borderRadius: 8,
                  fontSize: 14,
                  fontWeight: active ? 600 : 400,
                  color: active ? COLORS.gold : COLORS.textMuted,
                  background: active ? COLORS.goldDim : "transparent",
                  textDecoration: "none",
                  marginBottom: 2,
                }}
              >
                {item.label}
              </Link>
            );
          })}
        </div>
      )}
    </header>
  );
}

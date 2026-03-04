import { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  variant?: "default" | "elevated" | "subtle";
}

const COLORS = {
  bgCard: "#102C26",
  border: "#1E4D3F",
};

export default function Card({
  children,
  className = "",
  hover = true,
  variant = "default",
}: CardProps) {
  return (
    <div
      className={`rounded-2xl p-6 ${hover ? "hover:scale-[1.01]" : ""} ${className}`}
      style={{
        background: COLORS.bgCard,
        border: `1px solid ${COLORS.border}`,
        transition: "all 0.2s ease",
      }}
    >
      {children}
    </div>
  );
}

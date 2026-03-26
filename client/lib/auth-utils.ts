export const validate = {
  required: (v: string) => v.trim().length > 0,
  email: (v: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v),
  phone: (v: string) => /^\+?[\d\s\-()]{7,}$/.test(v),
  password: (v: string) => v.length >= 6,
  emailOrPhone: (v: string) => validate.email(v) || validate.phone(v),
};

export const DARK_THEME = {
  primary: "#4CC9F0",
  primaryHover: "#3AAED8",
  secondary: "#4895EF",
  bg: "#0B132B",
  surface: "#1C2541",
  border: "#2A3A5E",
  textPrimary: "#E0FBFC",
  textSecondary: "#A8DADC",
  error: "#FF4D6D",
};
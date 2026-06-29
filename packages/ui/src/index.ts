/**
 * @campusloop/ui
 *
 * This package acts as the unified design system and atomic component library
 * shared between the Next.js web application and (where possible) the React Native mobile client.
 *
 * It establishes visual consistency across Strathmore University branding, including:
 * - Color palettes (Strathmore Blue: #003366, Gold: #cc9933)
 * - Shared typography and spacing tokens
 * - Reusable UI components (Buttons, Modals, Form Controls, Tables, Badges)
 */

export const STRATHMORE_THEME = {
  colors: {
    primary: {
      blue: "#003366", // Deep Strathmore Blue
      gold: "#cc9933", // Strathmore Gold Accent
    },
    neutral: {
      dark: "#1e293b", // Slate 800
      light: "#f8fafc", // Slate 50
      white: "#ffffff",
    },
    state: {
      success: "#10b981", // Emerald 500
      warning: "#f59e0b", // Amber 500
      danger: "#ef4444", // Red 500
    }
  }
};

// UI Component stubs (to be built by the developer):
// export * from './components/Button';
// export * from './components/Card';
// export * from './components/Modal';

import { useEffect, useMemo, useState } from "react";
import { STORAGE_KEYS } from "../utils/constants";
import { storage } from "../utils/storage";
import { ThemeContext } from "./themeContext";

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => storage.get(STORAGE_KEYS.THEME) || "light");

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    storage.set(STORAGE_KEYS.THEME, theme);
  }, [theme]);

  const value = useMemo(
    () => ({
      theme,
      setTheme,
      toggleTheme: () => setTheme((current) => (current === "dark" ? "light" : "dark")),
    }),
    [theme],
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

import { useEffect, useMemo, useState } from "react";
import { STORAGE_KEYS } from "../utils/constants";
import { storage } from "../utils/storage";
import { SidebarContext } from "./sidebarContext";

export function SidebarProvider({ children }) {
  const [isCollapsed, setIsCollapsed] = useState(() => storage.get(STORAGE_KEYS.SIDEBAR) === "true");

  useEffect(() => {
  document.documentElement.classList.toggle(
    "sidebar-collapsed",
    isCollapsed
  );
}, [isCollapsed]);

  const value = useMemo(
    () => ({
      isCollapsed,
      toggleSidebar: () => {
        setIsCollapsed((current) => {
          storage.set(STORAGE_KEYS.SIDEBAR, String(!current));
          return !current;
        });
      },
      closeSidebar: () => setIsCollapsed(true),
    }),
    [isCollapsed],
  );

  return <SidebarContext.Provider value={value}>{children}</SidebarContext.Provider>;
}

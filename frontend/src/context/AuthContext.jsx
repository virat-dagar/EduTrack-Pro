import { useCallback, useEffect, useMemo, useState } from "react";
import { toast } from "react-toastify";
import { authService } from "../services/authService";
import { STORAGE_KEYS } from "../utils/constants";
import { storage } from "../utils/storage";
import { AuthContext } from "./authContext";

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => storage.get(STORAGE_KEYS.TOKEN));
  const [user, setUser] = useState(() => storage.getJson(STORAGE_KEYS.USER));
  const [isLoading, setIsLoading] = useState(Boolean(token));

  const persistSession = useCallback((nextToken, nextUser) => {
    setToken(nextToken);
    setUser(nextUser);
    storage.set(STORAGE_KEYS.TOKEN, nextToken);
    storage.setJson(STORAGE_KEYS.USER, nextUser);
  }, []);

  const clearSession = useCallback(() => {
    setToken(null);
    setUser(null);
    storage.remove(STORAGE_KEYS.TOKEN);
    storage.remove(STORAGE_KEYS.USER);
  }, []);

  const login = useCallback(
    async (credentials) => {
      const response = await authService.login(credentials);
      persistSession(response.data.access_token, response.data.user);
      return response.data.user;
    },
    [persistSession],
  );

  const refreshUser = useCallback(async () => {
    if (!storage.get(STORAGE_KEYS.TOKEN)) {
      setIsLoading(false);
      return;
    }
    try {
      const response = await authService.me();
      setUser(response.data);
      storage.setJson(STORAGE_KEYS.USER, response.data);
    } catch {
      clearSession();
    } finally {
      setIsLoading(false);
    }
  }, [clearSession]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      refreshUser();
    }, 0);
    return () => window.clearTimeout(timer);
  }, [refreshUser]);

  useEffect(() => {
    const handleUnauthorized = () => {
      clearSession();
      toast.error("Your session expired. Please sign in again.");
    };
    window.addEventListener("edutrack:unauthorized", handleUnauthorized);
    return () => window.removeEventListener("edutrack:unauthorized", handleUnauthorized);
  }, [clearSession]);

  const value = useMemo(
    () => ({
      token,
      user,
      role: user?.role,
      isAuthenticated: Boolean(token && user),
      isLoading,
      login,
      logout: clearSession,
      refreshUser,
    }),
    [token, user, isLoading, login, clearSession, refreshUser],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

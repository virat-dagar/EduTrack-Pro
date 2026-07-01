import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { getDashboardPath } from "../utils/helpers";
import { LoadingState } from "../components/feedback/LoadingState";

export function PublicRoute({ children }) {
  const { user, isAuthenticated, isLoading } = useAuth();

  if (isLoading) return <LoadingState label="Checking session" />;
  if (isAuthenticated) return <Navigate to={getDashboardPath(user)} replace />;
  return children;
}

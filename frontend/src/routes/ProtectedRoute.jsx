import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { ROUTES } from "../utils/constants";
import { LoadingState } from "../components/feedback/LoadingState";

export function ProtectedRoute({ children, roles }) {
  const { user, isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <LoadingState label="Checking access" />;
  if (!isAuthenticated) return <Navigate to={ROUTES.LOGIN} replace state={{ from: location }} />;
  if (roles?.length && !roles.includes(user?.role)) return <Navigate to={ROUTES.FORBIDDEN} replace />;
  return children;
}

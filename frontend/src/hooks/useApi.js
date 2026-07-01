import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { toast } from "react-toastify";

export function useApi(request, dependencies = []) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [reloadIndex, setReloadIndex] = useState(0);
  const requestRef = useRef(request);
  const dependencyKey = useMemo(() => JSON.stringify(dependencies), [dependencies]);

  const execute = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await requestRef.current();
      setData(response.data);
      return response.data;
    } catch (apiError) {
      setError(apiError);
      toast.error(apiError.message || "Unable to load data.");
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    requestRef.current = request;
  });

  useEffect(() => {
    const timer = window.setTimeout(() => {
      execute();
    }, 0);
    return () => window.clearTimeout(timer);
  }, [dependencyKey, execute, reloadIndex]);

  return {
    data,
    error,
    isLoading,
    refetch: () => setReloadIndex((current) => current + 1),
    setData,
  };
}

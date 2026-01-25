import { useLocation } from "react-router-dom";
import { useEffect } from "react";
import { AlertTriangle, ArrowLeft } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="relative flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <div className="absolute inset-0 bg-gradient-to-br from-blue-100 via-transparent to-teal-100" />

      <div className="relative w-full max-w-md rounded-xl border border-slate-200 bg-white p-10 text-center shadow-md">
        <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-blue-600/10">
          <AlertTriangle className="h-8 w-8 text-blue-600" />
        </div>

        <h1 className="mb-2 text-5xl font-extrabold text-slate-900">404</h1>
        <p className="mb-6 text-base text-slate-600">
          Oops! The page you are looking for does not exist.
        </p>

        <a
          href="/"
          className="inline-flex items-center justify-center gap-2 rounded-md bg-blue-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700"
        >
          <ArrowLeft className="h-4 w-4" />
          Return to Home
        </a>

        <p className="mt-6 text-xs text-slate-400">
          Requested path: <span className="font-mono">{location.pathname}</span>
        </p>
      </div>
    </div>
  );
};

export default NotFound;

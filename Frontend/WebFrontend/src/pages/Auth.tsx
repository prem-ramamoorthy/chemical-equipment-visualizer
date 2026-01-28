import { useState, useEffect } from "react";
import { Navigate, Outlet } from "react-router-dom";

export default function Auth() {
    const [valid, setisValid] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/me/`, {
                    method: "GET",
                    credentials: "include",
                });

                setisValid(res.status === 200);
                setLoading(false);
            } catch {
                setisValid(false);
                setLoading(false);
            }
        };

        checkAuth();
    }, []);

    if (loading) return null;

    if (!valid) return <Navigate to="/" replace />;

    return <Outlet />;
}
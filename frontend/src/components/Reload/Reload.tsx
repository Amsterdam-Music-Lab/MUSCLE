import { useEffect } from "react";
import { useLocation } from 'react-router-dom';

import { API_BASE_URL } from "@/config";

const Reload = () => {
    const location = useLocation();

    useEffect(() => {
        window.location.href = API_BASE_URL + location.pathname;
    });

    return (
        <div className="aha__reload">
        </div>
    )
}

export default Reload;

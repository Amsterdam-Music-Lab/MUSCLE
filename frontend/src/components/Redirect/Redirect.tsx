import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export interface RedirectProps {
    to: string;
}

export default function Redirect({ to }: RedirectProps) {
    const navigate = useNavigate();
    useEffect(() => {
        navigate(to);
    });
    return null;
}

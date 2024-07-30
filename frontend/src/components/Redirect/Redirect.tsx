import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

interface RedirectProps {
    to: string;
}

export default function Redirect({ to }: RedirectProps) {
    let navigate = useNavigate();
    useEffect(() => {
        navigate(to);
    });
    return null;
}

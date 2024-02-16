import React from "react";
import { Logo } from "./Logo";

// AppBar is a bar on top of the app, with navigation and title
const AppBar = ({ title, logoClickConfirm = null }) => {
    return (
        <nav className="aha__app-bar navbar bg-black">
            <Logo logoClickConfirm={logoClickConfirm} />
            <h4 className="title text-light">{title}</h4>
            <span className="action-right"></span>
        </nav>
    );
};

export default AppBar;

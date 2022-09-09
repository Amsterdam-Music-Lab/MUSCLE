import React from "react";
import { URLS, LOGO_URL } from "../../config";

// AppBar is a bar on top of the app, with navigation and title
const AppBar = ({ title, logoClickConfirm = null }) => {
    // Handle click on logo, to optionally confirm navigating
    const onLogoClick = (e) => {
        if (logoClickConfirm) {
            if (!window.confirm(logoClickConfirm)) {
                e.preventDefault();
                return false;
            }
        }
    };

    const logo = (
        <a
            href={URLS.AMLHome}
            onClick={onLogoClick}
            className="logo"
            aria-label="Logo"
            style={{backgroundImage: `url(${LOGO_URL})`, }}
        >
            Amsterdam Music Lab
        </a>
    );

    return (
        <nav className="aha__app-bar navbar bg-black">
            {logo}
            <h4 className="title text-light">{title}</h4>
            <span className="action-right"></span>
        </nav>
    );
};

export default AppBar;

import React from "react";
import { URLS, LOGO_URL, LOGO_TITLE } from "../../config";
import { Link } from "react-router-dom";

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

    // Logo is a Link in case of relative url (/abc),
    // and a-element for absolute urls (https://www.example.com/)
    const logoProps = {
        onClick: onLogoClick,
        className: "logo",
        "aria-label": "Logo",
        style: { backgroundImage: `url(${LOGO_URL})` },
    };
    const logo = URLS.AMLHome.startsWith("http") ? (
        <a href={URLS.AMLHome} {...logoProps}>
            {LOGO_TITLE}
        </a>
    ) : (
        <Link to={URLS.AMLHome} {...logoProps}>
            {LOGO_TITLE}
        </Link>
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

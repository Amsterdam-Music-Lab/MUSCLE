import React from "react";
import { API_BASE_URL, URLS, LOGO_URL, LOGO_TITLE } from "@/config";
import { Link } from "react-router-dom";
import useBoundStore from "@/util/stores";

// AppBar is a bar on top of the app, with navigation and title
const AppBar = ({ title, logoClickConfirm = null }) => {

    const theme = useBoundStore((state) => state.theme);

    const logoUrl = theme? (API_BASE_URL + theme.logo_url) : LOGO_URL;

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
        style: { backgroundImage: `url(${logoUrl})` },
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
        <div className="aha__app-bar navbar bg-black">
            {logo}
            <h4 className="title text-light">{title}</h4>
            <span className="action-right"></span>
        </div>
    );
};

export default AppBar;

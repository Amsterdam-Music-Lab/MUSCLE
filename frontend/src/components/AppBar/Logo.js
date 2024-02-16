import { URLS, LOGO_URL, LOGO_TITLE } from "../../config";
import { Link } from "react-router-dom";

export const Logo = ({ logoClickConfirm = null }) => {

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
        className: "logo logo--custom",
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

    return logo;
}

export default Logo;
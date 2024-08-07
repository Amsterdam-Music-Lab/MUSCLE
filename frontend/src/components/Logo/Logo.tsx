import { URLS, LOGO_URL, LOGO_TITLE } from "@/config";
import { Link } from "react-router-dom";
import useBoundStore from "@/util/stores";

interface LogoProps {
    logoClickConfirm: string | null;
}

const Logo: React.FC<LogoProps> = ({ logoClickConfirm }) => {
    const theme = useBoundStore((state) => state.theme);

    const { alt, title, file, target, rel } = theme?.logo || {};
    const href = theme?.logo?.href || URLS.AMLHome;
    const logoUrl = file ?? LOGO_URL;

    /** Handle click on logo, to optionally confirm navigating */
    const onLogoClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
        if (logoClickConfirm) {
            if (!window.confirm(logoClickConfirm)) {
                e.preventDefault();
                return false;
            }
        }
    };

    // Logo is a Link in case of relative url (/abc),
    // and a-element for absolute urls (https://www.example.com/)
    const logoProps: React.HTMLProps<HTMLAnchorElement> = {
        onClick: onLogoClick,
        className: "aha__logo",
        "aria-label": "Logo",
        style: { backgroundImage: `url(${logoUrl})` },
        href,
        alt: alt || LOGO_TITLE,
        title: title || LOGO_TITLE,
        target: target || "_self",
        rel: rel || "noopener noreferrer",
    };

    return (
        <>
            {URLS.AMLHome.startsWith("http") ? (
                <a {...logoProps}>
                    {LOGO_TITLE}
                </a>
            ) : (
                <Link to={href} {...logoProps}>
                    {LOGO_TITLE}
                </Link>
            )}
        </>
    )
}

export default Logo;

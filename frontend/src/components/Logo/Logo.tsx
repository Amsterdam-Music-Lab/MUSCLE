import { URLS, LOGO_URL, LOGO_TITLE } from "@/config";
import { Link } from "react-router-dom";
import useBoundStore from "@/util/stores";


const Logo: React.FC<{logoClickConfirm: string | null}> = ({logoClickConfirm=null}) => {
    const theme = useBoundStore((state) => state.theme);

    const logoUrl = theme?.logoUrl ?? LOGO_URL;

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
        className: "aha__logo",
        "aria-label": "Logo",
        style: { backgroundImage: `url(${logoUrl})` },
    };
    
    return (
        <>
            { URLS.AMLHome.startsWith("http") ? (
                <a href={URLS.AMLHome} {...logoProps}>
                    {LOGO_TITLE}
                </a>
                ) : (
                <Link to={URLS.AMLHome} {...logoProps}>
                    {LOGO_TITLE}
                </Link>
            )}
        </>
    )
}

export default Logo;
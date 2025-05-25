import { URLS, LOGO_URL, LOGO_TITLE } from "@/config";
import { Link } from "react-router-dom";
import useBoundStore from "@/util/stores";
import "./Logo.scss";

const Logo: React.FC = () => {
  const theme = useBoundStore((state) => state.theme);

  const { alt, title, file, target, rel } = theme?.logo || {};
  const href = theme?.logo?.href || URLS.AMLHome;
  const logoUrl = file ?? LOGO_URL;

  // Logo is a Link in case of relative url (/abc),
  // and a-element for absolute urls (https://www.example.com/)
  const logoProps = {
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
        <a {...logoProps}>{LOGO_TITLE}</a>
      ) : (
        <Link to={href} {...logoProps}>
          {LOGO_TITLE}
        </Link>
      )}
    </>
  );
};

export default Logo;

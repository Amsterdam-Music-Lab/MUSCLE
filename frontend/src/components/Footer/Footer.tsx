import React from "react";

import { API_BASE_URL } from "@/config";

import { Footer as IFooter, Logo as ILogo } from "@types/Footer";

export const Footer: React.FC<IFooter> = ({disclaimer, logos, privacy}) => {
    return (
        <div className="aha__footer">
            <p className="disclaimer" dangerouslySetInnerHTML={{
                __html: disclaimer,
                }}
            />
            <div className="logos">
                {logos.map((logo: ILogo) => (
                    <a
                        href={logo.href}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <img src={API_BASE_URL + logo.file} alt={logo.alt} />
                    </a>
                ))};
            </div>
            <div className="privacy">
                <p>
                    {privacy}
                </p>
            </div>
        </div>
    )
}

export default Footer;
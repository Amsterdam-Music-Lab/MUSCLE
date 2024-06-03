import React from "react";

import { API_BASE_URL } from "@/config";

import { Footer as IFooter, Logo as ILogo } from "@types/Footer";

export const Footer: React.FC<IFooter> = ({disclaimer, logos, privacy}) => {
    return (
        <div className="aha__footer">
            <div className="disclaimer" dangerouslySetInnerHTML={{
                __html: disclaimer,
                }}
            />
            <div className="logos">
                {logos.map((logo: ILogo, index: number) => (
                    <a
                        href={logo.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        key={index}
                    >
                        <img src={API_BASE_URL + logo.file} alt={logo.alt} />
                    </a>
                ))}
            </div>
            <div className="disclaimer" dangerouslySetInnerHTML={{
                __html: privacy,
                }}
            />
        </div>
    )
}

export default Footer;
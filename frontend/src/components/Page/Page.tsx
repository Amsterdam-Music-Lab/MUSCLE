import React from "react";
import { css } from '@emotion/react'
import useBoundStore from "@/util/stores";

interface PageProps {
    className?: string;
    children: React.ReactNode;
}

/** Page is a single page in the application */
const Page = ({ className, children }: PageProps) => {

    const theme = useBoundStore((state) => state.theme);
    const backgroundImageUrl = theme?.backgroundUrl;
    let style = {};

    if (backgroundImageUrl) {
        style = {
            backgroundImage: `url(${backgroundImageUrl})`
        }
    } else {
        style = {
            backgroundColor: theme?.colorBackground
        }
    }

    const stylePage = () => { 
        return css`
            color: ${theme?.colorText};
            h3.title:after {
                background-color: ${theme?.colorPrimary}
            }
        `
    }

    return (
        <div className={"aha__page " + (className ? className : "")} style={style} css={stylePage()}>
            {children}
        </div>
    );
};

export default Page;

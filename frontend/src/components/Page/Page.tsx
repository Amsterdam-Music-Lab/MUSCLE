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
    const backgroundColor = theme?.colorBackground;
    var style = {};

    if (backgroundImageUrl) {
        style = {
            backgroundImage: `url(${backgroundImageUrl})`
        }
    } else {
        style = {
            backgroundColor: backgroundColor
        }
    }

    return (
        <div className={"aha__page " + (className ? className : "")} style={style} css={css`color: ${theme?.colorText}`}>
            {children}
        </div>
    );
};

export default Page;

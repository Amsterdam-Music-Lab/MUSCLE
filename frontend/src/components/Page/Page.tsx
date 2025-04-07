import React from "react";
import useBoundStore from "@/util/stores";
import classNames from "classnames";
import { GradientCircles } from "@/components/svgs";

interface PageProps {
    className?: string;
    children: React.ReactNode;
}

/** Page is a single page in the application */
const Page = ({ className, children }: PageProps) => {

    const theme = useBoundStore((state) => state.theme);
    
    // @BC mark MCG theme as .mcg
    // @BC no default bg '/public/images/background.jpg', instead add .no-background
    const hasBackground = Boolean(theme?.backgroundUrl)

    return (
        <>
            <div 
                className={classNames('aha__page', className, !hasBackground && 'no-background', theme?.name == "MCG" && "mcg" )} 
                style={!hasBackground ? null : {backgroundImage: `url(${theme.backgroundUrl})`} }
            >
                {children}
            </div>
            {theme?.name == "MCG" && <GradientCircles color1="yellow" color2="pink" numCircles={30} />}
        </>
    );
};

export default Page;

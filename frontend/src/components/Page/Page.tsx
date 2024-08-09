import React from "react";
import useBoundStore from "@/util/stores";

interface PageProps {
    className?: string;
    children: React.ReactNode;
}

/** Page is a single page in the application */
const Page = ({ className, children }: PageProps) => {

    const theme = useBoundStore((state) => state.theme);
    const backgroundImageUrl = theme?.backgroundUrl || '/public/images/background.jpg';

    return (
        <div className={"aha__page " + (className ? className : "")} style={{ backgroundImage: `url(${backgroundImageUrl})` }}>
            {children}
        </div>
    );
};

export default Page;

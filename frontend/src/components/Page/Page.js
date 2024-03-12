import React from "react";
import useBoundStore from "util/stores";

// Page is a single page in the application
const Page = ({ className, children }) => {

    const theme = useBoundStore((state) => state.theme);
    const backgroundImageUrl = theme?.background_url || '/public/images/background.jpg';
    
    return (
        <div className={"aha__page " + (className ? className : "")} style={{ backgroundImage: `url(${backgroundImageUrl})` }}>
            {children}
        </div>
    );
};

export default Page;

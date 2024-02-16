import React from "react";

// Page is a single page in the application
const Page = ({ className, children }) => {
    return (
        <div className={"aha__page aha__page--custom" + (className ? className : "")}>
            {children}
        </div>
    );
};

export default Page;

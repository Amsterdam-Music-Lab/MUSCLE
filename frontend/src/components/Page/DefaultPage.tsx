import React from "react";
import Page from "./Page";
import AppBar from "../AppBar/AppBar";

interface DefaultPageProps {
    className?: string;
    title: string;
    children: React.ReactNode;
    fullwidth?: boolean;
    showAppBar?: boolean;
}

// @BC added a 'fullwidth' option. If false, children are wrapped in a fixed-width column.

/** DefaultPage is a Page with an AppBar and a width-restricted container for content (if fullwidth=true) */
const DefaultPage = ({ className, title, children, fullwidth = false, showAppBar = true }: DefaultPageProps) => {
    return (
        <Page className={className}>
            {showAppBar && <AppBar title={title} />}
            { fullwidth ? children : (
                <div className="container">
                    <div className="row justify-content-center py-3">
                        <div className="col-12">{children}</div>
                    </div>
                </div>
            )}
        </Page>
    );
};

export default DefaultPage;

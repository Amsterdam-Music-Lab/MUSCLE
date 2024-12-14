import React from "react";
import Page from "./Page";
import AppBar from "../AppBar/AppBar";

interface DefaultPageProps {
    className?: string;
    title: string;
    children: React.ReactNode;
}

/** DefaultPage is a Page with an AppBar and a width-restricted container for content */
const DefaultPage = ({ className, title, children }: DefaultPageProps) => {
    return (
        <Page className={className}>
            <AppBar title={title} />
            <div className="container">
                <div className="row justify-content-center py-3">
                    <div className="col-12">{children}</div>
                </div>
            </div>
        </Page>
    );
};

export default DefaultPage;

import React from "react";
import useBoundStore from "../../util/stores";

import Page from "./Page";
import AppBar from "../AppBar/AppBar";
import Header from "../Header/Header";

// DefaultPage is a Page with an AppBar and a width-restricted container for content
const DefaultPage = ({ className, title, logoClickConfirm, aboutSlug, nextExperiment, children }) => {

    const theme = useBoundStore((state) => state.theme);
    const headerProps = theme?.header;

    return (
        <Page className={className}>
            <AppBar title={title} logoClickConfirm={logoClickConfirm} />
            {headerProps && (
                <Header nextExperimentSlug={nextExperiment} collectionSlug={aboutSlug} {...headerProps }></Header>
            )}
            <div className="container">
                <div className="row justify-content-center py-3">
                    <div className="col-12">{children}</div>
                </div>
            </div>
        </Page>
    );
};

export default DefaultPage;

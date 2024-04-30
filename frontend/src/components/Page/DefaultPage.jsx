import React, { useEffect, useState } from "react";
import useBoundStore from "../../util/stores";

import Page from "./Page";
import AppBar from "../AppBar/AppBar";
import Header from "../Header/Header";

// DefaultPage is a Page with an AppBar and a width-restricted container for content
const DefaultPage = ({ className, title, logoClickConfirm, collectionSlug, nextExperimentSlug, children }) => {

    const theme = useBoundStore((state) => state.theme);
    const [headerProps, setHeaderProps] = useState(undefined);

    useEffect(() => {
        if (theme && theme.header) {
            const headerProps = {
                aboutButtonText: theme.header.about_button_text,
                nextExperimentButtonText: theme.header.next_experiment_button_text,
                showScore: theme.header.show_score,
                collectionSlug,
                nextExperimentSlug
            };
            setHeaderProps(headerProps);
        }
    }, [theme])
    

    return (
        <Page className={className}>
            <AppBar title={title} logoClickConfirm={logoClickConfirm} />
            {headerProps && (
                <Header {...headerProps }></Header>
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

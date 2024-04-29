import React from "react";
import classNames from "classnames";


// HTML is an experiment view, that shows custom HTML and a Form
const HTML = ({ body, innerClassName = "text-center pb-3" }) => {

    return (
        <div className={classNames("aha__HTML")}>
            <div
                className={classNames("html-content", innerClassName)}
                dangerouslySetInnerHTML={{ __html: body }}
            />
        </div>
    );
};

export default HTML;

import React from "react";
import classNames from "classnames";


// HTML is an experiment view, that shows custom HTML and a Form
const HTML = ({ body }) => {

    return (
        <div className={classNames("aha__HTML")}>
            <div
                className="html-content d-flex justify-content-center pb-3"
                dangerouslySetInnerHTML={{ __html: body }}
            />
        </div>
    );
};

export default HTML;

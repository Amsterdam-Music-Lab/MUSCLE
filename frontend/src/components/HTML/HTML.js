import React, { useCallback } from "react";
import classNames from "classnames";

import FeedbackForm from "../FeedbackForm/FeedbackForm";

// HTML is an experiment view, that shows custom HTML and a Form
const HTML = ({ html, form, style, onResult }) => {
    const makeResult = useCallback(
        (result) => {
            onResult(result);
        },
        [onResult]
    );

    return (
        <div className={classNames("aha__HTML",style || "neutral")}>
            <div
                className="html-content d-flex justify-content-center pb-3"
                dangerouslySetInnerHTML={{ __html: html }}
            />
            <FeedbackForm
                formActive={true}
                form={form.form}
                buttonLabel={form.submit_label}
                skipLabel={form.skip_label}
                isSkippable={form.is_skippable}
                onResult={makeResult}
                emphasizeTitle={false}
            />
        </div>
    );
};

export default HTML;

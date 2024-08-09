import classNames from "classnames";

interface HTMLProps {
    body: string | TrustedHTML;
    innerClassName?: string;
}

/** HTML is an block view, that shows custom HTML and a Form */
const HTML = ({ body, innerClassName = "text-center pb-3" }: HTMLProps) => {

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

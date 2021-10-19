import React from "react";

import { URLS } from "../../config";

const Social = ({ renderSocial, score }) => {
    /* Social is a view which returns social media links with icons
    if render_social is set to false, returns an empty diff
    */
    if (renderSocial) {
        return (
            <div className="share d-flex justify-content-center mt-4">
                <a
                    href={URLS.shareFacebook}
                    target="_blank"
                    className="ti-facebook"
                    rel="noopener noreferrer"
                >
                    Share on Facebook
                </a>
                <a
                    href={URLS.shareTwitter.replace("--SCORE--", score)}
                    target="_blank"
                    className="ti-twitter-alt"
                    rel="noopener noreferrer"
                >
                    Share on Twitter
                </a>
            </div>
        )
    }
    else return (<div></div>)
}

export default Social;
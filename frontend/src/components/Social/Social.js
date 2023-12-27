import React, { useRef } from "react";
import {
    FacebookShareButton, TwitterShareButton, WeiboShareButton, WhatsappShareButton,
} from "next-share"


const Social = ({ social }) => {
    /* Social is a view which returns social media links with icons
    if render_social is set to false, returns an empty diff
    */

    const showShare = useRef(
        navigator.share !== undefined && navigator.canShare !== undefined,
    )

    const shareContent = (text, url) => {
        const shareData = {
            text: text,
            url: url,
        }
        if (navigator.canShare(shareData)) {
            navigator.share(shareData).then(
                () => void 0,
                (error) => { console.error(error) },
            );
        }
    }

    const copyToClipboard = async (url) => {
        await navigator.clipboard.writeText(url);
    }

    return (
        <div className="aha__share d-flex justify-content-center mt-4">
            {social.apps.includes("facebook") && (
                <FacebookShareButton
                    url={social.url}
                    title={social.message}
                    hashtag={social.hashtags[0]}
                    blankTarget="true"
                >
                    <i className="fa-brands fa-facebook-f fa-2x"></i>
                </FacebookShareButton>
            )}
            {social.apps.includes("whatsapp") && (
                <WhatsappShareButton
                    url={social.url}
                    title={social.message}
                    blankTarget="true"
                >
                    <i className="fa-brands fa-whatsapp fa-2x"></i>
                </WhatsappShareButton>
            )}
            {social.apps.includes("twitter") && (
                <TwitterShareButton
                    url={social.url}
                    title={social.message}
                    hashtags={social.hashtags}
                    blankTarget="true"
                >
                    <i className="fa-brands fa-x-twitter fa-2x"></i>
                </TwitterShareButton>
            )}
            {social.apps.includes("weibo") && (
                <WeiboShareButton
                    url={social.url}
                    title={social.message}
                    blankTarget="true"
                >
                    <i className="fa-brands fa-weibo fa-2x"></i>
                </WeiboShareButton>
            )}
            {showShare.current && social.apps.includes("share") && (
                <div onClick={() => shareContent(social.text, social.url)}>
                    <i className="fa-solid fa-share-nodes fa-2x"></i>
                </div>
            )}
            {social.apps.includes("clipboard") && (
                <div onClick={() => copyToClipboard(social.url)}>
                    <i className="fa-solid fa-clipboard fa-2x"></i>
                </div>
            )}
        </div>
    );
};

export default Social;

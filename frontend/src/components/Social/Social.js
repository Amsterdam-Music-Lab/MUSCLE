import React, { useRef } from "react";
import {
    FacebookShareButton, TwitterShareButton, WeiboShareButton, WhatsappShareButton
  } from 'next-share'
  

const Social = ({ social }) => {
    /* Social is a view which returns social media links with icons
    if render_social is set to false, returns an empty diff
    */

    const showShare = useRef(
        window.isSecureContext && 
        navigator.userAgent.includes('Mobi') &&
        !navigator.userAgent.includes('Firefox'))
    
    const shareContent = (text, url) => {
        navigator.share(
            {
                text: text,
                url: url
            }
        )
    }
    
    return (
        <div className="aha__share d-flex justify-content-center mt-4">
            {social.apps.includes('facebook') && (
                <FacebookShareButton
                    url={social.url}
                    hashtag={social.hashtags[0]}
                    blankTarget="true"
                >
                    <i class="fa-brands fa-facebook-f fa-2x"></i>
                </FacebookShareButton>
            )}
            {social.apps.includes('whatsapp') && (
                <WhatsappShareButton
                    url={social.url}
                    title={social.message}
                    blankTarget="true"
                >
                    <i className="fa-brands fa-whatsapp fa-2x"></i>
                </WhatsappShareButton>
            )}
            {social.apps.includes('twitter') && (
                <TwitterShareButton
                    url={social.url}
                    title={social.message}
                    hashtags={social.hashtags}
                    blankTarget="true"
                >
                    <i className="fa-brands fa-x-twitter fa-2x"></i>
                </TwitterShareButton>
            )}
            {social.apps.includes('weibo') && (
                <WeiboShareButton
                    url={social.url}
                    title={social.message}
                    blankTarget="true"
                >
                    <i className="fa-brands fa-weibo fa-2x"></i>
                </WeiboShareButton>
            )}
            {social.apps.includes('share') && showShare && (
                <div onClick={() => shareContent(social.text, social.url)}>
                    <i className="fa-solid fa-share-nodes fa-2x"></i>
                </div>
            )}
        </div>
    );
};

export default Social;

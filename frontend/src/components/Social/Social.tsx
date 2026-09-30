import { useRef } from "react";
import {
    FacebookShareButton, TwitterShareButton, WeiboShareButton, WhatsappShareButton
} from 'react-share'
import ISocial from "@/types/Social";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFacebookF, faXTwitter, faWeibo, faWhatsapp } from '@fortawesome/free-brands-svg-icons'
import { faClipboard, faShareNodes } from '@fortawesome/free-solid-svg-icons'

export interface SocialProps {
    social: ISocial
}

/**
 * Social is a view which returns social media links with icons
 * if render_social is set to false, returns an empty diff
*/
const Social = ({ social }: SocialProps) => {

    const showShare = useRef(
        navigator.share !== undefined && navigator.canShare !== undefined
    )

    const shareContent = (text: string, url: string) => {
        const shareData = {
            text,
            url
        }
        if (navigator.canShare(shareData)) {
            navigator.share(shareData).then(
                () => void 0,
                (error) => { console.error(error) }
            );
        }
    }

    const copyToClipboard = async (url: string) => {
        await navigator.clipboard.writeText(url);
    }

    return (
        <div className="aha__share d-flex justify-content-center mt-4">
            {social.channels.includes('facebook') && (
                <FacebookShareButton
                    url={social.url}
                    title={social.content}
                    hashtag={social.tags[0]}
                >
                    <FontAwesomeIcon icon={faFacebookF}/>
                </FacebookShareButton>
            )}
            {social.channels.includes('whatsapp') && (
                <WhatsappShareButton
                    url={social.url}
                    title={social.content}
                >
                    <FontAwesomeIcon icon={faWhatsapp}/>
                </WhatsappShareButton>
            )}
            {social.channels.includes('twitter') && (
                <TwitterShareButton
                    url={social.url}
                    title={social.content}
                    hashtags={social.tags}
                >
                    <FontAwesomeIcon icon={faXTwitter}/>
                </TwitterShareButton>
            )}
            {social.channels.includes('weibo') && (
                <WeiboShareButton
                    url={social.url}
                    title={social.content}
                >
                    <FontAwesomeIcon icon={faWeibo}/>
                </WeiboShareButton>
            )}
            {showShare.current && social.channels.includes('share') && (
                <div onClick={() => shareContent(social.content, social.url)} data-testid="navigator-share">
                    <FontAwesomeIcon icon={faShareNodes}/>
                </div>
            )}
            {social.channels.includes('clipboard') && (
                <div onClick={() => copyToClipboard(social.url)} data-testid="clipboard-share">
                    <FontAwesomeIcon icon={faClipboard} />
                </div>
            )}
        </div>
    );
};

export default Social;

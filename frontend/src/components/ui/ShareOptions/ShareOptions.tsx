/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes, CSSProperties } from "react";
import type { ShareConfig, ShareChannel } from "@/types/share";

import { useRef } from "react";
import classNames from "classnames";
import {
  FacebookShareButton,
  TwitterShareButton,
  WeiboShareButton,
  WhatsappShareButton,
} from "react-share";

import styles from "./ShareOptions.module.scss";

interface ShareOptProps {
  config: ShareConfig;
  style?: CSSProperties;
}

function Facebook({ config, ...props }: ShareOptProps) {
  const { style, ...rest } = props;
  return (
    <FacebookShareButton
      url={config.url}
      title={config.content}
      hashtag={config.tags[0]}
      style={{ "--icon-size-correction": 0.85, ...style } as CSSProperties}
      {...rest}
    >
      <i className="fa-brands fa-facebook-f fa-2x"></i>
    </FacebookShareButton>
  );
}

function Whatsapp({ config, ...props }: ShareOptProps) {
  const { style, ...rest } = props;
  return (
    <WhatsappShareButton
      url={config.url}
      title={config.content}
      style={{ "--icon-size-correction": 1, ...style } as CSSProperties}
      {...rest}
    >
      <i className="fa-brands fa-whatsapp fa-2x"></i>
    </WhatsappShareButton>
  );
}

function Twitter({ config, ...props }: ShareOptProps) {
  return (
    <TwitterShareButton
      url={config.url}
      title={config.content}
      hashtags={config.tags}
      {...props}
      style={{ "--icon-size-correction": 0.9 } as CSSProperties}
    >
      <i className="fa-brands fa-x-twitter fa-2x"></i>
    </TwitterShareButton>
  );
}

function Weibo({ config, ...props }: ShareOptProps) {
  return (
    <WeiboShareButton url={config.url} title={config.content} {...props}>
      <i className="fa-brands fa-weibo fa-2x"></i>
    </WeiboShareButton>
  );
}

function Share({ config, ...props }: ShareOptProps) {
  const shareContent = (text: string, url: string) => {
    const shareData = { text, url };
    if (navigator.canShare(shareData)) {
      navigator.share(shareData).then(
        () => void 0,
        (error) => {
          console.error(error);
        }
      );
    }
  };
  return (
    <div
      onClick={() => shareContent(config.content, config.url)}
      data-testid="navigator-share"
      {...props}
    >
      <i className="fa-solid fa-share-nodes fa-2x"></i>
    </div>
  );
}

function ClipBoard({ config, ...props }: ShareOptProps) {
  const { style, ...rest } = props;
  const copyToClipboard = async (url: string) => {
    await navigator.clipboard.writeText(url);
  };
  return (
    <div
      onClick={() => copyToClipboard(config.url)}
      data-testid="clipboard-share"
      style={{ "--icon-size-correction": 0.85, ...style } as CSSProperties}
      {...rest}
    >
      <i className="fa-solid fa-clipboard fa-2x"></i>
    </div>
  );
}

const components: Record<ShareChannel, React.ComponentType<any>> = {
  facebook: Facebook,
  whatsapp: Whatsapp,
  twitter: Twitter,
  weibo: Weibo,
  share: Share,
  clipboard: ClipBoard,
};

export interface SocialProps extends HTMLAttributes<HTMLDivElement> {
  config: ShareConfig;
}

/**
 * Social is a view which returns social media links with icons
 * if render_social is set to false, returns an empty diff
 */
export default function ShareOptions({
  config,
  className,
  ...divProps
}: SocialProps) {
  const showShare = useRef(
    navigator.share !== undefined && navigator.canShare !== undefined
  );

  /** Check whether a channel should be shown */
  const show = (channel: ShareChannel) => {
    if (channel === "share" && !showShare.current) return false;
    return true;
  };

  const shareComponents = config.channels
    .filter(show)
    .map((channel: ShareChannel) => components[channel])
    .filter(Boolean);

  return (
    <div className={classNames(styles.share, className)} {...divProps}>
      {shareComponents.map((Component, i) => (
        <div key={i}>
          <Component config={config} className={styles.button} />
        </div>
      ))}
    </div>
  );
}

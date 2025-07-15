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
import { t } from "@/util/i18n";
import { Icon } from "@/components/icons";

const copyToClipboard = async (message: string) => {
  await navigator.clipboard.writeText(message);
};

interface ShareOptProps {
  config: ShareConfig;
  style?: CSSProperties;
}

function Facebook({ config, ...props }: ShareOptProps) {
  return (
    <FacebookShareButton
      url={config.url}
      title={config.content}
      hashtag={config.tags[0]}
      resetButtonStyle={false}
      {...props}
    >
      <Icon name="facebook" />
    </FacebookShareButton>
  );
}

function Whatsapp({ config, ...props }: ShareOptProps) {
  return (
    <WhatsappShareButton
      url={config.url}
      title={config.content}
      resetButtonStyle={false}
      {...props}
    >
      <Icon name="whatsapp" />
    </WhatsappShareButton>
  );
}

function Twitter({ config, ...props }: ShareOptProps) {
  return (
    <TwitterShareButton
      url={config.url}
      title={config.content}
      hashtags={config.tags}
      resetButtonStyle={false}
      {...props}
    >
      <Icon name="x" />
    </TwitterShareButton>
  );
}

function Weibo({ config, ...props }: ShareOptProps) {
  return (
    <WeiboShareButton
      resetButtonStyle={false}
      url={config.url}
      title={config.content}
      {...props}
    >
      <Icon name="weibo" />
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
    <button
      onClick={() => shareContent(config.content, config.url)}
      data-testid="navigator-share"
      {...props}
    >
      <Icon name="share" />
    </button>
  );
}

function ClipBoard({ config, ...props }: ShareOptProps) {
  const message = t("share.clipboard", {
    message: config?.content,
    url: config?.url,
  });
  return (
    <button
      onClick={() => copyToClipboard(message)}
      data-testid="clipboard-share"
      {...props}
    >
      <Icon name="clipboard" />
    </button>
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
        <Component config={config} className={styles.button} key={i} />
      ))}
    </div>
  );
}

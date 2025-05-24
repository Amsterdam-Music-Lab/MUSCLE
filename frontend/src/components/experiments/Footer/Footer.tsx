/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import type { Logo } from "@/types/Theme";

import classNames from "classnames";
import { RenderHtml } from "@/components/utils";
import "./Footer.scss";

export interface FooterProps extends HTMLAttributes<HTMLDivElement> {
  /** HTML string for the disclaimer text */
  disclaimerHtml?: string;

  /** HTML string for the privacy text */
  privacyHtml?: string;

  /** Logos */
  logos: Logo[];
}

export default function Footer({
  disclaimerHtml,
  logos,
  privacyHtml,
  ...divProps
}: FooterProps) {
  return (
    <div className={classNames("aha__footer", classNames)} {...divProps}>
      {disclaimerHtml && (
        <RenderHtml html={disclaimerHtml} className="disclaimer" />
      )}
      <div className="logos">
        {logos.map((logo: ILogo, index: number) => (
          <a
            href={logo.href}
            target="_blank"
            rel="noopener noreferrer"
            key={index}
          >
            <img src={logo.file} alt={logo.alt} />
          </a>
        ))}
      </div>
      {privacyHtml && <RenderHtml className="privacy" html={privacyHtml} />}
    </div>
  );
}

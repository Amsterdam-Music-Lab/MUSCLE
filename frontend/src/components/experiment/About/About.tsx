/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { Link } from "react-router-dom";
import { RenderHtml } from "@/components/utils";

export interface AboutProps {
  content: string;
  slug: string;
  backButtonText: string;
}

export default function About({ content, slug, backButtonText }: AboutProps) {
  return (
    <div className="container">
      <Link className="btn btn-lg btn-outline-primary mt-3" to={`/${slug}`}>
        <i className="fas fa-arrow-left mr-2"></i>
        {backButtonText}
      </Link>
      <div className="col-12 mt-3" role="contentinfo">
        <RenderHtml
          html={content}
          innerClassName="prose text-left pb-3 text-white"
        />
      </div>
    </div>
  );
}

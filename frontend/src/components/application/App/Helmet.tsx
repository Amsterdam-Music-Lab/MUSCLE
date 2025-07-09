/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { Helmet as ReactHelmet } from "react-helmet";

export default function Helmet({
  title,
  description,
  image,
  url,
  children,
  structuredData,
}) {
  const hasTitle = title && title !== "";
  const hasDescription = description && description !== "";
  const hasImage = image && image !== "";
  const hasUrl = url && url !== "";
  const hasStructuredData =
    structuredData || hasUrl || hasImage || hasTitle || hasDescription;

  if (hasStructuredData) {
    structuredData = {
      "@context": "http://schema.org",
      "@type": "Organization",
      url,
      logo: image,
      name: title,
      description,
      ...structuredData,
    };
  }

  return (
    <ReactHelmet>
      {hasTitle && <title>{title}</title>}
      {hasDescription && (
        <meta name="description" content={description ?? "HELLO THERE"} />
      )}

      {hasTitle && <meta property="og:title" content={title} />}
      {hasDescription && (
        <meta property="og:description" content={description} />
      )}
      {hasImage && <meta property="og:image" content={image} />}
      {hasUrl && <meta property="og:url" content={url} />}

      {hasTitle && <meta name="twitter:title" content={title} />}
      {hasDescription && (
        <meta name="twitter:description" content={description} />
      )}
      {hasImage && <meta name="twitter:image" content={image} />}
      <meta name="twitter:card" content="summary_large_image" />

      {hasUrl && <link rel="canonical" href={url} />}
      {hasStructuredData && (
        <script type="application/ld+json">
          {JSON.stringify(structuredData)}
        </script>
      )}

      {children}
    </ReactHelmet>
  );
}

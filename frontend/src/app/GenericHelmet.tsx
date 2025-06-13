// router.ts
import type { Component } from "react";
import { useLocation } from "react-router-dom";
import { Helmet } from "react-helmet-async";

export function getHelmetData({
  type = "Organization",
  context = "http://schema.org",
  ...data
}) {
  data = { "@context": context, "@type": type, ...data };
  return JSON.stringify(data);
}

export interface GenericHelmetProps extends Component {
  title?: string;
  description?: string;
  image?: string;
  url?: string;
  data?: Record<string, string>;
}

export function GenericHelmet({
  title,
  description,
  image,
  url = undefined,
  data = {},
  children,
}: GenericHelmetProps) {
  const { pathname } = useLocation();
  if (url === undefined) url = `${window.location.origin}${pathname}`;
  return (
    <Helmet>
      {title && <title>{title}</title>}
      {description && <meta name="description" content={description} />}
      {title && <meta property="og:title" content={title} />}
      {description && <meta property="og:description" content={description} />}
      {image && <meta property="og:image" content={image} />}
      {url && <meta property="og:url" content={url} />}

      {title && <meta name="twitter:title" content={title} />}
      {description && <meta name="twitter:description" content={description} />}
      {image && <meta name="twitter:image" content={image} />}
      <meta name="twitter:card" content="summary_large_image" />

      {url && <link rel="canonical" href={url} />}

      <script type="application/ld+json">
        {getHelmetData({
          name: title,
          description,
          logo: image,
          url,
          ...data,
        })}
      </script>
      {children}
    </Helmet>
  );
}

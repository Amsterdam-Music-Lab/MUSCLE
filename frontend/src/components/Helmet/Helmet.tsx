import { Helmet as ReactHelmet } from 'react-helmet';
import useBoundStore from "../../util/stores";

const Helmet = () => {
    const headData = useBoundStore(state => state.headData);
    const { description, image, url } = headData;

    const structuredData = {
        "@context": "http://schema.org",
        "@type": "Organization",
        url: url,
        logo: image,
        name: headData.title,
        description: description,
        ...headData.structuredData,
    };

    return (
        <ReactHelmet>
            <title>{headData.title}</title>
            <meta name="description" content={description} />
            <meta property="og:title" content={headData.title} />
            <meta property="og:description" content={description} />
            <meta property="og:image" content={image} />
            <meta property="og:url" content={url} />

            <meta name="twitter:title" content={headData.title} />
            <meta name="twitter:description" content={description} />
            <meta name="twitter:image" content={image} />
            <meta name="twitter:card" content="summary_large_image" />

            <link rel="canonical" href={url} />

            <link rel="icon" type="image/png" href="/favicon.ico" />
            <link rel="apple-touch-icon" href="/favicon.ico" />

            <script type="application/ld+json">
                {JSON.stringify(structuredData)}
            </script>
        </ReactHelmet>
    );
};

export default Helmet;

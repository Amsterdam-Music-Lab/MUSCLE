export default interface Image {
    title: string;
    description: string;
    file: string;
    alt: string;
    href: string;
    rel: string;
    target: '_blank' | '_self' | '_parent' | '_top' | string;
}
export default interface Social {
    apps: 'facebook' | 'whatsapp' | 'twitter' | 'weibo' | 'share' | 'clipboard',
    url: string,
    message: string,
    hashtags: string[],
    text: string
}

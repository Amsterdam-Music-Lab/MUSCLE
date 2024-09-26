export default interface Social {
    apps: Array<'facebook' | 'whatsapp' | 'twitter' | 'weibo' | 'share' | 'clipboard'>,
    url: string,
    message: string,
    hashtags: string[],
}

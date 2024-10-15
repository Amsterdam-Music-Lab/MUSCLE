export default interface Social {
    channels: Array<'facebook' | 'whatsapp' | 'twitter' | 'weibo' | 'share' | 'clipboard'>,
    url: string,
    content: string,
    tags: string[],
}

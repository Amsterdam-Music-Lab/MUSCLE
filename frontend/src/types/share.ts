export type ShareChannel =
  | "facebook"
  | "whatsapp"
  | "twitter"
  | "weibo"
  | "share"
  | "clipboard";

export interface ShareConfig {
  channels: ShareChannel[];
  url: string;
  content: string;
  tags: string[];
}

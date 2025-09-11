import { Facebook } from "./custom/Facebook";
import { X } from "./custom/X";
import { Weibo } from "./custom/Weibo";
import { Share } from "./custom/Share";
import { Whatsapp } from "./custom/Whatsapp";
import { ClipBoard } from "./custom/Clipboard";
import { Comment } from "./custom/Comment";

export const iconMap = {
  facebook: Facebook,
  x: X,
  weibo: Weibo,
  share: Share,
  whatsapp: Whatsapp,
  clipboard: ClipBoard,
  comment: Comment,
};

export type IconName = keyof typeof iconMap;

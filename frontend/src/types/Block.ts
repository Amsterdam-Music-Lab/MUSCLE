import IImage from "@/types/Image";
import Theme from "./Theme";

export default interface Block {
    id: number;
    slug: string;
    name: string;
    description: string;
    image?: IImage;
    bonus_points: number;
}

export interface Playlist {
    id: string;
    name: string;
}

export interface FeedbackInfo {
    header: string;
    button: string;
    contact_body: string;
    thank_you: string;
    show_float_button: boolean;
}

export interface ExtendedBlock extends Block {
    theme?: Theme;
    class_name: string;
    rounds: number;
    playlists: Playlist[];
    feedback_info: FeedbackInfo;
    session_id: number;
    loading_text: string;
}

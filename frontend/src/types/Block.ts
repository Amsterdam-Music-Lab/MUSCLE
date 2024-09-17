import IImage from "@/types/Image";
import Theme from "./Theme";

export default interface Block {
    slug: string;
    name: string;
    description: string;
    image?: IImage;
    bonus_points: number;
    theme?: Theme;
    class_name: string;
    rounds: number;
    playlists: Playlist[];
    feedback_info: FeedbackInfo;
    session_id: number;
    loading_text: string;
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

export interface Step {
    id: number;
    description: string;
}

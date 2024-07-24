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

export interface ExtendedBlock extends Block {
    theme?: Theme;
    class_name: string;
    rounds: number;
    playlists: { id: number; name: string }[];
    feedback_info: {
        header: string;
        button: string;
        contact_body: string;
        thank_you: string;
        show_float_button: boolean;
    }
    session_id: number;
}

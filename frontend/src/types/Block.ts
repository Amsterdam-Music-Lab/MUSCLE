import IButton from "@/types/Button";
import IImage from "@/types/Image";
import Theme from "@/types/Theme";

export default interface Block {
    identifier: string;
    name: string;
    description: string;
    image?: IImage;
    bonus_points: number;
    theme: Theme;
    className: string;
    rounds: number;
    feedbackInfo: FeedbackInfo;
    sessionId: number;
    experimentIdentifier: string;
    loadingText: string;
}

export interface FeedbackInfo {
    header: string;
    button: IButton;
    contact_body: string;
    thank_you: string;
    show_float_button: boolean;
}

export interface Step {
    id: number;
    description: string;
}

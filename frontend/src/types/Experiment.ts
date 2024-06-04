import IImage from "@/types/Image";

export default interface Experiment {
    id: number;
    name: string;
    slug: string;
    description: string;
    image: IImage;
    started_session_count: number;
    finished_session_count: number;
}
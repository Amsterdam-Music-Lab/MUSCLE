import IImage from "@/types/Image";

export default interface Experiment {
    id: number;
    name: string;
    slug: string;
    description: string;
    image?: IImage;
}
import IImage from "@/types/Image";

export default interface Block {
    id: number;
    name: string;
    slug: string;
    description: string;
    image?: IImage;
    bonus_points: number;
}

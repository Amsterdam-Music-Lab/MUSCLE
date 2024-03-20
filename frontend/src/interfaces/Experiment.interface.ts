export default interface Experiment {
    id: number;
    name: string;
    slug: string;
    description: string;
    image: string;
    finished_session_count?: number;
}
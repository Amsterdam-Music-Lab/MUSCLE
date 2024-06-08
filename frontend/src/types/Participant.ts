export default interface Participant {
    id: number;
    hash: string;
    csrf_token: string;
    participant_id_url: string;
    country: string;
}

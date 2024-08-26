export interface ParticipantLink {
    url: string;
    copy_message: string;
}

export default interface Participant {
    id: number;
    hash: string;
    csrf_token: string;
    participant_id_url: string;
    country: string;
}

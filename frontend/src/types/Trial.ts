export interface TrialConfig {
    response_time: number;
    auto_advance: boolean;
    listen_first: boolean;
    show_continue_button: boolean;
    continue_label: string;
    style: string;
    break_round_on: any;

    auto_advance_timer: number | null;
}

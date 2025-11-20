import IButton from  "@/types/Button";

interface BreakRoundOn {
    EQUALS?: string[];
    NOT?: string[];
}

export interface TrialConfig {
    response_time: number;
    auto_advance: boolean;
    listen_first: boolean;
    continueButton: IButton;
    break_round_on: BreakRoundOn;

    auto_advance_timer: number | null;
}

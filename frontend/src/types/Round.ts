import { Action } from "./Action";

export type Round = Action[];

export interface RoundResponse {
  next_round: Round;
}

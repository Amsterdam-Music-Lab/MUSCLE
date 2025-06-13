import axios from "axios";
import { API_BASE_URL } from "@/config";
import type Session from "@/types/Session";
import type Participant from "@/types/Participant";
import type Experiment from "@/types/Experiment";
import type Block from "@/types/Block";
import type { Round } from "@/types/Round";

export async function fetchData<T>(path: string): T {
  axios.defaults.withCredentials = true;
  const url = `${API_BASE_URL}/${path}`;
  const res = await axios.get<T>(url);
  return res.data;
}

export const fetchExperiment = (slug: string) =>
  fetchData<Experiment>(`experiment/${slug}`);

export const fetchParticipant = (id?: string | null) => {
  let path = id ? `participant?participant_id=${id}` : "participant";
  return fetchData<Participant>(path);
};

// TODO Why doesnt the api call depend on the experiment slug?
// Suggests that it requires globally unique block slugs?
export const fetchBlock = (slug: string) =>
  fetchData<Block>(`experiment/block/${slug}`);

export async function fetchNextRound(session: Session) {
  const path = `session/${session.id}/next_round/`;
  const data = await fetchData<{ next_round: Round }>(path);
  return data.next_round;
}

import { fetchParticipant } from "../api";

export async function participantLoader() {
  const urlParams = new URLSearchParams(window.location.search);
  const participantId = urlParams.get("participant_id");
  const participant = await fetchParticipant(participantId);
  if (!participant) throw "Could not load participant data";
  return { participant };
}

import { participantLoader } from "./participantLoader";

export async function rootLoader() {
  const participant = await participantLoader();
  return { participant };
}

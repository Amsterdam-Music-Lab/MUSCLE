import { fetchExperiment } from "../api";

export async function experimentLoader({ params }) {
  const experiment = await fetchExperiment(params.expSlug);
  if (!experiment) throw new Response("Experiment not found", { status: 404 });
  return { experiment };
}

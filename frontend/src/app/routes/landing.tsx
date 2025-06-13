import { useLoaderData } from "react-router-dom";
import { View } from "@/components/application";
import frontendConfig from "@/config/frontend";

export async function landingLoader() {
  return { plugins: frontendConfig.landing?.plugins };
}

export function LandingPage() {
  const { plugins } = useLoaderData();
  return <View name="landing" plugins={plugins} />;
}

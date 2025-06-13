import { useRouteLoaderData } from "react-router-dom";
import { ExperimentHelmet } from "./experiment";
import { View } from "@/components/application";

export function AboutPage() {
  const { experiment } = useRouteLoaderData("experiment");
  return (
    <>
      <ExperimentHelmet
        experiment={experiment}
        title={`About – ${experiment.name}`}
      />
      <View name="about" experiment={experiment} />;
    </>
  );
}

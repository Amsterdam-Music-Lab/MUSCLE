import { useRouteLoaderData } from "react-router-dom";
import { ExperimentHelmet } from "./experiment";
import { View } from "@/components/application";

export function DashboardPage() {
  const { experiment } = useRouteLoaderData("experiment");

  return (
    <>
      <ExperimentHelmet
        experiment={experiment}
        title={`Dashboard – ${experiment.name}`}
      />
      <View name="dashboard" experiment={experiment} />
    </>
  );
}

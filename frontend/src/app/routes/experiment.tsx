import type Experiment from "@/types/Experiment";
import type { GenericHelmetProps } from "../GenericHelmet";
import { Navigate, useRouteLoaderData } from "react-router-dom";
export { experimentLoader } from "../loaders/experimentLoader";
import { GenericHelmet } from "../GenericHelmet";

export interface ExperimentHelmetProps extends GenericHelmetProps {
  experiment: Experiment;
}

export function ExperimentHelmet({
  experiment,
  ...genericHelmetProps
}: ExperimentHelmetProps) {
  return (
    <GenericHelmet
      title={experiment.name}
      description={experiment.description}
      image={experiment?.image?.file}
      {...genericHelmetProps}
    />
  );
}

export function ExperimentPage() {
  const { experiment } = useRouteLoaderData("experiment");
  const hasDashboard = experiment?.dashboard.length;
  const nextBlock = experiment?.nextBlock;

  // Redirect to consent form
  if (experiment.consent && false) return <Navigate to="/consent" />;

  // Redirect to block
  if (!hasDashboard && nextBlock) {
    return <Navigate to={`block/${nextBlock.slug}`} />;
  }

  return <Navigate to="dashboard" />;
}

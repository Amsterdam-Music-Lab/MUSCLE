// router.ts
import { createBrowserRouter } from "react-router-dom";
import AppLayout from "./AppLayout";
import { ExperimentPage, experimentLoader } from "./routes/experiment";
import { BlockPage, blockLoader } from "./routes/block";
import { AboutPage } from "./routes/about";
import { DashboardPage } from "./routes/dashboard";
import { ErrorPage } from "./routes/error";
import { LandingPage, landingLoader } from "./routes/landing";
import { rootLoader } from "./loaders/rootLoader";
import { RoundPage, roundLoader } from "./routes/round";

export const router = createBrowserRouter([
  {
    path: "/",
    id: "root",
    loader: rootLoader,
    Component: AppLayout,
    ErrorBoundary: ErrorPage,
    children: [
      { path: "landing", Component: LandingPage, loader: landingLoader },
      {
        path: ":expSlug",
        id: "experiment",
        loader: experimentLoader,
        children: [
          { index: true, Component: ExperimentPage },
          { path: "about", Component: AboutPage },
          { path: "dashboard", Component: DashboardPage },
          {
            path: "block/:blockSlug",
            id: "block",
            loader: blockLoader,
            // Component: BlockPage,
            children: [
              {
                path: "next",
                loader: roundLoader,
                Component: RoundPage,
              },
            ],
          },
        ],
      },
    ],
  },
]);

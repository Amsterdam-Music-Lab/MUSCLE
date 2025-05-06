import { Page } from "../../application/Page";
import { NarrowLayout } from "@/components/layout";
import PluginRenderer from "@/components/plugins/PluginRenderer";
import { Card, LinkButton } from "@/components/ui";

interface LandingPageProps {
  experimentUrl;
  showGradientCircles: boolean;
}

const DEFAULT_PLUGINS = [
  {
    name: "linkButton",
    args: {
      children: "Start the game!",
    },
  },
];

export default function LandingPage({
  experimentUrl,
  showGradientCircles = true,
  title = "bla",
  className,
  plugins = DEFAULT_PLUGINS,
}: LandingPageProps) {
  if (plugins) {
    plugins = plugins.map((plugin) => {
      const updated: AllPluginSpec = { args: {}, ...plugin };
      if (plugin.name == "linkButton") {
        updated.args = { ...updated.args, link: experimentUrl };
      }
      return updated;
    });
  }
  return (
    <>
      <Page
        useBackendTheme={false}
        title={title}
        className={className}
        showGradientCircles={showGradientCircles}
      >
        <NarrowLayout>
          {plugins ? (
            <PluginRenderer plugins={plugins as AllPluginSpec[]} />
          ) : (
            // Superfluous fallback
            <Card>
              <Card.Section title="An error occured">
                No plugins were specified, and so this page is empty...
              </Card.Section>
            </Card>
          )}
        </NarrowLayout>
      </Page>
    </>
  );
}

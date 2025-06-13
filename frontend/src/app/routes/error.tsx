import { useRouteError, isRouteErrorResponse } from "react-router-dom";
import { Helmet, HelmetProvider } from "react-helmet-async";
import { ThemeProvider } from "@/theme/ThemeProvider";
import { BaseLayout } from "@/components/layout";
import { View } from "@/components/application";
const helmetContext = {};
export function ErrorPage() {
  const error = useRouteError();
  let message = "An unexpected error occurred.";
  if (isRouteErrorResponse(error)) {
    message =
      `${error.statusText}: ${error.data}` || error.data?.message || message;
  } else if (error instanceof Error) {
    message = error.message;
  }
  return (
    <HelmetProvider context={helmetContext}>
      <ThemeProvider>
        <Helmet>
          <title>Error</title>
        </Helmet>
        <BaseLayout>
          <View name="error" message={message} />
        </BaseLayout>
      </ThemeProvider>
    </HelmetProvider>
  );
}

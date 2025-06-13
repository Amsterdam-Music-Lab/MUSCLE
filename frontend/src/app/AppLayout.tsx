// App.tsx
import { Outlet } from "react-router-dom";
import { ThemeProvider } from "@/theme/ThemeProvider";
import { BaseLayout } from "@/components/layout";
import useDisableRightClickOnTouchDevices from "@/hooks/useDisableRightClickOnTouchDevices";
import useDisableIOSPinchZoomOnTouchDevices from "@/hooks/useDisableIOSPinchZoomOnTouchDevices";
import { Helmet, HelmetProvider } from "react-helmet-async";
const helmetContext = {};

export default function App() {
  // Disable gestures on touch devices
  useDisableRightClickOnTouchDevices();
  useDisableIOSPinchZoomOnTouchDevices();

  return (
    <HelmetProvider context={helmetContext}>
      <ThemeProvider>
        <Helmet>
          <title>MUSCLE</title>
        </Helmet>
        <BaseLayout>
          <Outlet />
        </BaseLayout>
      </ThemeProvider>
    </HelmetProvider>
  );
}

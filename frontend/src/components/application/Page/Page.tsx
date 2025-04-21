import type { HTMLAttributes, ReactNode } from "react";
import classNames from "classnames";
import useBoundStore from "@/util/stores";
import { useTheme } from "@/theme/ThemeProvider";
import AppBar from "@/components/AppBar/AppBar";
import { GradientCircles } from "@/components/svg";
import styles from "./Page.module.scss";

interface PageProps extends HTMLAttributes<HTMLDivElement> {
  className?: string;
  title?: string;
  children?: ReactNode;
  fullwidth?: boolean;
  showAppBar?: boolean;
  showGradientCircles?: boolean;
  showBackgroundImage?: boolean;
}

/**
 * Page is a Page with an AppBar and a width-restricted container for content (if fullwidth=true)
 */
export default function Page({
  className,
  title,
  children,
  showAppBar,
  showGradientCircles,
  showBackgroundImage,
  ...divProps
}: PageProps) {
  const backendTheme = useBoundStore((state) => state.theme);
  const { theme } = useTheme();
  showAppBar = showAppBar ?? theme.showAppBar ?? true;
  showGradientCircles =
    showGradientCircles ?? theme.showGradientCircles ?? true;
  showBackgroundImage =
    showBackgroundImage ?? theme.showBackgroundImage ?? false;

  return (
    <>
      {/* Main page content */}
      <div className={classNames(styles.page, className)} {...divProps}>
        {showAppBar && <AppBar title={title ?? ""} />}
        {children}
      </div>

      {/* Background div */}
      {(showGradientCircles ||
        (showBackgroundImage && backendTheme?.backgroundUrl)) && (
        <div className={styles.bg}>
          {showBackgroundImage && backendTheme?.backgroundUrl && (
            <div
              className={styles.bgImg}
              style={{
                backgroundImage: `url(${backendTheme.backgroundUrl})`,
              }}
            />
          )}
          {showGradientCircles && <GradientCircles blur={50} animate={true} />}
        </div>
      )}
    </>
  );
}

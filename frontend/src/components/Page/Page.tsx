import React from "react";
import useBoundStore from "@/util/stores";
import classNames from "classnames";
import { GradientCircles } from "@/components/svg";

interface PageProps {
  className?: string;
  children: React.ReactNode;
}

/** Page is a single page in the application */
const Page = ({ className, children }: PageProps) => {
  const theme = useBoundStore((state) => state.theme);

  // @BC mark MCG theme as .mcg
  // @BC no default bg '/public/images/background.jpg', instead add .no-background
  const hasBackground = Boolean(theme?.backgroundUrl);

  return (
    <>
      <div
        className={classNames(
          "aha__page",
          className,
          !hasBackground && "no-background",
          theme?.name == "MCG" && "mcg"
        )}
        style={
          !hasBackground
            ? { zIndex: 1 }
            : { backgroundImage: `url(${theme.backgroundUrl})`, zIndex: 1 }
        }
      >
        {children}
      </div>
      {theme?.name == "MCG" && <GradientCircles blur={50} animate={true} />}
    </>
  );
};

export default Page;

import type { HTMLAttributes } from "react";
import { Background } from "../Background";

export interface BaseLayoutProps extends HTMLAttributes<HTMLDivElement> {}

export default function BaseLayout({ children }: BaseLayoutProps) {
  return (
    <div>
      {children}
      <Background />
    </div>
  );
}

import type { IconName, IconProps } from "./icons";
import { iconMap } from "./icons";

export type IconProps = Omit<SVGProps<SVGSVGElement>, "viewBox" | "xmlns">;

export interface GenericIconProps extends Omit<IconProps, "height" | "width"> {
    name: IconName;
    size?: string | number;
}

export default function Icon({
    name,
    size = "1.5em",
    fill = "currentColor",
    ...props
}: GenericIconProps) {
    const IconComponent = iconMap[name];
    if (!IconComponent) return null;
    return <IconComponent width={size} height={size} fill={fill} {...props} />;
}

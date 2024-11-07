import Logo from "@/components/Logo/Logo";

interface AppBarProps {
    title: string;
}

/** AppBar is a bar on top of the app, with navigation and title */
const AppBar = ({ title }: AppBarProps) => (
    <div className="aha__app-bar navbar bg-black">
        <Logo />
        <h4 className="title text-light">{title}</h4>
        <span className="action-right"></span>
    </div>
);
export default AppBar;

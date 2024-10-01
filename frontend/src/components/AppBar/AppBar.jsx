import React from "react";

import Logo from "@/components/Logo/Logo";


// AppBar is a bar on top of the app, with navigation and title
const AppBar = ({ title, }) => {

    return (
        <div className="aha__app-bar navbar bg-black">
            <Logo />
            <h4 className="title text-light">{title}</h4>
            <span className="action-right"></span>
        </div>
    );
};

export default AppBar;

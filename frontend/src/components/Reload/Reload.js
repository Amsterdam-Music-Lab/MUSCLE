import React, { useRef } from "react";

import { useReloadParticipant } from "../../API";

const Reload = () => {
    const [link, reloadLink] = useReloadParticipant(id, hash);

    return (
        <div className="aha__reload">
        </div>
    )
}

export default Reload;
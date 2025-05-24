import { useState } from "react";
import classNames from "classnames";
import { Link, useNavigate } from "react-router-dom";
import * as EmailValidator from "email-validator";
import { URLS } from "@/config";
import useBoundStore from "../../util/stores";
import { shareParticipant } from "../../API";
import { Page } from "@/components/application";
import { Loading } from "@/components/views";
import Participant from "@/types/Participant";

// StoreProfile enables participants to store their profile for later access
const StoreProfile = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");

    const validEmail = email && EmailValidator.validate(email);
    const participant = useBoundStore((state) => state.participant);

    const sendLink = async (participant: Participant) => {

        if (validEmail) {
            const result = await shareParticipant({ email, participant });
            if (!result) {
                alert(
                    "An error occurred while sending the link. Try again later."
                );
            } else {
                alert("You will receive an e-mail shortly");
            }
            navigate(URLS.profile);
        }
    };

    if (!participant) {
        return <Loading />;
    }

    return (
        <Page className="aha__store-profile" title="Store Profile">
            <h3 className="title">Personal Link</h3>
            <p>
                We will send you a personal link by email, which provides access
                to your profile at a later moment or on another system.
            </p>

            <input
                className="mb-3 w-100"
                type="email"
                placeholder="name@example.com"
                required
                value={email}
                onChange={(e) => {
                    setEmail(e.target.value);
                }}
            />

            {/* Buttons */}
            <div className="d-flex justify-content-between">
                {/* Cancel */}
                <Link to={URLS.profile} className="btn btn-gray btn-lg">
                    Cancel
                </Link>

                {/* Send link */}
                <div
                    key={Math.random()}
                    className={classNames("btn btn-primary btn-lg", {
                        disabled: !validEmail,
                    })}
                    onClick={() => sendLink(participant)}
                >
                    Send me the link
                </div>
            </div>
        </Page>
    );
};

export default StoreProfile;

import { Page } from "@/components/application";
import { Loading } from "../Loading";
import { useParticipantScores } from "@/API";
import ProfileView, { ProfileViewProps } from "./ProfileView";

/** Profile loads and shows the profile of a participant for a given experiment */
const Profile = () => {
    // API hooks
    const [data, loadingData] = useParticipantScores<ProfileViewProps>();

    if (loadingData) {
        return <Loading />;
    }

    return (
        <Page title="Profile" className="aha__profile">
            {data ? (
                <ProfileView {...data} />
            ) : (
                <p>
                    An error occurred while
                    <br />
                    loading your profile
                </p>
            )}
        </Page>
    );
};

export default Profile;

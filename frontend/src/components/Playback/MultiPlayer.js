import PlayerSmall from "./PlayButton/PlayerSmall";

const MultiPlayer = ({sections, instructions, config}) => {
    return (
        <div className="aha__multiplayer d-flex justify-content-center">
        {Object.keys(sections).map((index) => (
            <PlayerSmall />
        )}
        </div>
    )
}
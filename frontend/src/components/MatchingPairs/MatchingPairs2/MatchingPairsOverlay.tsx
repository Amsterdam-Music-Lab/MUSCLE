import Overlay from "@/components/Overlay/Overlay";

interface MatchingPairsOverlayProps {}

function MatchingPairsOverlay({}: MatchingPairsOverlayProps) {
  return (
    <>
      <div
        className="matching-pairs__overlay"
        onClick={finishTurn}
        style={{ display: inBetweenTurns ? "block" : "none" }}
        data-testid="overlay"
      />

      <Overlay
        isOpen={tutorialState.isOpen}
        title={tutorialState.title}
        content={tutorialState.content}
        onClose={() => {
          finishTurn();
          setTutorialState({ ...tutorialState, isOpen: false });
        }}
      />
    </>
  );
}

export default MatchingPairsOverlay;

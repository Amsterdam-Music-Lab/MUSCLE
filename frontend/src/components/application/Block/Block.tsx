/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type Session from "@/types/Session";
import type { Action } from "@/types/Action";
import type { Round } from "@/types/Round";

import { useState, useEffect, useCallback, useRef } from "react";
import { useParams } from "react-router-dom";
import classNames from "classnames";

import useResultHandler from "@/hooks/useResultHandler";
import useBoundStore from "@/util/stores";
import { getNextRound, useBlock } from "@/API";
import {
  Trial,
  ErrorView,
  Info,
  ExplainerView,
  FinalView,
  Score,
  Loading,
  Playlists,
} from "@/components/views";
import { FloatingActionButton } from "@/components/ui";
import { UserFeedbackForm } from "@/components/user";

import { Page } from "../Page";
import { PageTransition } from "../PageTransition";
import styles from "./Block.module.scss";

/**
 * Block handles the main (experiment) block flow:
 * - Loads the block and participant
 * - Renders the view based on the state that is provided by the server
 * - It handles sending results to the server
 * - Implements participant_id as URL parameter, e.g. http://localhost:3000/bat?participant_id=johnsmith34
 * Empty URL parameter "participant_id" is the same as no URL parameter at all
 */
const Block = () => {
  const { slug } = useParams();
  const startState = { view: "LOADING" } as Action;
  // Stores
  const setError = useBoundStore((state) => state.setError);
  const participant = useBoundStore((state) => state.participant);
  const setSession = useBoundStore((state) => state.setSession);
  const session = useBoundStore((state) => state.session);
  const theme = useBoundStore((state) => state.theme);
  const setTheme = useBoundStore((state) => state.setTheme);
  const resetTheme = useBoundStore((state) => state.resetTheme);
  const setBlock = useBoundStore((state) => state.setBlock);
  const setCurrentAction = useBoundStore((state) => state.setCurrentAction);

  const setHeadData = useBoundStore((state) => state.setHeadData);
  const resetHeadData = useBoundStore((state) => state.resetHeadData);

  // Current block state
  const [actions, setActions] = useState<Round>([]);
  const [state, setState] = useState<Action | null>(startState);
  const [key, setKey] = useState<number>(Math.random());
  const playlist = useRef(null);

  // API hooks
  const [block, loadingBlock] = useBlock(slug!);

  const loadingText = block ? block.loading_text : "";
  const className = block ? block.class_name : "";

  /** Set new state as spread of current state to force re-render */
  const updateState = useCallback((state: Action) => {
    if (!state) return;

    setState({ ...state });
    setKey(Math.random());
  }, []);

  const updateActions = useCallback(
    (currentActions: Round) => {
      const newActions = currentActions;
      setActions(newActions);
      const newState = newActions.shift();
      const currentAction = newState ? newState : null;
      setCurrentAction({ ...currentAction });
      updateState(newState);
    },
    [updateState, setCurrentAction]
  );

  const continueToNextRound = async (activeSession: Session) => {
    // Try to get next_round data from server
    const round = await getNextRound({
      session: activeSession,
    });
    if (round) {
      updateActions(round.next_round);
    } else {
      setError(
        "An error occured while loading the data, please try to reload the page. (Error: next_round data unavailable)"
      );
      setCurrentAction(null);
      setState(null);
    }
  };

  // trigger next action from next_round array, or call session/next_round
  const onNext = async (doBreak = false) => {
    if (!doBreak && actions.length) {
      updateActions(actions);
    } else {
      continueToNextRound(session as Session);
    }
  };

  // Start first_round when block and partipant have been loaded
  useEffect(() => {
    // Check if done loading
    if (!loadingBlock && participant) {
      // Loading succeeded
      if (block) {
        // Set Helmet Head data
        setHeadData({
          title: block.name,
          description: block.description,
          image: block.image?.file ?? "",
          url: window.location.href,
          structuredData: {
            "@type": "Block",
          },
        });

        setBlock(block);

        if (block.session_id) {
          setSession({ id: block.session_id });
        } else if (!block.session_id && session) {
          setError("Session could not be created");
        }

        continueToNextRound({ id: block.session_id });
      } else {
        // Loading error
        setError("Could not load block");
      }
    }

    // Cleanup
    return () => {
      resetHeadData();
    };
  }, [block, loadingBlock, participant, setError, updateActions]);

  useEffect(() => {
    if (block?.theme) {
      // Set theme if block has theme
      setTheme(block.theme);
    } else if (!block?.theme && theme) {
      // Reset theme if new block has no theme
      resetTheme();
    }
  }, [block, theme, setTheme, resetTheme]);

  const onResult = useResultHandler({
    session,
    participant,
  });

  // Render block state
  const render = () => {
    // Show view, based on the unique view ID:
    switch (state.view) {
      // Block views
      // -------------------------
      case "TRIAL_VIEW":
        return (
          <Trial
            key={key}
            playback={state.playback}
            html={state.html}
            feedback_form={state.feedback_form}
            config={state.config}
            onNext={onNext}
            onResult={onResult}
          />
        );

      // Information & Scoring
      // -------------------------
      case "EXPLAINER":
        return (
          <ExplainerView
            key={key}
            instruction={state.instruction}
            button_label={state.button_label}
            steps={state.steps}
            timer={state.timer}
            onNext={onNext}
          />
        );

      case "SCORE":
        return (
          <Score
            key={key}
            last_song={state.last_song}
            score_meesage={state.score_meesage}
            total_score={state.total_score}
            texts={state.texts}
            icon={state.icon}
            feedback={state.feedback}
            timer={state.timer}
            onNext={onNext}
          />
        );

      case "FINAL":
        return (
          <FinalView
            key={key}
            block={block}
            participant={participant}
            action_texts={state.action_texts}
            button={state.button}
            onNext={onNext}
            show_participant_link={state.show_participant_link}
            participant_id_only={state?.participant_id_only}
            show_profile_link={state.show_profile_link}
            social={state.social}
            feedback_info={state.feedback_info}
            percentile={state.percentile}
            score={state.score}
            totalScore={undefined} // TODO
            timeline={undefined}
            timelineStep={undefined}
            sessions_played={state.sessions_played}
            // plugins={matchingPairsConfig.final.plugins as AllPluginSpec[]}
            // final_text={state.final_text}
            // points={state.points}
          />
        );

      // Generic / helpers
      // -------------------------
      case "PLAYLIST":
        return (
          <Playlists
            key={key}
            playlist={playlist}
            playlists={block?.playlists}
            onSelect={onNext}
            title="Playlists..."
            instruction={state.instruction}
          />
        );

      case "LOADING":
        return <Loading key={key} label={loadingText} />;

      case "INFO":
        return (
          <Info
            key={key}
            html={state?.body}
            title={state?.heading}
            buttonText={state?.button_label}
            buttonLink={state?.button_link}
            onButtonClick={onNext}
          />
        );

      case "REDIRECT":
        window.location.replace(state.url);
        return null;

      case "ERROR":
      case undefined:
      case null:
        return <ErrorView message="No valid state" />;

      default:
        return <ErrorView title="Unknown view">Unknown view: {view}</ErrorView>;
    }
  };

  // Fail safe
  if (!state) {
    setError("No valid state");
  }

  // Also show background fill for feedback forms
  const showBackgroundFill = !(
    state?.view !== "TRIAL_VIEW" || state?.feedback_form !== undefined
  );

  // BC: I've removed the FontLoader as this theme doesn't use fonts
  // in that way anyway.
  // <FontLoader fontUrl={theme?.heading_font_url} fontType="heading" />
  // <FontLoader fontUrl={theme?.body_font_url} fontType="body" />

  return (
    <PageTransition
      transitionKey={state?.view}
      className={classNames(
        styles.block,
        !loadingBlock && block ? "block-" + block.slug : ""
      )}
      data-testid="block-wrapper"
    >
      {!loadingBlock && block ? (
        <Page
          title={state.title}
          className={className}
          showBackgroundFill={showBackgroundFill}
        >
          {render()}

          {block?.feedback_info?.show_float_button && (
            <FloatingActionButton>
              <UserFeedbackForm
                blockSlug={block.slug}
                participant={participant}
                feedbackInfo={block.feedback_info}
                inline={false}
              />
            </FloatingActionButton>
          )}
        </Page>
      ) : (
        <Loading label={loadingText} />
      )}
    </PageTransition>
  );
};

export default Block;

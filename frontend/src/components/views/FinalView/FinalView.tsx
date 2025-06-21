/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ScoreBoardProps } from "@/components/modules/ScoreBoard/ScoreBoard";
import type { AllPluginSpec } from "@/components/plugins/pluginRegistry";

import { useEffect } from "react";
import { routes } from "@/config";
import { finalizeSession } from "@/API";
import useBoundStore from "@/util/stores";
import { Final as FinalAction } from "@/types/Action";
import { PluginRenderer } from "@/components/plugins";
import frontendConfig from "@/config/frontend";

export interface FinalViewProps extends FinalAction, ScoreBoardProps, PluginRendererProps {
    onNext: () => void;
    plugins?: AllPluginSpec[];
}

const DEFAULT_PLUGINS = [
    { name: "scoreboard" },
    { name: "linkButton" },
    { name: "userFeedback" },
] as AllPluginSpec[];

/**
 * Final is a block view that shows the final scores of the block
 * It can only be the last view of a block
 */
export default function FinalView({
    block,
    participant,
    action_texts: userLinkTexts,
    button,
    onNext,
    show_participant_link,
    participant_id_only,
    show_profile_link,
    social: shareConfig,
    feedback_info,
    percentile,
    score: turnScore,
    totalScore,
    timeline,
    timelineStep,
    trophyIcon,
    plugins = frontendConfig?.final?.plugins || DEFAULT_PLUGINS,
    ...pluginRendererProps
}: FinalViewProps) {
    const session = useBoundStore((state) => state.session);
    useEffect(() => {
        finalizeSession({ session: session!, participant });
    }, [session, participant]);

    // Pass data to plugins
    plugins = plugins?.map((plugin) => {
        const updated: AllPluginSpec = { args: {}, ...plugin };
        switch (plugin.name) {
            case "scoreboard":
                updated.args = {
                    ...updated.args,
                    turnScore,
                    totalScore,
                    percentile,
                    timeline,
                    timelineStep,
                    shareConfig,
                    trophyIcon,
                };
                break;

            case "userPages":
                updated.args = {
                    ...updated.args,
                    links: [
                        {
                            link: routes.externalHome(),
                            text: userLinkTexts.all_experiments,
                        },
                        { link: routes.profile(), text: userLinkTexts.profile },
                    ],
                };
                break;

            case "userFeedback":
                updated.args = {
                    ...updated.args,
                    blockSlug: block.slug,
                    participant,
                    // TODO: cannot yet customize this text...
                    feedbackInfo: feedback_info,
                };
                if (!feedback_info) return null;
                break;

            case "participantLink":
                updated.args = {
                    ...updated.args,
                    participantIDOnly: participant_id_only,
                };
                break;

            case "linkButton":
                updated.args = {
                    ...updated.args,
                    link: button.link,
                    onClick: onNext,
                    children: button.text,
                };
                break;
        }

        return updated as AllPluginSpec;
    });

    return <PluginRenderer plugins={plugins as AllPluginSpec[]} {...pluginRendererProps} />;
}

FinalView.viewName = "final";
FinalView.usesOwnLayout = false;
FinalView.getViewProps = ({ block, action, participant, onNext, experiment }) => {
    const timeline = frontendConfig?.tunetwins?.timeline;
    const numSteps = timeline?.symbols.length || 0;
    const sessionsPlayed = experiment.playedSessions || 0;
    const timelineStep = sessionsPlayed % numSteps;
    const symbol = timeline?.symbols[timelineStep - 1] || "dot";
    const trophyIcon = symbol !== "dot" ? symbol : undefined;
    return {
        block,
        participant,
        action_texts: action.action_texts,
        button: action.button,
        onNext,
        show_participant_link: action.show_participant_link,
        participant_id_only: action?.participant_id_only,
        show_profile_link: action.show_profile_link,
        social: action.social,
        feedback_info: action.feedback_info,
        percentile: action.percentile,
        score: action.score,
        totalScore: experiment.accumulatedScore,
        timeline,
        timelineStep,
        trophyIcon,
    };
};
FinalView.dependencies = ["block", "state", "participant", "onNext"];

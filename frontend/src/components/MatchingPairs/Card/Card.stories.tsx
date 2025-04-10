/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import Card from "./Card";

export default {
    title: "Matching Pairs/Card",
    component: Card,
    parameters: {
        layout: "fullscreen",
    },
    tags: ["autodocs"]
};

const decorator = (Story) => (
    <div style={{ width: "256px", height: "256px", padding: "1rem" }}>
        <Story />
    </div>
)

export const Back = {
    args: {},
    decorators: [decorator]
};

export const Front = {
    args: {
        flipped: true,
    },
    decorators: [decorator]
};

export const Disabled = {
    args: {
        disabled: true,
    },
    decorators: [decorator]
};

export const NoEvents = {
    args: {
        noEvents: true,
    },
    decorators: [decorator]
};


const frontStyles = {
    background: "pink", 
    textAlign: "center", 
    display: "flex", 
    justifyContent: "center",
    flexDirection: "column",
}

const backStyles = {
    ...frontStyles,
    background: "#ccc",
}

export const CustomSides = {
    args: {
        children: [
            <Card.Front style={frontStyles}>Front</Card.Front>,
            <Card.Back style={backStyles}>Back</Card.Back>
        ]
    },
    decorators: [decorator]
};

export const RectangularContainer = {
    args: {},
    decorators: [(Story) => (
        <div style={{ width: "150px", height: "300px", padding: "1rem" }}>
            <Story />
        </div>
    )]
}
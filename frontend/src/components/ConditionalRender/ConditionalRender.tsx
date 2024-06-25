import React from 'react';

interface ConditionalRenderProps {
    condition: boolean;
    children?: React.ReactNode;
    fallback?: React.ReactNode;
}

const ConditionalRender = ({ condition, children, fallback }: ConditionalRenderProps) => {
    if (condition) {
        return children;
    }

    return fallback || null;
};

export default ConditionalRender;

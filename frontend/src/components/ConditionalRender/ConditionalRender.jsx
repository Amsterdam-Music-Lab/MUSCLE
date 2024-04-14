import React from 'react';
import PropTypes from 'prop-types';

const ConditionalRender = ({ condition, children, fallback }) => {
    if (condition) {
        return children;
    }

    return fallback || null;
};

ConditionalRender.propTypes = {
    condition: PropTypes.bool.isRequired,
    children: PropTypes.node,
    fallback: PropTypes.node
};

export default ConditionalRender;

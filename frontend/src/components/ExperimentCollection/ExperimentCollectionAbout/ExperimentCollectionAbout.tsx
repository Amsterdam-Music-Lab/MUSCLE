import React from 'react';

interface ExperimentCollectionAboutProps {
    content: string;
}

export const ExperimentCollectionAbout: React.FC<ExperimentCollectionAboutProps> = ({ content = '' }) => {
    return (
        <div className='hero'>
            <div role="contentinfo">
                {content}
            </div>
        </div>
    );
};

export default ExperimentCollectionAbout;
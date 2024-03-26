import React from 'react';

import HTML from '../../HTML/HTML';

interface ExperimentCollectionAboutProps {
    content: string;
}

export const ExperimentCollectionAbout: React.FC<ExperimentCollectionAboutProps> = ({ content = '' }) => {
    return (
        <div className="container">
            <div className="col-12 mt-3">
                <div className="hero">
                    <div role="contentinfo">
                        <HTML body={content} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ExperimentCollectionAbout;
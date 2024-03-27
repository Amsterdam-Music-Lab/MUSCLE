import React from 'react';

import HTML from '../../HTML/HTML';

interface ExperimentCollectionAboutProps {
    content: string;
}

export const ExperimentCollectionAbout: React.FC<ExperimentCollectionAboutProps> = ({ content = '' }) => {
    return (
        <div className="container">
            <div className="col-12 mt-3" role="contentinfo">
                <HTML body={content} innerClassName="prose text-left pb-3 text-white" />
            </div>
        </div>
    );
};

export default ExperimentCollectionAbout;
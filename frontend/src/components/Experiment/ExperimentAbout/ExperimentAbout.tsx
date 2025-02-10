import React from 'react';
import { Link } from 'react-router-dom';
import HTML from '../../HTML/HTML';

interface ExperimentAboutProps {
    content: string;
    slug: string;
    backButtonText: string;
}

export const ExperimentAbout: React.FC<ExperimentAboutProps> = (props: ExperimentAboutProps) => {

    const { content, slug, backButtonText } = props;

    return (
        <div className="container">
            <Link className="btn btn-lg btn-outline-primary mt-3" to={`/${slug}`}>
                <i className="fas fa-arrow-left mr-2"></i>
                {backButtonText}
            </Link>
            <div className="col-12 mt-3" role="contentinfo">
                <HTML body={content} innerClassName="prose text-left pb-3 text-white" />
            </div>
        </div>
    );
};

export default ExperimentAbout;

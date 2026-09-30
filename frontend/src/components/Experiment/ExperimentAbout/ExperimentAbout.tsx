import React from 'react';
import { Link } from 'react-router-dom';
import { css } from '@emotion/react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons'

import HTML from '../../HTML/HTML';
import IExperiment from "@/types/Experiment";
import { styleButtonOutline } from "@/util/stylingHelpers";

export const ExperimentAbout: React.FC<IExperiment> = ({ aboutContent, backButtonText, identifier, theme }) => {

    const styleAboutText = (primaryColor: string) => {
        return css`
            h1, h2, h3 {
                position: relative;
                padding-bottom: 15px;
                margin-bottom: 15px;
                text-align: left;

                &:after {
                    content: "";
                    position: absolute;
                    background-color: ${primaryColor};
                    bottom: -5px;
                    width: 100px;
                    height: 5px;
                }
            }

            blockquote * {
                margin: 50px 30px;
                color: ${primaryColor};
                text-shadow: 0 0 30px ${primaryColor};
        
                @media (max-width: 720px) {
                    margin: 30px 20px;
                }

                &::after {
                    display: none;
                }
            }
        `
    }

    return (
        <div className="container">
            <Link className="btn btn-lg mt-3" css={styleButtonOutline(theme?.colorPrimary || '')} to={`/${identifier}`}>
                <FontAwesomeIcon icon={faArrowLeft} alt="BackButtonIcon"/>
                {backButtonText}
            </Link>
            <div className="col-12 mt-3" role="contentinfo" style={{color: theme?.colorText}} css={styleAboutText(theme?.colorPrimary || '')}>
                <HTML body={aboutContent}  innerClassName="about-text text-left pb-3" />
            </div>
        </div>
    );
};

export default ExperimentAbout;

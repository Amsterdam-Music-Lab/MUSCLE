import React from 'react';
import { Redirect, RouteComponentProps } from 'react-router-dom';

// this component is a route, so it will receive the route props
interface InternalRedirectProps extends RouteComponentProps {}

export const InternalRedirect: React.FC<InternalRedirectProps> = (props) => {
    const { path } = props.match.params as { path: string };
    const { search } = props.location;

    // Redirect to the experiment path
    return <Redirect to={`/${path}${search}`} />;
}
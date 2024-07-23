import React from 'react';
import { RouteComponentProps } from 'react-router-dom';
import Redirect from '@/components/Redirect/Redirect';

// this component is a route, so it will receive the route props
interface InternalRedirectProps extends RouteComponentProps { }

export const InternalRedirect: React.FC<InternalRedirectProps> = (props) => {
    const { path } = props.match.params as { path: string };
    const { search } = props.location;

    // Redirect to the experiment path
    return <Redirect to={`/${path}${search}`} />;
}

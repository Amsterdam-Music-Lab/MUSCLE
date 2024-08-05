import React from 'react';
import { useLocation, useParams } from 'react-router-dom';
import Redirect from '@/components/Redirect/Redirect';

export const InternalRedirect: React.FC = () => {

    const { path } = useParams<{ path: string }>();
    const { search } = useLocation();

    // Redirect to the experiment path
    return <Redirect to={`/${path}${search}`} />;
}

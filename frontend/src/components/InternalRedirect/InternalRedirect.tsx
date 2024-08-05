import React from 'react';
import { useLocation, } from 'react-router-dom';
import Redirect from '@/components/Redirect/Redirect';

export const InternalRedirect: React.FC = () => {

    const location = useLocation();
    const { pathname, search } = location;
    const path = pathname.replace(/^\/redirect\/?/, '');

    // Redirect to the experiment path
    return <Redirect to={`/${path}${search}`} />;
}

import { useEffect } from 'react';
import IExperiment from "@/types/Experiment";
import { DocumentHeadSlice } from '@/util/stores';

const useHeadDataFromExperiment = (experiment: IExperiment | null, setHeadData: DocumentHeadSlice['setHeadData'], resetHeadData: DocumentHeadSlice['resetHeadData']) => {
    useEffect(() => {
        if (experiment) {
            // De-htmlify the description's HTML string
            const descriptionDiv = document.createElement("div");
            descriptionDiv.innerHTML = experiment.description;
            const description = descriptionDiv.textContent || '';

            setHeadData({
                title: experiment.name,
                description: description,
                image: experiment.theme?.logo?.file ?? "/images/aml-logolarge-1200x630.jpg",
                url: window.location.href,
                structuredData: {
                    "@type": "Experiment",
                },
            });
        }

        return () => {
            resetHeadData();
        };
    }, [experiment, setHeadData, resetHeadData]);
};

export default useHeadDataFromExperiment;

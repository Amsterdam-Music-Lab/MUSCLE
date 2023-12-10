import Experiment from '../components/Experiment/Experiment';
import { MemoryRouter, Route } from 'react-router-dom';

export default {
    title: 'Experiment',
    component: Experiment,
    parameters: {
        layout: 'fullscreen',
        // Adding controls for slug and participant_id
        argTypes: {
            slug: {
                control: 'text',
                defaultValue: 'gold-msi',
            },
            participant_id: {
                control: 'text',
                defaultValue: '123',
            }
        }
    },
};

const ExperimentWrapper = ({ slug }) => (
    <Route path="/:slug" render={({ match, location }) => (
        <Experiment match={match} location={location} />
    )} />
);

export const Default = {
    args: {
        slug: 'gold-msi', // Default slug value
        participant_id: '123', // Default participant_id value
    },
    decorators: [
        (Story, context) => (
            <MemoryRouter initialEntries={[`/${context.args.slug}?participant_id=${context.args.participant_id}`]}>
                <div style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                    <Story />
                </div>
            </MemoryRouter>
        ),
    ],
    render: (args) => <ExperimentWrapper {...args} />
};

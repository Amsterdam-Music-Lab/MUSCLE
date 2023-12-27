import UserFeedback from '../components/UserFeedback/UserFeedback';

export default {
    title: 'UserFeedback',
    component: UserFeedback,
    parameters: {
        layout: 'fullscreen',
    },
};

export const Default = {
    args: {
        experimentSlug: 'test',
        participant: 'test',
        feedbackInfo: {
            header: 'Feedback',
            button: 'Submit',
            thank_you: 'Thank you for your feedback!',
            contact_body: '<p>Please contact us at <a href="mailto:info@example.com">info@example.com</a> if you have any questions.</p>'
        }
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#fff', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
};

import UserFeedback from 'components/UserFeedback/UserFeedback';
import FloatingActionButton from '../components/FloatingActionButton/FloatingActionButton';

export default {
    title: 'FloatingActionButton',
    component: FloatingActionButton,
    parameters: {
        layout: 'fullscreen',
    },
};

const userFeedbackProps = {
    experimentSlug: 'test',
    participant: 'test',
    feedbackInfo: {
        header: 'Feedback',
        button: 'Submit',
        thank_you: 'Thank you for your feedback!',
        contact_body: '<p>Please contact us at <a href="mailto:info@example.com">info@example.com</a> if you have any questions.</p>'
    },
    inline: false
}

export const Default = {
    args: {
        children: (
            <UserFeedback {...userFeedbackProps} />
        ),
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#aaa', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
};

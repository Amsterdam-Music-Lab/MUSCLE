import { vi } from 'vitest';

const makeDefaultProps = (overrides = {}) => ({
    last_song: 'Test Song',
    score: 10,
    score_message: 'Great job!',
    total_score: 50,
    texts: { score: 'Score', next: 'Next' },
    icon: 'fa-icon',
    feedback: 'Well done!',
    timer: null,
    onNext: vi.fn(),
    ...overrides,
});

export default makeDefaultProps;

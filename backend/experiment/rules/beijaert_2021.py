import random
from .base import Base
from .views import TwoAlternativeForced, FinalScore, Explainer, Consent, StartSession, Playlist, Question
from .util.questions import next_question, DEMOGRAPHICS
from .util.goldsmiths import MSI_FG_GENERAL, MSI_ALL
from .util.stomp import STOMP20
from .util.tipi import TIPI
from .util.actions import combine_actions


class Beijaert2021(Base):
    """
    MFCC experiment for Beijaert et al., 2021
    """

    ID = 'BEIJAERT_2021'

    @staticmethod
    def first_round(experiment):
        """Create data for the first experiment rounds"""

        # 1. General explainer
        explainer = Explainer.action(
            instruction="How to Participate",
            steps=[
                Explainer.step(
                    description="You will hear a short fragment music that we have processed with audio effects.",
                    number=1),
                Explainer.step(
                    description="For each fragment, you can choose between two labels to describe the music. Don't think too hard: as soon as you have a feeling, click on your choice!",
                    number=2),
                Explainer.step(
                    description="Next, we will ask how sure you were about your answer.",
                    number=3),
                Explainer.step(
                    description="Between songs, there will be some questions about your personal and musical background.",
                    number=4),
                Explainer.step(
                    description="After 30 fragments, you will be finished! The whole experiment should take about 15 minutes."
                )
            ])

        # 2. Consent with default text
        consent = Consent.action(
            """
<p>You will be taking part in a research project conducted by Dr John Ashley Burgoyne of the Music Cognition Group at the University of Amsterdam’s Institute for Logic, Language, and Computation. Before the research project can begin, it is important that you read about the procedures we will be applying. Make sure to read this information carefully.</p>

<h4>Purpose of the research project</h4>

<p>One of the most difficult things to measure about music is its timbre: the overall sound or tone colour of a piece of music outside of its loudness, notes, and rhythms. Many researchers measure timbre using a set of statistics called Mel-frequency cepstral coefficients, or MFCCs for short. We know that two music recordings with very different timbres will usually also have very different MFCCs, but researchers still do not have a good understanding of how specific MFCCs sound. In this experiment, you will hear short audio clips where the MFCCs have been changed in some way, and we will ask you how you would describe these clips (e.g., whether it sounds more like rock or more like heavy metal).</p>

<h4>Who can take part in this research?</h4>

<p>Anybody with sufficiently good hearing, natural or corrected, to enjoy music listening is welcome to participate in this research. Your device must be able to play audio, and you must have a sufficiently strong data connection to be able to stream short MP3 files. Headphones are recommended for the best results, but you may also use either internal or external loudspeakers. You should adjust the volume of your device so that it is comfortable for you.</p>

<h4>Instructions and procedure</h4>

<p>You will hear short fragments of music and two possible labels for describing each fragment. You will also have a slider where you can tell us which label you think describes the music best: e.g., <em>definitely rock</em>, <em>probably rock</em>, <em>possibly rock</em>, <em>not sure</em>, <em>possibly metal</em>, <em>probably metal</em>, or <em>definitely metal</em>.</p>

<p>In between fragments, we will ask you some simple survey questions to better understand your musical background and how you engage with music in your daily life.</p>

<h4>Voluntary participation</h4>

<p>You will be participating in this research project on a voluntary basis. This means you are free to stop taking part at any stage. This will not have any personal consequences and you will not be obliged to finish the procedures described above.</p>

<p>At the end of the experiment, you will be given an anonymous participant code. You can use this code to withdraw your consent. If you decide to withdraw your consent, please contact us with the participant code and state that you are withdrawing your consent to participate. All the information associated with the participant code will be permanently deleted.</p>

<h4>Discomfort, risks, and insurance</h4>

<p>The risks of participating in this research are no greater than in everyday situations at home. Previous experience in similar research has shown that no or hardly any discomfort is to be expected for participants. For all research at the University of Amsterdam, a standard liability insurance applies.</p>

<h4>Confidential treatment of your details</h4>

<p>The information gathered over the course of this research will be used for further analysis and publication in scientific journals only. Fully anonymised data collected during the experiment may be made available online in tandem with these scientific publications. Your personal details will not be used in these publications, and we guarantee that you will remain anonymous under all circumstances.</p>

<h4>Further information</h4>

<p>For further information on the research project, please contact John Ashley Burgoyne (phone number: +31 20 525 7034; e-mail: j.a.burgoyne@uva.nl; Science Park 107, 1098 GE Amsterdam).</p>

<p>If you have any complaints regarding this research project, you can contact the secretary of the Ethics Committee of the Faculty of Humanities of the University of Amsterdam (phone number: +31 20 525 3054; e-mail: commissie-ethiek-fgw@uva.nl; Kloveniersburgwal 48, 1012 CX Amsterdam).</p>

<h4>Informed consent</h4>

<p>I hereby declare that I have been clearly informed about the research project Cognitive Correlates of MFCCs at the University of Amsterdam, Institute for Logic, Language and Computation, conducted by John Ashley Burgoyne as described above.</p>

<p>I consent to participate in this research on an entirely voluntary basis. I retain the right to revoke this consent without having to provide any reasons for my decision. I am aware that I am entitled to discontinue the research at any time and can withdraw my participation up to 8 days after the research has ended. If I decide to stop or withdraw my consent, all the information gathered up until then will be permanently deleted.</p>

<p>If my research results are used in scientific publications or made public in any other way, they will be fully anonymised. My personal information may not be viewed by third parties without my express permission.</p>
            """
        )

        # 3. Choose playlist
        playlist = Playlist.action(experiment.playlists.all())

        # 4. Start session
        start_session = StartSession.action()

        return [
            explainer,
            consent,
            playlist,
            start_session
        ]

    @staticmethod
    def get_random_question(session):
        """Get a random question from each question list, in priority completion order.

        Participants will not continue to the next question set until they
        have completed their current one. Only participants who have participated in
        previous AML experiments will get past general music sophistication.
        """

        # Constantly re-randomising is mildly inefficient, but it's not
        # worth the trouble to save blocked, randomised question lists persistently.

        # 1. Demographic questions (7 questions)
        question = \
            next_question(
                session,
                random.sample(DEMOGRAPHICS, len(DEMOGRAPHICS)),
            )

        # 2. General music sophistication (18 questions)
        if question is None:
            question = \
                next_question(
                    session,
                    random.sample(MSI_FG_GENERAL, len(MSI_FG_GENERAL)),
                )

        # 3. Complete music sophistication (20 questions)
        if question is None:
            # next_question() will skip the FG questions from before
            question = \
                next_question(
                    session,
                    random.sample(MSI_ALL, len(MSI_ALL)),
                )

        # 4. STOMP (20 questions)
        if question is None:
            question = \
                next_question(
                    session,
                    random.sample(STOMP20, len(STOMP20)),
                )

        # 5. TIPI (10 questions)
        if question is None:
            question = \
                next_question(
                    session,
                    random.sample(TIPI, len(TIPI)),
                )

        return question

    @staticmethod
    def next_round(session):
        """Get action data for the next round"""

        # If the number of results equals the number of experiment.rounds
        # Close the session and return data for the final_score view
        if session.rounds_complete():
            # Finish and save session
            session.finish()
            session.final_score = 30
            session.save()

            # Return a dummy final score view
            return combine_actions(
                FinalScore.action(
                    session = session,
                    final_text = "Thank you for participating in our experiment! This one isn't a game, but we'll give you 30 points for every question you answered.",
                    rank = FinalScore.RANKS['SILVER']
                )
            )

        # Prepare an action list
        actions = []

        # Add profile questions starting at round 5
        if session.get_next_round() >= 5:
            actions.append(Beijaert2021.get_random_question(session))

        # Get a section for the next round
        section = Beijaert2021.next_section(session)
        is_flipped = section.tag_id >= 1000
        tag = section.tag_id - 1000 if is_flipped else section.tag_id
        left_label = Beijaert2021.TAGS[tag][0]
        right_label = Beijaert2021.TAGS[tag][1]

        # Add a two-alternative forced choice and certainty question
        actions.append(
            TwoAlternativeForced.action(
                session = session,
                section = section,
                introduction = "Answer whenever you are ready",
                instruction = "Which label fits the music best?",
                ready_message = "",
                ready_time = 0.5,
                decision_time = 10,
                auto_play = True,
                listen_first = False,
                expected_result = right_label if is_flipped else left_label,
                button1_label = left_label,
                button1_color = "blue",
                button2_label = right_label,
                button2_color = "teal",
                auto_advance = False,
                time_pass_break = False
            )
        )

        actions.append(
            Question.text_range(
                key = section.group_id,
                explainer = "Drag the slider to rate your confidence",
                question = "How sure are you about your label choice?",
                choices = [
                    "Definitely " + left_label,
                    "Probably " + left_label,
                    "Possibly " + left_label,
                    "I just guessed",
                    "Possibly " + right_label,
                    "Probably " + right_label,
                    "Definitely " + right_label,
                ],
                view=Question.ID_RESULT_QUESTION
            )
        )

        return combine_actions(*actions)

    @staticmethod
    def next_section(session, filter_by={}):
        """Get next section for given session"""
        section = session.section_from_unused_song(filter_by)
        return section if section else session.section_from_any_song(filter_by)

    # Tag list referenced by external CSV
    TAGS = [
        ("Dance/Electronic", "Hiphop/Jazz/R&B"),
        ("Punk", "Hiphop/Jazz/R&B"),
        ("Heavy Metal", "Punk"),
        ("Heavy Metal", "Hiphop/Jazz/R&B"),
        ("Chillout", "Electronica"),
        ("Electronica", "World/New Age"),
        ("Metal/Hardcore", "Heavy Metal"),
        ("Punk", "Heavy Metal"),
        ("Metal/Hardcore", "Hiphop/Jazz/R&B"),
        ("Dance/Electronic", "Metal/Hardcore"),
        ("Metal/Hardcore", "Soul/Blues/Funk"),
        ("Mellow/Sad", "Folk"),
        ("’80s/New Wave", "Folk"),
        ("Hiphop/Jazz/R&B", "Electronica"),
        ("Pop/Classic Rock", "Hiphop/Jazz/R&B"),
        ("Dance/Electronic", "Chillout"),
        ("Dance/Electronic", "Reggae/Ska"),
        ("Electronica", "Metal/Hardcore"),
        ("Indie/Alternative", "Electronica"),
        ("Hiphop/Jazz/R&B", "Metal/Hardcore"),
        ("’80s/New Wave", "Hiphop/Jazz/R&B"),
        ("Hiphop/Jazz/R&B", "Dance/Electronic"),
        ("Pop/Classic Rock", "Dance/Electronic"),
        ("British/Indie", "Dance/Electronic"),
        ("’80s/New Wave", "Dance/Electronic"),
        ("Catchy/Fun", "Dance/Electronic"),
        ("Latin/Spanish", "Electronica"),
        ("Indie/Alternative", "Folk"),
        ("Electronica", "Folk"),
        ("Heavy Metal", "Folk"),
        ("World/New Age", "Folk"),
        ("Hiphop/Jazz/R&B", "Indie/Alternative"),
        ("Electronica", "Heavy Metal"),
        ("Soul/Blues/Funk", "Electronica"),
        ("Mellow/Sad", "Electronica"),
        ("’80s/New Wave", "Electronica"),
        ("Metal/Hardcore", "Folk"),
        ("Electronica", "Dance/Electronic"),
        ("Rock/Hard Rock", "Electronica"),
        ("Dance/Electronic", "World/New Age"),
        ("World/New Age", "Dance/Electronic"),
        ("Electronica", "Indie/Alternative"),
        ("Experimental Rock/Electronic", "Heavy Metal"),
        ("Heavy Metal", "World/New Age"),
        ("Electronica", "Rock/Hard Rock"),
        ("Heavy Metal", "Electronica"),
        ("Dance/Electronic", "Electronica"),
        ("Heavy Metal", "Metal/Hardcore"),
        ("Experimental Rock/Electronic", "Metal/Hardcore"),
        ("Metal/Hardcore", "Dance/Electronic"),
        ("Latin/Spanish", "Dance/Electronic"),
        ("Heavy Metal", "Experimental Rock/Electronic"),
        ("Indie/Alternative", "Heavy Metal"),
        ("Folk", "Hiphop/Jazz/R&B"),
        ("Electronica", "Chillout"),
        ("Folk", "’80s/New Wave"),
        ("Folk", "Latin/Spanish"),
        ("Chillout", "Dance/Electronic"),
        ("Dance/Electronic", "British/Indie"),
        ("British/Indie", "Electronica"),
        ("Latin/Spanish", "Folk"),
        ("Folk", "British/Indie"),
        ("Heavy Metal", "Indie/Alternative"),
        ("Dance/Electronic", "Heavy Metal"),
        ("Folk", "Indie/Alternative"),
        ("Folk", "Chillout"),
        ("Metal/Hardcore", "Punk"),
        ("’80s/New Wave", "Metal/Hardcore"),
        ("Electronica", "Latin/Spanish"),
        ("Soul/Blues/Funk", "Dance/Electronic"),
        ("Electronica", "Reggae/Ska"),
        ("Punk", "Dance/Electronic"),
        ("Folk", "Mellow/Sad"),
        ("Rock/Hard Rock", "Folk"),
        ("Dance/Electronic", "Latin/Spanish"),
        ("Dance/Electronic", "Folk"),
        ("Punk", "Metal/Hardcore"),
        ("Folk", "Metal/Hardcore"),
        ("Metal/Hardcore", "Electronica"),
        ("Punk", "Electronica"),
        ("Folk", "Electronica"),
        ("Metal/Hardcore", "Experimental Rock/Electronic"),
        ("Hiphop/Jazz/R&B", "Heavy Metal"),
        ("Catchy/Fun", "Heavy Metal"),
        ("Chillout", "Heavy Metal"),
        ("World/New Age", "Heavy Metal"),
        ("Folk", "Heavy Metal"),
        ("Dance/Electronic", "Punk"),
        ("Heavy Metal", "Dance/Electronic"),
        ("Latin/Spanish", "Hiphop/Jazz/R&B"),
        ("Dance/Electronic", "Catchy/Fun"),
        ("Rock/Hard Rock", "Dance/Electronic"),
        ("Experimental Rock/Electronic", "Hiphop/Jazz/R&B"),
        ("Folk", "Catchy/Fun"),
        ("British/Indie", "Heavy Metal"),
        ("Hiphop/Jazz/R&B", "Latin/Spanish"),
        ("Rock/Hard Rock", "Heavy Metal"),
        ("Heavy Metal", "Chillout"),
        ("Electronica", "Soul/Blues/Funk"),
        ("Pop/Classic Rock", "Folk"),
        ("World/New Age", "Hiphop/Jazz/R&B"),
        ("Electronica", "Punk"),
        ("Electronica", "Mellow/Sad"),
        ("Dance/Electronic", "Rock/Hard Rock"),
        ("Folk", "World/New Age"),
        ("Hiphop/Jazz/R&B", "Mellow/Sad"),
        ("Folk", "Dance/Electronic"),
        ("Rock/Hard Rock", "Metal/Hardcore"),
        ("Metal/Hardcore", "World/New Age"),
        ("British/Indie", "Hiphop/Jazz/R&B"),
        ("Electronica", "Hiphop/Jazz/R&B"),
        ("Latin/Spanish", "Heavy Metal"),
        ("Catchy/Fun", "Folk"),
        ("Dance/Electronic", "Soul/Blues/Funk"),
        ("Heavy Metal", "Soul/Blues/Funk"),
        ("Heavy Metal", "Mellow/Sad"),
        ("Heavy Metal", "Latin/Spanish"),
        ("Indie/Alternative", "Hiphop/Jazz/R&B"),
        ("Chillout", "Metal/Hardcore"),
        ("Pop/Classic Rock", "Electronica"),
        ("Electronica", "British/Indie"),
        ("Dance/Electronic", "Mellow/Sad"),
        ("Hiphop/Jazz/R&B", "’80s/New Wave"),
        ("Hiphop/Jazz/R&B", "Reggae/Ska"),
        ("Electronica", "Experimental Rock/Electronic"),
        ("Punk", "Folk"),
        ("Reggae/Ska", "Hiphop/Jazz/R&B"),
        ("Dance/Electronic", "Indie/Alternative"),
        ("Reggae/Ska", "Heavy Metal"),
        ("Chillout", "Hiphop/Jazz/R&B"),
        ("Hiphop/Jazz/R&B", "World/New Age"),
        ("Hiphop/Jazz/R&B", "Punk"),
        ("Catchy/Fun", "Electronica"),
        ("Mellow/Sad", "Hiphop/Jazz/R&B"),
        ("Metal/Hardcore", "Latin/Spanish"),
        ("Experimental Rock/Electronic", "Folk"),
        ("Latin/Spanish", "Metal/Hardcore"),
        ("World/New Age", "Electronica")
    ]

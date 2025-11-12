# Playback and player widgets

The `Trial` object may also contain a `Playback` object, which can refer to one of the following player widgets:

- Autoplay (plays and optionally shows an animation)
- PlayButton (starts audio on click)
- ImagePlayer (a special case of PlayButton, can show an image aligned with the button)
- MultiPlayer (multiple PlayButtons)
- MatchingPairs (showing PlayButtons as cards, and perform special logic every time the user selects a "pair")

## Initalizing a Playback object
An example of how a `Playback` object is initalized in the Python backend:
```python
playback = PlayButton(
   [section]
)
```
The only required argument for `Playback` objects is an array of audio sections. For `Autoplay`, `PlayButton` and `ImagePlay`, the first (and only) section in the array is used automatically. For `MultiPlayer` and `MatchingPairs`, the participant can control which section is being played by interacting with buttons or cards.

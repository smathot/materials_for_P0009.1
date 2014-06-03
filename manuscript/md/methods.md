## Participants, software, and apparatus

Seventeen naive observers (9 women; age range 19-24 years) participated in the experiment. Participants provided written informed consent. The experiment was conducted with approval of the Aix-Marseille Université ethics committee. The right eye was recorded with an EyeLink 1000 (SR Research, Mississauga, Canada, ON), a video-based eye tracker sampling at 1000 Hz. Stimuli were presented on a 21" ViewSonic pf227f CRT monitor (1024 x 768 px, 100 Hz) with OpenSesame [@MathSchreij2012] / PsychoPy [@Peirce2007]. Data, materials, and supplementary analyses are available from
<https://github.com/smathot/materials_for_P0009.1>.

## Stimuli and procedure

%--
figure:
 id: FigParadigm
 source: FigParadigm.svg
 caption: Schematic experimental paradigm. This example demonstrates a valid cue-bright trial, because the movement cue appeared on the bright side of the display and correctly predicted the location of the target. The exact duration of the adaptation period depended on the duration of the drift correction procedure. The upwards arrow indicates the motion direction of the cue.
--%

Before the experiment, a nine-point eye-tracker calibration was performed. At trial start, the display was divided into a bright (88.5 cd/m2) and a dark half (0.2 cd/m2), separated by a central luminance gradient (10.0° wide). Participants were instructed to fixate a blue central fixation dot throughout the trial. Two horizontally oriented Gabor patches were presented 10° to the left and right of the center. After an adaptation period of 1250 ms, an automatic one-point recalibration ('drift correction') was performed. From this point onwards, the luminance gradient was locked to horizontal gaze position by a continuous gaze-contingent algorithm. This ascertained that the eyes were always centered exactly in between the bright and dark sides. After 1250 ms, one Gabor patch (the cue) changed phase for 50 ms. This gave the appearance of a sudden upwards motion and attracted attention. After a stimulus-onset asynchrony (SOA) of 100, 1000, or 2500 ms relative to cue onset, both Gabor patches changed orientation. One patch (the distractor) changed to a vertical orientation. The other patch (the target) was tilted 45° clockwise or counterclockwise from a vertical orientation. After 50 ms, both stimuli were masked with random-noise patches. Participants indicated the orientation of the target as quickly and accurately as possible by pressing the left (for counterclockwise) or right (for clockwise) button on a response box. The trial ended when a button was pressed or when a timeout occurred after 3000 ms.

Cue validity (50% valid, 50% invalid), SOA (25% 100 ms, 25% 1000 ms, 50% 2500 ms), and brightness of the cued side (50% Bright, 50% Dark) were mixed within blocks. Because only the 2500 ms SOA provided a sufficiently long 'uncontaminated' interval for the pupil-trace analysis, this SOA occurred on half the trials. The experiment consisted of one practice block, followed by 16 experimental blocks (512 trials), and took approximately two hours.

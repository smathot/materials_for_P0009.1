## Materials and availability

Data, materials, and analysis scripts are available from <https://github.com/smathot/materials_for_P0009.1>.

## Participants, software, and apparatus

Seventeen naive observers (9 women; age range 19-24 years) participated in the experiment. Participants provided written informed consent. The experiment was conducted with approval of the Aix-Marseille Université ethics committee. The right eye was recorded with an EyeLink 1000 (SR Research, Mississauga, Canada, ON), a video-based eye tracker sampling at 1000 Hz. Stimuli were presented on a 21" ViewSonic p227f CRT monitor (1024 x 768 px, 100 Hz) with OpenSesame [@MathSchreij2012] / PsychoPy [@Peirce2007].

## Stimuli and procedure

%--
figure:
 id: FigParadigm
 source: FigParadigm.svg
 caption: Schematic experimental paradigm. This example demonstrates a Valid Bright-Side-Cued trial, because the movement cue appeared on the bright side of the display and correctly predicted the location of the target. The exact duration of the adaptation period depended on the duration of the drift-correction procedure. The upwards arrow indicates the motion direction of the cue.
--%

Before the experiment, a nine-point eye-tracker calibration was performed. At the start of the trial, the display was divided into a bright (88.5 cd/m2) and a dark half (0.2 cd/m2), separated by a central luminance gradient (10.0° wide). Participants were instructed to fixate a blue central fixation dot throughout the trial. Two horizontally oriented Gabor patches (*σ* = 0.63°, *sf* = 0.85 cycles/°, 100% contrast, 30% opacity) were presented 10° to the left and right of the center. After an adaptation period of 1250 ms, an automatic one-point recalibration ('drift correction') was performed. From this point onwards, the luminance gradient was locked to horizontal gaze position by a gaze-contingent algorithm. ++The display was updated every 10 ms, using up-to-date gaze-position information. This retinal-stabilization procedure ascertained that gaze was always centered exactly in between the bright and dark sides, and kept visual stimulation constant, even when participants made fixational eye movements.++ After another adaptation period of 1250 ms, one Gabor patch (the cue) changed phase for 50 ms. This gave the appearance of a sudden upwards motion. The cue served to capture attention, but did not predict the location of the target. After a stimulus-onset asynchrony (SOA) of 100, 1000, or 2500 ms relative to cue onset, both Gabor patches changed orientation. One patch (the distractor) changed to a vertical orientation. The other patch (the target) was tilted 45° clockwise or counterclockwise from a vertical orientation. After 50 ms, both stimuli were masked with random-noise patches with the same size, average brightness, and opacity as the Gabor patches. Participants indicated the orientation of the target as quickly and accurately as possible by pressing the left (for counterclockwise) or right (for clockwise) button on a response box. The trial ended when a button was pressed or when a timeout occurred after 3000 ms.

Cue validity (50% valid, 50% invalid), SOA (25% 100 ms, 25% 1000 ms, 50% 2500 ms), and brightness of the cued side (50% bright, 50% dark) were mixed within blocks. ++Because only the 2500 ms SOA provided a sufficiently long 'uncontaminated' interval for the pupil-trace analysis, this SOA occurred on half of the trials, and is the focus of our main analyses.++ The experiment consisted of one practice block, followed by 16 experimental blocks (512 trials), and lasted approximately two hours.

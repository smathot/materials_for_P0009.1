## Significance and trial-exclusion criteria

For the correlation analyses, we used a significance threshold of p < .05, for the linear mixed-effects analyses we used t > 2 [cf. @BaayenDavidsonBates2008]. An additional criterion for the pupil-trace analysis was that t > 2 for at least 200 consecutive samples [cf. @Mathôt2013Plos]. Trials were excluded when, at any point after cue onset and before feedback, participants fixated more than 2.9° from the left or right of the horizontal display center (4.9%). No other filtering criteria were applied. No participants were excluded. 8278 trials were entered into the analysis.

## Behavioral results

We conducted a linear mixed-effects analysis with SOA (continuous: 100, 1000, 2500 ms) and Cue Validity (valid, invalid) as fixed effects, participant as random effect on the intercept, and accuracy as dependent measure (see %FigBehavior). This revealed marginal main effects of Cue Validity (t = 1.71) and SOA (t = 1.51), and a reliable Cue-Validity by SOA interaction (t = 2.47). The same analysis using inverse response time (1/RT) as dependent measure [we used inversion as an alternative to outlier removal, cf. @Ratcliff1993] revealed a similar pattern of results: A marginal main effect of Cue Validity (t = 1.27), a reliable main effect of SOA (t = 3.68), and a reliable Cue-Validity by SOA interaction (t = 2.51). In summary, the behavioral results showed the classic bi-phasic pattern of facilitation at the short cue-target interval, followed by IOR at longer cue-target intervals.

%--
figure:
 id: FigBehavior
 source: FigBehavior.svg
 caption: |
  Accuracy (a) and response time (b) as a function of Cue Validity and SOA. Error bars indicate standard errors. b) Data points are based on the grand mean of the inverse response time, as described in the main text.
--%

## Pupil-trace analysis

We analyzed pupil surface during the cue-target epoch, relative to a baseline period 100 ms prior to the cue onset. Blinks where reconstructed using cubic-spline interpolation [@Mathôt2013Blinks]. We analyzed only the 2500 ms SOA, which provides a large temporal window during which pupil size can be analyzed. For each 1 ms sample separately, we conducted an LME with Cued-Side-Brightness (Bright, Dark) as fixed effect, participant as random effect on the intercept, and pupil size as dependent measure.

%--
figure:
 id: FigPupilTrace
 source: FigPupilTrace.svg
 caption: |
  Pupil size as a function of Cued-Side-Brightness and time since cue onset, in the 2500 ms SOA. Error shadings indicate standard errors. The green shading indicates pupillary facilitation. The red shading indicates pupillary inhibition. Blue shadings indicate cue and target presentation.
--%

As shown in %FigPupilTrace, from 476 to 893 ms after cue onset, the pupil was smaller when the bright side, relative to the dark side of the display is cued (from now on: pupillary facilitation). This pattern reversed significantly from 1054 to 1316 ms after cue onset (from now on: pupillary inhibition), although the reversal qualitatively persisted until the end of the trial.

## Reliability and correlation analyses

In general, there is considerable between-subject variability in IOR [e.g., @TheeuwesMathôtGrainger2014Object]. This was apparent in our data as well, in both behavior and pupil size. To test whether these individual differences were reliable, we randomly split the data (2500 ms SOA only; ±128 trials per participant in each subset) in two subsets and determined the correlation between the cuing effects in both subsets. We repeated this procedure 10,000 times to create a bootstrap estimate of the correlation (i.e. the split-half reliability) and the probability of obtaining a positive correlation. For the cuing effect based on accuracy this gave r = .71, *P*(r > 0) = .99. For the cuing effect based on RT this gave r = .46, *P*(r > 0) = .98. We conducted the same analysis for pupillary inhibition, i.e. the difference in pupil size between Cued-Side-Bright and Cued-Side-Dark trials for the sample at which overall pupillary inhibition was largest (cf. %FigCorrelation::b). This gave r = .41, *P*(r > 0) = .99.

Finally, we tested whether pupillary inhibition was related to behavioral IOR. We quantified behavioral IOR (for the 2500 ms SOA) for each participant and for both accuracy and response times. We also quantified pupillary inhibition for each participant and each 1 ms sample. Next, we determined the correlation between pupillary inhibition and behavioral IOR, separately for accuracy and RT and for each 1 ms sample. This analysis resulted in two 'correlation traces', which are shown in %FigCorrelation.

%--
figure:
 id: FigCorrelation
 source: FigCorrelation.svg
 caption: |
  a) Correlation between the pupillary cuing effect and the behavioral cuing effect (based on accuracy and response times) for the 2500 ms SOA, as a function of time since cue onset. The gray shading indicates a significant correlation based on accuracy. b) Individual data points for the strongest correlation, observed for accuracy at 1852 ms post-cue.
--%

The correlation between pupillary inhibition and behavioral IOR was strong and reliable (%FigCorrelation::a) during the interval at which overall pupillary inhibition was observed. An identical, but weaker correlation was was observed for behavioral IOR based on RTs.

To summarize, individual differences in the strength of behavioral IOR and pupillary inhibition were highly reliable. Moreover, behavioral IOR and pupillary inhibition are closely correlated.

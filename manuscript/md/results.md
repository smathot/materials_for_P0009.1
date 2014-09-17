## Significance and trial-exclusion criteria

For the individual-differences and correlation analyses, we used a significance threshold of p < .05. For the linear mixed-effects (LME) analyses we used t > 2. This is comparable to a p < .05 threshold [@BaayenDavidsonBates2008]. However, in light of recent concerns about p-value estimation for LME models, we have omitted explicit p-values. For the pupil-trace analysis, we considered only sequences of at least 200 consecutive samples where t > 2 to be significant [cf. @Mathôt2013Plos]. ++For the correlation-trace analysis, we considered only sequences of at least 200 consecutive data points where p < .05 to be significant.++ Trials were excluded when, at any point after cue onset and before feedback, participants fixated more than 2.9° from the left or right of the horizontal display center (4.9%). No other filtering criteria were applied. No participants were excluded. In total, 8278 trials (95.1%) were entered into the analysis.

## Behavioral results

We conducted an LME analysis with SOA (continuous: 100, 1000, 2500 ms) and Cue Validity (valid, invalid) as fixed effects, participant as random effect on the intercept, and accuracy as dependent measure (see %FigBehavior). This revealed marginal main effects of Cue Validity (t = 1.71) and SOA (t = 1.51), and a reliable Cue-Validity by SOA interaction (t = 2.47). The same analysis using inverse response time (1/RT) as dependent measure [we used inversion as an objective alternative to outlier removal, cf. @Ratcliff1993] revealed a similar pattern of results: A marginal main effect of Cue Validity (t = 1.27), a reliable main effect of SOA (t = 3.68), and a reliable Cue-Validity by SOA interaction (t = 2.51). Separate analyses, as above but with only Cue Validity as fixed effect, showed facilitation at the 100 ms SOA (accuracy: t = 3.20; 1/RT: t = 8.67) and IOR at the combined 1000 and 2500 ms SOAs (accuracy: t = 2.36; 1/RT: t = 2.31). In summary, the behavioral results showed the classic bi-phasic pattern of facilitation at the short SOA, followed by IOR at longer SOAs.

%--
figure:
 id: FigBehavior
 source: FigBehavior.svg
 caption: |
  Accuracy (a) and response time (b) as a function of Cue Validity and SOA. Error bars indicate standard errors. Where not shown, error bars are smaller than symbols. b) Data points are based on the grand mean of the inverse response time, consistent with the analysis described in the main text.
--%

## Pupil-trace analysis

We analyzed pupil surface during the cue-target epoch, relative to a baseline period 100 ms prior to the cue onset [cf. @Mathôt2013Plos]. Blinks were reconstructed using cubic-spline interpolation [@Mathôt2013Blinks]. No other filtering or smoothing procedures were applied. ++Our main analyses focus on the 2500 ms SOA, which provides a large temporal window during which pupil size can be analyzed. (See Appendix for additional analyses.)++ For each 1 ms sample separately, we conducted an LME with Cued-Side-Brightness (Bright, Dark) as fixed effect, participant as random effect on the intercept, and pupil size as dependent measure.

%--
figure:
 id: FigPupilTrace
 source: FigPupilTrace.svg
 caption: |
  Pupil size as a function of Cued-Side-Brightness and time since cue onset (grey and orange lines), and the difference in pupil size between Cue-on-Dark and Cue-on-Bright trials (pupillary cuing effect; blue line). Data from the 2500 ms SOA. Pupil size is shown as a proportion of baseline size during the 100 ms prior to cue onset. Error shadings indicate standard errors. Green shading indicates pupillary facilitation. Red shading indicates pupillary inhibition. Blue shadings indicate cue (0-50 ms) and target (2500-2550 ms) presentation. Data reflects the unsmoothed grand mean signal.
--%

++The presentation of the cue triggered a fast, overall dilation, which reflects an orienting response [@WangBoehnke2012]. In addition, there was a slow dilation that persisted until the end of the trial and reflects steadily increasing arousal. For our purpose, pupil dilation relative to the start of the trial is not informative, because it does not contain spatial information: It tells you that the participant paid attention to something, but not where in space attention was directed. Therefore, we focus on the difference in pupil size between Cue-on-Bright and Cue-on-Dark trials, which does contain spatial information: This pupil-size difference reflects whether attention was (mostly) directed at the cued or the uncued side of the display, and is shown as the 'pupillary cuing effect' in %FigPupilTrace [see @Binda2013JNeurosci;@Mathôt2013Plos;@Mathôt2014JExpPsy for a similar logic].++

From 476 to 893 ms after cue onset, the pupil was smaller when the bright side, relative to the dark side of the display was cued (from now on: pupillary facilitation). This effect peaked after 665 ms, and in absolute terms corresponded to a relative 2.8% pupil-area decrease. ++This is comparable to that observed for endogenous cuing [@Mathôt2013Plos], but much smaller than the pupil-area decrease that results from direct fixation [under similar conditions; @Mathôt2014JExpPsy].++ This pattern reversed significantly from 1054 to 1316 ms after cue onset (from now on: pupillary inhibition), reaching a relative peak pupil-area increase of 1.0% after 1126 ms. ++Pupillary inhibition qualitatively persisted until the end of the trial.++

## Individual differences and correlation analyses

In general, there is considerable between-subject variability in IOR [e.g., @TheeuwesMathôtGrainger2014Object]. This was apparent in our data as well. However, rather than assume that these individual differences reflected measurement noise, we tested their reliability and used them to link pupil size to behavior.

First, to test the reliability of the individual differences, we randomly split the data in two subsets and determined the correlation between the strength of behavioral IOR in both subsets (2500 ms SOA only; ±128 trials per participant in each subset). We repeated this procedure 10,000 times to create bootstrap estimates and 95% confidence intervals for the correlation (i.e. the split-half reliability). For behavioral IOR based on accuracy this gave r = .71 (.49 - .88). For behavioral IOR based on RTs this gave r = .46 (.02 - .79). We conducted the same analysis for pupillary inhibition, i.e. the difference in pupil size between Cued-Side-Bright and Cued-Side-Dark trials for the sample at which overall pupillary inhibition was largest (cf. %FigCorrelation::b). This gave r = .41 (.05 - .72).

Finally, we tested whether pupillary inhibition was related to behavioral IOR. We quantified behavioral IOR (for the 2500 ms SOA) for each participant and for both accuracy and RTs. We also quantified pupillary inhibition for each participant and for each 1 ms sample. Next, we determined correlations between pupillary inhibition and behavioral IOR, separately for accuracy and RT and for each 1 ms sample. This analysis resulted in two 'correlation traces', shown in %FigCorrelation.

%--
figure:
 id: FigCorrelation
 source: FigCorrelation.svg
 caption: |
  a) Correlation between pupillary inhibition and behavioral IOR (based on accuracy and response times) for the 2500 ms SOA, as a function of time since cue onset. The gray shading indicates a significant correlation based on accuracy. b) Individual data points for the strongest correlation, observed for accuracy at 1852 ms post-cue. Dots in the red area indicate participants that show both pupillary inhibition and behavioral IOR. Dots in the green area indicate participants that show (sustained) pupillary facilitation and behavioral facilitation.
--%

The correlation between pupillary inhibition and behavioral IOR based on accuracy was reliable from 817 ms post-cue until target presentation, i.e. roughly during the interval at which overall pupillary inhibition was observed (%FigCorrelation::a). An identical, but less reliable correlation was observed between pupillary inhibition and behavioral IOR based on RTs. ++Correlation traces for the other SOAs are included in the Appendix. (As visible in %FigCorrelation::b, one participant showed particularly strong behavioral IOR and pupillary inhibition. To check whether the behavior-pupil correlations were not driven by 'outliers', we conducted the same analysis, but excluded, for every correlation,  participants for which the behavioral and/ or pupillary cuing effect deviated more than 2 *SD* from the mean. This analysis also revealed reliable correlations that peaked at approximately the same time.)++

To summarize, individual differences in the strength of behavioral IOR and pupillary inhibition were reliable. Moreover, participants who showed strong pupillary inhibition showed strong behavioral IOR, and vice versa.


# What is the Optimal Number of Trials

<details>

<summary>Convenience functions (click to see the code)</summary>

<p>

``` r
library(tidyverse)
library(easystats)
## # Attaching packages (red = needs update)
## <U+2714> insight     0.6.0        <U+2714> bayestestR  0.4.0     
## <U+26A0> performance 0.3.0.9000   <U+2714> parameters  0.2.5     
## <U+2714> see         0.2.1.9000   <U+2714> effectsize  0.0.1     
## <U+2714> correlation 0.1.0        <U+2714> estimate    0.1.0     
## <U+2714> report      0.1.0        
## Restart the R-Session and update packages in red with 'easystats::easystats_update()'.
library(cowplot)

compute_cumulative <- function(data, fun = mean, col = "RT"){
  cumu <- c()
  for(i in 1:nrow(data)){
    cumu <- c(cumu,
              fun(data[1:i, col], na.rm = TRUE))
  }
  cumu
}

cumulative_data <- function(data){
  data$Cumulative_Mean <- compute_cumulative(data, fun = mean)
  data$Cumulative_SD <- compute_cumulative(data, fun = sd)
  data$Cumulative_CI_high <- data$Cumulative_Mean + data$Cumulative_SD * 1.96
  data$Cumulative_CI_low <- data$Cumulative_Mean - data$Cumulative_SD * 1.96

  data$Change_Mean <- c(NA, tail(data$Cumulative_Mean, -1) - head(data$Cumulative_Mean, -1))
  data$Change_SD <- c(NA, tail(data$Cumulative_SD, -1) - head(data$Cumulative_SD, -1))
  data[c("Participant", "Task", "Trial_Order",
         "Cumulative_Mean", "Cumulative_SD", "Cumulative_CI_high", "Cumulative_CI_low",
         "Change_Mean", "Change_SD")]
}
```

</p>

</details>

## Reaction Time

### Task 1: Simple Reaction Time

<details>

<summary>See code</summary>

<p>

``` r
df <- data.frame()
for(path in list.files(path = "data/", pattern = "*_ProcessingSpeed.csv", full.names = TRUE)){
  df <- rbind(df, cumulative_data(read.csv(path)))
}

fig1 <- cowplot::plot_grid(
  df %>%
    ggplot(aes(x = Trial_Order, y = Cumulative_Mean)) +
    geom_vline(xintercept = 50, linetype = "dotted") +
    geom_ribbon(aes(ymin = Cumulative_CI_low, ymax = Cumulative_CI_high, fill = Participant), alpha = 0.1) +
    geom_line(aes(color = Participant), size = 1) +
    theme_modern() +
    scale_color_viridis_d(guide = FALSE) +
    scale_fill_viridis_d(guide = FALSE),
  cowplot::plot_grid(df %>%
    ggplot(aes(x = Trial_Order, y = Change_Mean)) +
    geom_vline(xintercept = 50, linetype = "dotted") +
    geom_hline(yintercept = 0) +
    geom_line(aes(color = Participant), size = 1) +
    theme_modern() +
    scale_color_viridis_d(guide = FALSE),
  df %>%
    ggplot(aes(x = Trial_Order, y = Change_SD)) +
    geom_vline(xintercept = 50, linetype = "dotted") +
    geom_hline(yintercept = 0) +
    geom_line(aes(color = Participant), size = 1) +
    theme_modern() +
    scale_color_viridis_d(guide = FALSE)),
  nrow = 2
)
```

</p>

</details>

![](figures/unnamed-chunk-4-1.png)<!-- -->

### Task 2: Response Selection

<details>

<summary>See code</summary>

<p>

``` r
df <- data.frame()
for(path in list.files(path = "data/", pattern = "*_ResponseSelection.csv", full.names = TRUE)){
  df <- rbind(df, cumulative_data(read.csv(path)))
}

fig2 <- cowplot::plot_grid(
  df %>%
    ggplot(aes(x = Trial_Order, y = Cumulative_Mean)) +
    geom_vline(xintercept = 60, linetype = "dotted") +
    geom_ribbon(aes(ymin = Cumulative_CI_low, ymax = Cumulative_CI_high, fill = Participant), alpha = 0.1) +
    geom_line(aes(color = Participant), size = 1) +
    theme_modern() +
    scale_color_viridis_d(guide = FALSE) +
    scale_fill_viridis_d(guide = FALSE),
  cowplot::plot_grid(df %>%
    ggplot(aes(x = Trial_Order, y = Change_Mean)) +
    geom_vline(xintercept = 60, linetype = "dotted") +
    geom_hline(yintercept = 0) +
    geom_line(aes(color = Participant), size = 1) +
    theme_modern() +
    scale_color_viridis_d(guide = FALSE),
  df %>%
    ggplot(aes(x = Trial_Order, y = Change_SD)) +
    geom_vline(xintercept = 60, linetype = "dotted") +
    geom_hline(yintercept = 0) +
    geom_line(aes(color = Participant), size = 1) +
    theme_modern() +
    scale_color_viridis_d(guide = FALSE)),
  nrow = 2
)
```

</p>

</details>

![](figures/unnamed-chunk-6-1.png)<!-- -->

### Task 4: Conflict Resolution

<details>

<summary>See code</summary>

<p>

``` r
df <- data.frame()
for(path in list.files(path = "data/", pattern = "*_ConflictResolution_2.csv", full.names = TRUE)){
  dat <- read.csv(path)
  cong <- cumulative_data(dat[dat$Congruence == "CONGRUENT", ])
  cong$Conflict <- FALSE
  incong <- cumulative_data(dat[dat$Congruence != "CONGRUENT", ])
  incong$Conflict <- TRUE
  df <- rbind(df, rbind(cong, incong))
}

fig3 <- cowplot::plot_grid(
  df %>%
    ggplot(aes(x = Trial_Order, y = Cumulative_Mean)) +
    geom_vline(xintercept = 120, linetype = "dotted") +
    geom_ribbon(aes(ymin = Cumulative_CI_low, ymax = Cumulative_CI_high, fill = Participant), alpha = 0.1) +
    geom_line(aes(color = Participant), size = 1) +
    theme_modern() +
    scale_color_viridis_d(guide = FALSE) +
    scale_fill_viridis_d(guide = FALSE) +
    facet_grid(~Conflict, labeller = "label_both") +
    coord_cartesian(ylim = c(100, 1000)),
  cowplot::plot_grid(df %>%
    ggplot(aes(x = Trial_Order, y = Change_Mean)) +
    geom_vline(xintercept = 120, linetype = "dotted") +
    geom_hline(yintercept = 0) +
    geom_line(aes(color = Participant), size = 1) +
    theme_modern() +
    scale_color_viridis_d(guide = FALSE) +
    facet_grid(~Conflict, labeller = "label_both") +
    coord_cartesian(ylim = c(-200, 100)),
  df %>%
    ggplot(aes(x = Trial_Order, y = Change_SD)) +
    geom_vline(xintercept = 120, linetype = "dotted") +
    geom_hline(yintercept = 0) +
    geom_line(aes(color = Participant), size = 1) +
    theme_modern() +
    scale_color_viridis_d(guide = FALSE) +
    facet_grid(~Conflict, labeller = "label_both") +
    coord_cartesian(ylim = c(-100, 100))),
  nrow = 2
)
```

</p>

</details>

![](figures/unnamed-chunk-8-1.png)<!-- -->

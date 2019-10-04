library(ggplot2)
library(gridExtra)
library(plyr)
library(latex2exp)
library(tikzDevice)


drawScatter <- function(fname, sname){
  data <- read.csv(fname, sep = '\t', header = TRUE)
  
  #data$abruptness_prob <- scale(data$abruptness, scale = TRUE, center = TRUE)
  
  #cdat <- ddply(data, "genre", summarise, m=mean(branchiness))
  
  #print(cdat)
  #print(data)
  
  p1 <- ggplot(data)
  p1 <- p1 + geom_jitter(aes(x=abruptness_note, y=abruptness_freq, color=genre))
  #p1 <- p1 + geom_density(alpha=0.25, adjust=2, size=1)
  #p1 <- p1 + geom_line(stat='density', size=1)
  #p1 <- p1 + geom_vline(data=cdat, aes(xintercept=m, color=genre), linetype='dashed', show.legend = FALSE, size=1)
  p1 <- p1 + theme_classic()
  #p1 <- p1 + scale_x_sqrt()
  #p1 <- p1 + scale_x_log10()
  #p1 <- p1 + coord_cartesian(xlim=c(10,10000))
  #p1 <- p1 + xlim(1, 10000)
  p1 <- p1 + scale_color_brewer(palette="Set2") + scale_fill_brewer(palette="Set2")
  #p1 <- p1 + xlim(-2.5,2.5)
  #p1 <- p1 + theme(legend.position="none") + labs(fill='',color='') + xlab('Abruptness (Frequency)') + ylab('Density')
  
  #tikz(file = sname, width = 4, height = 2.5, standAlone = TRUE)
  #print(p1)
  #dev.off()
  
  return(p1)
}


drawDistribution <- function(fname, sname){
  data <- read.csv(fname, sep = '\t', header = TRUE)
  
  #data$abruptness_prob <- scale(data$abruptness, scale = TRUE, center = TRUE)

  cdat <- ddply(data, "genre", summarise, m=mean(pitch_edge))
  
  print(cdat)
  #print(data)
  
  p1 <- ggplot(data, aes(x=pitch_edge,  color=genre, fill=genre))
  #p1 <- p1 + geom_density(alpha=0.25, adjust=2, size=1)
  p1 <- p1 + geom_line(stat='density', size=1, adjust=1.5)
  p1 <- p1 + geom_vline(data=cdat, aes(xintercept=m, color=genre), linetype='dashed', show.legend = FALSE, size=1)
  p1 <- p1 + theme_classic()
  #p1 <- p1 + scale_x_sqrt()
  #p1 <- p1 + scale_x_log10()
  #p1 <- p1 + coord_cartesian(xlim=c(10,10000))
  p1 <- p1 + xlim(0, 20)
  p1 <- p1 + scale_color_brewer(palette="Set1") + scale_fill_brewer(palette="Set1")
  #p1 <- p1 + xlim(-2.5,2.5)
  p1 <- p1 + theme(legend.position="bottom") + labs(fill='',color='') + xlab('Pitch Range across Edge') + ylab('Density')
  
  tikz(file = sname, width = 4, height = 2.5, standAlone = TRUE)
  print(p1)
  dev.off()
  
  return(p1)
}

plotClassificationAccuracy <- function(fname, sname) {
  data <- read.csv(fname, sep = '\t', header = TRUE)
  data <- data[which(data$classifier == 'MLP'),]
  
  pl <- ggplot(data)
  pl <- pl + geom_bar(aes(x=classes, y=accuracy_mean, fill=method),stat="identity", position=position_dodge())
  pl <- pl + geom_errorbar(aes(ymin=accuracy_mean-accuracy_std, ymax=accuracy_mean+accuracy_std, x=classes, group=method), width=.5, position=position_dodge(.9)) 
  pl <- pl + coord_cartesian(ylim=c(0.45,1.0))
  pl <- pl + theme_minimal()
  pl <- pl + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  #pl <- pl + guides(fill=FALSE) 
  pl <- pl + xlab('') + ylab('Accuracy') + ylim(0,1.0)
  pl <- pl + theme(axis.text.x = element_text(size=12, face='bold'), axis.text.y = element_text(size=12, face='bold'), axis.title.y = element_text(size=12))
  pl <- pl + theme(legend.position="bottom") + labs(fill='')
  
  tikz(file = sname, width = 4, height = 2.5, standAlone = TRUE)
  print(pl)
  dev.off()
  
  return(pl)
}
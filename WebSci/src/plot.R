library(ggplot2)
library(gridExtra)
library(plyr)
library(latex2exp)
library(tikzDevice)

drawDistribution <- function(fname, sname){
  data <- read.csv(fname, sep = '\t', header = TRUE)
  cdat <- ddply(data, "genre", summarise, m=mean(melodic_mean))
  
  pl <- ggplot(data, aes(x=melodic_mean, color=genre))
  pl <- pl + geom_density()
  pl <- pl + geom_vline(data=cdat, aes(xintercept=m, color=genre), linetype='dashed', size=1)
  pl <- pl + theme_bw()
  #pl <- pl + scale_x_sqrt()
  pl <- pl + scale_color_brewer(palette="Set2")
  pl <- pl + theme(legend.position="bottom") + labs(fill='',color='') + xlab('Melodic') + ylab('Density')
  
  tikz(file = sname, width = 5, height = 3, standAlone = TRUE)
  print(pl)
  dev.off()
  
  return(pl)
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
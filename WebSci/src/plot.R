library(ggplot2)
library(gridExtra)
library(plyr)
library(latex2exp)
library(tikzDevice)
library(Rmisc) 


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


drawRepeatedness <- function(fname) {
  data <- read.csv(fname, sep = '\t', header = TRUE)
  
  sdata <- summarySE(data, measurevar="variance", groupvars=c("l","genre"))
  print(sdata)
  
  p0 <- ggplot(sdata) + theme_classic()
  p0 <- p0 + geom_errorbar(aes(x=factor(l), ymin=variance-sd, ymax=variance+sd, color=genre), size=1, width=0.3)
  p0 <- p0 + geom_point(aes(x=factor(l), y=variance, color=genre), size=1)
  p0 <- p0 + geom_line(aes(x=l, y=variance, color=genre), size=1)
  #p0 <- p0 + geom_boxplot(aes(x=factor(l),y=variance,  color=genre), outlier.shape = NA, width=0.7, size=1)
  #p0 <- p0 + scale_y_log10()
  #p0 <- p0 + geom_jitter(aes(x=l, y=variance, color=genre))
  #p0 <- p0 + geom_smooth(aes(x=l, y=variance, color=genre))
  #p0 <- p0 + coord_cartesian(ylim=c(1e-8,1e-1))
  
  return(p0)
  
  
  l <- summarySE(data, measurevar="len", groupvars=c("supp","dose"))
  
  p1 <- ggplot(data) + theme_classic()
  #p1 <- p1 + geom_jitter(aes(x=l, y=skewness, color=genre))
  p1 <- p1 + geom_boxplot(aes(x=factor(l),y=skewness,  color=genre), outlier.shape=NA, width=0.7, size=1)
  p1 <- p1 + scale_y_log10()
  p1 <- p1 + coord_cartesian(ylim=c(0.1,1e2))
  
  return(p0)
}


drawDistribution <- function(fname, sname){
  data0 <- read.csv(fname, sep = '\t', header = TRUE)
  
  cdat0 <- ddply(data0, "genre", summarise, m=median(repeatedness, na.rm = TRUE))
  
  print(cdat0)
  
  p0 <- ggplot(data0, aes(x=repeatedness,  color=genre, fill=genre))
  p0 <- p0 + geom_line(stat='density', size=1, adjust=1.5)
  p0 <- p0 + geom_vline(data=cdat0, aes(xintercept=m, color=genre), linetype='dashed', show.legend = FALSE, size=1)
  p0 <- p0 + theme_classic()
  #p1 <- p1 + scale_x_sqrt()
  p0 <- p0 + scale_x_log10()
  p0 <- p0 + coord_cartesian(xlim=c(1e-8,1))
  #p0 <- p0 + xlim(0, 12.5)
  p0 <- p0 + theme(text = element_text(size=8))
  p0 <- p0 + scale_color_brewer(palette="Set1") + scale_fill_brewer(palette="Set1")
  p0 <- p0 + theme(legend.position="none") + labs(fill='',color='') + xlab('Repeatedness') + ylab('Density')
  
  tikz(file = sname, width = 3, height = 2, standAlone = TRUE)
  print(p0)
  dev.off()
  
  return(p0)
}

plotPCA <- function(fname, sname) {
  data <- read.csv(fname, sep = '\t', header = TRUE)
  
  #data <- data[which(data$genre %in% c('CLASSICAL','POP','JAZZ')),]
  
  p0 <- ggplot(data, aes(x=pc0, y=pc1, color=genre)) + theme_classic()
  p0 <- p0 + geom_point(alpha=0.1) 
  p0 <- p0 + stat_ellipse(type='t',level = 0.67, size=1, linetype=1)
  p0 <- p0 + xlab('Principal Component 0') + ylab('Principal Component 1') + theme(legend.position="right")
  p0 <- p0 + labs(color='') + theme(legend.text=element_text(size=8))
  p0 <- p0 + xlim(-4,4) + ylim(-2,2.5)
  p0 <- p0 + scale_color_brewer(palette="Set1") + scale_fill_brewer(palette="Set1")
  
  #p1 <- ggplot(data, aes(x=pc1, y=pc2, color=genre)) + theme_classic()
  #p1 <- p1 + geom_point(alpha=0.1) 
  #p1 <- p1 + stat_ellipse(type='t',level = 0.67, size=1, linetype=1)
  #p1 <- p1 + xlab('Principal Component 1') + ylab('Principal Component 2') + theme(legend.position="none")
  #p1 <- p1 + scale_color_brewer(palette="Set1") + scale_fill_brewer(palette="Set1")
  
  #p2 <- ggplot(data, aes(x=pc2, y=pc0, color=genre)) + theme_classic()
  #p2 <- p2 + geom_point(alpha=0.1) 
  #p2 <- p2 + stat_ellipse(type='t',level = 0.67, size=1, linetype=1)
  #p2 <- p2 + xlab('Principal Component 2') + ylab('Principal Component 0') + theme(legend.position="none")
  #p2 <- p2 + scale_color_brewer(palette="Set1") + scale_fill_brewer(palette="Set1")
  
  
  legend <- get_legend(p0)
  p0 <- p0 + theme(legend.position = 'none')
  #p0 <- p0 + stat_ellipse(type='t',level = 0.95, size=1, linetype=2)
  #pl <- pl + stat_ellipse(type='norm',level = 0.67, linetype=2)
  #pl <- pl + scale_color_gradientn(colours = c("white", "black" ,"black"), values = c(0, 0.25, 1))
  
  pl <- grid.arrange(p0, legend, nrow=1, widths=c(2, 0.8))
  
  tikz(file = sname, width = 4, height = 2.5, standAlone = TRUE)
  print(grid.arrange(p0, legend, nrow=, widths=c(2, 0.8)))
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

plotClassificationAUC <- function(fname, sname){
  data <- read.csv(fname, sep = '\t', header = TRUE)
  #data$g0 <- factor(data$g0, levels=c('MOZART','BACH','VIVALDI','BEATLES'))
  #data$g1 <- factor(data$g1, levels=c('BACH','VIVALDI','BEATLES','NIRVANA'))
  
  pl <- ggplot(data = data, aes(y=auc_m, ymin=auc_m-auc_s, ymax=auc_m+auc_s, x=clf, color=fea, fill=fea)) 
  pl <- pl + theme_bw()
  #pl <- pl + geom_point(position = 'dodge')
  pl <- pl + geom_errorbar(position = "dodge", width=0.5, size=1)
  #pl <- pl + geom_bar(stat='identity', color='white', position = "dodge", width = 0.6)
  #pl <- pl + coord_cartesian(ylim=c(0.5,1.0))
  pl <- pl + facet_grid(g0 ~ g1, scales = "free_y") + theme(legend.position="bottom")
  pl <- pl + scale_color_brewer(palette="Set1") + scale_fill_brewer(palette="Set1") 
  pl <- pl + labs(color='', fill='') + xlab('Classifier') + ylab('AUC ROC')
  pl <- pl + theme( strip.background = element_blank())
  
  
  tikz(file = sname, width = 8, height = 8, standAlone = TRUE)
  print(pl)
  dev.off()
  
  return(pl)
}
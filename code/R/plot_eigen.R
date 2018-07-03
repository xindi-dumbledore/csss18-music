library(tidyverse)
library(igraph)

## theme for plotting

mytheme <- theme_bw() + theme(
                            legend.title  = element_text( size=17),
                                        #  legend.position = "bottom",
                                        #	legend.direction = "horizontal",
                            legend.key = element_blank(),
                            legend.text  = element_text( size=17),
                            panel.background = element_blank(),
                            panel.grid = element_blank(),
                            text = element_text( family="Helvetica", size=19),
                            panel.border = element_rect( colour = "black", size=2.5),
                            axis.ticks = element_line(size = 2.),
                            strip.background = element_rect( fill = "transparent", size = 2.5, colour = "black"  ),
                            strip.text = element_text(size = 19)
                        )



## get networks
dir <- "../../HON/network_nopause"
Data_networks <- map(list.files(dir), function(f){
    print(f)
    network <- read.graph(paste(c(dir, f), collapse = "/"), format = c("gml"))
    A <- as.matrix(as_adjacency_matrix(network, attr = 'weight'))
    p <- rowSums(A)
    D <- diag(0, nrow(A), nrow(A))
    diag(D) <- ifelse( p > 0, 1/p, 1)
    A <- D %*% A
    diag(A) <- 1 - rowSums(A)
    e <- eigen(A, only.values = TRUE)$values
    n <- length(e)
    e <- e
    splits <- str_split(f, " ")[[1]]
    type <- splits[1]
    comp <- splits[2]
    data_frame(evals_r= Re(e), evals_i = Im(e), name = f, size = n, composer = comp, type = type)
}) %>% bind_rows()

## subset of "representative" networks

data_plot <- Data_networks %>% filter(name %in% c('Metal_Rock midi g green_day Jesus_Of_Suburbia_9-network.gml',
                                                  'Classical_Greatest Mozart Piano Sonatas Piano Sonata n02 K280_4-network.gml',
                                                  'Classical_Greatest Beethoven Piano Concerto n1 op15 3mov_8-network.gml'))



data_plot$name <- factor(data_plot$name)
levels(data_plot$name) <- c("Beethoven Piano Concerto 1", "Mozart K280", "GD Jesus of Suburbia")


## get elliptic law expectation

dir <- "../../HON/network_nopause"
Data_evals_expectation <- map(list.files(dir), function(f){
    print(f)
    network <- read.graph(paste(c(dir, f), collapse = "/"), format = c("gml"))
    A <- as.matrix(as_adjacency_matrix(network, attr = 'weight'))
    n <- nrow(A)
    if (n > 50) {

        p <- rowSums(A)
        D <- diag(0, nrow(A), nrow(A))
        diag(D) <- ifelse( p > 0, 1/p, 1)
        A <- D %*% A
        diag(A) <- 1 - rowSums(A)
        dm <- mean(diag(A))
        L <- c(A[upper.tri(A)], A[lower.tri(A)])
        sd2 <- var(L)
        mu <- mean(c(A[upper.tri(A)], A[lower.tri(A)]))
        p <- cor(A[upper.tri(A)], t(A)[upper.tri(A)])

        xlim <- sqrt(sd2 * nrow(A)) * (1 + p)
        xseq <- seq(-xlim, xlim, length = 500)
        yseq <- (1-p)  * sqrt(sd2*nrow(A) - (xseq/(1+p))^2)
        yseq[is.na(yseq)] <- 0
        splits <- str_split(f, " ")[[1]]
        type <- splits[1]
        comp <- splits[2]
        data_frame(evals_r= c(xseq,rev(xseq)), evals_i = c(yseq,-yseq), name = f, size = nrow(A), composer = comp, type = type)
    }
    else{
        NULL}

}) %>% bind_rows()



data_plot_expectation <- Data_evals_expectation  %>% filter(name %in% c('Metal_Rock midi g green_day Jesus_Of_Suburbia_9-network.gml',
                                                  'Classical_Greatest Mozart Piano Sonatas Piano Sonata n02 K280_4-network.gml',
                                                  'Classical_Greatest Beethoven Piano Concerto n1 op15 3mov_8-network.gml'))


data_plot_expectation$name <- factor(data_plot_expectation$name)
levels(data_plot_expectation$name) <- c("Beethoven Piano Concerto 1", "Mozart K280", "GD Jesus of Suburbia")



## plotting

plot_eigen <- data_plot %>% ggplot(aes(x = evals_r, y = evals_i)) +  facet_wrap(~name, ) + coord_fixed() + mytheme  + geom_point(size = 2.) + xlab(expression(Re(lambda))) + ylab(expression(Im(lambda))) + geom_path(data = data_plot_expectation, linetype = "dashed")

ggsave("eigenvalues_comparisons.pdf", plot_eigen, width = 13)

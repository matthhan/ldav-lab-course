data <- read.csv("res.csv")
data %>% count(X0)  %>% ggplot() + aes(X0,n) + geom_line() + scale_y_log10() + xlim(0,100)

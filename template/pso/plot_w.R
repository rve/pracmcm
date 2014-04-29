d=read.table("test.out", header=F, sep=" ") 
png(filename="./fig4.png", height=600, width=600, bg="white")
plot(0,0,type="l", xlim=c(1,2000), ylim=c(50,500),xlab="iteration", ylab="fitness")

len = 5
cl = rainbow(len)
names <- vector()
for (i in 1:len) {
  d1 <- subset(d, V2==i*5/10.0)
  lines(d1$V3, d1$V4, col=cl[i], type="l")
  names <- c(names, sprintf("c=%f", i*5/10))
}
legend("topright", inset=.05, names, lty=c(1,1), lwd=c(2.5,2.5),col=cl)
dev.off()

dds <- function(OBJFUN, xBounds.df, numIter,iniPar=NA, r = 0.2, ...){
  # Format xBounds.df colnames
  colnames(xBounds.df) <- c("min", "max")
  # Generate initial first guess
  #xBounds.df<-data.frame(col1 = rep(10,10), col2=rep(100, 10))
  if (is.na(iniPar[1])){  # identification of initial parameters
    x_init <- apply(xBounds.df, 1, function(x) runif(1, x[1], x[2]))
  }else{
    x_init <- as.numeric(iniPar)
  }
  
  x_best <- data.frame(x = x_init)
  x_test <- data.frame(x = x_init)
  
  # Evaluate first cost function
  y_init <- OBJFUN(x_init, ...)
  y_test <- y_init
  y_best <- y_init
  
  # Select which entry to peturb at each iteration
  xDims <- nrow(xBounds.df)
  Prob <- matrix(1 - log(1:numIter) / log(numIter), ncol = 1) # Returns numIter length list of entries to be peturbed
  peturbIdx <- apply(t(apply(Prob,1, function(x) as.logical(rbinom(xDims, 1, x)))), 1, which)
  # identify where it is not changing any parameter and assign one ramdomly
  Correct.Peturb <- which(unlist(lapply(peturbIdx,sum)) == 0)
  peturbIdx[Correct.Peturb] <- sample(1:xDims, length(Correct.Peturb), replace = TRUE)
  
  # Peturb each entry by N(0,1)*r(x_max - x_min) reflecting if @ boundaries
  sigma <- xBounds.df$max - xBounds.df$min
  
  pb1 <- txtProgressBar(style = 3)
  for(i in 2:numIter){
    setTxtProgressBar(pb1, i/numIter, title = paste(i/numIter,"% of Calibration"))
    # Set up test x
    x_test[ ,i] <- as.matrix(x_best)
    # Get entries we will peturb
    idx <- peturbIdx[[i]]
    # Initialize vector of peturbations initially zeros with same length of x so we will add this vector to peturb x
    peturbVec <- rep(0, nrow(x_test[ ,i]))
    # Generate the required number of random normal variables
    N <- rnorm(nrow(x_test[,i]), mean = 0, sd = 1)
    # Set up vector of peturbations
    peturbVec[idx] <- r * N[idx] * sigma[idx]
    # Temporary resulting x value if we peturbed it
    x_test[,i] <- x_test[,i] + peturbVec  
    # Find the values in testPeturb that have boundary violations.
    B.Vio.min.Idx <- which(x_test[ ,i] < xBounds.df$min)
    B.Vio.max.Idx <- which(x_test[ ,i] > xBounds.df$max)
    # Correct them by mirroring set them to the minimum or maximum values
    x_test[B.Vio.min.Idx,i] <- xBounds.df$min[B.Vio.min.Idx] + (xBounds.df$min[B.Vio.min.Idx] - x_test[B.Vio.min.Idx, i])
    set.min <- B.Vio.min.Idx[x_test[B.Vio.min.Idx, i] > xBounds.df$max[B.Vio.min.Idx]]  # which are still out of bound
    x_test[set.min, i] <- xBounds.df$min[set.min]
    x_test[B.Vio.max.Idx,i] <- xBounds.df$max[B.Vio.max.Idx] - (x_test[B.Vio.max.Idx,i] - xBounds.df$max[B.Vio.max.Idx])
    set.max <- B.Vio.max.Idx[x_test[B.Vio.max.Idx,i] < xBounds.df$min[B.Vio.max.Idx]]
    x_test[set.max, i]<- xBounds.df$max[set.max]
    
    # Evaluate objective function
    y_test[i] <- OBJFUN(x_test[ ,i], ...)
    y_best <- min(c(y_test[i], y_best))
    bestIdx <- which.min(c(y_test[i], y_best))
    x_choices <- cbind(x_test[ ,i], as.matrix(x_best))
    x_best <- x_choices[ ,bestIdx]
  }
  close(pb1)
  output.list <- list(X_BEST = t(x_best), Y_BEST = y_best, X_TEST = t(x_test), Y_TEST = y_test)
  return(output.list)
}

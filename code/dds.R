dds <- function(fitness, x_Min, x_Max, x_Init = NA, max_iter = 100, r = 0.2, ...){
  ## S.1 Set initial parameters ####
  if (is.na(x_Init)) x_Init <- (x_Min + x_Max) / 2
  
  x_Best <- x_Init
  
  ## S.2 Evaluate initial ####
  y_Init <- fitness(x_Init, ...)
  y_Best <- y_Init
  
  ## S.3 Select peturb J of the D decision
  n_x <- length(x_Min)
  P_i <- 1 - log(1:max_iter) / log(max_iter)
  randm_Para <- apply(as.matrix(P_i), 1, function(x) as.logical(rbinom(n_x, 1, x)))
  idx_null <- which(colSums(randm_Para) == 0)
  idx_new4null <- sample(1:n_x, length(idx_null), replace = T)
  randm_Para[idx_new4null, idx_null] <- TRUE
  lst_Cali_x <- apply(randm_Para, 2, which)
  
  ## S.4 Peturb each entry by N(0,1)*r(x_max - x_min) reflecting 
  sigma_ <- x_Max - x_Min
  
  bar_progress <- txtProgressBar(style = 3)
  for(i in 2:max_iter){
    setTxtProgressBar(bar_progress, i/max_iter, title = paste(i/max_iter,"% of Calibration"))
    
    x_New <- x_Best
    idx <- lst_Cali_x[[i]]
    N_01 <- rnorm(n_x)
    x_New0 <- (x_Best + r * N_01 * sigma_)
    x_New1 <- maxVector(2 * x_Min - x_New0, x_Min)
    x_New2 <- minVector(2 * x_Max - x_New0, x_Max)
    x_New0[x_New0 < x_Min] <- x_New1[x_New0 < x_Min]
    x_New0[x_New0 > x_Max] <- x_New2[x_New0 > x_Max]
    x_New[idx] <- x_New0[idx]
    ## S.5 Evaluate objective function
    y_New <- fitness(x_New, ...)
    if(y_New < y_Best){
      x_Best <- x_New
      y_Best <- y_New
    }
  }
  close(bar_progress)
  return(list(x_Best = x_Best, y_Best = y_Best))
}


#' Finding the minimum value of the corresponding position of two equal large vectors
#' @param VctA vector, numic, first Vector
#' @param VctB vector, numic, second Vector
#' @return vector, result
#' @examples
#' A = c(1, 2, 3)
#' B = c(2, 2, 2)
#' minVector(A, B)
#' @export
minVector <- function(VctA, VctB){
  VctC = VctA - VctB
  VctD = VctB
  VctD[which(VctC < 0.0)] = VctA[which(VctC < 0.0)]
  return(VctD)
}


#' Finding the maximum value of the corresponding position of two equal large vectors
#'
#' @param VctA vector, numic, first Vector
#' @param VctB vector, numic, second Vector
#' @return vector, result
#' @examples
#' A = c(1, 2, 3)
#' B = c(2, 2, 2)
#' maxVector(A, B)
#' @export
maxVector <- function(VctA, VctB){
  VctC = VctA - VctB
  VctD = VctA
  VctD[which(VctC < 0.0)] = VctB[which(VctC < 0.0)]
  return(VctD)
}

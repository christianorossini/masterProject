library(irr)


### OVERAL AGREEMENT
path = "/mnt/d/Christiano/Documentos/dissertation/projeto/experiment/csv_evaluation_matrix/"
df_dt <- read.csv(paste(path,"overall_agreement_eval_matrix_DT.csv",sep=''),header = FALSE)
df_noDt <- read.csv(paste(path,"overall_agreement_eval_matrix_noDT.csv",sep=''),header = FALSE)

print("### DT")
kappam.fleiss(df_dt)               # Fleiss' Kappa
#kappam.fleiss(diagnoses, exact=TRUE)   # Exact Kappa
#kappam.fleiss(diagnoses, detail=TRUE)  # Fleiss' and category-wise Kappa
#kappam.fleiss(diagnoses[,1:4])         # Fleiss' Kappa of raters 1 to 4
print("### NO DT")
kappam.fleiss(df_noDt)



### ACADEMY AGREEMENT
df_dt <- read.csv(paste(path,"academy_agreement_eval_matrix_DT.csv",sep=''),header = FALSE)
df_noDt <- read.csv(paste(path,"academy_agreement_eval_matrix_noDT.csv",sep=''),header = FALSE)

print("### DT")
kappam.fleiss(df_dt)  
print("### noDT")
kappam.fleiss(df_noDt)


### BOTH: ACADEMY AND INDUSTRY AGREEMENT
df_dt <- read.csv(paste(path,"both_agreement_eval_matrix_DT.csv",sep=''),header = FALSE)
df_noDt <- read.csv(paste(path,"both_agreement_eval_matrix_noDT.csv",sep=''),header = FALSE)

print("### DT")
kappam.fleiss(df_dt)  
print("### noDT")
kappam.fleiss(df_noDt)


### EXPERIENCE: SMELL DETECTION
df_dt <- read.csv(paste(path,"sdetection_agreement_eval_matrix_DT.csv",sep=''),header = FALSE)
df_noDt <- read.csv(paste(path,"sdetection_agreement_eval_matrix_noDT.csv",sep=''),header = FALSE)

print("### DT")
kappam.fleiss(df_dt)  
print("### noDT")
kappam.fleiss(df_noDt)
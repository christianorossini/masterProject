library(irr)


### OVERAL AGREEMENT
path = "/mnt/d/Christiano/Documentos/dissertation/projeto/experiment/csv_evaluation_matrix/"
df_p1_dt <- read.csv(paste(path,"overall_agreement_eval_matrix_p1_dt.csv",sep=''),header = FALSE)
df_p2_dt <- read.csv(paste(path,"overall_agreement_eval_matrix_p2_dt.csv",sep=''),header = FALSE)
df_p1_noDt <- read.csv(paste(path,"overall_agreement_eval_matrix_p1_noDT.csv",sep=''),header = FALSE)
df_p2_noDt <- read.csv(paste(path,"overall_agreement_eval_matrix_p2_noDT.csv",sep=''),header = FALSE)

print("### p1 DT")
kappam.fleiss(df_p1_dt)               # Fleiss' Kappa
print("### p2 DT")
kappam.fleiss(df_p2_dt)               # Fleiss' Kappa
print("### p1 no DT")
kappam.fleiss(df_p1_noDt)               # Fleiss' Kappa
print("### p2 no DT")
kappam.fleiss(df_p2_noDt)               # Fleiss' Kappa

#kappam.fleiss(diagnoses, exact=TRUE)   # Exact Kappa
#kappam.fleiss(diagnoses, detail=TRUE)  # Fleiss' and category-wise Kappa
#kappam.fleiss(diagnoses[,1:4])         # Fleiss' Kappa of raters 1 to 4



### ACADEMY AGREEMENT
df_p1_dt <- read.csv(paste(path,"academy_agreement_eval_matrix_p1_dt.csv",sep=''),header = FALSE)
df_p2_dt <- read.csv(paste(path,"academy_agreement_eval_matrix_p2_dt.csv",sep=''),header = FALSE)
df_p1_noDt <- read.csv(paste(path,"academy_agreement_eval_matrix_p1_noDT.csv",sep=''),header = FALSE)
df_p2_noDt <- read.csv(paste(path,"academy_agreement_eval_matrix_p2_noDT.csv",sep=''),header = FALSE)

print("### p1 DT")
kappam.fleiss(df_p1_dt)               # Fleiss' Kappa
print("### p2 DT")
kappam.fleiss(df_p2_dt)               # Fleiss' Kappa
print("### p1 no DT")
kappam.fleiss(df_p1_noDt)               # Fleiss' Kappa
print("### p2 no DT")
kappam.fleiss(df_p2_noDt)               # Fleiss' Kappa


### BOTH: ACADEMY AND INDUSTRY AGREEMENT
df_dt <- read.csv(paste(path,"both_agreement_eval_matrix_DT.csv",sep=''),header = FALSE)
df_noDt <- read.csv(paste(path,"both_agreement_eval_matrix_noDT.csv",sep=''),header = FALSE)

print("### DT")
kappam.fleiss(df_dt)  
print("### noDT")
kappam.fleiss(df_noDt)


### EXPERIENCE: SMELL DETECTION
df_p1_dt <- read.csv(paste(path,"csDetection_agreement_eval_matrix_p1_dt.csv",sep=''),header = FALSE)
df_p2_dt <- read.csv(paste(path,"csDetection_agreement_eval_matrix_p2_dt.csv",sep=''),header = FALSE)
df_p1_noDt <- read.csv(paste(path,"csDetection_agreement_eval_matrix_p1_noDT.csv",sep=''),header = FALSE)
df_p2_noDt <- read.csv(paste(path,"csDetection_agreement_eval_matrix_p2_noDT.csv",sep=''),header = FALSE)

print("### p1 DT")
kappam.fleiss(df_p1_dt)               # Fleiss' Kappa
print("### p2 DT")
kappam.fleiss(df_p2_dt)               # Fleiss' Kappa
print("### p1 no DT")
kappam.fleiss(df_p1_noDt)               # Fleiss' Kappa
print("### p2 no DT")
kappam.fleiss(df_p2_noDt)               # Fleiss' Kappa

### EXPERIENCE: JAVA Lenguage
df_p1_dt <- read.csv(paste(path,"java_agreement_eval_matrix_p1_dt.csv",sep=''),header = FALSE)
df_p2_dt <- read.csv(paste(path,"java_agreement_eval_matrix_p2_dt.csv",sep=''),header = FALSE)
df_p1_noDt <- read.csv(paste(path,"java_agreement_eval_matrix_p1_noDT.csv",sep=''),header = FALSE)
df_p2_noDt <- read.csv(paste(path,"java_agreement_eval_matrix_p2_noDT.csv",sep=''),header = FALSE)

print("### p1 DT")
kappam.fleiss(df_p1_dt)               # Fleiss' Kappa
print("### p2 DT")
kappam.fleiss(df_p2_dt)               # Fleiss' Kappa
print("### p1 no DT")
kappam.fleiss(df_p1_noDt)               # Fleiss' Kappa
print("### p2 no DT")
kappam.fleiss(df_p2_noDt)               # Fleiss' Kappa
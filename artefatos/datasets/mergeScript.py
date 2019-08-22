import pandas as pd
import numpy as np
from pandas.io.common import EmptyDataError
import os
from sklearn.utils import resample

## PROJETOS QUE ESTÃO SENDO UTILIZADOS NO ESTUDO
ant = pd.Series(["ant","apache-ant-data","apache_1.8.3"])
cassandra = pd.Series(["cassandra","apache-cassandra","apache-cassandra-1.1"])
eclipse = pd.Series(["eclipse.jdt.core","eclipse-data","org.eclipse.jdt.core_3.6.1_OK"])
elasticSearch = pd.Series(["elasticsearch","elastic-search-data","elasticsearch-elasticsearch-0.19_OK"])
hadoop = pd.Series(["hadoop","apache-hadoop-data","pat2mongo-hadoop-0.9_OK"])
hbase = pd.Series(["hbase","apache-hbase-data","optimistdk-hbase-0.94_OK"])
lucene = pd.Series(["lucene","apache-lucene","blueshen-lucene-solr-3.6_OK"])
nutch = pd.Series(["nutch","apache-nutch-data","danielfagerstrom-nutch-1.4_OK"])
pig = pd.Series(["pig","apache-pig-data","cloudera-pig-0.8_OK"])
qpid = pd.Series(["qpid","apache-qpid-data","dekellum-qpid-0.18_OK"])
hive = pd.Series(["hive","apache-hive-data","itisaid-hive-0.9_OK"])
ivy = pd.Series(["ivy","apache-ivy-data","ivy_2.1.0_OK"])
karaf = pd.Series(["karaf","apache-karaf-data","apache-karaf-2.3"])
wicket = pd.Series(["wicket","apache-wicket-data","l0rdn1kk0n-wicket-1.4.20_OK"])
xerces = pd.Series(["xerces","apache-xerces-data","xerces-2.3.0_OK"])

## ADICIONAR OS PROJETOS NA PRÓXIMA LINHA
projects = pd.DataFrame([ant, cassandra, eclipse, elasticSearch, hadoop, hbase, lucene, nutch, pig, qpid, hive, ivy, karaf, wicket, xerces])
projects.columns = columns=["name","validatedPjDir","validatedPjVersion"]
                  
#TIPOS DE CODE SMELLS ESTUDADOS
gc = pd.Series(["godClass","candidate_Large_Class.csv","gc", "class"])
cdsbp = pd.Series(["classDataShouldBePrivate","candidate_Class_Data_Should_Be_Private.csv","cdsbp","class"])
lm = pd.Series(["longMethod","candidate_Long_Methods.csv","lm","method"])
lpl = pd.Series(["longParameterList","candidate_Long_Parameter_List.csv","lpl","method"])

# ADICIONAR OS CODE SMELLS NA LINHA ABAIXO
csType = pd.DataFrame([gc, cdsbp, lm, lpl])
csType.columns=["csName", "csCSV", "cs", "granularity"]

# FILTRO DE MÉTRICAS CLASS LEVEL
dsClassHeader = ["AvgCyclomatic","AvgCyclomaticModified","AvgCyclomaticStrict","AvgEssential","AvgLine",
"AvgLineBlank","AvgLineCode","AvgLineComment","CountClassBase","CountClassCoupled","CountClassDerived",
"CountDeclClassMethod","CountDeclClassVariable","CountDeclMethod","CountDeclMethodAll","CountDeclInstanceMethod",
"CountDeclInstanceVariable","CountDeclMethodDefault","CountDeclMethodPrivate", "CountDeclMethodProtected",
"CountDeclMethodPublic","CountLine","CountLineBlank","CountLineCode","CountLineCodeDecl","CountLineCodeExe",
"CountLineComment","CountSemicolon","CountStmt","CountStmtDecl", "MaxCyclomatic","MaxCyclomaticModified","MaxCyclomaticStrict",
"MaxEssential","MaxInheritanceTree","MaxNesting","PercentLackOfCohesion","PercentLackOfCohesionModified","RatioCommentToCode",
"SumCyclomatic","SumCyclomaticModified","SumCyclomaticStrict","SumEssential"]        

# FILTRO DE MÉTRICAS METHOD LEVEL
dsMethodHeader = ["CountInput", "CountLine","CountLineBlank","CountLineCode","CountLineCodeDecl","CountLineCodeExe","CountLineComment","CountOutput","CountPath",
"CountPathLog","CountSemicolon","CountStmt","CountStmtDecl","CountStmtExe","Cyclomatic","CyclomaticModified","CyclomaticStrict","Essential", 
"Knots","MaxEssentialKnots","MaxNesting","MinEssentialKnots","RatioCommentToCode","SumCyclomatic","SumCyclomaticModified","SumCyclomaticStrict","SumEssential"]

for index, row in projects.iterrows():                
        csmells = pd.DataFrame()
        
        for indexCs, rowCs in csType.iterrows():
                                
                try:
                        # LEITURA DOS CODE SMELLS VALIDADOS
                        path = "validated_code_smells/dataset/"+  row["validatedPjDir"] +"/" + row["validatedPjVersion"] + "/Validated/" + rowCs["csCSV"]
                        print("## Lendo de " + path)
                        csmells = pd.read_csv(path, sep=';', header=None)
                        
                        if rowCs["granularity"]=="class":                                
                                csmells[0] = csmells[0].str.replace(".java","")
                                # id = PACOTE + CLASSE
                                csmells["id"] = csmells[1].str.strip() + "." + csmells[0].str.strip()
                        else:                                
                                csmells[1] = csmells[1].str.replace(".java","")
                                # id = PACOTE + CLASSE + NOME DO MÉTODO
                                csmells["id"] = csmells[2].str.strip() + "." + csmells[1].str.strip() + "." + csmells[0].str.strip() 
                        
                        csmells["id"] = csmells["id"].str.strip() #retira os espaços em branco

                        ### LEITURA DOS DATASET DE MÉTRICAS E FAZ UM MATCH COM OS CODE SMELLS VALIDADOS
                        dfMetrics = pd.read_csv("metrics_extracted/" + row["name"] + "/" + row["name"] + ".csv")

                        arrInitialDsLayout = ["project", "Kind" ,"Name"]
                        if rowCs["granularity"]=="class":
                                # Escolhe os tipos "Class"    
                                dfMetrics = dfMetrics[dfMetrics["Kind"].str.contains("Class")]
                                # escolha apenas as métricas (colunas) que tem escopo de CLASSE
                                dfMetrics = dfMetrics.loc[:,arrInitialDsLayout + dsClassHeader]
                        else:
                                # Escolhe os tipos "Constructor" e "Method"                        
                                dfMetrics = dfMetrics[dfMetrics["Kind"].str.contains("Method|Constructor")]
                                # escolha apenas as métricas "colunas" que tem escopo de MÉTODO
                                dfMetrics = dfMetrics.loc[:,arrInitialDsLayout + dsMethodHeader]
                                # retira todos os métodos com repetição de nome do ds de métricas, 
                                # pois o dataset de codesmells validados contém apenas o nome do método 
                                # sem especificar sua assinatura completa. Isto poderá gerar o problema de 
                                # haver várias ocorrências do mesmo método classificado como code smell de forma injusta.        
                                dfMetrics = dfMetrics[~dfMetrics.Name.duplicated(keep=False)]
                                               
                        # inclui uma coluna de nome do projeto
                        dfMetrics["project"] = row["name"]
                        
                        # faz o merge entre o dataset de métricas e o dataset de code smells
                        targetName = "is_" + rowCs["cs"]
                        dfMergedDs = dfMetrics.copy()  
                        dfMetrics[targetName] = dfMetrics["Name"].isin(csmells["id"])
                              
                        #### Datasets gerados estão desbalanceados. Resolvendo o desbalanceamento dos datasets através de undersampling
                        
                        # Class count
                        count_class_0, count_class_1 = dfMetrics[targetName].value_counts()

                        # Divide by class
                        df_class_0 = dfMetrics[dfMetrics[targetName] == 0]
                        df_class_1 = dfMetrics[dfMetrics[targetName] == 1]

                        df_class_0_under = df_class_0.sample(count_class_1*4) # proporção True/False será 1/4
                        dfMetrics = pd.concat([df_class_0_under, df_class_1], axis=0)

                        print('Random under-sampling:')
                        print(dfMetrics[targetName].value_counts())
                                                                        
                        """ #### Datasets gerados estão desbalanceados. Resolvendo o desbalanceamento dos datasets

                        # Separate majority and minority classes
                        df_majority = dfMetrics[dfMetrics[targetName]==False]
                        df_minority = dfMetrics[dfMetrics[targetName]==True]                        
                        
                        # Downsample majority class
                        df_majority_downsampled = resample(df_majority, 
                                                        replace=False,    # sample without replacement
                                                        n_samples=3*df_minority.size,     # 3 times minority class
                                                        random_state=123) # reproducible results
                        
                        # Combine minority class with downsampled majority class
                        dfMetrics = pd.concat([df_majority_downsampled, df_minority])
                        
                        # Display new class counts
                        #df_downsampled.balance.value_counts() """

                        #escreve o novo CSV se no projeto houver alguma ocorrência do tipo de codesmell                        
                        print("--> Escrevendo em " + "oracle_dataset/" + rowCs["cs"] + "/" + row["name"] + ".csv")
                        dfMetrics.to_csv("oracle_dataset/" + rowCs["cs"] + "/" + row["name"] + ".csv", index=False) 

                except (EmptyDataError, ValueError) as err:
                        print("*** VAZIO: " + path)
                                       
## FAZENDO O MERGE DE TODOS OS DATASETS, DIVIDINDO POR TIPO DE CODE SMELL
print("####### JUNTANDO OS DATASETS DOS PROJETOS, AGRUPADOS POR TIPO DE CODE SMELL")        
for indexCs, rowCs in csType.iterrows():        
            
        destdir = 'oracle_dataset/' + rowCs["cs"]
        files = [ f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir,f)) ]

        csDataset = pd.DataFrame()
        for file in files:
                csvFile = pd.read_csv(destdir + "/" + file)
                csDataset = csDataset.append(csvFile)

        mergedPath = "oracle_dataset/" + rowCs["cs"] + ".csv"
        print("--> Escrevendo em " + mergedPath)            
        csDataset.to_csv(mergedPath, index=False)        
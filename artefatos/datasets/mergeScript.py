import pandas as pd
import numpy as np
from pandas.io.common import EmptyDataError
import os

## PROJETOS QUE ESTÃO SENDO UTILIZADOS NO ESTUDO
ant = pd.Series(["ant","apache-ant-data","apache_1.8.3"])
cassandra = pd.Series(["cassandra","apache-cassandra","apache-cassandra-1.1"])
eclipse = pd.Series(["eclipse.jdt.core","eclipse-data","org.eclipse.jdt.core_3.6.1_OK"])
elasticSearch = pd.Series(["elasticsearch","elastic-search-data","elasticsearch-elasticsearch-0.19_OK"])
hadoop = pd.Series(["hadoop","apache-hadoop-data","pat2mongo-hadoop-0.9_OK"])
hbase = pd.Series(["hbase","apache-hbase-data","optimistdk-hbase-0.94_OK"])
lucene = pd.Series(["lucene","apache-lucene","blueshen-lucene-solr-3.6_OK"])
hive = pd.Series(["hive","apache-hive-data","itisaid-hive-0.9_OK"])
ivy = pd.Series(["hive","apache-hive-data","itisaid-hive-0.9_OK"])

## ADICIONAR OS PROJETOS NA PRÓXIMA LINHA
projects = pd.DataFrame([ant, cassandra, eclipse, elasticSearch, hadoop, hbase, lucene, hive, ivy])
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
"CountDeclClass","CountDeclClassMethod","CountDeclClassVariable","CountDeclInstanceMethod","CountDeclInstanceVariable",
"CountDeclMethod","CountDeclMethodAll","CountDeclInstanceMethod","CountDeclInstanceVariable","CountDeclMethod","CountDeclMethodAll",
"CountDeclMethodDefault","CountDeclMethodPrivate", "CountDeclMethodProtected", "CountDeclMethodPublic","CountLine","CountLineBlank",
"CountLineCode","CountLineCodeDecl","CountLineCodeExe","CountLineComment","CountSemicolon","CountStmt","CountStmtDecl", "MaxCyclomatic",
"MaxCyclomaticModified","MaxCyclomaticStrict","MaxEssential","MaxInheritanceTree","MaxNesting","PercentLackOfCohesion","PercentLackOfCohesionModified",
"RatioCommentToCode","SumCyclomatic","SumCyclomaticModified","SumCyclomaticStrict","SumEssential"]        

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

                        arrInitialDsLayout = ["project","Name"]
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
                                               
                        # inclui uma coluna de nome do projeto
                        dfMetrics["project"] = row["name"]
                        #atribuição da coluna de classificação
                        dfMetrics["is_" + rowCs["cs"]] = dfMetrics["Name"].isin(csmells["id"])

                        #escreve o novo CSV se no projeto houver alguma ocorrência do tipo de codesmell                        
                        print("--> Escrevendo em " + "oracle_dataset/" + rowCs["cs"] + "/" + row["name"] + ".csv")
                        dfMetrics.to_csv("oracle_dataset/" + rowCs["cs"] + "/" + row["name"] + ".csv", index=False) 

                except EmptyDataError:
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
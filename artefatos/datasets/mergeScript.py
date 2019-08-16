import pandas as pd
import numpy as np
from pandas.io.common import EmptyDataError

ant = pd.Series(["ant","apache-ant-data","apache_1.8.3"])
cassandra = pd.Series(["cassandra","apache-cassandra","apache-cassandra-1.1"])
eclipse = pd.Series(["eclipse.jdt.core","eclipse-data","org.eclipse.jdt.core_3.6.1_OK"])
elasticSearch = pd.Series(["elasticsearch","elastic-search-data","elasticsearch-elasticsearch-0.19_OK"])
hadoop = pd.Series(["hadoop","apache-hadoop-data","pat2mongo-hadoop-0.9_OK"])
hbase = pd.Series(["hbase","apache-hbase-data","optimistdk-hbase-0.94_OK"])
#lucene = pd.Series(["lucene","apache-lucene","blueshen-lucene-solr-3.6_OK"])

projects = pd.DataFrame([ant, cassandra, eclipse, elasticSearch, hadoop, hbase])
projects.columns = columns=["name","validatedPjDir","validatedPjVersion"]
                  
gc = pd.Series(["godClass","candidate_Large_Class.csv","gc", "class"])
cdsbp = pd.Series(["classDataShouldBePrivate","candidate_Class_Data_Should_Be_Private.csv","cdsbp","class"])
lm = pd.Series(["longMethod","candidate_Long_Methods.csv","lm","method"])
lpl = pd.Series(["longParameterList","candidate_Long_Parameter_List.csv","lpl","method"])

csType = pd.DataFrame([gc, cdsbp, lm])
csType.columns=["csName", "csCSV", "cs", "granularity"]

for index, row in projects.iterrows():                
        csmells = pd.DataFrame()
        
        for indexCs, rowCs in csType.iterrows():
                
                # LEITURA DOS CODE SMELLS VALIDADOS
                try:
                        csmells = pd.read_csv("validated_code_smells/dataset/"+  row["validatedPjDir"] +"/" + row["validatedPjVersion"] + "/Validated/" + rowCs["csCSV"], sep=';', header=None)
                        #csmells=csmells.iloc[:,[0,1]] #elimina as 2 últimas colunas
                        if rowCs["granularity"]=="class":
                                # id = PACOTE + CLASSE
                                csmells[0] = csmells[0].str.replace(".java","")
                                csmells["id"] = csmells[1].str.strip() + "." + csmells[0].str.strip()
                        else:
                                # id = PACOTE + CLASSE + NOME DO MÉTODO
                                csmells[1] = csmells[1].str.replace(".java","")
                                csmells["id"] = csmells[2].str.strip() + "." + csmells[1].str.strip() + "." + csmells[0].str.strip() 
                        
                        csmells["id"] = csmells["id"].str.strip() #retira os espaços em branco

                except EmptyDataError:
                        csmells = pd.DataFrame()               

                # LEITURA DOS DATASET DE MÉTRICAS E FAZ UM MATCH DOS CODE SMELLS VALIDADOS
                dfMetrics = pd.read_csv("metrics_extracted/" + row["name"] + "/" + row["name"] + ".csv")
                            
                if rowCs["granularity"]=="class":
                        # Escolhe os tipos "Class"    
                        dfMetrics = dfMetrics[dfMetrics["Kind"].str.contains("Class|")]
                else:
                        #Escolhe os tipos "Constructor" e "Method"                        
                        dfMetrics = dfMetrics[dfMetrics["Kind"].str.contains("Method|Constructor")]
                
                # TODO filtrar as colunas por métricas OO nível de classe ou método
                
                # inclui uma coluna de nome do projeto
                dfMetrics["project"] = row["name"]
                #atribuição da coluna de classificação
                dfMetrics["is_" + rowCs["cs"]] = dfMetrics["Name"].isin(csmells["id"])

                #escreve o novo CSV se no projeto houver alguma ocorrência do tipo de codesmell
                if csmells.size>0:
                        dfMetrics.to_csv("oracle_dataset/" + rowCs["cs"] + "/" + row["name"] + ".csv") 
                        



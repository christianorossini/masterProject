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

projects = pd.DataFrame([ant, cassandra, eclipse, elasticSearch, hadoop, hbase""" , lucene """])
projects.columns = columns=["name","metricsDir","metricsVersion"]


for index, row in projects.iterrows():                
        csmells = pd.DataFrame()
        # LEITURA DOS CODE SMELLS VALIDADOS
        try:
                csmells = pd.read_csv("validated_code_smells/dataset/"+  row["metricsDir"] +"/" + row["metricsVersion"] + "/Validated/candidate_Large_Class.csv", sep=';', header=None)
                csmells=csmells.iloc[:,[0,1]] #elimina as 2 últimas colunas
                csmells.columns = ["classname","package"]
                csmells["fullclassname"] = csmells["package"] + "." + csmells.classname.str.replace(".java","")
                csmells["fullclassname"] = csmells["fullclassname"].str.strip() #retira os espaços em branco
        except EmptyDataError:
                csmells = pd.DataFrame()               

        # LEITURA DOS DATASET DE MÉTRICAS E FAZ UM MATCH DOS CODE SMELLS VALIDADOS
        
        # Escolhe os tipos "Public Class"
        metrics = pd.read_csv("metrics_extracted/" + row["name"] + "/" + row["name"] + ".csv")
        is_publicclass = metrics["Kind"]=="Public Class"
        metrics_pclass = metrics[is_publicclass]
        # TODO filtrar as colunas por métricas OO nível de classe 
        
        # inclui uma coluna de nome do projeto
        metrics_pclass["project"] = row["name"]
        metrics_pclass["is_god_class"] = metrics_pclass["Name"].isin(csmells["fullclassname"])

        #escreve o novo CSV se no projeto houver alguma ocorrência do Smell
        if csmells.size>0:
                metrics_pclass.to_csv("oracle_dataset/gc/" + row["name"] + ".csv")
import pandas as pd
import numpy as np

pd.Series(["godClass"])


csmells = pd.DataFrame()
csmells = pd.read_csv("validated_code_smells/dataset/apache-cassandra/apache-cassandra-1.1/Validated/candidate_Large_Class.csv")
csmells = pd.read_csv('oracle_dataset/candidate_Large_Class.csv', sep=';', header=None) 
csmells=csmells.iloc[:,[0,1]] #elimina as 2 últimas colunas
csmells.columns = ["classname","package"]
csmells["fullclassname"] = csmells["package"] + "." + csmells.classname.str.replace(".java","")
csmells["fullclassname"] = csmells["fullclassname"].str.strip() #retira os espaços em branco

# Escolhe os tipos "Public Class"
metrics = pd.DataFrame()
metrics = pd.read_csv("metrics_extracted/cassandra/cassandra.csv")
is_publicclass = metrics["Kind"]=="Public Class"
metrics_pclass = metrics[is_publicclass]
# filtrar as colunas por métricas OO nível de classe

# inclui uma coluna de nome do projeto
metrics_pclass["project"]="cassandra"
metrics_pclass["is_god_class"] = metrics_pclass["Name"].isin(csv["fullclassname"])

#escreve o novo CSV
metrics_pclass.to_csv("godClass.csv")





data_url = 'http://bit.ly/2cLzoxH'
# read data from url as pandas dataframe
gapminder = pd.read_csv(data_url)
is_1957 = gapminder["year"]==1957
gapminder.to_csv('teste.csv')


""" raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'], 
        'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'], 
        'age': [42, 52, 36, 24, 73], 
        'preTestScore': [4, 24, 31, ".", "."],
        'postTestScore': ["25,000", "94,000", 57, 62, 70]}
df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
print(df)
df.to_csv('example.csv')
 """






dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
df[0:2]
df.loc['20130102':'20130104', ['A', 'B']]
df[df.A>0]

serie = pd.Series({
        a:"123",
        b:[1,2,3]
})

df2 = df.copy()
df2["E"] =  ['one', 'one', 'two', 'three', 'four', 'three']
df2[df2['E'].isin(['two', 'four'])]

df2[df2 > 0] = -df2

df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ['E'])
df1.loc[dates[0]:dates[1], 'E'] = 1

df1.dropna()
df1.fillna(value="4")
pd.isna(df1)
df1.b.isna()

df.mean(1)

s = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates).shift(2)

df.sub(s, axis='index')

pd.Series(np.random.randint(0, 7, size=10))
s.value_counts()


np.random.randn(8, 4)
df = pd.DataFrame(np.random.randn(8, 4), columns=['A', 'B', 'C', 'D'])
df
s = df.iloc[3]
df.append(s, ignore_index=False)

import matplotlib
ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
ts.plot()
matplotlib.pyplot.show()



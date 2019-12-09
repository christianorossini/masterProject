# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus

import numpy as np
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from matplotlib import pyplot as plt

from GA import gaPreProcessing as ga
import os
import csv


pyPath = os.path.dirname(os.path.abspath(__file__))
dfExportEffectiveness = pd.DataFrame(columns=['splitting_criterion', 'num_of_leaves', 'depth', 'TN', 'TP', 'FN', 'FP', "Precision", "Recall", "F-measure"])

# treina o modelo com um número de folhas
number_of_leaves = [3,7,9]
# Gini index e Information Gain ("entropy")
splitting_critera = ['gini','entropy']

xlsIdx = list()
for cSmell in ["lpl","lm","gc","cdsbp"]:
#for cSmell in ["gc","cdsbp"]:

    # load dataset
    dfCs = pd.read_csv(os.path.dirname(os.path.abspath(__file__))+"/../datasets/oracle_dataset/{0}.csv".format(cSmell))

    #split dataset in features and target variable
    if(cSmell in ["gc","cdsbp"]):                       #code smells de classe
        csvSoftMetricsList = pd.read_csv(pyPath + "/../software_metrics/software_class_level_metrics.csv", delimiter=";")
        # filtra apenas as colunas das métricas que escolhi
        csvSoftMetricsList = csvSoftMetricsList[csvSoftMetricsList['apply']==1]
        # filtra o dataset a ser treinado apenas com as métricas filtradas
        feature_cols = dfCs.loc[:,csvSoftMetricsList["apiname"]].columns
          
    else:                                               #code smells de método        
        csvSoftMetricsList = pd.read_csv(pyPath + "/../software_metrics/software_method_level_metrics.csv", delimiter=";")
        csvSoftMetricsList = csvSoftMetricsList[csvSoftMetricsList['apply']==1]
        feature_cols = dfCs.loc[:,csvSoftMetricsList["apiname"]].columns

    #feature_cols = dfCs.iloc[:,3:30].columns
    X = dfCs[feature_cols] # Features
    classLabel = "is_{0}".format(cSmell)
    y = dfCs[classLabel] # Target variable
    
    for criteria in splitting_critera:
        
        for idx, depth in enumerate(number_of_leaves): #itera sobre o número de folhas que a árvore terá

            # Split dataset into training set and test set
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test

            # Create Decision Tree classifer object        
            #clf = DecisionTreeClassifier(criterion="entropy", min_samples_leaf=5, max_depth=depth)
            clf = DecisionTreeClassifier(criterion=criteria, max_leaf_nodes=depth)        

            # Train Decision Tree Classifer
            clf = clf.fit(X_train,y_train)

            #Predict the response for test dataset
            y_pred = clf.predict(X_test)

            dot_data = StringIO()
            export_graphviz(clf, 
                            out_file=dot_data,                          
                            rounded=True,
                            special_characters=True,
                            feature_names = csvSoftMetricsList['name'],
                            class_names=['0','1'], 
                            impurity=False)

            csRoot = "{0}/dt/{1}".format(pyPath, cSmell)
            dotPath = "{0}/dot/{1}_{2}.dot".format(csRoot, depth, criteria)
            graphPath = "{0}/img/{1}_{2}.png".format(csRoot, depth, criteria)
            csvPredictionPath = "{0}/prediction/{1}_{2}.csv".format(csRoot, depth, criteria)

            # cria o diretório caso não exista
            for dir in list([csRoot, dotPath, graphPath, csvPredictionPath]):
                dirName = os.path.dirname(dir)
                if not os.path.exists(dirName):
                    os.makedirs(dirName)
                
            #cria o csv com as predições
            dfPredictions = dfCs.copy()
            dfPredictions = dfPredictions.iloc[y_test.index,]
            dfPredictions[classLabel] = y_pred
            dfPredictions.to_csv(csvPredictionPath)            
            
            dotFile = pydotplus.graph_from_dot_data(dot_data.getvalue()).to_string()
            #graphPath = ('{0}_ga.png' if applyPreProcessingWGA else "{0}.png")        
            
            ## expressões regulares que excluem elementos indesejados da decision tree
            import re                                        
            dotFile = re.sub('(samples = [0-9]+<br\/>)', '', dotFile)
            dotFile = re.sub('(value = \[[0-9]+, [0-9]+\]<br\/>)', '', dotFile)
            dotFile = re.sub('(<br\/>class = [0-9])', '', dotFile)
            dotFile = re.sub('(class = 1)', '<u><b>smelly code</b></u>', dotFile)
            dotFile = re.sub('(class = 0)', 'not smelly code', dotFile)
            ## RE para modificar o tamanho do nó
            dotFile = re.sub('(style="rounded")', 'style="rounded", width=0.5, fontsize=10', dotFile)
            
            with open(dotPath, 'w') as file:
                file.write(dotFile)

            graph = pydotplus.graph_from_dot_file(dotPath)                   
                    
            #graph.set_size('"10!"')
            graph.write_png(graphPath)
            Image(graph.create_png())

            """ labels = ['Class 0', 'Class 1']
            fig = plt.figure()
            ax = fig.add_subplot(111)
            cax = ax.matshow(conf_mat, cmap=plt.cm.Blues)
            fig.colorbar(cax)
            ax.set_xticklabels([''] + labels)
            ax.set_yticklabels([''] + labels)
            plt.xlabel('Predicted')
            plt.ylabel('Expected')
            plt.show()

            dfCs["is_{0}".format(cSmell)].value_counts().plot(kind='bar', title='Count (target)')
            """
            #if applyPreProcessingWGA:
            #    print("### Decision tree com pre processamento com Algoritmo Genetico")
            
            # Model Accuracy, how often is the classifier correct?
            accuracy = metrics.accuracy_score(y_test, y_pred)

            # Recall, precision, F-measure
            recall = metrics.recall_score(y_test, y_pred)
            precision = metrics.precision_score(y_test, y_pred)
            fmeasure = metrics.f1_score(y_test, y_pred)

            conf_mat = confusion_matrix(y_true=y_test, y_pred=y_pred)
            dfConfMat = pd.DataFrame(conf_mat, columns=["F","T"], index=["F","T"])
            print('Confusion matrix:\n', dfConfMat)
            tp = dfConfMat.loc["T","T"]
            tn = dfConfMat.loc["F","F"]
            fn = dfConfMat.loc["T","F"]
            fp = dfConfMat.loc["F","T"]
            print('TP: {}, TN: {}, FN: {}, FP: {} \n'.format(tp, tn, fn, fp))
            #print('Accuracy: {0}'.format(accuracy))
            print("Precision: {} \nRecall: {}\nF-Measure: {}\n".format(precision, recall, fmeasure))

            dfExportEffectiveness = dfExportEffectiveness.append({'splitting_criterion':criteria, 'num_of_leaves':clf.get_n_leaves(), 'depth': clf.get_depth(),  'TN':tn, 'TP':tp, 'FN':fn, 'FP':fp, "Precision":precision, "Recall":recall, "F-measure":fmeasure}, ignore_index=True)
            
            xlsIdx.append('{0}'.format(cSmell))

#dfExportEffectiveness.index = ["longParameterList","longParameterList*","longMethod","longMethod*","godClass","godClass*","classDataShouldBePrivate","classDataShouldBePrivate*"]
dfExportEffectiveness.index = xlsIdx
dfExportEffectiveness.to_excel(os.path.dirname(os.path.abspath(__file__))+"/modelEffectiveness.xls")


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


pyPath = os.path.dirname(os.path.abspath(__file__))
dfExportEffectiveness = pd.DataFrame(columns=['TN', 'TP', 'FN', 'FP', "Precision", "Recall", "F-measure"])

xlsIdx = list()
#for cSmell in ["lpl","lm","gc","cdsbp"]:
for cSmell in ["lpl"]:

    # load dataset
    dfCs = pd.read_csv(os.path.dirname(os.path.abspath(__file__))+"/../datasets/oracle_dataset/{0}.csv".format(cSmell))

    #split dataset in features and target variable
    if(cSmell in ["gc","cdsbp"]):
        feature_cols = dfCs.iloc[:,3:46].columns
    else:
        feature_cols = dfCs.iloc[:,3:30].columns

    #feature_cols = dfCs.iloc[:,3:30].columns
    X = dfCs[feature_cols] # Features
    y = dfCs["is_{0}".format(cSmell)] # Target variable
    
    #for applyPreProcessingWGA in [False, True]:
    for idx, depth in enumerate([4,7,10,13]): #itera sobre o número de folhas que a árvore terá

       # if applyPreProcessingWGA:
       #     columns = ga.doGAPreProcessing(X,y)
       #     X = X.iloc[:,columns] # filtra as colunas do dataframe de features com a selecao do pre processamento
       #     feature_cols = X.columns
        
        # Split dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test

        # Create Decision Tree classifer object        
        #clf = DecisionTreeClassifier(criterion="entropy", min_samples_leaf=5, max_depth=depth)
        clf = DecisionTreeClassifier(criterion="entropy", max_leaf_nodes=depth)        

        # Train Decision Tree Classifer
        clf = clf.fit(X_train,y_train)

        #Predict the response for test dataset
        y_pred = clf.predict(X_test)

        dot_data = StringIO()
        export_graphviz(clf, 
                        out_file=dot_data,                          
                        rounded=True,
                        special_characters=True,
                        feature_names = feature_cols,
                        class_names=['0','1'], 
                        impurity=False)

        csRoot = "{0}/dt/{1}".format(pyPath, cSmell)
        dotPath = "{0}/dot/{1}.dot".format(csRoot, depth)
        graphPath = "{0}/img/{1}.png".format(csRoot, depth)
        
        dotFile = pydotplus.graph_from_dot_data(dot_data.getvalue()).to_string()
        #graphPath = ('{0}_ga.png' if applyPreProcessingWGA else "{0}.png")        
        
        ## inserir expressão regular para excluir elementos indesejados da decision tree
        import re                        
        #dotFile = re.sub('(\\\\nsamples = [0-9]+)(\\\\nvalue = \[[0-9]+, [0-9]+, [0-9]+\])', '', graph)
        #dotFile = re.sub('(samples = [0-9]+)(\\\\nvalue = \[[0-9]+, [0-9]+, [0-9]+\])\\\\n', '', graph)
        dotFile = re.sub('(samples = [0-9]+<br\/>)', '', dotFile)
        dotFile = re.sub('(value = \[[0-9]+, [0-9]+\]<br\/>)', '', dotFile)
        dotFile = re.sub('(<br\/>class = [0-9])', '', dotFile)
        dotFile = re.sub('(class = 1)', '<u><b>smelly code</b></u>', dotFile)
        dotFile = re.sub('(class = 0)', 'not smelly code', dotFile)
        
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

        dfExportEffectiveness = dfExportEffectiveness.append({'TN':tn, 'TP':tp, 'FN':fn, 'FP':fp, "Precision":precision, "Recall":recall, "F-measure":fmeasure}, ignore_index=True)
        
        xlsIdx.append('{0}_{1}'.format(cSmell,depth))

#dfExportEffectiveness.index = ["longParameterList","longParameterList*","longMethod","longMethod*","godClass","godClass*","classDataShouldBePrivate","classDataShouldBePrivate*"]
dfExportEffectiveness.index = xlsIdx
dfExportEffectiveness.to_excel(os.path.dirname(os.path.abspath(__file__))+"/modelEffectiveness.xls")


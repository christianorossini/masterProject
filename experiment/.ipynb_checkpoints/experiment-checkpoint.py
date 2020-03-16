# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '../../../../../../tmp'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# # Dataset inspection

#%%
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "last"
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#%% [markdown]
# ## Analysing and removing careless or biased participations
# 
# We created "Dummy tasks", randomly selected code components not affected by any of the code smells considered in our study. This was done to limit the bias in the study, i.e., avoid that participants always indicate that the code contains a problem.
# 
# So, we first look for participants that accomplish tasks in a careless and/or biased way, analysing how they performed tasks when faced with dummy tasks. For instance, we intentionally created a dummy task that defines a god class, however the correspondent java code have just few line of codes. Thus, we expected that the participant would mark "I strongly disagree" or, at minimun, "I Slightly disagree". After data inspection, we noted that almost all of the participant not behave biased ou carelessly. Except for 1 participant, all of them marks some degree of disagreement when evaluated dummy tasks.

#%%
header = ["id","questionnaire_id","task_id","secondsToAnswer","isDt","answer_ptr_id","answer_csagreement","answer_description","answer_dtDescription"]
answer =  pd.read_csv('answer.csv', header=None, escapechar="\\", encoding="latin_1")
answer.columns=header

dummy_id = "13,14,15,16"
answer_dummy = answer.query("task_id in ({0})".format(dummy_id))

# o questionnaire id 25 será retirado
answer_dummy[answer_dummy.questionnaire_id==25].loc[:,'id':'answer_csagreement']


#%%
# retira as atividades dummy
answer_no_dummy = answer[~answer.id.isin(answer_dummy.id)]

# retira o participante cujo questionnaire_id=25
answer_no_dummy = answer_no_dummy[answer_no_dummy.questionnaire_id!=25]

# 12 participantes x 8 atividades = 96 rows
answer_no_dummy.head()

#%% [markdown]
# # Experiment results

#%%
import  statsmodels.stats.inter_rater as ir

answer_no_dummy_dt = answer_no_dummy[answer_no_dummy.isDt==1]
answer_no_dummy_noDt = answer_no_dummy[answer_no_dummy.isDt==0]

# calcula os agreements agrupando por atividade e agreement
df_count_agreement = answer_no_dummy_dt[['task_id','answer_csagreement']].groupby(['task_id','answer_csagreement']).size().reset_index(name='size')

list_count_agreement = list()
tasks = answer_no_dummy.task_id.unique()
df_agreement_frame = pd.DataFrame([[-2,0],[-1,0],[1,0],[2,0]])

for task in tasks:
    df_tmp = df_count_agreement[df_count_agreement.task_id==task].iloc[:,1:3]
    df_merged = pd.merge_ordered(df_tmp, df_agreement_frame, fill_method='ffill', right_by="answer_csagreement", how="left")        
    list_count_agreement.append(df_merged['size'].tolist()) 
    
df_kappaTable = pd.DataFrame(list_count_agreement)
df_disagree = df_kappaTable[0]+df_kappaTable[1]
df_agree = df_kappaTable[2]+df_kappaTable[3]

df_kappaTable = pd.concat([df_disagree, df_agree], axis=1)

ir.fleiss_kappa(df_kappaTable, method='fleiss')


#%%
df_kappaTable.columns = ['disagree','agree'] 

df_kappaTable

#%% [markdown]
# ## Evaluation effort

#%%
answer_no_dummy_dt                  
    

labels = ['DT', 'No DT']

answerDtMinutes = answer_no_dummy_dt.secondsToAnswer
answerNoDtMinutes = answer_no_dummy_noDt.secondsToAnswer

all_data = [answerDtMinutes,answerNoDtMinutes]

plt.boxplot(all_data,
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=labels)  # will be used to label x-ticks
#plt.show()

# df_table = pd.DataFrame([answerDtMinutes.tolist(),answerNoDtMinutes])
# df_table.T






#%%
import numpy as np

# Random test data
np.random.seed(19680801)
all_data = [np.random.normal(0, std, size=100) for std in range(1, 4)]
labels = ['x1', 'x2', 'x3']

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

# rectangular box plot
bplot1 = axes[0].boxplot(all_data,
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=labels)  # will be used to label x-ticks
axes[0].set_title('Rectangular box plot')

# notch shape box plot
bplot2 = axes[1].boxplot(all_data,
                         notch=True,  # notch shape
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=labels)  # will be used to label x-ticks
axes[1].set_title('Notched box plot')

# fill with colors
colors = ['pink', 'lightblue', 'lightgreen']
for bplot in (bplot1, bplot2):
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

# adding horizontal grid lines
for ax in axes:
    ax.yaxis.grid(True)
    ax.set_xlabel('Three separate samples')
    ax.set_ylabel('Observed values')

plt.show()


#%%
header = ["inviteId","codeRevision","codeSmellIdentification","degree","devExperience","javaExperience","objOrientedExperience","origin","yearsDevExperience"]
participants =  pd.read_csv('participant.csv', header=None)
participants.columns=header


#participants.to_csv('participant.csv', index=False)
        
#participants


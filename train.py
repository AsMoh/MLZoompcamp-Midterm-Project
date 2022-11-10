#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.width', 4000)
pd.set_option('display.max_colwidth', 4000)

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA as sklearnPCA

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score , recall_score, precision_score
from sklearn.metrics import roc_curve ,confusion_matrix , auc, roc_auc_score, classification_report , f1_score




data=pd.read_csv('UNSW_NB15_training-set.csv')



df=data.copy()




## is_ftp_login is binary feature, it should be either 0 or 1
df = df.drop(index=df[df['is_ftp_login']==2].index)




cols_to_delete=['id', 'attack_cat', 'proto']



df=df.drop(cols_to_delete, axis=1)



df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)

df_full_train = df_full_train.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)

y_train = df_full_train.label
y_test = df_test.label

del df_full_train['label']
del df_test['label']



categorical_cols=['service', 'state'  , 'is_ftp_login' , 'ct_ftp_cmd' , 'is_sm_ips_ports' ]
numerical_cols= list(df.columns.drop(['service', 'state'  , 'is_ftp_login' , 'ct_ftp_cmd' , 'is_sm_ips_ports' , 'label']))



print(numerical_cols)



### Converting categorical features to numerical data using DictVectorizer

dv = DictVectorizer(sparse=False)

train_dict = df_full_train[categorical_cols].to_dict(orient='records')
X_train_categorical = dv.fit_transform(train_dict )

test_dict = df_test[categorical_cols].to_dict(orient='records')
X_test_categorical = dv.transform(test_dict)




len(dv.feature_names_)



##standardized numerical data

sc = StandardScaler()
X_std_train_numerical = sc.fit_transform(df_full_train[numerical_cols])
X_std_test_numerical  = sc.transform(df_test[numerical_cols])  

### combing the numerial arrays & categorical arrays
X_std_train = np.concatenate((X_train_categorical,X_std_train_numerical) , axis=1)
X_std_test = np.concatenate((X_test_categorical,X_std_test_numerical) , axis=1)




pca = sklearnPCA()
sklearn_pca = pca.fit(X_std_train)
train_pca = sklearn_pca.transform(X_std_train)
test_pca = sklearn_pca.transform(X_std_test)

var_per = sklearn_pca.explained_variance_ratio_
cum_var_per = sklearn_pca.explained_variance_ratio_.cumsum()

n_comp=len(cum_var_per[cum_var_per <= 0.90])

sklearn_pca = sklearnPCA(n_components=n_comp)
train_pca = sklearn_pca.fit_transform(X_std_train)
test_pca = sklearn_pca.transform(X_std_test)



X_train= train_pca
X_test= test_pca




import xgboost as xgb




eta=0.1
max_depth=8

dtrain = xgb.DMatrix(X_train, label=y_train)

dtest = xgb.DMatrix(X_test, label=y_test)





watchlist = [(dtrain, 'train'), (dtest, 'test')]




xgb_params = {
    'eta': eta, 
    'max_depth': max_depth,
    'min_child_weight': 1,
    
    'objective': 'binary:logistic',
    'eval_metric': 'auc',

    'nthread': 8,
    'seed': 1,
    'verbosity': 1,
}



model = xgb.train(xgb_params, dtrain, num_boost_round=200,
                  verbose_eval=5,
                  evals=watchlist)



#y_pred = model.predict_proba(X_val)[:, 1] 
scores={}
y_pred=model.predict(dtest)
y_predicted= (y_pred>=0.5).astype(int)
print(confusion_matrix(y_test, y_predicted))
print(classification_report(y_test, y_predicted))

fpr,tpr, th=roc_curve(y_test, y_predicted)
   
scores= {'classiffier': "XGboost" , 'accuracy':round(accuracy_score(y_test,y_predicted),3)
                , 'recall':round(recall_score(y_test,y_predicted),3)
                , 'precision': round(precision_score(y_test,y_predicted),3)
              , 'f1-score': round(f1_score(y_test,y_predicted), 3)  , 'roc_auc_score': round(roc_auc_score(y_test, y_pred),3)}

scores




print(y_pred[0])





print(y_pred[400])





import bentoml



bentoml.xgboost.save_model(
    'cyber_attack_model',
    model,
    custom_objects={
        'dictVectorizer': dv,
        'StandardScaler': sc,
        'PCA':sklearn_pca
              
        
    },signatures={
"predict": {
    "batchable":True,
    "batch_dim":0
}
    }
)




import json



request = df_test.iloc[0].to_dict()
print(json.dumps(request, indent=2))





request = df_test.iloc[400].to_dict()
print(json.dumps(request, indent=2))







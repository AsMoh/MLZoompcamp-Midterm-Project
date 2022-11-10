import numpy as np

import bentoml
from bentoml.io import JSON

from pydantic import BaseModel

class AttackPredictionApplication(BaseModel):
  dur: float
  service: str
  state: str
  spkts: int
  dpkts: int
  sbytes: int
  dbytes: int
  rate: float
  sttl: int
  dttl: int
  sload: float
  dload: float
  sloss: int
  dloss: int
  sinpkt: float
  dinpkt: float
  sjit: float
  djit: float
  swin: int
  stcpb: int
  dtcpb: int
  dwin: int
  tcprtt: float
  synack: float
  ackdat: float
  smean: int
  dmean: int
  trans_depth: int
  response_body_len: int
  ct_srv_src: int
  ct_state_ttl: int
  ct_dst_ltm: int
  ct_src_dport_ltm: int
  ct_dst_sport_ltm: int
  ct_dst_src_ltm: int
  is_ftp_login: int
  ct_ftp_cmd: int
  ct_flw_http_mthd: int
  ct_src_ltm: int
  ct_srv_dst: int
  is_sm_ips_ports: int
  
  
model_ref = bentoml.xgboost.get("cyber_attack_model:a5qrwec6x2eyf5bz")
dv = model_ref.custom_objects['dictVectorizer']
sc=model_ref.custom_objects['StandardScaler']
sklearn_pca= model_ref.custom_objects['PCA']

categorical_cols=['service', 'state'  , 'is_ftp_login' , 'ct_ftp_cmd' , 'is_sm_ips_ports' ]

numerical_cols= ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt', 'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean', 'dmean', 'trans_depth', 'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'ct_flw_http_mthd', 'ct_src_ltm', 'ct_srv_dst']

model_runner = model_ref.to_runner()

svc = bentoml.Service("cyber_attack_classifier", runners=[model_runner])


@svc.api(input=JSON(pydantic_model=AttackPredictionApplication), output=JSON())
async def classify(AttackPredictionApplication_data):
    application_data=AttackPredictionApplication_data.dict()

    print(application_data)
    numerical_list = []

    for key in numerical_cols:
        numerical_list.append(application_data.get(key))
        
    categorical_dict = {}

    for key in categorical_cols:
        categorical_dict[key]=application_data.get(key)
        
        
    vector2= sc.transform(np.array(numerical_list).reshape(1,-1))
   ## vector1 = dv.transform(np.array(categorical_list).reshape(1,-1))
    vector1= dv.transform (categorical_dict)
    vec = np.concatenate((vector1,vector2) , axis=1)

    vector_pca= sklearn_pca.transform(vec)
    prediction = await model_runner.predict.async_run(vector_pca)
    print(prediction)
    result = prediction[0]

    if result > 0.5:
        return {
            "status": "Attack",
            "attack_prob": result

        }
    else:
        return {
            "status": "Not attack",
            "attack_prob": result

        }
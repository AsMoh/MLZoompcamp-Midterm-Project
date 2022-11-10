# MLZoompcamp-Midterm-Project
This repository contains my midterm project for ML zoom camp 2022. 
Dataset source: https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15 

The Cyber Range Lab of the Australian Centre for Cyber Security (ACCS) has created the raw network packets of the UNSW-NB 15 dataset by the IXIA PerfectStorm tool. The purpose of this dataset is to generate a hybrid of real modern normal activities and synthetic contemporary attack behaviours.

My goal is to develop ML model that predicts whether a certain raw network packets is a cybersecurity attack or not. 
<div>
<img src="https://www.cuinsight.com/wp-content/uploads/2022/04/bigstock-Hacker-In-Binary-Code-Digital-449899955.jpg" width="500"/>
</div>
<br>

The UNSW-NB15_features.csv file that is uploaded in this repo includes the features description.

The total number of records is two million and 540,044 which are stored in the four CSV files, namely, UNSW-NB151.csv, UNSW-NB152.csv, UNSW-NB153.csv and UNSW-NB154.csv.

In my project, I have used the data available in UNSW_NB15_training-set.csv file ( uploaded in this repository). 

Let's predict the probability that a raw network packet can be cybersecurity attack.
<br>

# Running the model using BentoML

You need first to run 


## Docker Image
### To deploy the model locally and run it, you need first to pull the docker image by running the below command:
docker pull asia2022/cyber_attack_classifier:c3ixmwk73cecv5bz

Then run the below command to run the service:
docker run -it --rm -p 3000:3000 cyber_attack_classifier:c3ixmwk73cecv5bz serve --production

The data json that needs to be passed to the model should be in this format:

<code>
{
  "dur": 0,
  "service": "string",
  "state": "string",
  "spkts": 0,
  "dpkts": 0,
  "sbytes": 0,
  "dbytes": 0,
  "rate": 0,
  "sttl": 0,
  "dttl": 0,
  "sload": 0,
  "dload": 0,
  "sloss": 0,
  "dloss": 0,
  "sinpkt": 0,
  "dinpkt": 0,
  "sjit": 0,
  "djit": 0,
  "swin": 0,
  "stcpb": 0,
  "dtcpb": 0,
  "dwin": 0,
  "tcprtt": 0,
  "synack": 0,
  "ackdat": 0,
  "smean": 0,
  "dmean": 0,
  "trans_depth": 0,
  "response_body_len": 0,
  "ct_srv_src": 0,
  "ct_state_ttl": 0,
  "ct_dst_ltm": 0,
  "ct_src_dport_ltm": 0,
  "ct_dst_sport_ltm": 0,
  "ct_dst_src_ltm": 0,
  "is_ftp_login": 0,
  "ct_ftp_cmd": 0,
  "ct_flw_http_mthd": 0,
  "ct_src_ltm": 0,
  "ct_srv_dst": 0,
  "is_sm_ips_ports": 0
}
</code>

- Below are some data samples that can be used to test the model:
<br>

1- Non attack ativity
<br>
<code>
{
  "dur": 0.453854,
  "service": "-",
  "state": "FIN",
  "spkts": 10,
  "dpkts": 6,
  "sbytes": 714,
  "dbytes": 268,
  "rate": 33.050276,
  "sttl": 254,
  "dttl": 252,
  "sload": 11334.04102,
  "dload": 3948.40625,
  "sloss": 2,
  "dloss": 0,
  "sinpkt": 6578.2406,
  "dinpkt": 10961.736,
  "sjit": 653840.0681,
  "djit": 24336.61,
  "swin": 255,
  "stcpb": 2906150044,
  "dtcpb": 3830409389,
  "dwin": 255,
  "tcprtt": 0.177939,
  "synack": 0.089164,
  "ackdat": 0.088775,
  "smean": 71,
  "dmean": 45,
  "trans_depth": 0,
  "response_body_len": 0,
  "ct_srv_src": 6,
  "ct_state_ttl": 1,
  "ct_dst_ltm": 4,
  "ct_src_dport_ltm": 4,
  "ct_dst_sport_ltm": 4,
  "ct_dst_src_ltm": 6,
  "is_ftp_login": 0,
  "ct_ftp_cmd": 0,
  "ct_flw_http_mthd": 0,
  "ct_src_ltm": 4,
  "ct_srv_dst": 7,
  "is_sm_ips_ports": 0
}
</code>
<br>


2- Attack activity 
<br>

<code>

{
  "dur": 4e-06,
  "service": "dns",
  "state": "INT",
  "spkts": 2,
  "dpkts": 0,
  "sbytes": 114,
  "dbytes": 0,
  "rate": 250000.0006,
  "sttl": 254,
  "dttl": 0,
  "sload": 114000000.0,
  "dload": 0.0,
  "sloss": 0,
  "dloss": 0,
  "sinpkt": 0.004,
  "dinpkt": 0.0,
  "sjit": 0.0,
  "djit": 0.0,
  "swin": 0,
  "stcpb": 0,
  "dtcpb": 0,
  "dwin": 0,
  "tcprtt": 0.0,
  "synack": 0.0,
  "ackdat": 0.0,
  "smean": 57,
  "dmean": 0,
  "trans_depth": 0,
  "response_body_len": 0,
  "ct_srv_src": 7,
  "ct_state_ttl": 2,
  "ct_dst_ltm": 7,
  "ct_src_dport_ltm": 7,
  "ct_dst_sport_ltm": 3,
  "ct_dst_src_ltm": 7,
  "is_ftp_login": 0,
  "ct_ftp_cmd": 0,
  "ct_flw_http_mthd": 0,
  "ct_src_ltm": 8,
  "ct_srv_dst": 7,
  "is_sm_ips_ports": 0
}
</code>

Below link is a demo for running the model using the docker image.

https://youtu.be/mN3jBV4ABLA

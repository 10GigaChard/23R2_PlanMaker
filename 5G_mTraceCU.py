"""
Release Date : 20220321
Develope By(nokia_plan) : Kevin Song(Kyoungbin Song)
contact : +82-10-9970-8968
uptated Version : 1.7

This's a prototype of Plan Maker.

This Code is for Making Neighboring Plan for replacing DU10 to DU20

It contains copy & delete & modify legacy Neighbor(5G SA mode) MO to DU20 side:

MRBTS/NRBTS>NRADJNRCELL
MRBTS/NRBTS>NRADJGNB
MRBTS/NRBTS>XNLINK

MRBTS/NRBTS/NRCELL>NRREL

Inter-RAT HO:
    
MRBTS/NRBTS>NRADJECELL

MRBTS/NRBTS/NRCELL>NRRELE


If someone wanna edit this code by any reasons.
Help yourself. 

***********************
Lang :
    Python 3.9.6
Pkg :
    pandas 1.3.1
    numpy 1.21.1
    xlrd 1.2.0

nokia_plan recommended PKG : 
    up to 22R1

************************    
"""

# 원본파일 commition

# 불필요한 주석제거


# %%

import pandas as pd
import numpy as np
import os
import os.path
import glob
import csv
import warnings
warnings.simplefilter(action='ignore',category=FutureWarning())


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)



current_path="C:/nokia_plan"

###### input data field.


path_input_data = "C:/nokia_plan/workingset.csv"

###### sub output data field.
path_input_data2 = "C:/nokia_plan/sub_Replacement/input_data2.csv"
path_input_data_nrrel = "C:/nokia_plan/sub_Replacement/input_data_nrrel.csv"
path_sub_netact_nradjnrcell = "C:/nokia_plan/sub_Replacement/sub_target_nradjnrcell.csv"
path_sub_netact_nrrel = "C:/nokia_plan/sub_Replacement/sub_target_nrrel.csv"


###### output data field.
path_modify_PLAN= "C:/nokia_plan/[2]all_mTraceCU_create_flagON_PLAN.csv"
path_DU20delete_PLAN= "C:/nokia_plan/[1]all_mTraceCU_delete_PLAN.csv"

####### output delete plan

path_sub_delete_nradjgnb = "C:/nokia_plan/sub_Replacement/sub_ngbrdelete_nradjgnb.csv"
path_sub_delete_xnlink = "C:/nokia_plan/sub_Replacement/sub_ngbrdelete_xnlink.csv"



####### output copy plan
path_sub_copy_nradjgnb = "C:/nokia_plan/sub_Replacement/sub_copy_nradjgnb.csv"
path_sub_copy_xnlink = "C:/nokia_plan/sub_Replacement/sub_copy_xnlink.csv"
path_sub_copy_nradjnrcell = "C:/nokia_plan/sub_Replacement/sub_copy_nradjnrcell.csv"
path_sub_copy_nrrel = "C:/nokia_plan/sub_Replacement/sub_copy_nrrel.csv"
path_sub_copy_nrrele= "C:/nokia_plan/sub_Replacement/sub_copy_nrrele.csv"
path_sub_copy_nradjecell = "C:/nokia_plan/sub_Replacement/sub_copy_nradjecell.csv"

######## output modify plan

path_sub_modify_nradjnrcell = "C:/nokia_plan/sub_Replacement/sub_modify_nradjnrcell.csv"
path_sub_modify_nradjgnb = "C:/nokia_plan/sub_Replacement/sub_modify_nradjgnb.csv"
path_sub_modify_xnlink = "C:/nokia_plan/sub_Replacement/sub_modify_xnlink.csv"
path_sub_modify_nrrel = "C:/nokia_plan/sub_Replacement/sub_modify_nrrel.csv"

path_sub_ngbrmodify_xnlink = "C:/nokia_plan/sub_Replacement/sub_ngbrmodify_xnlink.csv"
path_sub_ngbrmodify_nradjgnb = "C:/nokia_plan/sub_Replacement/sub_ngbrmodify_nradjgnb.csv"


## declare teamporary dictionary variables
new_dic_nradjnrcell = []
new_dic_nradjgnb = []
new_dic_xnlink = []
new_dic_nradjecell = []
new_dic_nrrel = []
new_dic_nrrele = []



modify_dic_nradjnrcell = []
modify_dic_nrrel = []
modify_dic_nradjgnb = []
modify_dic_xnlink = []

delete_dic_nradjgnb=[]
delete_dic_xnlink=[]


nradjnrcell_dic ={}
nradjgnb_dic ={}
xnlink_dic={}
nradjecell_dic={}

nrrel_dic ={}
nrrele_dic ={}

xnlink_nradjgnb_dic={}




new_dic_delete_nrrel=[]
new_dic_delete_nrrele=[]



#### PLMN loading.... from input_data.csv


PLMN = pd.read_csv(path_input_data, usecols=[11,12], dtype=str)
PLMN.columns = ['MCC', 'MNC']
mcc=PLMN['MCC'][0]
mnc=PLMN['MNC'][0]
print(mcc)
print(mnc)


## Eliminating Duplicated data in Input file

temp_du = open(path_input_data,'r')
temp_lines= csv.reader(temp_du)

temp_du_out = open(path_input_data2,'w' ,newline='')
temp_write=csv.writer(temp_du_out)


for a in temp_lines:
    tar_du = a[0]
    sor_du = a[2]
    print(a)
    if (tar_du != sor_du) :
        temp_write.writerow(a)

    
temp_du.close()
temp_du_out.close()
temp_input2=pd.read_csv(path_input_data2, dtype=str)
temp_input=pd.read_csv(path_input_data, dtype=str)


## declare main fuction 


print("\n\n")
print("=================================================================================================================")
print("==================      Starting Plan Maker                       ===============================================")
print("==================  For 5G NR mTRACE CU object delete & creation  =====    Made by  : Kyoungbin1004           ===")
print("==================================================================    Contact  : kyoungbin.song@nokia.com     ===")
print("==================================================================    Version  : 202305 - 23R2                ===")
print("=================================================================================================================")
print("\n")






#%%  nrrel         copy, modify

################### NRREL copy, modify plan making ############################################

target_nrrel_info = pd.read_csv(path_input_data,  usecols=[0], dtype=str)
target_nrrel_info.columns = ['DN']
target_nrrel_info['DN'].replace('', np.nan, inplace=True)
target_nrrel_info.dropna(subset=['DN'], inplace=True)

elements2 = target_nrrel_info['DN'].str.split("/", expand=True)
NRBTS = elements2[2].str.split("-", expand=True)



target_nrrel_info['NRBTS'] = NRBTS[1]



elements2 = None


"""

"""
      

    
result_nrrel=result_nrrel.drop(['IDX_nrrel','key_nrrel','before_gnbid','before_cellid','before_lcr','after_gnbId','after_cellid','after_lcr','DN','NN1','NN2'],axis=1)

nrrel_dup_key=result_nrrel['NRBTS'].astype(str) + "_" + result_nrrel['NRCELL'].astype(str) + "_" + result_nrrel['gnbid'].astype(str) + "_" + result_nrrel['lcr'].astype(str)
result_nrrel['nrrel_dup_key'] =nrrel_dup_key
result_nrrel=result_nrrel.drop_duplicates(['nrrel_dup_key'], keep ='first',ignore_index = True)

result_nrrel.to_csv(path_new_nrrel, index=False, header=False)






n_nrrel = open(path_new_nrrel, 'r')
new_nrrel_lines = csv.reader(n_nrrel)

def get_nrrel_copy_list(new_dic_nrrel, lines):
    for l1 in lines:
        key_idx = str(l1[3])+"_"+ str(l1[4])
        for k in range(0, 256):
            if ((key_idx + "_" + str(k)) not in nrrel_dic):
                new_dic_nrrel.append(
                ['PLMN-PLMN/MRBTS-' + str(l1[3]) + '/NRBTS-' + str(l1[3]) + '/NRCELL-' + str(l1[4]) + '/NRREL-' + str(k),'create',str(l1[0]), '24', '24', str(l1[1]) , '22', str(mcc), str(mnc), '2',str(l1[2]),'0' ,'1','0','0' ])
                nrrel_dic[(key_idx + "_" + str(k))] = {}
                break



get_nrrel_copy_list(new_dic_nrrel,new_nrrel_lines)         
dt_nrrel=pd.DataFrame(new_dic_nrrel)
n_nrrel.close()



if (dt_nrrel.empty != True):
    output_format5 = pd.DataFrame({'1': [None,'com.nokia.srbts.nrbts:NRREL', '$dn', None, None], '2': [None, None, '$operation', None, None], '3': [None, None, '$version', None, None], '4': [None, None, 'cellIndividualSsbRsrpOffset', None, None], '5': [None, None, 'cellIndividualSsbRsrqOffset', None, None], '6': [None, None, 'gNbId', None, None], '7': [None, None, 'gNbIdLength', None, None], '8': [None, None, 'mcc', None, None], '9': [None, None, 'mnc', None, None], '10': [None, None, 'mncLength', None, None], '11': [None, None, 'lcrId', None, None], '12': [None, None, 'removeNotAllowed', None, None], '13': [None, None, 'handoverAllowedSA', None, None], '14': [None, None, 'handoverAllowedSARedCap', None, None], '15': [None, None, 'nrDcAllowed', None, None]})
    dt_nrrel.columns = ['1', '2', '3', '4', '5', '6', '7', '8','9','10', '11','12','13','14','15']
    pd.concat([output_format5, dt_nrrel],axis=0,sort=False).to_csv(path_sub_copy_nrrel, index=False, header=False)




modify_result_nrrel = pd.merge(modify_input_nrrel_info,modify_target_nrrel_info, how='left', left_on='modify_nrrel_key', right_on='modify_nrrel_key')



for index,row in modify_result_nrrel.iterrows():
    if ( (str(row["NRBTS"])+'_'+str(row["NRCELL"])) in intra_nrrel_dic2 ):
        row["DN"]=None

modify_result_nrrel.dropna(subset=['DN'], inplace=True)

modify_result_nrrel['gnbid']=modify_result_nrrel['after_gnbId']
modify_result_nrrel['lcr']=modify_result_nrrel['after_lcr']
modify_result_nrrel['NN']=modify_result_nrrel['NRBTS']+'_'+modify_result_nrrel['NRCELL']+'_'+modify_result_nrrel['gnbid']+'_'+modify_result_nrrel['lcr']
modify_result_nrrel=modify_result_nrrel.drop_duplicates(['NN'], keep ='first',ignore_index = True)


modify_result_nrrel=modify_result_nrrel.drop(['NRBTS','NRCELL','modify_nrrel_key','before_gnbid','before_cellid','before_lcr','after_gnbId','after_cellid','after_lcr','NN'],axis=1)





def get_nrrel_modify_list(modify_dic_nrrel, df):
    for index,row in df.iterrows():
        modify_dic_nrrel.append([str(row["DN"]),'update','24','24',str(row["gnbid"]),'22',str(mcc),str(mnc),'2',str(row["lcr"]),'0','1','0','0'])

get_nrrel_modify_list(modify_dic_nrrel,modify_result_nrrel)         


dt_modify_nrrel=pd.DataFrame(modify_dic_nrrel)



if (dt_modify_nrrel.empty != True):
    output_format5 = pd.DataFrame({'1': [None,'com.nokia.srbts.nrbts:NRREL', '$dn', None, None], '2': [None, None, '$operation', None, None], '3': [None, None, 'cellIndividualSsbRsrpOffset', None, None], '4': [None, None, 'cellIndividualSsbRsrqOffset', None, None], '5': [None, None, 'gNbId', None, None], '6': [None, None, 'gNbIdLength', None, None], '7': [None, None, 'mcc', None, None], '8': [None, None, 'mnc', None, None], '9': [None, None, 'mncLength', None, None], '10': [None, None, 'lcrId', None, None], '11': [None, None, 'removeNotAllowed', None, None],'12': [None, None, 'handoverAllowedSA', None, None], '13': [None, None, 'handoverAllowedSARedCap', None, None], '14': [None, None, 'nrDcAllowed', None, None]})

    dt_modify_nrrel.columns = ['1', '2', '3', '4', '5', '6', '7', '8','9','10', '11','12', '13','14']
    pd.concat([output_format5, dt_modify_nrrel],axis=0,sort=False).to_csv(path_sub_modify_nrrel, index=False, header=False)




#%%  xnlink        copy , delete ,create


############# XNLINK copy , delete ,create plan


target_xnlink_info = pd.read_csv(path_netact_xnlink, skiprows=[0,1, 2], usecols=[0,3, 4], dtype=str)
target_xnlink_info.columns = ['DN','version', 'target_ip']
target_xnlink_info['DN'].replace('', np.nan, inplace=True)
target_xnlink_info.dropna(subset=['DN'], inplace=True)

elements = target_xnlink_info['DN'].str.split("/", expand=True)
NRBTS = elements[2].str.split("-", expand=True)
key_xnlink = NRBTS[1]
target_xnlink_info['source_gnb'] = NRBTS[1]



modify_target_xnlink_info=pd.DataFrame(columns=range(2))
modify_target_xnlink_info.columns = ['DN', 'target_ip']
modify_target_xnlink_info['DN']=target_xnlink_info['DN']
modify_target_xnlink_info['target_ip']=target_xnlink_info['target_ip']
modify_target_xnlink_info['modify_xnlink_key']=modify_target_xnlink_info['target_ip']

target_xnlink_info['key_xnlink'] = key_xnlink
elements = None


input_xnlink_info = pd.read_csv(path_input_data, usecols=[0,3, 5,8], dtype=str)
input_xnlink_info.columns = ['before_gnbid', 'before_gnbip','after_gnbId','after_gnbip']
input_xnlink_info.dropna(subset=['before_gnbid'], inplace=True)
modify_input_xnlink_info=pd.DataFrame(columns=range(4))

modify_input_xnlink_info.columns = ['before_gnbid', 'before_gnbip','after_gnbId','after_gnbip']

modify_input_xnlink_info['before_gnbid']=input_xnlink_info['before_gnbid']
modify_input_xnlink_info['before_gnbip']=input_xnlink_info['before_gnbip']
modify_input_xnlink_info['after_gnbId']=input_xnlink_info['after_gnbId']
modify_input_xnlink_info['after_gnbip']=input_xnlink_info['after_gnbip']
modify_input_xnlink_info['modify_xnlink_key']=modify_input_xnlink_info['before_gnbip']









key_xnlink = input_xnlink_info['before_gnbid']

input_xnlink_info['key_xnlink'] = key_xnlink

result_xnlink = pd.merge(input_xnlink_info,target_xnlink_info, how='left', left_on='key_xnlink', right_on='key_xnlink')


input_xnlink_info['NN1']=input_xnlink_info['before_gnbip']

result_xnlink['NN1']=result_xnlink['before_gnbip']
result_xnlink['NN2']=result_xnlink['target_ip']


new_list_xnlink=pd.DataFrame()

print("========================================================================================================================")
print("=========================      XNLINK intra to inter processing    =====================================================")
print("=========================      it will take several minutes        =====================================================")
print("========================================================================================================================")

for index,row in input_xnlink_info.iterrows():
    for index2,row2 in result_xnlink.iterrows():
        if (str(row["NN1"])==str(row2["NN2"])):
            new_list_xnlink=new_list_xnlink.append(result_xnlink.loc[index2])
            result_xnlink.iloc[index2,7]=row["after_gnbip"]
            
                



result_xnlink['source_gnb']=result_xnlink['after_gnbId']

result_xnlink['xnlink_dup_key']=result_xnlink['source_gnb'].astype(str)+'_'+result_xnlink['target_ip'].astype(str)
result_xnlink.dropna(subset=['DN'], inplace=True)
result_xnlink =result_xnlink.drop_duplicates(['xnlink_dup_key'], keep ='first',ignore_index = True)

### Case C : intra to inter conversioning, producing New XNLINK for inter HO
c_input_xnlink_info=pd.DataFrame(columns=range(5))

c_input_xnlink_info.columns = ['before_gnbid', 'before_gnbip','after_gnbId','after_gnbip','version']

c_input_xnlink_info['before_gnbid']=input_xnlink_info['before_gnbid']
c_input_xnlink_info['before_gnbip']=input_xnlink_info['before_gnbip']
c_input_xnlink_info['after_gnbId']=input_xnlink_info['after_gnbId']
c_input_xnlink_info['after_gnbip']=input_xnlink_info['after_gnbip']

       
"""     
for index,row in c_input_xnlink_info.iterrows():
    for index2,row2 in target_xnlink_info.iterrows():
        if (str(row["before_gnbid"])==str(row2["source_gnb"])):
            row["version"]=row2["version"]
            break
                
"""

for index,row in c_input_xnlink_info.iterrows():
    row["version"]="NRBTSCL22R1_2109_102"
            



inter_xnlink_dic={} 

df_inter_xnlink=pd.DataFrame(columns=range(4))
df_inter_xnlink.columns=['version','target_ip','source_gnb','xnlink_dup_key']
len(inter_xnlink_dic)

############# 04/21 intra -> inter 코드 수정###########################
############# 04/21 cell
for index,row in c_input_xnlink_info.iterrows():
    for index2,row2 in c_input_xnlink_info.iterrows():
        if (str(row["before_gnbid"]) == str(row2["before_gnbid"]) and str(row["after_gnbId"]) != str(row2["after_gnbId"]) ):
            new_list_xnlink = {
                'version': row2["version"],
                'target_ip': row2["after_gnbip"],
                'source_gnb':row["after_gnbId"],
                'xnlink_dup_key':row["after_gnbId"]+"_"+row2["after_gnbip"]
                }
            df_inter_xnlink=df_inter_xnlink.append(new_list_xnlink,ignore_index=True)
           

for index,row in c_input_xnlink_info.iterrows():
        new_list_xnlink = {
            'version': row["version"],
            'target_ip': row["before_gnbip"],
            'source_gnb':row["after_gnbId"],
            'xnlink_dup_key':row["after_gnbId"]+"_"+row["before_gnbip"]
            }
        df_inter_xnlink=df_inter_xnlink.append(new_list_xnlink,ignore_index=True)
        new_list_xnlink = {
            'version': row["version"],
            'target_ip': row["after_gnbip"],
            'source_gnb':row["before_gnbid"],
            'xnlink_dup_key':row["before_gnbid"]+"_"+row["after_gnbip"]
            }
        df_inter_xnlink=df_inter_xnlink.append(new_list_xnlink,ignore_index=True)
       





df_inter_xnlink=df_inter_xnlink.drop_duplicates(['xnlink_dup_key'], keep ='first',ignore_index = True)
############################################################################   
#############################################################



for index3,row3 in result_xnlink.iterrows():
     if (row3["after_gnbip"]==row3["target_ip"]):
         result_xnlink=result_xnlink.drop([index3])        #result_nradjgnb.drop(result_nradjgnb.index[index3],inplace=True)
            




result_xnlink=result_xnlink.drop(['before_gnbip','after_gnbip','key_xnlink','DN','NN1','NN2'], axis=1)
result_xnlink=result_xnlink.append(df_inter_xnlink,ignore_index=True)
result_xnlink['xnlink_dup_key']=result_xnlink['source_gnb'].astype(str)+'_'+result_xnlink['target_ip'].astype(str)
result_xnlink =result_xnlink.drop_duplicates(['xnlink_dup_key'], keep ='first',ignore_index = True)


def get_copy_xnlink_list(new_dic_xnlink, df):
    for index,row in df.iterrows():
        key_idx = row['source_gnb']
        for k in range(0, 256):
            if ((key_idx + "_" + str(k)) not in xnlink_dic):
                new_dic_xnlink.append(
                ['PLMN-PLMN/MRBTS-' + str(key_idx) + '/NRBTS-' + str(key_idx) + '/XNLINK-' + str(k),'create',str(row['version']),str(row['target_ip']),'0'])
                xnlink_dic[(key_idx + "_" + str(k))] = {}
                xnlink_nradjgnb_dic[str(row['xnlink_dup_key'])]= str(k)
                break

result_xnlink.to_csv(path_new_xnlink, index=False, header=False)


dt_xnlink=pd.DataFrame()  

get_copy_xnlink_list(new_dic_xnlink,result_xnlink)         
dt_xnlink=pd.DataFrame(new_dic_xnlink)   




if (dt_xnlink.empty != True):
    output_format3 = pd.DataFrame({'1': [None,'com.nokia.srbts.nrbts:XNLINK', '$dn', None, None], '2': [None, None, '$operation', None, None],'3': [None, None, '$version', None, None], '4': [None, None, 'cPlaneIpAddr', None, None], '5': [None, None, 'cPlaneIpAddrCtrl', None, None]})
    dt_xnlink.columns = ['1', '2','3','4','5']
    pd.concat([output_format3, dt_xnlink],axis=0,sort=False).to_csv(path_sub_copy_xnlink, index=False, header=False)



modify_result_xnlink = pd.merge(modify_input_xnlink_info,modify_target_xnlink_info, how='left', left_on='modify_xnlink_key', right_on='modify_xnlink_key')

elements = modify_result_xnlink['DN'].str.split("/", expand=True)
NRBTS = elements[2].str.split("-", expand=True)
modify_result_xnlink['source_gnb'] = NRBTS[1]
elements=None
modify_result_xnlink["NN"]=modify_result_xnlink['source_gnb']+'_'+modify_result_xnlink['target_ip']+'_'+modify_result_xnlink['after_gnbip']
modify_result_xnlink =modify_result_xnlink.drop_duplicates(['NN'], keep ='first',ignore_index = True)
modify_result_xnlink.dropna(subset=['DN'], inplace=True)

modify_result_xnlink=modify_result_xnlink.drop(['before_gnbip','before_gnbid','after_gnbId','NN','modify_xnlink_key'], axis=1)

dud_result_xnlink = pd.merge(target_xnlink_info,modify_result_xnlink, how='left', left_on='key_xnlink', right_on='source_gnb')
dud_result_xnlink.dropna(subset=['source_gnb_y'], inplace=True)
elements = dud_result_xnlink['DN_x'].str.split("/", expand=True)
idx = elements[3].str.split("-", expand=True)
dud_result_xnlink['idx_xnlink'] = idx[1]
elements=None
dud_result_xnlink=dud_result_xnlink.drop(['version','target_ip_x','target_ip_y','DN_x','DN_y'], axis=1)

dud_result_xnlink.to_csv(path_sub_netact_xnlink, index=False, header=False)


xnlink = open(path_sub_netact_xnlink, 'r')
xnlink_lines = csv.reader(xnlink)
xnlink_dic2={}
for xnlink_l1 in xnlink_lines:
    key_idx = xnlink_l1[3]
    IDX_du = xnlink_l1[4] 
    if ((key_idx + "_" + str(IDX_du)) not in xnlink_dic2):
        xnlink_dic2[(key_idx+"_"+IDX_du)] = {}
        NRBTS = xnlink_l1[4]
        xnlink_dic2[key_idx+"_"+IDX_du] = (NRBTS)

xnlink.close()




delete_result_xnlink=modify_result_xnlink










def get_xnlink_delete_list(delete_dic_xnlink, df):
    for index,row in df.iterrows():
        delete_dic_xnlink.append([str(row["DN"]),'delete',str(row["target_ip"]),'0'])


modify_result_xnlink.sort_values(by=['DN'],inplace=True)

get_xnlink_delete_list(delete_dic_xnlink,modify_result_xnlink)      
   


dt_delete_xnlink=pd.DataFrame(delete_dic_xnlink)



if (dt_delete_xnlink.empty != True):
    output_format3 = pd.DataFrame({'1': [None,'com.nokia.srbts.nrbts:XNLINK', '$dn', None, None], '2': [None, None, '$operation', None, None], '3': [None, None, 'cPlaneIpAddr', None, None], '4': [None, None, 'cPlaneIpAddrCtrl', None, None]})
    dt_delete_xnlink.columns = ['1', '2','3','4']
    pd.concat([output_format3, dt_delete_xnlink],axis=0,sort=False).to_csv(path_sub_delete_xnlink, index=False, header=False)



####중복제거



modify_result_xnlink['target_ip']=modify_result_xnlink['after_gnbip']
modify_result_xnlink['NN']=modify_result_xnlink['source_gnb']+'_'+modify_result_xnlink['target_ip']
modify_result_xnlink = modify_result_xnlink.drop_duplicates(['NN'], keep ='first',ignore_index = True)



xnlink_nradjgnb_dic2={}
def get_xnlink_modify_list(modify_dic_xnlink, df):
    for index,row in df.iterrows():
        key_idx = str(row["source_gnb"])
        ip = str(row["target_ip"])
        xnlinkref_key=str(key_idx)+"_"+str(ip)
        for k in range(0, 256):
            if ((key_idx + "_" + str(k)) not in xnlink_dic2):
                modify_dic_xnlink.append(
                ['PLMN-PLMN/MRBTS-' + str(key_idx) + '/NRBTS-' + str(key_idx) + '/XNLINK-' + str(k),'create','',str(ip),'0'])
                xnlink_dic2[(key_idx + "_" + str(k))] = {}
                xnlink_nradjgnb_dic2[xnlinkref_key]= str(k)
                break

get_xnlink_modify_list(modify_dic_xnlink,modify_result_xnlink)         


dt_modify_xnlink=pd.DataFrame(modify_dic_xnlink)



if (dt_modify_xnlink.empty != True):
    output_format3 = pd.DataFrame({'1': [None,'com.nokia.srbts.nrbts:XNLINK', '$dn', None, None], '2': [None, None, '$operation', None, None],'3': [None, None, '$version', None, None], '4': [None, None, 'cPlaneIpAddr', None, None], '5': [None, None, 'cPlaneIpAddrCtrl', None, None]})

    dt_modify_xnlink.columns = ['1', '2','3','4','5']
    pd.concat([output_format3, dt_modify_xnlink],axis=0,sort=False).to_csv(path_sub_ngbrmodify_xnlink, index=False, header=False)











## Preparing to Eliminate Duplicated DU info, Cell info






print("========================================================================================================================")
print("========================================================================================================================")
print(">>>>>>>>>>>>>>>>>>>> Target NRADJNRCELL DATA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
print("\n")
print(target_nradjnrcell_info)
print("\n")
print(">>>>>>>>>>>>>>>>>>>> Elimininated duplicate NRADJNRCELL DATA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
print("\n")

print(">>>>>>>>>>>>>>>>>>>> Target NRREL DATA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
print("\n")
print(target_nrrel_info)
print("\n")
print(">>>>>>>>>>>>>>>>>>>> Elimininating duplicate NRREL DATA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
print("\n")

print("\n")
print("========================================================================================================================")
print("========================================================================================================================")
print("\n\n")
print("[4]  Generating Sub files....")


print("[5]  Main Function start(Generating PLAN Data)......................")    
print("[6]  If the Target&Input Data are BIG, it will take several minutes.")
print(".\n.\n.\n.\n.\n")

## operate function


print("[7]  Main Function FINISHED(Generating PLAN Data)..................")  

print("[8]  Making Plan...............")

print("[9]  Plan Making Completed!!!")


print(len(result_nrrel))
print(len(modify_result_nrrel)*2)





copyFile_list = glob.glob(os.path.join(current_path, 'sub_copy_*.csv'))
alldata = []
for file in copyFile_list:
    df= pd.read_csv(file)
    alldata.append(df)

datacomb_copy = pd.concat(alldata,axis=1,sort=False).to_csv(path_output_PLAN, index=False, header=False)




modifyFile_list = glob.glob(os.path.join(current_path, 'sub_modify_*.csv'))
alldata = []
for file in modifyFile_list:
    df= pd.read_csv(file)
    alldata.append(df)

datacomb_modify = pd.concat(alldata,axis=1,sort=False).to_csv(path_modify_PLAN, index=False, header=False)


ngbrdeleteFile_list = glob.glob(os.path.join(current_path, 'sub_ngbrdelete_*.csv'))
alldata = []
for file in ngbrdeleteFile_list:
    df= pd.read_csv(file)
    alldata.append(df)

datacomb_ngbrdelete = pd.concat(alldata,axis=1,sort=False).to_csv(path_DU20delete_PLAN, index=False, header=False)

ngbrcreateFile_list = glob.glob(os.path.join(current_path, 'sub_ngbrmodify_*.csv'))
alldata = []
for file in ngbrcreateFile_list:
    df= pd.read_csv(file)
    alldata.append(df)

datacomb_ngbrmodify = pd.concat(alldata,axis=1,sort=False).to_csv(path_DU20modify_PLAN, index=False, header=False)





print("[10]  generating Combined .csv file")

print("[11] All process of Plan Making tool is completed..")
print(".\n.\n.\n")
print("[12]  Press <esc> key to turn off this tool. ")
print("\n")
os.system('Pause')



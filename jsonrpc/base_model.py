#!/usr/bin/env python3
import numpy as np
import math
import scipy.io
import pickle
import os

begin_position=-50
end_position=-10
flanking_len=5

def change_precision(a):
    b=("%.6f" % a)
    return b


def transform2window(flanking_segment):
     segment_vectors=[]
     for i in range(flanking_len,-begin_position+flanking_len-5):
            segment_vectors.append(flanking_segment[i-5:i+4])
     return segment_vectors

def calculateSparse(flanking_segment):
    dict= {'A':'1000', 'C':'0100','G':'0010','T':'0001'}
    num=len(flanking_segment)
    seq_str=''
    for i in range(0,num):
        seq_str=seq_str+dict.get(flanking_segment[i])
    vector=[]
    for i in range(0,len(seq_str)):
        vector.append(int(seq_str[i]))
        # vector=np.concatenate((vector,int(seq_str[i])))
    return vector

def calculateBiSparse(flanking_segment):
    dict= {'AA':'0000', 'AC':'0001','CA':'0010','AG':'0011','GA':'0100','AT':'0101','TA':'0110','CC':'0111','CG':'1000','GC':'1001', 'CT':'1010','TC':'1011','GG':'1100','GT':'1101','TG':'1110','TT':'1111'}
    seq_str=''
    for i in range(0,len(flanking_segment)-1):
        seq_str=seq_str+dict.get(flanking_segment[i:i+2])
    vector=[]
    for i in range(0,len(seq_str)):
        vector.append(int(seq_str[i]))
    return vector

def calculate_in_Markov(seq,probability_matrix_P,probability_matrix_N):
    dict= {'A':0, 'C':1,'G':2,'T':3,'AC':4,'AG':5,'AT':6,'CG':7,'CT':8,'GT':9,'CA':10,'GA':11,'TA':12,'GC':13,'TC':14,'TG':15,'AA':16,'CC':17,'GG':18,'TT':19}
    probability_list=[]
    seq_len=len(seq)
    # print(seq)
    probability_list.append(probability_matrix_P[0][dict.get(seq[0])])

    p=probability_matrix_P[0][dict.get(seq[0])]
    for i in range(1,seq_len):
        conditional_probability=probability_matrix_P[dict.get(seq[i-1:i+1])][i]*1.0/probability_matrix_P[dict.get(seq[i-1])][i]
        probability_list.append(conditional_probability)
        p=p*conditional_probability

    n=probability_matrix_N[0][dict.get(seq[0])]
    for i in range(1,seq_len):
        conditional_probability=probability_matrix_N[dict.get(seq[i-1:i+1])][i]*1.0/probability_matrix_N[dict.get(seq[i-1])][i]
        probability_list.append(conditional_probability)
        n=n*conditional_probability

    if n!=0:
        return math.log(p/n)
    else:
        return 0

def getMorkovfeatureVector(flanking_segment,probability_matrix_P,probability_matrix_N):
    seqs=transform2window(flanking_segment)
    vector=[]
    for i in range(0,len(seqs)):
        vector=np.concatenate((vector,[calculate_in_Markov(seqs[i],probability_matrix_P,probability_matrix_N)]))
    return vector


def calculate_in_pssm(seq,PSSM):
    length=len(seq)
    feature=0
    for i in range(0,length):
       feature=feature+(PSSM.get(seq[i]))[i]
    return feature


def getPSSMfeatureVector(flanking_segment,pssm):
   seqs=transform2window(flanking_segment)
   train_vector=[]
   for i  in range(0,len(seqs)):
        train_vector=np.concatenate((train_vector,[calculate_in_pssm(seqs[i],pssm)]))
   return train_vector


def sequence_encode(seq):  # -55-0
     base_dir = os.path.dirname(os.path.realpath(__file__))
     strname=base_dir+'/parameter/round_'+str(0)+'_parameter.txt'
     f=open(strname,"rb")
     train_p_matrix=pickle.load(f)
     train_n_matrix=pickle.load(f)
     train_pssm=pickle.load(f)
     f.close()

     MorkovfeatureVector=getMorkovfeatureVector(seq,train_p_matrix,train_n_matrix)
     PSSMfeatureVector=getPSSMfeatureVector(seq,train_pssm)
     BiSparsefeatureVector=np.array(calculateBiSparse(seq))
     sparse_featureVector=np.array(calculateSparse(seq))

     # print(MorkovfeatureVector.shape)
     # print(PSSMfeatureVector.shape)
     # print(BiSparsefeatureVector.shape)
     # print(sparse_featureVector.shape)

     vector=list(np.concatenate((MorkovfeatureVector,PSSMfeatureVector,BiSparsefeatureVector,sparse_featureVector),axis=1))
     return vector

def get_predict_parameter():
    base_dir = os.path.dirname(os.path.realpath(__file__))
    pls_model= scipy.io.loadmat(base_dir+'/parameter/pls_model.mat')
    pls_model_W=pls_model['beta']
    cca_model= scipy.io.loadmat(base_dir+'/parameter/cca_model.mat')
    cca_model_W=cca_model['W']
    lscca_model= scipy.io.loadmat(base_dir+'/parameter/lscca_model.mat')
    lscca_model_W=lscca_model['W_x']
    normalize=scipy.io.loadmat(base_dir+'/parameter/normalize.mat')
    XmeanTrain=normalize['XmeanTrain']
    XmeanTrain=XmeanTrain.tolist()
    return  pls_model_W,cca_model_W,lscca_model_W,XmeanTrain[0]

def predict(seq):
     pls_model_W,cca_model_W,lscca_model_W,XmeanTrain=get_predict_parameter()
     X_dimension=len(XmeanTrain)
     vector=sequence_encode(seq)

     for i in range(0,X_dimension):
         vector[i]=vector[i]-XmeanTrain[i]

     pls_model_predict=np.matrix([1]+vector)*pls_model_W
     cca_model_predict=np.matrix(vector)*cca_model_W
     lscca_model_predict=np.matrix(vector)*lscca_model_W

     ensemble_predict=(pls_model_predict+cca_model_predict+lscca_model_predict)/3
     ensemble_predict_vector=np.array(ensemble_predict)[0]
     for i in range(0,len(ensemble_predict_vector)):
        ensemble_predict_vector[i]=change_precision(ensemble_predict_vector[i])
     return ensemble_predict_vector


def format_one_intron(intron_seq,intron_result):
    num=len(intron_seq)
    objects=[]
    y_pos = np.arange(num)
    for i in range(0,num):
      objects.append(intron_seq[i])
    #print(y_pos)
    #print(intron_result)
    '''
    plt.bar(y_pos, intron_result, align='center')

    plt.xticks(y_pos, objects)
    plt.ylabel('Usage')
    plt.title('Programming language usage')
    plt.savefig('temp.png')
    # print("<img src='/temp.png' width='300',height='100'></img><br>")
    '''
def branchpoint_predict(input_sequence):
    if (len(input_sequence)<55):
        return None
    else:
       seq=input_sequence[-55:]
       if 'N' in seq:
           return None
       result=predict(seq)
       format_one_intron(seq[5:45],result)
       return list(result)



branchpoint_predict('AGGACTTGGGCATATTTGGCCAATGTAACACATTTTTATGGTGATTGTTTTCTAG')
# print(branchpoint_predict('TATGGAGGACTTGGGCATATTTGGCCAATGTAACACATTTTTATGGTGATTGTTTTCTAG'))
# print(get_input_and_predict('TATTTGGCCAATGTAACACATTTTTATGGTGATTGTTTTCTAG'))

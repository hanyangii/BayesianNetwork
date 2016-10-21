from Calcurate_Posibility import *
import random
import sys

class TopoNode:
	def __init__(self, name, parent):
		self.name = name.split('\'')[0]
		self.parents=[]
		i=0
		for i in range(len(parent)):
			self.parents.append(parent[i])
		self.cpt=[pow(2,len(self.parents))]
		
	def cpt_cal(self, TrainData,FeatureName):
		for i in range(pow(2,len(self.parents))):
			cpt_val=P_CPT(i,TrainData, self.name, self.parents, FeatureName)
			self.cpt.append(cpt_val)

print sys.argv

TopologyFile = open(sys.argv[1],'rb')
InferenceFile = open(sys.argv[2],'rb')
TrainFile = open(sys.argv[3],'rb')

Topology=[]
Features=[]

#Topology File read
while True:
	line = TopologyFile.readline()
	line = line.strip('\r\n')
	if not line: break
	nodes=line.split(',')
	Features.append(nodes[0])
	node = TopoNode(nodes[0],nodes[1:]) 
	Topology.append(node)

#print Topology
TopologyFile.close()

TrainData =[]
#Train File read
#node name input
l = TrainFile.readline()
l = l.strip('\r\n')
FeatureName = l.split(',')

#features input
while True:
	line = TrainFile.readline()
	line = line.strip('\r\n')
	if not line: break
	features = line.split(',')
	TrainData.append(features)

TrainFile.close()

#CPT 
for i in range(len(Topology)):
	Topology[i].cpt_cal(TrainData,FeatureName)

#Prior Sampling 10000
SFile=open("Samples.txt",'wb')
Samples=[]
for i in range(10000):
	sample = [0 for col in range(len(Topology))]
	sample_feature=[0 for col in range(len(Topology))]
	tt=''
	for j in range(len(Topology)):
		rnd_num=random.uniform(0,1)
		sample[FeatureName.index(Topology[j].name)]=rnd_num
		
		sample_parent=[]
		for k in range(len(Topology[j].parents)):
			sample_parent.append(sample_feature[FeatureName.index(Topology[j].parents[k])])
		
		par_ind=0
		for k in range(len(sample_parent)):
			index=len(sample_parent)-1-k
			par_ind=par_ind + int(sample_parent[index])*pow(2,k)

		cpt_val = Topology[j].cpt[par_ind+1]
		#print Topology[j].cpt, j
		#print 'probability: ',cpt_val, par_ind
		if cpt_val>rnd_num:
			sample_feature[FeatureName.index(Topology[j].name)]='1'
			tt=tt+'1'
		else:
			sample_feature[FeatureName.index(Topology[j].name)]='0'
			tt=tt+'0'
	
	#print sample_feature
	Samples.append(sample_feature)
	SFile.write(tt+'\n')

SFile.close()
OutputFile = open("output.txt",'wb')
InferenceFile.readline()

#Read Inference file
Inference_query=[]
while True:
    	line = InferenceFile.readline()
	line = line.strip('\r\n')
	
	if ">" == line or not line:
		#print Inference_query
		output_line = ">\nP("
		parent_index=[]
		parent_fea=[]
		cur_index=''
		cur_val=''
		for i in range(len(Inference_query)):
			output_line=output_line+str(Inference_query[i][1])
			if i < len(Inference_query)-1:
				output_line=output_line+'|'
			tmp_line=str(Inference_query[i]).split('=')
			#print i
			if i == 0 :
				cur_index =  FeatureName.index(tmp_line[0].split("'")[3])
				#print 'ppp'
				#print cur_index
				cur_val = tmp_line[1].split("'")[0]
			else:
				parent_fea.append(tmp_line[1].split("'")[0])
				parent_index.append(FeatureName.index(tmp_line[0].split("'")[3]))
		
		son_num, paren_num = cnt_p(parent_fea, Samples, parent_index, cur_index)
		if cur_val == '0':
			son_num = paren_num-son_num
		output_line=output_line+")="+str(float(son_num)/float(paren_num))+"\n"
		#print output_line
		OutputFile.write(output_line)
		if not line: break
		Inference_query=[]

	else:
		line=line.split(':')
		#print line
		Inference_query.append(line)
	
InferenceFile.close()
OutputFile.close()

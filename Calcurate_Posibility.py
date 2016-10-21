def cnt_p(fea, TrainData, p_index, s_index):
	p_num=0
	s_num=0
	for i in range(len(TrainData)):
		t = TrainData[i]
		p_num = p_num+1
		temp=True
		for j in range(len(p_index)):
			if t[p_index[j]]!=fea[j]:
				p_num = p_num-1
				temp=False
				break
		if temp==True and t[s_index] == "1" : s_num = s_num+1
	return s_num, p_num


def P_CPT(i, TrainData, name, parent,FeatureName):
	binary = bin(i)
	parent_fea=binary[2:]
	if len(parent_fea)!=len(parent):
		ll = []
		for j in range(len(parent)-len(parent_fea)):
			ll.append('0')
		
		for j in range(len(parent_fea)):
			ll.append(parent_fea[j])
		parent_fea = ll
	parent_index=[]
	
	for i in range(len(parent)):
		parent_index.append(FeatureName.index(parent[i]))

	son_num, paren_num = cnt_p(parent_fea, TrainData, parent_index, FeatureName.index(name))
	return float(son_num)/float(paren_num)

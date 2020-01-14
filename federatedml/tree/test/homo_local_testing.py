import arch
from arch.api import session, WorkMode, Backend
import pandas as pd
import numpy as np
from federatedml.feature.instance import Instance
from federatedml.tree.homo_secureboosting_tree_guest import HomoSecureBoostingTreeGuest
from federatedml.param import DecisionTreeParam
from federatedml.param import BoostingTreeParam
from federatedml.param import ObjectiveParam
import copy

df = pd.read_csv(r'/home/cwj/FATE/standalone-fate-master-1.1.1/examples/data/breast_b.csv')
data_list = []
array = df.to_numpy()
for arr in array:
    inst = Instance(inst_id=arr[0],label=arr[1],features=arr[2:])
    data_list.append(inst)

session.init("a_job_id", WorkMode.STANDALONE, Backend.EGGROLL)
data1 = copy.deepcopy(data_list[0:20])
# data1.extend(data_list[:-100])
# print(len(data1))
dtable = session.parallelize(data1)
test_dtable = session.parallelize(data_list[-100:])
header = ['x0','x1','x2','x3','x4','x5','x6','x7','x8','x9']
dtable.schema['header'] = header

if __name__ == '__main__':
    boosting_tree_param = BoostingTreeParam(tree_param=DecisionTreeParam(max_depth=2,),num_trees=3,subsample_feature_rate=1,
                                            n_iter_no_change=False,bin_num=32,early_stopping=-1,validation_freqs=None,
                                            use_missing=True,objective_param=ObjectiveParam(objective='cross_entropy'),
                                            zero_as_missing=False)
    boosting_tree_guest = HomoSecureBoostingTreeGuest()
    boosting_tree_guest._init_model(boosting_tree_param)
    data = boosting_tree_guest.fit(dtable,None)
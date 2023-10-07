import random
import pandas as pd


Random_Seeds_Dict = {'Seeds':[]}
for i in range(5):
    random.seed(random.random())
    Random_Seeds_Dict['Seeds'].append(random.random())

Random_Arrival_Dict = {}
for i in range(5):
    Random_Arrival_Dict[i] = []
Random_ExpServTime_Dict = {}
for i in range(5):
    Random_ExpServTime_Dict[i] = []
Random_RookServTime_Dict = {}
for i in range(5):
    Random_RookServTime_Dict[i] = []
Random_TechServTime_Dict = {}
for i in range(5):
    Random_TechServTime_Dict[i] = []

for i in range(5):
    random.seed(Random_Seeds_Dict['Seeds'][i])
    for t in range(170000):
        n1 = random.random()
        Random_Arrival_Dict[i].append(n1)
        n2 = random.random()
        Random_ExpServTime_Dict[i].append(n2)
        n3 = random.random()
        Random_RookServTime_Dict[i].append(n3)
        n4 = random.random()
        Random_TechServTime_Dict[i].append(n4)


Random_Arrival_DF = pd.DataFrame(Random_Arrival_Dict)
Random_ExpServTime_DF = pd.DataFrame(Random_ExpServTime_Dict)
Random_RookServTime_DF = pd.DataFrame(Random_RookServTime_Dict)
Random_TechServTime_DF = pd.DataFrame(Random_TechServTime_Dict)

# create a excel writer object
with pd.ExcelWriter(r'D:/Term 6/Fundamentals of Simulation/Project/RandomNumbersS2.xlsx') as writer:
   
    # use to_excel function and specify the sheet_name and index
    # to store the dataframes in specified sheet
    Random_Arrival_DF.to_excel(writer, sheet_name="Arrival", index=False)
    Random_ExpServTime_DF.to_excel(writer, sheet_name="Expert", index=False)
    Random_RookServTime_DF.to_excel(writer, sheet_name="Rookie", index=False)
    Random_TechServTime_DF.to_excel(writer, sheet_name="Technical", index=False)
    

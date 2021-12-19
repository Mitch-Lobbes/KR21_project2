#test.create_bn(variables = ["R", "E", "A", "C", "B"], edges = [("E", "R"), ("E", "A"), ("B", "A"), ("A", "C")], cpts = {'R': [1, 2], 'E': [3,4], 'A': [5,6], "C": [3,4], "B": [8,9]})
pruning = FrenchPruning()

pruning.run(bn=test, query={'Wet Grass?'}, evidence={'Winter?': True, 'Rain?': False})

data_1 = {'B': [True, True, True, True, False, False, False, False],
          'C': [True, True, False, False, True, True, False, False],
          'D': [True, False, True, False, True, False, True, False],
          'p': [0.95, 0.05, 0.9, 0.1, 0.8, 0.2, 0, 1]}

df_1 = pd.DataFrame(data=data_1)

data_2 = {'D': [True, True, False, False],
          'E': [True, False, True, False],
          'p': [0.448, 0.192, 0.112, 0.248]}

df_2 = pd.DataFrame(data=data_2)

factors = [df_1, df_2]

f = pruning.multi_fly(factors=factors)

print(f)

#test.draw_structure()

#reasoner = BNReasoner(test)
#
# d_seperator = DSeparated()
#
#
# X = set('R')
# Y = set('C')
# Z = set([])
#
# result = d_seperator.d_separated(
#     bayesNet=reasoner.bn,
#     X=X,
#     Z=Z,
#     Y=Y
# )
#
# print(result)

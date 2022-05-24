import pandas as pd
df1=pd.read_csv("проба.csv", encoding='ansi',sep=';')
def rule(q_min, q_25,q_50,q_75,q_max,x):
    
    if int(x) <= q_25:
         return(str(q_min)+'-'+str(q_25))
    elif int(x)<=q_50:
         return(str(q_25)+'-'+str(q_50))
    elif int(x)<=q_75:
         return(str(q_50)+'-'+str(q_75))
    elif int(x)<=q_max:
         return(str(q_75)+'-'+str(q_max))

def quartel(col):
    quartels=df1[col].quantile([0.25,0.5,0.75])
    qu=[df1[col].min()]
    for q in quartels:
        qu.append(round(q))
    qu.append(df1[col].max())
    return(qu)

def handling():
    uni={}
    num_df=df1._get_numeric_data() 
    num_df.columns
    for col in df1.columns:

        if col!='Id товара' and col!='название':
            if col in num_df.columns:
                qu=quartel(col)
                df1[col] = df1[col].apply(lambda x: rule(qu[0],qu[1],qu[2],qu[3],qu[4],x))
            uni[str(col)]=len(df1[col].unique())
    uni
    sorted_values = sorted(uni.values()) 
    sorted_dict = {}
    for i in sorted_values:
        for k in uni.keys():
            if uni[k] == i:
                sorted_dict[k] = uni[k]

    true_list=['Id товара','название']+list(sorted_dict.keys())
    df2 = df1[true_list]
    df2.to_csv("dataset.csv", encoding='ansi',sep=';',index=False)

handling()


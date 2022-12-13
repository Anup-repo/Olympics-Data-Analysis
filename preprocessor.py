import pandas as pd


def preprocess(df,region_df):
    #checking for only summer
    df=df[df["Season"]=="Summer"]
    #merging the data with region
    df= df.merge(region_df,on="NOC",how="left")
    #deleting all the duplicate rows
    df.drop_duplicates(inplace=True)
    #performing one hot encoding 
    df=pd.concat([df,pd.get_dummies(df["Medal"])],axis=1)
    return df
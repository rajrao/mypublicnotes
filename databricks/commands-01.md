Based on **Basic EDA with Azure Databricks** from https://docs.microsoft.com/en-us/learn/modules/perform-exploratory-data-analysis-with-azure-databricks/3-complete-labs-in-databricks

Run a cell: SHIFT + ENTER

1. Create dataFrame (Spark DF)
   
       df = spark.sql("SELECT * FROM usedcars_csv1")
1. Display the DF

       df
1. Display the data
      
        display(df)      
1. Convert PySpark DF to Pandas

       pdf = df.toPandas()
       
      [Pandas vs PySpark DF](https://databricks.com/blog/2015/08/12/from-pandas-to-apache-sparks-dataframe.html)
1. Show top 10 as raw

       df.head(10)
1. Show top 10 with ascii table formatting

       df.show(10)
1. Show info about the DF (types, columns)

        df.dtypes
1. Display summaries for all columns

        summary = df.describe()
        display(summary)
1. Display summary for a column called Price

        display(df.describe('Price'))
1. Type the data in a DF

        df_typed = spark.sql("SELECT cast(Price as int), cast(Age as int), cast(KM as int), FuelType, cast(HP as int), cast(MetColor as int), cast(Automatic as int), cast(CC as int), cast(Doors as int), cast(Weight as int) FROM usedcars_#####")
df_typed
1. Display distinct values

        display(df_typed.select("FuelType").distinct())
1. Replace values

        df_cleaned_fueltype = df_typed.na.replace(["Diesel","Petrol","CompressedNaturalGas","methane","CNG"],["diesel","petrol","cng","cng","cng"],"FuelType")
display(df_cleaned_fueltype.select("FuelType").distinct())
1. Cleanup of NULLs

        df_cleaned_of_nulls = df_cleaned_fueltype.na.drop("any",subset=["Price", "Age", "KM"])
        display(df_cleaned_of_nulls.describe())
1. Save DF as a table

        df_cleaned_of_nulls.write.mode("overwrite").saveAsTable("usedcars_clean_csv1")
1. Plot the data using defaults

        %sql
        SELECT Price, Age FROM usedcars_clean_##### WHERE FuelType = 'petrol'
1. Plot using MatPlotLib and Pandas

        import matplotlib.pyplot as plt
        import numpy as np
        import seaborn as sns
        
        fig, ax = plt.subplots()
        pdf = df_cleaned_of_nulls.toPandas()
        ax.scatter(pdf.Age, pdf.Price)
        
        display(fig)
1. Plot Histograpm

        fig, ax = plt.subplots()
        
        bins= np.arange(0, 250000, 5000)
        pdf['KM'].plot(kind='hist')
        
        display(fig)

1. Scatter plot

        fig, ax = plt.subplots()
        ax.scatter(pdf.KM, pdf.Price)
        display(fig)

1. Generate a Correlation Matrix (color coded)

        fig, ax = plt.subplots()
        sns.heatmap(pdf[['Price','Age', 'KM', 'Weight', 'CC', 'HP']].corr(),annot=True, center=0, cmap='BrBG', annot_kws={"size": 14})
        display(fig)
        
 1. Generate a correlation matrix
 
        #create plot objects
        fig, ax = plt.subplots()
        #filter the df for data regarding diesel records
        dieselDf = pdf.query('FuelType=="diesel"')
        #generate heatmap
        sns.heatmap(dieselDf[['Price','Age', 'KM', 'Weight', 'CC', 'HP']].corr(),annot=True, center=0, cmap='BrBG', annot_kws={"size": 14})
        display(fig)

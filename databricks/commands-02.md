Based on **Advanced EDA with Azure Databricks** from https://docs.microsoft.com/en-us/learn/modules/perform-exploratory-data-analysis-with-azure-databricks/3-complete-labs-in-databricks

1. Create a DF from SQL

        import numpy as np
        import pandas as pd

        df = spark.sql("SELECT * FROM usedcars_clean_csv1")
1. train a parsimonious model, a basic model to get a sense of the predictive capability of our data

        df_affordability = df.selectExpr("Age","KM", "CASE WHEN Price < 12000 THEN 1 ELSE 0 END as Affordable")
        display(df_affordability)
1. Convert to arrays

        X = df_affordability.select("Age", "KM").toPandas().values
        y = df_affordability.select("Affordable").toPandas().values
1. Scale data

        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
1. View scaled data

        print(pd.DataFrame(X).describe().round(2))
        print(pd.DataFrame(X_scaled).describe().round(2))
1. Train model

        from sklearn import linear_model
        # Create a linear model for Logistic Regression
        clf = linear_model.LogisticRegression(C=1)

        # we create an instance of Neighbours Classifier and fit the data.
        clf.fit(X_scaled, y)
1. Widgets

        dbutils.widgets.text("Age","40", "Age (months)")
        dbutils.widgets.text("Distance Driven", "40000","Distance Driven (KM)")
1. Use widgest to check model

        age = int(dbutils.widgets.get("Age"))
        km = int(dbutils.widgets.get("Distance Driven"))

        scaled_input = scaler.transform([[age, km]])

        prediction = clf.predict(scaled_input)

        print("Can I afford a car that is {} month(s) old with {} KM's on it?".format(age,km))
        print("Yes (1)" if prediction[0] == 1 else "No (1)")\
        
1. x

        scaled_inputs = scaler.transform(X)
        predictions = clf.predict(scaled_inputs)
        print(predictions)

1. Print model accuracy

         from sklearn.metrics import accuracy_score
         score = accuracy_score(y, predictions)
         print("Model Accuracy: {}".format(score.round(3)))
         
 1. One-Hot encoding
 
        df_ohe = df.toPandas().copy(deep=True)
        df_ohe['FuelType'] = df_ohe['FuelType'].astype('category')
        df_ohe = pd.get_dummies(df_ohe)

        df_ohe.head(15)
1. Scaled dataset

        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        columns_to_scale = ['Age', 'KM', 'HP', 'CC','Weight']
        df_ohe_scaled = df_ohe.dropna().copy()
        df_ohe_scaled[columns_to_scale] = scaler.fit_transform(df_ohe.dropna()[columns_to_scale])

        df_ohe_scaled.head(15)

1. Dimensional reduction

        from sklearn.decomposition import PCA 
        import matplotlib.pyplot as plt
        import seaborn as sns

        fig, ax = plt.subplots()

        features = ['Age', 'KM', 'HP', 'Weight', 'CC', 'Doors',  'Automatic', 'MetColor', 'FuelType_cng', 'FuelType_diesel', 'FuelType_petrol']

        x_2d = PCA(n_components=2).fit_transform(df_ohe_scaled[features])
        sc = plt.scatter(x_2d[:,0], x_2d[:,1], c=df_ohe_scaled['Price'], s=10, alpha=0.7)
        plt.colorbar(sc) 

        display(fig)
1. Estimate Feature Importance

        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split

        fig, ax = plt.subplots()

        features_RFR = ['Age', 'KM', 'HP', 'Weight', 'CC', 'Doors', 'Automatic', 'MetColor', 'FuelType_cng', 'FuelType_diesel', 'FuelType_petrol']

        # Create train and test data
        X = df_ohe[features_RFR].as_matrix()
        y = df.toPandas()['Price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state =0)

        # Initialize  a random forest regressor
        # 'Train' the model
        RandomForestReg = RandomForestRegressor()
        RandomForestReg.fit(X_train, y_train)

        imp = pd.DataFrame(
                RandomForestReg.feature_importances_ ,
                columns = ['Importance'] ,
                index = features_RFR
            )
        imp = imp.sort_values( [ 'Importance' ] , ascending = True )
        imp['Importance'].plot(kind='barh')

        display(fig)
      
        

# Predicting Churn of Teclo through Machine Learning
Utilising Kaggle Telco Customer Churn's [dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn/data) to predict the customer churn of a telco company.

## Project Overview

A telco company would like to know which existing customers will continue their subscriptions for another month, and which are likely to end their contract.

This project aims to study whether it is possible to predict the churn of a telco company.

### Data Overview

The data is provided through a csv file:
```WA_Fn-UseC_-Telco-Customer-Churn.csv```

The data set includes information about:

 - Customers who left within the last month – the column is called Churn
- Services that each customer has signed up for – phone, multiple lines, internet, online security, online backup, device protection, tech support, and streaming TV and movies
- Customer account information – how long they’ve been a customer, contract, payment method, paperless billing, monthly charges, and total charges
- Demographic info about customers – gender, age range, and if they have partners and dependents

## Data Understanding

EDA was achieved by plotting various graphs such as bar chats and stacked bar charts to understand the relationships between the variables. A heatmap was plotted to investigate correlation, and further investigated through Variable Inflation Factors (VIF).

Because of the number of categorical columns, label encoding and one-hot encoding were used on certain columns. For those with less than 2 unique categories, label encoding was utilised. For those with more than 2, one-hot encoding was preferred. It was discovered through Exploratory Data Analysis that the dataset did not have missing values, and there was some strong positive correlation between variables. Through VIF, I was able to determine multi collinearity between some the payments features.

## Modeling and Evaluation

The dataset was split with `train_test_split` into a 80% train and 20% test set. Due to the inclusion of payment charges variables, StandardScaler was used to standardise the features.

As the number of columns were large, Principal Component Analysis was utilised to reduce the dimensionality of the results. To find the optimum number of PCA components selected, I chose to keep up to 95% of variance, which yields 18 variables. This is down from 39 initial columns. These were then used to transform the existing X training and test sets.

As the predictor variable is on churn where `1` represents leaving and `0` represents staying this is a binary logistic problem.

The following models were used and compared against:
- Logistic Regression
- Support Vector Machine (Linear and RBF)
- K-Nearest Neighbours
- Naive Bayes (Gaussian)
- Decision Tree Classifier
- Random Forest Classifier

The metric chosen was to compare the ROC AUC score. Through running and comparing the models, it was discovered that `Logistic Regression` and `Linear SVC` outperformed the other models.

I further improved some models for comparison such as finding the optimal K for K-nearest based on iterative testing, and for Random Forest, I tested for optimal n_estimators. 

For second reiteration, the consideration shifted to testing for precision, recall and F2 scores as the ideal metric. This was as False Negatives are more costly for a churn (in my opinion).

After comparing all the methods, the best model was found to be Logistic Regression which has the best balance between Precision and Recall.

Finally, GridSearch was utilised to find the best hyper parameters, concluding with a Logistic Regression model with 71% accuracy. As an added bonus, I build a propensity score besides the absolute predicted outcome so that there is an additional layer of highlighting the percentage probability to take action.

## Conclusion

The model achieved a relatively high accuracy of 71%, however there are ways to perform better.

In the initial stage, I made the decision to instantly perform PCA on the number of features. Instead, I could have eliminated more features first based on the correlation score to 'Churn', which will cut down the number of features for modeling that can introduce more uncertainty.

I was also able to learn from this project about PCA and how it works as I did not understand how to reduce the number of features to be tested well. I also learnt about business thinking and including a propensity score which can better manage the predictions and actions taken.

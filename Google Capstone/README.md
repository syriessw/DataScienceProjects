# Providing data-driven suggestions for HR on employee churn
Utilising Kaggle Telco Customer Churn's [dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn/data) to predict the customer churn of a telco company.

## Project Overview

The HR department at Salifort Motors wants to take some initiatives to improve employee satisfaction levels at the company. They collected data from employees, but now they don’t know what to do with it. They refer to you as a data analytics professional and ask you to provide data-driven suggestions based on your understanding of the data. They have the following question: what’s likely to make the employee leave the company?

Your goals in this project are to analyze the data collected by the HR department and to build a model that predicts whether or not an employee will leave the company.

If you can predict employees likely to quit, it might be possible to identify factors that contribute to their leaving. Because it is time-consuming and expensive to find, interview, and hire new employees, increasing employee retention will be beneficial to the company.

### Data Overview

The data is provided through a csv file:
```HR_capstone_dataset.csv```

The data set includes information about:

 - `satisfaction_level` Employee-related satisfaction level [0-1]
- `last_evaluation` Score of employee's last performance review [0-1]
- `number_project` Number of projects employee contributes to
- `average_monthly_hours` Average number of hours employee worked per month
- `time_spend_company` How long the employee has been with the company (years)
- `Work_accident` Whether or not the employee experienced an accident while at work
- `left` Whether or not the employee has left the company
- `promotion_last_5years` Whether or not the employee was promoted in the last 5 years
- `Department` The employee's department
- `salary` The employee's salary (U.S. dollars)

## Data Understanding

EDA was achieved by plotting various graphs such as histograms and scatterplots to understand the relationships between the variables. It was evident that the employees were working far over the expected hours an average person was working, and there were very few positive evaluations. A heatmap was plotted to investigate correlation between variables which yielded results that `number_project`, `last_evaluation` and `average_monthly_hours` were positively related to `left`.

Because of the number of categorical columns, label encoding and one-hot encoding were used on certain columns. For `salary`, label encoding was used, while `Department` was one-hot encoded into various columns.

Prior investigation has led to discover that there are outliers regarding tenure in company which would not be effective for Logistic Regression. Hence there was consideration to remove outliers through IQR.

## Modeling and Evaluation

The dataset was split with `train_test_split` into a 75% train and 25% test set with stratification after discovering the size of `left` is not even.

As the predictor variable is on churn where `1` represents leaving and `0` represents staying this is a binary logistic problem.

The following models were used and compared against:
- Logistic Regression
- Decision Tree
- Random Forest Classifier

The metric chosen was to compare the precision score. Through running and comparing the models, it was discovered that `Decision Tree` and `Random Forest` outperformed `Logistic Regression`. GridSearch was used during this phase to find the best hyper parameters.

For second reiteration, I considered data leakage and chose to engineer a binary `overworked` column out of `average_monthly_hours`. I also eliminated `satisfaction_level` as a consideration that it cannot be presumed to be correct, or available all the time.

After comparing all the methods, the best model was found to be the former Decision Tree. Unfortunately, the feature engineering did not improve either Decision Tree nor Random Forest models.

On performing feature importance on both Decision Tree and Random Forest, it was confirmed that `last_evaluation`, `number_project` and `time_spend_company` are the most important features for the models. However, the order of importance was different between Decision Tree and Random Forest, leading to the difference in their performance.

## Conclusion

The Decision Tree model achieved an accuracy of 98.3%, Precision of 97.2%, Recall of 93.0% and F1 score or 95.1% which is very good.

The features importance confirmed that employees at the company are overworked and under appreciated. A few suggestions can be made to management to reduce the number of projects per individuals and spread out the workload. There should also be a look into the evaluation to reward everyone fairly. Finally, there can be consideration to look into other types of models such as KMeans or Naive Bayes.

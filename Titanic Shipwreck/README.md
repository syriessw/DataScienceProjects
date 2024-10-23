# Titanic Shipwreck Predictions through Machine Learning
Utilising Kaggle Titanic's [dataset](https://www.kaggle.com/competitions/titanic) to predict through a series of Machine Learning models on whether the passengers survived or not.

## Project Overview

The sinking of the Titanic is one of the most infamous shipwrecks in history.

On April 15, 1912, during her maiden voyage, the widely considered “unsinkable” RMS Titanic sank after colliding with an iceberg. Unfortunately, there weren’t enough lifeboats for everyone onboard, resulting in the death of 1502 out of 2224 passengers and crew.

While there was some element of luck involved in surviving, it seems some groups of people were more likely to survive than others.

In this challenge, the ask is to build a predictive model that answers the question: “what sorts of people were more likely to survive?” using passenger data (ie name, age, gender, socio-economic class, etc).

### Data Overview

The data has been split into two groups:

    training set (train.csv)
    test set (test.csv)

The dataset contains:
- survival
- pclass
- sex
- Age
- sibsp (# of siblings / spouses aboard the Titanic)
- parch (# of parents / children aboard the Titanic)
- ticket
- fare
- cabin
- embarked

__Variable Notes__

1. pclass: A proxy for socio-economic status (SES)
   - 1st = Upper
   - 2nd = Middle
   - 3rd = Lower

2. age: Age is fractional if less than 1. If the age is estimated, is it in the form of xx.5

3. sibsp: The dataset defines family relations in this way...
   - Sibling = brother, sister, stepbrother, stepsister
   - Spouse = husband, wife (mistresses and fiancés were ignored)

4. parch: The dataset defines family relations in this way...
   - Parent = mother, father
   - Child = daughter, son, stepdaughter, stepson
   - Some children travelled only with a nanny, therefore parch=0 for them.

## Data Understanding

`train.csv` was used to train the models, with feature engineering engaged on the features `sibsp`, `parch`.

EDA was achieved by plotting various graphs such as bar chats and histograms to understand the relationships between the variables.

For missing data, imputation was performed. As the `age` variable is missing from a significant portion of the dataset, a variety of imputation methods were considered, including Grouping imputation, K-Nearest Neighbour and Multivariate Imputation by Chained Equations. These were then compared to through their scores before deciding on best method for imputation.

Lastly, encoding was utilised. From the dataset, we can see that pclass has already been encoded. For remaining data, one-hot encoding was utilised.

## Modeling and Evaluation

As the predictor variable is on survival, where `1` represents survival and `0` represents death, this is a binary logistic problem.

The following models were used and compared against:
- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine (Linear and RBF)
- XGBoost Classifier
- K-Nearest Neighbour
- Naive Bayes (Gaussian)

The models were compared through using their Accuracy, Precision, Recall and F1 score. They were also cross-validated and GridSearch was used to find the hyper parameters.

Further reiteration of the models testing were done to attempt to improve the models. 

After comparing all the methods, the best model was found to be Random Forest which achieved an accuracy of 79%.

## Conclusion

The model achieved a relatively high accuracy of 79%, however there are ways to perform better.

In terms of feature engineering, perhaps it could be looked into eliminating `Title` altogether as a engineered feature as it did not add as much value as originally perceived. There can also be consideration of the `ticket` variable which was dropped as an unimportant feature before testing.

I was also able to learn from this project about more imputation methods to deal with missing data, and could see how much faster XGB library performs compared to sklearn.

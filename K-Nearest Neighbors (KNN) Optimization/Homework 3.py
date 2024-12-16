"""
DS2500
Homework 3
Janav Sama
Fall 2023

"""

# Importing necessary libraries and functions
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score

def min_max_normalize(column):
    
    """
    A function to perform min-max normalization on a given column of data.
    """
    
    return (column - column.min()) / (column.max() - column.min())

def accuracy_k(integer, X, y):
    
    """
    A function to compute the mean accuracy of a k-Nearest Neighbors classifier 
    with a specified integer value for 'k' using 4-fold cross-validation.
    """
    
    mean_accuracy = {}

    knn = KNeighborsClassifier(n_neighbors=integer)

    cross_fold = KFold(n_splits = 4, random_state = 0, shuffle = True)

    accuracy_scores = cross_val_score(knn, X, y, cv=cross_fold)
    mean_accuracy[integer] = accuracy_scores.mean()

    return mean_accuracy

def precision_k(integer, X, y):
    
    """
    A function to calculate the mean precision of a k-Nearest Neighbors 
    classifier with a specified integer value for 'k' using 4-fold 
    cross-validation.
    """
    
    precision_scores = []

    knn = KNeighborsClassifier(n_neighbors=integer)
    
    cross_fold = KFold(n_splits = 4, random_state = 0, shuffle = True)

    precision_scores = cross_val_score(knn, X, y, cv=cross_fold, 
                                       scoring = "precision")
    mean_precision = precision_scores.mean()
    
    return mean_precision

def recall_k(integer, X, y):
    
    """
    A function to compute the mean recall of a k-Nearest Neighbors classifier 
    with a specified integer value for 'k' using 4-fold cross-validation.
    """
    
    recall_scores = []

    knn = KNeighborsClassifier(n_neighbors=integer)
    
    cross_fold = KFold(n_splits = 4, random_state = 0, shuffle = True)

    recall_scores = cross_val_score(knn, X, y, cv=cross_fold, 
                                    scoring = "recall")
    mean_precision = recall_scores.mean()
    
    return mean_precision

def accuracy(X,y):
    
    """
    A function to find the best k value for a k-Nearest Neighbors classifier
    in terms of accuracy and display the results, including the best k and
    its corresponding maximum accuracy, as well as the lowest mean accuracy.
    """
    
    max_accuracy = -1
    best_k_accuracy = -1
    min_mean = 1 
    classifier = {}

    for i in range(4, 19):
        classifier = accuracy_k(i, X, y)
        if classifier[i] > max_accuracy:
            max_accuracy = classifier[i]
            best_k_accuracy = i
        if classifier[i] < min_mean:
            min_mean = classifier[i]

    print("Best k for Accuracy:", best_k_accuracy,
          "Max Accuracy:", max_accuracy)
    
    print(f"Lowest mean accuracy: {min_mean}")
    
def optimal(X, y, mean):
    
    """
    A function to find the optimal value of 'k' for a k-Nearest Neighbors 
    classifier based on a given mean function (precision, or recall) 
    and return the best 'k' value.
    """
    
    best_k = None  
    best_value = None  
    
    for i in range(4, 19):
        mean_val = mean(i, X, y)
        if best_k is None or mean_val > best_value:
            best_value = mean_val
            best_k = i

    return best_k


def plot_confusion_matrix(X_train, X_test, y_train, y_test,k):
    
    """
    A function to plot the confusion matrix for a k-Nearest Neighbors 
    classifier with a specified value of k using test data, 
    visualizing the predicted versus actual values.
    """

    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)

    y_pred = knn.predict(X_test)

    confusion_matrix = metrics.confusion_matrix(y_test, y_pred)
    
    sns.heatmap(confusion_matrix, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Predicted 0", "Predicted 1"],
                yticklabels=["Actual 0", "Actual 1"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix for k = 5 (Recall)")
    plt.show()

def plot_k_values_evaluation_precision_recall(X,y,best_k_precision, 
                                              best_k_recall):
    
    """
    A function to plot the evaluation of different values of 'k' 
    (number of neighbors) for a k-Nearest Neighbors classifier based on
    precision and recall scores, with vertical lines indicating the 
    optimal 'k' values for precision and recall.
    """   
    
    k_values = range(4, 19)  
    mean_precisions = [precision_k(k, X, y) for k in k_values]
    mean_recalls = [recall_k(k, X, y) for k in k_values]
    
    # Plot for k for precision and recall
    plt.figure(figsize=(10, 6))

    # Plot mean precision
    plt.plot(k_values, mean_precisions, label="Mean Precision", marker='o', 
             linestyle='-', color="red")
    
    # Plot mean recall
    plt.plot(k_values, mean_recalls, label="Mean Recall", marker='o', 
             linestyle='-', color="black")
    
    # Plotting details
    plt.axvline(x=best_k_precision, color='red', linestyle='--', 
                label=f"Optimal k for Precision: {best_k_precision}")
    plt.axvline(x=best_k_recall, color='black', linestyle='--', 
                label=f"Optimal k for Recall: {best_k_recall}")
    
    plt.title("Evaluation of k Values for Different Scoring Metrics")
    plt.xlabel("k (Number of Neighbors)")
    plt.ylabel("Mean Score")
    plt.legend()
    plt.show()
    

def analyze_insured_institutions(X_train, X_test, y_train, y_test,
                                 insured_institutions, institutions,
                                 insured_columns_to_normalize):
    
    """
    A function to analyze the performance of a k-Nearest Neighbors classifier
    on a dataset of insured institutions, including calculating the F1 score 
    for the 'Failed' class, counting the number of correctly predicted failed
    banks, and making predictions for a specific bank, such as "Southern 
    Community Bank of Fayetteville."
    """
    
    
    knn = KNeighborsClassifier(n_neighbors=12)
    knn.fit(X_train, y_train)

    y_pred = knn.predict(X_test)

    f1_failed = f1_score(y_test, y_pred)

    print(f"F1 score for the 'Failed' class: {f1_failed}")

    failed_banks = []

    for i in range(len(y_pred)):
        if y_pred[i] == 0 and y_test.iloc[i] == 0:
            failed_banks.append(y_pred[i])

    print("The number of banks that are predicted to fail and have" 
          "actually failed:", len(failed_banks))

    cert_number = 0

    insured_institutions["CERT"] = institutions["CERT"]

    for i in range(len(institutions)):
        if institutions["NAME"][i] == "Southern Community Bank"\
            and institutions["CITY"][i] == "Fayetteville":
            cert_number = institutions["CERT"][i]

    if cert_number is not None:
        X_specific_bank = insured_institutions[insured_institutions["CERT"] 
                                == cert_number][insured_columns_to_normalize]

        y_pred_specific_bank = knn.predict(X_specific_bank)

        if y_pred_specific_bank[0] == 1:
            print("The model predicts the failure of Southern Community\
                  Bank of Fayetteville.")
        else:
            print("The model predicts that Southern Community Bank of\
                  Fayetteville will not fail.")

def main():
    
    # Reading the files
    institutions = pd.read_csv("institutions.csv", low_memory = False)
    bank_list = pd.read_csv("banklist.csv", encoding ='cp1252')
    
    
    # Cleaning up the data using CERT values to determine if they are failed or not
    failed = institutions["CERT"].isin(bank_list["Cert "])
    failed = failed.replace({True: 1, False: 0})
    institutions["Failed?"] = failed

    # Columns where values that needs to be normalized are placed
    insured_columns_to_normalize = ['ASSET', 'DEP', 'DEPDOM', 'NETINC', 
                                    'OFFDOM', 'ROA', 'ROAPTX', 'ROE']

    # Creating a DataFrame with values only from the above columns 
    insured_institutions = pd.DataFrame\
        (institutions[insured_columns_to_normalize])

    # Removing the empty values/cells from the DataFrame
    insured_institutions = insured_institutions.dropna\
        (subset = insured_columns_to_normalize)

    # Normalizing the values
    for column in insured_columns_to_normalize:
        insured_institutions[column] = \
            min_max_normalize(insured_institutions[column])

    # Readding the "Failed?" column (was removed earlier to make 
                                        # normalization possible)
    insured_institutions["Failed?"] = failed

    
    # Part 1 
    
    X = insured_institutions[insured_columns_to_normalize]
    y = insured_institutions["Failed?"]
  
    # Question 1 and 2
    accuracy(X,y)
    
    # Question 3
    best_k_precision = optimal(X,y,precision_k)

    print(f"Best k for Precision: {best_k_precision}")

    # Question 4
    best_k_recall = optimal(X,y,recall_k)

    print(f"Best k for Recall: {best_k_recall}")
    
    # Question 5
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    analyze_insured_institutions(X_train, X_test, y_train, y_test,
                                 insured_institutions, institutions,
                                 insured_columns_to_normalize)
    
    # Part 2
    
    # Plot 1: Confusion Matrix
    plot_confusion_matrix(X_train, X_test, y_train, y_test,best_k_recall)
       
    # Part 2: A line plot with showing optimal values of k
    plot_k_values_evaluation_precision_recall(X,y,
                                              best_k_precision, best_k_recall)

if __name__ == "__main__":
    main()

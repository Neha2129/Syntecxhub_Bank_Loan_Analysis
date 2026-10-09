USE bank_loan_analysis;
SELECT COUNT(*) FROM credit_train;

SELECT COUNT(*) AS Total_Rows
FROM credit_train;

SELECT `Loan Status`, COUNT(*) AS Applications
FROM credit_train
GROUP BY `Loan Status`;

DESCRIBE credit_train;

SELECT `Term`, COUNT(*) AS Applications
FROM credit_train
GROUP BY `Term`;

SHOW COLUMNS FROM credit_train;

SELECT `Loan Status`, COUNT(*) AS Applications
FROM credit_train
GROUP BY `Loan Status`;

SELECT
    CASE
        WHEN `Loan Status` = 'Fully Paid' THEN 'Good Loan'
        WHEN `Loan Status` = 'Charged Off' THEN 'Bad Loan'
        ELSE 'Other'
    END AS Loan_Category,
    COUNT(*) AS Applications
FROM credit_train
GROUP BY Loan_Category;

SELECT Purpose,
       ROUND(AVG(`Current Loan Amount`), 2) AS Average_Loan_Amount
FROM credit_train
GROUP BY Purpose
ORDER BY Average_Loan_Amount DESC;

SELECT `Loan Status`,
       ROUND(AVG(`Credit Score`), 2) AS Average_Credit_Score
FROM credit_train
GROUP BY `Loan Status`;

SELECT `Home Ownership`, COUNT(*) AS Applications
FROM credit_train
GROUP BY `Home Ownership`
ORDER BY Applications DESC;


import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load training dataset
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "Dataset" / "credit_train.csv"
OUTPUT_DIR = BASE_DIR / "Dataset" / "Analysis_Outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Clean column names and blank values
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

print("Dataset Shape:", df.shape)
print("\nColumn Names:\n", df.columns.tolist())
print("\nMissing Values:\n", df.isnull().sum())
print("\nLoan Status Distribution:\n", df["Loan Status"].value_counts(dropna=False))

# Clean numeric columns
numeric_cols = [
    "Current Loan Amount",
    "Credit Score",
    "Annual Income",
    "Monthly Debt",
    "Maximum Open Credit",
    "Bankruptcies",
    "Tax Liens"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Loan status analysis
status_summary = (
    df.groupby("Loan Status", dropna=False)
    .agg(
        Applications=("Loan Status", "size"),
        Average_Loan_Amount=("Current Loan Amount", "mean"),
        Average_Income=("Annual Income", "mean"),
        Average_Credit_Score=("Credit Score", "mean")
    )
    .reset_index()
)

status_summary.to_csv(
    OUTPUT_DIR / "Loan_Status_Analysis.csv", index=False
)

# Loan purpose analysis
if "Purpose" in df.columns:
    purpose_summary = (
        df.groupby("Purpose", dropna=False)
        .agg(
            Applications=("Purpose", "size"),
            Average_Loan_Amount=("Current Loan Amount", "mean")
        )
        .reset_index()
    )
    purpose_summary.to_csv(
        OUTPUT_DIR / "Loan_Purpose_Analysis.csv", index=False
    )

# Home ownership analysis
if "Home Ownership" in df.columns:
    home_summary = (
        df.groupby("Home Ownership", dropna=False)
        .agg(Applications=("Home Ownership", "size"))
        .reset_index()
    )
    home_summary.to_csv(
        OUTPUT_DIR / "Home_Ownership_Analysis.csv", index=False
    )

# Good vs bad loan classification
df["Loan Category"] = df["Loan Status"].map({
    "Fully Paid": "Good Loan",
    "Charged Off": "Bad Loan"
})

loan_category = (
    df["Loan Category"]
    .value_counts(dropna=False)
    .rename_axis("Loan Category")
    .reset_index(name="Applications")
)

loan_category.to_csv(
    OUTPUT_DIR / "Good_Bad_Loan_Analysis.csv", index=False
)

# Correlation analysis
if "Loan Status" in df.columns:
    df["Loan_Status_Numeric"] = df["Loan Status"].map({
        "Fully Paid": 1,
        "Charged Off": 0
    })

correlation_cols = [
    col for col in [
        "Loan_Status_Numeric", "Current Loan Amount",
        "Credit Score", "Annual Income", "Monthly Debt",
        "Years of Credit History", "Number of Open Accounts"
    ] if col in df.columns
]

df[correlation_cols].corr(numeric_only=True).to_csv(
    OUTPUT_DIR / "Correlation_Analysis.csv"
)

# KPI summary
total_applications = len(df)
good_loans = (df["Loan Category"] == "Good Loan").sum()
bad_loans = (df["Loan Category"] == "Bad Loan").sum()

kpis = pd.DataFrame({
    "KPI": [
        "Total Applications",
        "Good Loan Applications",
        "Bad Loan Applications",
        "Good Loan Rate",
        "Bad Loan Rate"
    ],
    "Value": [
        total_applications,
        good_loans,
        bad_loans,
        good_loans / total_applications if total_applications else 0,
        bad_loans / total_applications if total_applications else 0
    ]
})

kpis.to_csv(OUTPUT_DIR / "Loan_KPI_Summary.csv", index=False)

# Chart: loan status
df["Loan Status"].value_counts().plot(
    kind="bar", title="Loan Applications by Status"
)
plt.ylabel("Number of Applications")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "Loan_Status.png")
plt.close()

# Chart: good vs bad loans
loan_category.set_index("Loan Category")["Applications"].plot(
    kind="bar", title="Good Loans vs Bad Loans"
)
plt.ylabel("Number of Applications")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "Good_vs_Bad_Loans.png")
plt.close()

print("\nAnalysis completed successfully!")
print("Output folder:", OUTPUT_DIR)
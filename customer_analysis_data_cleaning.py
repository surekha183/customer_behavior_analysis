import pandas as pd
df = pd.read_csv('customer_shopping_behavior.csv')

## print(df.head())
## print(df.info())
## print(df.describe(include="all"))
## print(df.isnull().sum())

df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
## print(df.isnull().sum())

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ","_")
df = df.rename(columns = {"purchase_amount_(usd)" : "purchase_amount"})
#print(df.columns)


# creating a column age_group
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q = 4, labels = labels)
## print(df[['age', 'age_group']].head(10))


# creating column purchase_frequency_days
frequency_mapping = {
    'Fortnightly' : 14,
    'Weekly' : 7,
    'Monthly' : 30,
    'Quarterly' : 90,
    'Bi-Weekly' : 14,
    'Annually' : 365,
    'Every 3 Months' : 90
    
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
## print(df[['purchase_frequency_days', 'frequency_of_purchases']].head(10))

## print((df['discount_applied'] == df['promo_code_used']).all())  "since discount_applied and promo_code_used has same values"
df = df.drop('promo_code_used', axis = 1)
## print(df.columns)

from sqlalchemy import create_engine
# Step 1: Connect to PostgreSQL\n,
# Replace placeholders with your actual details,
username = "postgres"      # default user\n",
password = "Surekha%40183" # the password you set during installation,
host = "localhost"         # if running locally,
port = "5432"              # default PostgreSQL port,
database = "customer_behaviour"    # the database you created in pgAdmin,

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Step 2: Load DataFrame into PostgreSQL,
table_name = "customer"   # choose any table name,
df.to_sql(table_name, engine, if_exists="replace", index=False),
    
print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")


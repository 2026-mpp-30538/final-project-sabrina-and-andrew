import pandas as pd
import altair as alt
import geopandas as gpd
from pathlib import Path
import os

full_data = pd.read_csv('data\derived_data\Full Data.csv')

BASE_DIR = Path(__file__).parent.parent
os.chdir(BASE_DIR)

SAVE_DIR = os.path.join(BASE_DIR, 'figures')


vars = [
      'Gini (Standardized)',
      'Median House Price for Below-Median Income Families (Standardized)',
      'Poverty Rate (Standardized)', 
      'Murder and nonnegligent manslaughter_rate',
      'Income Segregation (Standardized)',
      'Location Affordability of Very Low-Income Individual',
      'School Expenditure per Student (Standardized)',
      'Labor Force Participation (Standardized)',
      'Migration Outlflow Rate (Standardized)',
      'Fraction Religious (Standardized)',
      'Fraction of Children with Single Mothers (Standardized)',
      'Violent crime_rate',
      'Racial Segregation (Standardized)',
      'Number of Colleges per Capita (Standardized)',
      'Number of Colleges per Capita (Standardized)',
      'High School Dropout Rate (Income adjusted) (Standardized)',
      'College Graduation Rate (Income Adjusted) (Standardized)',
      'Teenage (14-16) Labor Force Participation (Standardized)',
      'Median House Rent for Below-Median Income Families (Standardized)',
      'Unemployment Rate (Standardized)',
      'Fraction of Adults Married (Standardized)'
]

full_data = full_data[full_data['Ownership'] != 'Total Covered']

county_summary = full_data.groupby('County FIPS 2000').agg({
    'Local Wage Share': lambda x: 1 / (x**2).sum(),
    'Gini (Standardized)': 'first',
    'Median House Price for Below-Median Income Families (Standardized)': 'first',
    'Poverty Rate (Standardized)': 'first', 
    'Murder and nonnegligent manslaughter_rate': 'first',
    'Income Segregation (Standardized)': 'first',
    'Location Affordability of Very Low-Income Individual': 'first',
    'School Expenditure per Student (Standardized)': 'first',
    'Labor Force Participation (Standardized)': 'first',
    'Migration Outlflow Rate (Standardized)': 'first',
    'Fraction Religious (Standardized)': 'first',
    'Fraction of Children with Single Mothers (Standardized)': 'first',
    'Violent crime_rate': 'first',
    'Racial Segregation (Standardized)': 'first',
    'Number of Colleges per Capita (Standardized)': 'first',
    'High School Dropout Rate (Income adjusted) (Standardized)': 'first',
    'College Graduation Rate (Income Adjusted) (Standardized)': 'first',
    'Teenage (14-16) Labor Force Participation (Standardized)': 'first',
    'Median House Rent for Below-Median Income Families (Standardized)': 'first',
    'Unemployment Rate (Standardized)': 'first',
    'Fraction of Adults Married (Standardized)': 'first'
})

county_summary = county_summary.rename(columns={
    'Local Wage Share': 'Inverse HHI'
})

outcome = 'Inverse HHI'
results = []
for var in vars:

    clean_data = county_summary[[var, outcome]].dropna()
    correlation = clean_data[var].corr(clean_data[outcome])
    
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        clean_data[var],
        clean_data[outcome]
          )

          # Get mean of causal measure for this industry
    mean_mobility = clean_data[outcome].mean()

          # Get SD of Employment Location Quotient
    var_std = clean_data[var].std()

          # Effect of 1 SD increase
    effect_per_sd = slope * var_std

          # Percentage effect
    pct_effect = (effect_per_sd / mean_mobility) * 100

    results.append({
              'Variable': var,
              'Effect_per_SD': effect_per_sd,
              'Pct_Change': pct_effect,
              'Correlation': correlation,
              'P_value': p_value,
              'Significant': p_value < 0.05
          })
results_df = pd.DataFrame(results)
results_df

results_signif = results_df[results_df['Significant'] == True]

results_signif['Variable'] = results_signif['Variable'].str.replace(' (Standardized)', '', regex=False)
results_signif['Variable'] = results_signif['Variable'].str.replace('(Income adjusted)', '', regex=False)
results_signif['Variable'] = results_signif['Variable'].str.replace('Teenage (14-16) Labor Force Participation', 'Teen (14-16) LFP', regex=False)
results_signif['Variable'] = results_signif['Variable'].str.replace(' for Below-Median Income Families', ', Low-Income', regex=False)
results_signif['Variable'] = results_signif['Variable'].str.replace(' of Very Low-Income Individual', ', Very Low-Income', regex=False)

results_signif['Correlation'] = results_signif['Correlation'].astype(str)

results_signif = results_signif.sort_values('Pct_Change', ascending=False)
ordered_vars = results_signif['Variable'].tolist()

max_x = results_signif['Pct_Change'].max()
min_x = results_signif['Pct_Change'].min()

# Add extra space to right side

results_signif['Corr_X'] = 60
bars = alt.Chart(results_signif).mark_bar().encode(
    x=alt.X('Pct_Change:Q',
            title='Percent Change in Wage Concentration',
            scale=alt.Scale(domain=[-15, 55])),  
    y=alt.Y('Variable:O',
            scale=alt.Scale(domain=ordered_vars),
            title='Crime and Mobility Measures')
).properties(height=500, width=600,
             title={
        "text": "Association Between 1 SD Increase of Crime/Economic Measures with Wage Concentration",
        "subtitle": "With Associated Correlation Coefficients, All Statistically Significant at .05 Level",
        })

corr_text = alt.Chart(results_signif).mark_text(
).encode(
    x=alt.value(580),
    y=alt.Y('Variable:O',
            scale=alt.Scale(domain=ordered_vars),
            title=None),
    text=alt.Text('Correlation:Q', format='.2f'))


zero_line = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(
    strokeDash=[5, 5],
    color='black'
).encode(x='x:Q')

final_chart = (bars + zero_line + corr_text).configure_view(clip=False)

final_chart.save(os.path.join(SAVE_DIR, 'Wage Concentration Chart.png'), scale_factor=2)
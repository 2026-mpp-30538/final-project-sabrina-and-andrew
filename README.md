[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/YlfKWlZ5)
# Economic Mobility and Socioeconomic Factors

This project processes and visualizes data on economic mobility, industry concentration, and crime to explore the causal effect of place. 

## Setup

```bash
conda env create -f environment.yml
conda activate fire_analysis
```

## Project Structure

```
Due the the size of our data, we use a Google Drive to store the files that can be accessed here: https://drive.google.com/drive/folders/1spfMCOnuv5OpxtNFlrOwabe6jGVzijCf?usp=sharing. For replicability, download the drive in a folder in the repository called 'data'.

The original data sets can be found at the following links and we last accessed on February 8th, 2026:
  

data/
  derived-data/                   # Filtered data and output plots
    Full Data with Geography.gpkg # Full cleaned dataset for analysis
code/
  our_preprocessing.py            # Harmonizes crime data and combines this with Chetty-Hendren data on mobility, QCEW data on industry concentration, and census shapefiles. 
  crime_map.py                    # Plots maps for both violent and property crime
  app.py                          # Contains script to create Streamlit Dashboard. 
```

## Usage

1. Run preprocessing to filter data:
   ```bash
   python code/preprocessing.py
   ```

2. Generate the fire perimeter plot:
   ```bash
   python code/plot_fires.py
   ```

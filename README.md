# **ORGANOLEPTIC PROJECT**
This project is a simple Python script to randomly generate organoleptic data with customizable numbers of participants and parameters. The resulting data will be saved in Excel format (`hasil_organoleptik.xlsx`). The data generated will be 100% similar to data processed with SPSS.

_Skrip Python sederhana untuk menghasilkan data organoleptik secara acak dengan jumlah partisipan dan parameter yang dapat disesuaikan. Data yang dihasilkan akan disimpan dalam format Excel_ (`hasil_organoleptik.xlsx`). _Data yang dihasilkan 100% sama seperti olah data dengan SPSS._


## **Features**
- CUSTOM Number of panelists
- CUSTOM Number of formulations
- Parameters to be tested (e.g., Aroma, Taste, Texture)
- Whether you want to introduce a significant effect in any parameter
- The panelists' ratings for each formulation and parameter
- ANOVA results for each parameter
- Duncan test results if the ANOVA test shows significant differences

## **Requirements:**
Ensure you have the following packages installed:
- Python3
- pandas
- numpy
- scipy
- statsmodels
- openpyxl

## Installation

#### Terminal/Termux
1. Repository
```sh
git clone https://github.com/iwanggawae/project-orlep
```
2. Open Directory
```sh
cd project-orlep
```
3. Requirements Installation
```sh
python3 -m pip install -r requirements.txt
```
4. Run
```sh
python3 orlep.py
```

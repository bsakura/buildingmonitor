import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import os
# Converting IT Asset Subcategory
# The input of the function is from the drop down button on the website
def get_encoded_subcategory (subcategory):
    subcategory_dict = {
        'Access Point': 0.0,
        'CPU': 1.0,
        'Copier': 2.0,
        'Core Switch': 3.0,
        'Edge Switch': 4.0,
        'Fast Ethernet Switch': 5.0,
        'Gigabit Ethernet Switch': 6.0,
        'High performance servers in-house': 7.0,
        'Hubs': 8.0,
        'In-house servers not cooled': 9.0,
        'In-house standard servers cooled': 10.0,
        'Ink-Jet Printer': 11.0,
        'LCD Monitors': 12.0,
        'LED Monitors': 13.0,
        'Laser Printer': 14.0,
        'Multifuncion Devices': 15.0,
        'Other Computer Devices': 17.0,
        'Other Imaging Devices': 18.0,
        'Other Network Devices': 19.0,
        'Other Phone Devices': 20.0,
        'PoE (Power over Ethernet)': 21.0,
        'Power Desktop PCs': 22.0,
        'Power Laptop': 23.0,
        'Printer': 24.0,
        'Projectors': 25.0,
        'Scanner': 26.0,
        'Smart Phones': 27.0,
        'Standard Desktop PCs': 28.0,
        'Standard Laptop': 29.0,
        'Tablet': 30.0,
        'Thin Clients': 31.0,
        'UPS': 32.0,
        'VOIP Phones': 33.0,
        'Video Conference Devices': 34.0,
        'Wireless Router': 35.0
    }
    if subcategory in subcategory_dict:
        return subcategory_dict[subcategory]
    else:
        return 36.0 # Not found condition

# For single use
def get_predicted_unit(year, subcategory):
  df_subcategory = df[df["IT Asset Subcategory"] == subcategory]
  X = df_subcategory['Tahun Perolehan']
  y = df_subcategory['Jumlah Unit']
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  f = np.polyfit(X_train, y_train, 2)
  p = np.poly1d(f)
  z = np.array(year)
  return(round(p(z)))

def get_predicted_energy(units, subcategory, target):
  df_subcategory = df[df["IT Asset Subcategory"] == subcategory]
  X = df_subcategory['Jumlah Unit']
  y = df_subcategory[target]
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  f = np.polyfit(X_train, y_train, 2)
  p = np.poly1d(f)
  z = np.array(units)
  return (p(z))

file_path_carbon = os.path.abspath(os.path.join(os.path.dirname(__file__), "df_carbon.xlsx"))
file_path_agg = os.path.abspath(os.path.join(os.path.dirname(__file__), "df_agg.xlsx"))

df = pd.read_excel(file_path_carbon)
df1 = pd.read_excel(file_path_agg)
# unit_model = pickle.load(open(("jumlah_unit"), 'rb'))
# energy_model = pickle.load(open(("energy"), 'rb'))
server = ['In-house servers not cooled',
          'In-house standard servers cooled',
          'High performance servers in-house']
komputer = ['Power Desktop PCs',
            'Standard Desktop PCs',
            'Power Laptop',
            'Standard Laptop',
            'LCD Monitors',
            'LED Monitors',
            'Thin Clients',
            'Tablet',
            'CPU',
            'UPS',
            'Other Computer Devices']
jaringan = ['Fast Ethernet Switch',
          'Gigabit Ethernet Switch',
          'Core Switch',
          'Access Point',
          'Wireless Router',
          'Hubs',
          'Edge Switch',
          'PoE (Power over Ethernet)',
          'Other Network Devices']
telepon = ['VOIP Phones',
           'Smart Phones',
           'Other Phone Devices']
imaging = ['Laser Printer',
          'Ink-Jet Printer',
          'Scanner',
          'Copier',
          'Multifuncion Devices',
          'Printer',
          'Other Imaging Devices']
av = ['Projectors',
      'Video Conference Devices',
      'Other AV Devices']

years = [2008, 2009, 2011, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

def stacked_count_category():
    counts_category = []
    for year in years:
        units = {}
        a, b, c, d, e, f = 0, 0, 0, 0, 0, 0
        for sub in server:
            a += get_predicted_unit(year, sub)
        for sub in komputer:
            b += get_predicted_unit(year, sub)
        for sub in jaringan:
            c += get_predicted_unit(year, sub)
        for sub in imaging:
            d += get_predicted_unit(year, sub)
        for sub in telepon:
            e += get_predicted_unit(year, sub)
        for sub in av:
            f += get_predicted_unit(year, sub)
        units["stacked_server"] = a
        units["stacked_komputer"] = b
        units["stacked_jaringan"] = c
        units["stacked_imaging"] = d
        units["stacked_telepon"] = e
        units["stacked_av"] = f
        counts_category.append(units)
  
    return counts_category

def pie_count_category():
  return (df1['Total'][:-1].to_list())
  
#table data
def get_category_details(category):
    return df[df["IT Asset Category"] == category].head(10).to_dict(orient="records")

#table form
def get_predicted_unit_wrapper(row, year):
  return get_predicted_unit(year, row["IT Asset Subcategory"])

def get_predicted_energy_wrapper(row, year):
  return get_predicted_energy(get_predicted_unit_wrapper(row, year), row["IT Asset Subcategory"], "Energy")

def get_predicted_cost_wrapper(row, year):
  return get_predicted_energy(get_predicted_unit_wrapper(row, year), row["IT Asset Subcategory"], "Cost")

def get_predicted_carbon_wrapper(row, year):
  return get_predicted_energy(get_predicted_unit_wrapper(row, year), row["IT Asset Subcategory"], "Carbon")

def get_tabel_form_predicted(year, category):
  category_details = get_category_details(category)
  as_is_data = pd.DataFrame(category_details)
  as_is_data = as_is_data.groupby("IT Asset Subcategory")["Jumlah Unit"].sum().reset_index()
  as_is_data[f"Predicted Unit 2022"] = as_is_data.apply(get_predicted_unit_wrapper, year=2022, axis=1)
  as_is_data[f"Predicted Energy 2022"] = as_is_data.apply(get_predicted_energy_wrapper, year=2022, axis=1)
  as_is_data[f"Predicted Cost 2022"] = as_is_data.apply(get_predicted_cost_wrapper, year= 2022, axis=1)
  as_is_data[f"Predicted Carbon 2022"] = as_is_data.apply(get_predicted_carbon_wrapper, year=2022, axis=1)
  as_is_data[f"Predicted Unit 2021"] = as_is_data.apply(get_predicted_unit_wrapper, year=2021, axis=1)
  as_is_data[f"Predicted Energy 2021"] = as_is_data.apply(get_predicted_energy_wrapper, year=2021, axis=1)
  as_is_data[f"Predicted Cost 2021"] = as_is_data.apply(get_predicted_cost_wrapper, year= 2021, axis=1)
  as_is_data[f"Predicted Carbon 2021"] = as_is_data.apply(get_predicted_carbon_wrapper, year=2021, axis=1)
  as_is_data[f"Predicted Unit 2020"] = as_is_data.apply(get_predicted_unit_wrapper, year=2020, axis=1)
  as_is_data[f"Predicted Energy 2020"] = as_is_data.apply(get_predicted_energy_wrapper, year=2020, axis=1)
  as_is_data[f"Predicted Cost 2020"] = as_is_data.apply(get_predicted_cost_wrapper, year= 2020, axis=1)
  as_is_data[f"Predicted Carbon 2020"] = as_is_data.apply(get_predicted_carbon_wrapper, year=2020, axis=1)
  as_is_data[f"Predicted Unit 2019"] = as_is_data.apply(get_predicted_unit_wrapper, year=2019, axis=1)
  as_is_data[f"Predicted Energy 2019"] = as_is_data.apply(get_predicted_energy_wrapper, year=2019, axis=1)
  as_is_data[f"Predicted Cost 2019"] = as_is_data.apply(get_predicted_cost_wrapper, year= 2019, axis=1)
  as_is_data[f"Predicted Carbon 2019"] = as_is_data.apply(get_predicted_carbon_wrapper, year=2019, axis=1)
  return as_is_data.to_dict(orient="records")

def pie_get_category(category, target):
  grouped_df = df[df["IT Asset Category"] == category].groupby("IT Asset Subcategory")[target].sum().reset_index()
  subcategory_array = grouped_df["IT Asset Subcategory"].to_dict()
  target_array = grouped_df[target].to_dict()
  return (subcategory_array, target_array)

def pie_get_category_predicted(year, category, target):
    df = get_tabel_form_predicted(year, category)
    df= pd.DataFrame(df)
    grouped_df = df.groupby("IT Asset Subcategory").agg({f"Predicted {target} {year}": "sum"}).reset_index()
    subcategory_array = grouped_df["IT Asset Subcategory"].to_dict()
    target_array = grouped_df[f"Predicted {target} {year}"].to_dict()
    return (subcategory_array, target_array)

def initiatives(year, category):
    year = int(year)
    prev = year - 1
    a, prev_energies = pie_get_category_predicted(prev, category, "Energy")
    b, prev_costs = pie_get_category_predicted(prev, category, "Cost")
    c, prev_carbons = pie_get_category_predicted(prev, category, "Carbon")
    g, prev_units = pie_get_category_predicted(prev, category, "Unit")
    treshold_energy = sum(prev_energies.values())
    treshold_cost = sum(prev_costs.values())
    treshold_carbons = sum(prev_carbons.values())
    treshold_units = sum(prev_units.values())

    d, energies = pie_get_category_predicted(year, category, "Energy")
    e, costs = pie_get_category_predicted(year, category, "Cost")
    f, carbons = pie_get_category_predicted(year, category, "Carbon")
    h, units = pie_get_category_predicted(year, category, "Unit")
    energy = sum(energies.values())
    cost = sum(costs.values())
    carbon = sum(carbons.values())
    unit = sum(units.values())

    if (energy >= treshold_energy) or (cost >= treshold_cost) or (carbon >= treshold_carbons):
        procured = unit - treshold_units
        percentage = (procured/unit)*100
        return f"You should start limiting your use of {category}\n" \
               f"Maximum Number of Procurement {category} Assets in {year}: {treshold_units}\n" \
               f"Predicted Reduction Number Procurement {category} Assets in {year}: {procured}\n" \
               f"Predicted Reduction Percentation Number Procurement {category} Assets in {year}: {percentage}%"
    else:
        return f"The {year} prediction is all good. However, you could also reuse and recycle your IT Asset on {category} to support sustainability."

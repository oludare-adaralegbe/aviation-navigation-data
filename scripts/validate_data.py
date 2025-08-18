#!/usr/bin/env python
# coding: utf-8

# In[13]:


import geopandas as gpd

# Load GeoJson files
gdf_apt = gpd.read_file("openaip/gb_airport.geojson", engine="fiona")
gdf_asp = gpd.read_file("openaip/gb_airspace.geojson", engine="fiona")
gdf_nav = gpd.read_file("openaip/gb_navaid.geojson", engine="fiona")
gdf_obs = gpd.read_file("openaip/gb_obstacle.geojson", engine="fiona")


# In[14]:


print(f'airport = {list(gdf_apt.columns)}')
print(f'airspace = {list(gdf_asp.columns)}')
print(f'navaid = {list(gdf_nav.columns)}')
print(f'obstruction = {list(gdf_obs.columns)}')


# In[15]:


display(gdf_obs.head())


# In[16]:


gdf_apt.plot()


# ### 1. Removing entries with missing coordinates

# In[17]:


# Function to clean missing geometries
def remove_missing_geometry(gdf, name):
    gdf_clean = gdf[gdf.geometry.notnull() & gdf.is_valid]
    print(f"[{name}] Removed {len(gdf) - len(gdf_clean)} entries with missing/invalid coordinates")
    return gdf_clean

gdf_apt = remove_missing_geometry(gdf_apt, "Airports")
gdf_asp = remove_missing_geometry(gdf_asp, "Airspace")
gdf_nav = remove_missing_geometry(gdf_nav, "Navaids")
gdf_obs = remove_missing_geometry(gdf_obs, "Obstructions")


# ### 2. Flagging unrealistic altitudes

# Based on research and aviation standards, here are the altitude thresholds that would be considered unrealistic for obstruction and airspace values.
# 
# **Obstruction:**
# Elevation (AMSL): Realistic range: -400m (-1,312 ft) to 6,000m (19,685 ft) || Unrealistic: Above 8,848m (29,029 ft) - Mount Everest height
# 
# Height (AGL): Realistic range: 0.1m (0.3 ft) to 1,000m (3,281 ft) || Unrealistic: Above 1,500m (4,921 ft)
# 
# **Airspace Altitudes:**
# Floor Altitude: Realistic range: -400m (-1,312 ft) to 18,000m (59,055 ft) || Unrealistic: Above 20,000m (65,617 ft)
# 
# Ceiling Altitude: Realistic range: 100m (328 ft) to 20,000m (65,617 ft) || Unrealistic: Above 25,000m (82,021 ft)
# 
# **Airport Elevations:**
# Lower bound: Around -400m (-1,312 ft) - constrained by Dead Sea region ||
# 
# Upper bound: Around 4,400m (14,400 ft) - highest operational airports || unrealistic: Above 6,000m (19,685 ft)
# 
# **NAVAID Equipment Heights:**
# Elevation (AMSL): Realistic range: -400m (-1,312 ft) to 6,000m (19,685 ft) || unrealistic: Above 8,000m (26,247 ft)

# In[18]:


# Step 1: Extract numeric values
# The elevation/height values are in dictionaries. The numeric values need to be extracted first.
def extract_value(col):
    """Extract the 'value' from a dictionary in a column, return NaN if missing."""
    return col.apply(lambda x: x.get('value') if isinstance(x, dict) and 'value' in x else float('nan'))

# Airports
gdf_apt['elevation_val'] = extract_value(gdf_apt['elevation'])

# Airspace
gdf_asp['upperLimit_val'] = extract_value(gdf_asp['upperLimit'])
gdf_asp['lowerLimit_val'] = extract_value(gdf_asp['lowerLimit'])

# Navaids
gdf_nav['elevation_val'] = extract_value(gdf_nav['elevation'])

# Obstructions
gdf_obs['elevation_val'] = extract_value(gdf_obs['elevation'])
gdf_obs['height_val'] = extract_value(gdf_obs['height'])


# In[19]:


# Airports
print("Airports – Extracted Elevation Values")
display(gdf_apt[['name', 'elevation', 'elevation_val']])

# Airspace
print("\nAirspace – Extracted Upper & Lower Limit Values")
display(gdf_asp[['name', 'upperLimit', 'upperLimit_val', 'lowerLimit', 'lowerLimit_val']])

# Navaids
print("\nNavaids – Extracted Elevation Values")
display(gdf_nav[['name', 'elevation', 'elevation_val']])

# Obstructions
print("\nObstructions – Extracted Elevation & Height Values")
display(gdf_obs[['name', 'elevation', 'elevation_val', 'height', 'height_val']])


# In[20]:


import pandas as pd

# Step 2: Flagging unrealistic altitudes using the extracted values
# Airports (values in metres)
gdf_apt['altitude_flag'] = gdf_apt['elevation_val'].apply(lambda x: 'unrealistic' if pd.isna(x) or x < -400 or x > 6000 else 'ok')

# Airspace (values in ft)
gdf_asp['altitude_flag'] = gdf_asp.apply(
    lambda row: 'unrealistic' if pd.isna(row['lowerLimit_val']) or pd.isna(row['upperLimit_val'])
                or row['lowerLimit_val'] < -400 or row['upperLimit_val'] > 66000 else 'ok',
    axis=1
)

# Navaids (values in metres)
gdf_nav['altitude_flag'] = gdf_nav['elevation_val'].apply(lambda x: 'unrealistic' if pd.isna(x) or x < -400 or x > 8000 else 'ok')

# Obstructions (values in metres)
gdf_obs['altitude_flag'] = gdf_obs.apply(
    lambda row: ('ok' if (pd.notna(row['elevation_val']) and -400 <= row['elevation_val'] <= 10000 # Elevation must be valid (always required)
            # Height is optional: either missing or valid
            and (pd.isna(row['height_val']) or (-400 <= row['height_val'] <= 1500))
        )
        else 'unrealistic'),
    axis=1
)


# In[21]:


# Show unrealistic rows for each dataset
flagged_airports = gdf_apt[gdf_apt['altitude_flag'] == 'unrealistic']
flagged_airspace = gdf_asp[gdf_asp['altitude_flag'] == 'unrealistic']
flagged_navaids = gdf_nav[gdf_nav['altitude_flag'] == 'unrealistic']
flagged_obstructions = gdf_obs[gdf_obs['altitude_flag'] == 'unrealistic']

# Display them
print("Airports – Unrealistic Altitudes")
display(flagged_airports)

print("\nAirspace – Unrealistic Altitudes")
display(flagged_airspace)

print("\nNavaids – Unrealistic Altitudes")
display(flagged_navaids)

print("\nObstructions – Unrealistic Altitudes")
display(flagged_obstructions)


# ### 3. Checking date fields for outdated info

# In[10]:


from datetime import datetime

current_year = datetime.now().year

def flag_old_dates(gdf, date_columns, name, years_threshold=5):
    for col in date_columns:
        if col in gdf.columns:
            gdf[col] = pd.to_datetime(gdf[col], errors='coerce')
            flag_col = col + '_flag'
            gdf[flag_col] = gdf[col].apply(
                lambda x: 'outdated' if pd.notnull(x) and (current_year - x.year > years_threshold) else 'ok'
            )
            outdated_count = (gdf[flag_col] == 'outdated').sum()
            print(f"[{name}] {outdated_count} entries in '{col}' are outdated")
    return gdf

gdf_apt = flag_old_dates(gdf_apt, ['createdAt', 'updatedAt'], "Airports")
gdf_asp = flag_old_dates(gdf_asp, ['createdAt', 'updatedAt'], "Airspace")
gdf_nav = flag_old_dates(gdf_nav, ['createdAt', 'updatedAt'], "Navaids")
gdf_obs = flag_old_dates(gdf_obs, ['createdAt', 'updatedAt', 'osmUpdatedAt'], "Obstructions")


# In[23]:


# Export GeoDataFrames to GeoJSON
gdf_apt.to_file("cleaned_airports.geojson", driver="GeoJSON")
gdf_asp.to_file("cleaned_airspace.geojson", driver="GeoJSON")
gdf_obs.to_file("cleaned_obstructions.geojson", driver="GeoJSON")
gdf_nav.to_file("cleaned_navaids.geojson", driver="GeoJSON")


# In[ ]:





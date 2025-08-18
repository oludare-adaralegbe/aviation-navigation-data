#!/usr/bin/env python
# coding: utf-8

# In[2]:


import geopandas as gpd
import folium

# Load cleaned GeoJSON files
gdf_apt = gpd.read_file("cleaned_data/cleaned_airports.geojson")
gdf_asp = gpd.read_file("cleaned_data/cleaned_airspace.geojson")
gdf_obs = gpd.read_file("cleaned_data/cleaned_obstructions.geojson")
gdf_nav = gpd.read_file("cleaned_data/cleaned_navaids.geojson")


# In[4]:


# Initialise map centred on mean airport location
centre = [gdf_apt.geometry.y.mean(), gdf_apt.geometry.x.mean()]
m = folium.Map(location=centre, zoom_start=6, tiles="CartoDB positron")

# Airports Layer (blue plane markers)
airports_layer = folium.FeatureGroup(name="Airports")
for _, row in gdf_apt.iterrows():
    if row.geometry is not None:
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=f"Airport: {row.get('name', 'N/A')} ({row.get('icaoCode', '---')})",
            icon=folium.Icon(color='blue', icon='plane', prefix='fa')
        ).add_to(airports_layer)
airports_layer.add_to(m)

# Airspace Layer (green polylines/polygons)
airspace_layer = folium.FeatureGroup(name="Airspace")
for _, row in gdf_asp.iterrows():
    if row.geometry is not None:
        if row.geometry.geom_type == 'Polygon':
            folium.PolyLine(
                locations=[(lat, lon) for lon, lat in row.geometry.exterior.coords],
                color="green",
                weight=2,
                popup=f"Airspace: {row.get('name', 'N/A')}"
            ).add_to(airspace_layer)
        elif row.geometry.geom_type == 'LineString':
            folium.PolyLine(
                locations=[(lat, lon) for lon, lat in row.geometry.coords],
                color="green",
                weight=2,
                popup=f"Airspace: {row.get('name', 'N/A')}"
            ).add_to(airspace_layer)
airspace_layer.add_to(m)

# Obstructions Layer (red warning markers)
obstructions_layer = folium.FeatureGroup(name="Obstructions")
for _, row in gdf_obs.iterrows():
    if row.geometry is not None:
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=f"Obstruction: {row.get('name', 'N/A')} | Elev: {row.get('elevation_val', 'N/A')} m",
            icon=folium.Icon(color='red', icon='warning', prefix='fa')
        ).add_to(obstructions_layer)
obstructions_layer.add_to(m)

# Navaids Layer (orange broadcast tower markers)
navaids_layer = folium.FeatureGroup(name="Navaids")
for _, row in gdf_nav.iterrows():
    if row.geometry is not None:
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=f"Navaid: {row.get('name', 'N/A')} ({row.get('identifier', '---')}) | Freq: {row.get('frequency', '---')}",
            icon=folium.Icon(color='orange', icon='broadcast-tower', prefix='fa')
        ).add_to(navaids_layer)
navaids_layer.add_to(m)

# Add Layer Control
folium.LayerControl().add_to(m)

# Show Map
m


# In[6]:


# Save interactive map as standalone HTML
m.save("outputs/interactive_cockpit_map.html")


# In[ ]:





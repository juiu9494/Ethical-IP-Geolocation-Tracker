import requests
import folium
import os

def get_location_from_ip(ip_address):
    try:
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "success":
            return {
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "isp": data.get("isp")
            }
        else:
            return {"error": "Failed to retrieve data. IP may be private or invalid."}
    except Exception as e:
        return {"error": str(e)}

def draw_map(location_data, output_file="location_map.html"):
    if "error" in location_data:
        print(location_data["error"])
        return

    lat = location_data["latitude"]
    lon = location_data["longitude"]
    city = location_data["city"]
    country = location_data["country"]

    # Create map
    m = folium.Map(location=[lat, lon], zoom_start=12)

    # Add marker
    folium.Marker(
        location=[lat, lon],
        popup=f"{city}, {country}",
        tooltip="Target Location"
    ).add_to(m)

    # Save map
    m.save(output_file)
    print(f"[+] Map saved to {os.path.abspath(output_file)}")
    

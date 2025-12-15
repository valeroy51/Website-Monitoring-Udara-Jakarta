import pandas as pd
import numpy as np
import os
import glob
from sklearn.preprocessing import MinMaxScaler
import re
import requests
import time
from haversine import haversine
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

#=======================================================#
#====================RUNNING DATASET====================#
#=======================================================#

Dataset = r"D:\Skripsi\Program\Script\Dataset\Data"

def load_excels(folder_path, skip_header=False):
    excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))
    df_dict = {}

    for file in excel_files:
        name = os.path.splitext(os.path.basename(file))[0]
        print(f"\nProcessing: {name}.xlsx")

        station_raw = None

        if skip_header:
            df_info = pd.read_excel(file, header=None)
            station_raw = df_info.iloc[1, 2] if df_info.shape[1] > 2 else "UnknownStation"

            if isinstance(station_raw, str):
                station_raw = re.sub(r"Stasiun(\s+Meteorologi)?\s*", "", station_raw, flags=re.IGNORECASE)
                station_raw = station_raw.replace("Jakarta", "").strip()
                station_raw = re.sub(r'[<>:"/\\|?*]', "", station_raw).strip()
            else:
                station_raw = "UnknownStation"

        df = pd.read_excel(file, skiprows=7 if skip_header else 0)
        df = df.dropna(how="all")

        ket_idx = df[df.iloc[:, 0].astype(str)
                     .str.contains("KETERANGAN", case=False, na=False)].index
        if len(ket_idx) > 0:
            df = df.loc[:ket_idx[0] - 1]

        df.columns = [str(c).strip() for c in df.columns]

        df.rename(columns=lambda x: "tanggal" if x.strip().lower() == "tanggal" else x, inplace=True)


        if skip_header:
            df.insert(1, "stasiun", station_raw)
        else:
            pass

        station_name = str(df.iloc[0, 1]).strip()

        station_name = re.sub(r"\bDKI\s*\d+\b", "", station_name, flags=re.IGNORECASE)
        station_name = re.sub(r"\bDKI\b", "", station_name, flags=re.IGNORECASE)

        sn_lower = station_name.lower().replace("  ", " ")

        if "kebun jeruk" in sn_lower:
            station_name = "Kebon Jeruk"


        station_name = re.sub(r'[<>:"/\\|?*]', '', station_name).strip()

        print(f"Stasiun terdeteksi: {station_name}")

        output_dir = r"D:\Skripsi\Program\Script\Dataset\Validasi new\1.new data"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, f"{station_name}.xlsx")
        df.to_excel(output_path, index=False)

        print(f"File disimpan sebagai: {output_path}")

        df_dict[station_name] = df

    print("\nSemua file selesai diproses!\n")
    return df_dict

folders = [os.path.join(Dataset, f) for f in os.listdir(Dataset) if os.path.isdir(os.path.join(Dataset, f))]

if len(folders) < 2:
    print("Harus ada minimal 2 folder di dalam Data/")
    exit()

meteorologi, polutan = folders[0], folders[1]
print(f"\nFolder Meteorologi: {meteorologi}")
print(f"Folder Polutan: {polutan}")

df_meteorologi = load_excels(meteorologi, skip_header=True)
df_polutan = load_excels(polutan)


#=====================================================#
#====================PREPROCESSING====================#
#=====================================================#

#CLEANING DATA
def dataclean(df,name):
    df = df.dropna(how='all')
    
    footnote_index = df[df.iloc[:, 0].astype(str).str.startswith('KETERANGAN:')].index
    
    if len(footnote_index) > 0:
        df = df.loc[:footnote_index[0] - 1]
    
    df = df.replace([8888,'-'],np.nan)
    
    # buat validasi
    output_dir = r"D:\Skripsi\Program\Script\Dataset\Validasi try\1.Clean Data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{name}_Clean.xlsx")
    df.to_excel(output_path, index=False)
    print(f"Hasil data '{name}' yang sudah diclean datanya disimpan di: {output_path}")
    
    return df

#FILLING MISSING VALUE - MISSING WINDOW MEDIAN
def missingwindowmedian(df,name, window=15):
    df_filled = df.copy()
    numeric_cols = df_filled.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        nan_indices = df_filled[df_filled[col].isna()].index
        for i in nan_indices:
            start = max(0, i - window)
            end = min(len(df_filled), i + window + 1)
            window_values = df_filled.loc[start:end, col].dropna()
            
            if not window_values.empty:
                median_val = window_values.median()
                df_filled.at[i, col] = median_val
    
    # buat validasi
    output_dir = r"D:\Skripsi\Program\Script\Dataset\Validasi try\2.Missing Value"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{name}_Missing Value.xlsx")
    df.to_excel(output_path, index=False)
    print(f"Hasil data '{name}' yang sudah diisi missing valuenya disimpan di: {output_path}")
    
    return df_filled

#DETEKSI OUTLIER - INTERQUARTILE RANGE
def Interquartiloutlier(df, name):
    df_clean = df.copy()
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns  # hanya kolom numerik
    
    for col in numeric_cols:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df_clean.loc[(df_clean[col] < lower_bound) | (df_clean[col] > upper_bound), col] = np.nan
        df_clean = missingwindowmedian(df_clean, name)

    
    # buat validasi
    output_dir = r"D:\Skripsi\Program\Script\Dataset\Validasi try\3.Outlier"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{name}_Outlier.xlsx")
    df.to_excel(output_path, index=False)
    print(f"Hasil data '{name}' yang sudah dicek outliernya disimpan di: {output_path}")
    
    return df_clean

#NORMALISASI - MINMAX
def normalisasiminmax(df, name, feature_range=(0, 1)):
    df_scaled = df.copy()
    numeric_cols = df_scaled.select_dtypes(include=[np.number]).columns
    scaler = MinMaxScaler(feature_range=feature_range)

    output_dir_minmax = r"D:\Skripsi\Program\Script\Dataset\Validasi try\4.Normalisasi\4.1. Data Normalisasi"
    os.makedirs(output_dir_minmax, exist_ok=True)
    output_path_minmax = os.path.join(output_dir_minmax, f"{name}_MinMax.xlsx")

    minmax_data = []
    for col in numeric_cols:
        min_val = df_scaled[col].min()
        max_val = df_scaled[col].max()
        minmax_data.append({"kolom": col, "min": min_val, "max": max_val})

    df_minmax = pd.DataFrame(minmax_data)
    df_minmax.to_excel(output_path_minmax, index=False)
    print(f"File min–max disimpan: {output_path_minmax}")

    for col in numeric_cols:
        col_data = df_scaled[[col]]
        if col_data.min().values[0] == col_data.max().values[0]:
            df_scaled[col] = 0
        else:
            df_scaled[col] = scaler.fit_transform(col_data)

    zero_cols = [col for col in numeric_cols if (df_scaled[col] == 0).all()]
    if zero_cols:
        df_scaled.drop(columns=zero_cols, inplace=True)
        print(f"Kolom dengan semua nilai 0 dihapus: {zero_cols}")

    # buat validasi
    output_dir_norm = r"D:\Skripsi\Program\Script\Dataset\Validasi try\4.Normalisasi"
    os.makedirs(output_dir_norm, exist_ok=True)
    output_path_norm = os.path.join(output_dir_norm, f"{name}_Normalisasi.xlsx")
    df_scaled.to_excel(output_path_norm, index=False)
    print(f"Hasil data '{name}' yang sudah dinormalisasikan disimpan di: {output_path_norm}")

    return df_scaled, scaler

def preprocess_dict(df_dict):
    processed = {}
    for name, df in df_dict.items():
        print(f"\nPreprocessing: {name}")

        df1 = dataclean(df, name)
        df2 = missingwindowmedian(df1, name)
        df3 = Interquartiloutlier(df2, name)
        df4, _ = normalisasiminmax(df3, name, feature_range=(0, 1))

        processed[name] = df4
        print(f"Selesai: {name} → shape {df4.shape}")
    return processed

#CEK LONGTITUDE DAN LAITITUDE - HAVERSINE
def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "MyGeocodingApp/1.0 (valeroy@example.com)"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return {"alamat": address, "lat": lat, "lon": lon}
    return {"alamat": address, "lat": None, "lon": None}

#MENGHITUNG JARAK- HAVERSINE
def calculate(address1, address2):
    if address1["lat"] is None or address2["lat"] is None:
        return None
    loc1 = (address1["lat"], address1["lon"])
    loc2 = (address2["lat"], address2["lon"])
    return haversine(loc1, loc2)

#MENAMBAHKAN LAT DAN LONG KE DATASET - HAVERSINE
def get_stations_from_dfs(df_names):
    stations = []
    for var_name in df_names:
        loc_name = var_name.replace("_", " ")
        station = geocode_address(loc_name + ", Indonesia")
        station["df_name"] = var_name
        stations.append(station)
        print(f"{loc_name} → Lat: {station['lat']}, Lon: {station['lon']}")
        time.sleep(1)
    return stations

#MENAMPILKAN MATRIKS HASIL HAVERSINE
def matriks(stations1, stations2, calculate_func, output_dir, nama_file, gambar = True):
    os.makedirs(output_dir, exist_ok=True)
    
    df_jarak = pd.DataFrame(
        index=[s["alamat"] for s in stations1],
        columns=[s["alamat"] for s in stations2]
    )

    for s1 in stations1:
        for s2 in stations2:
            jarak = calculate_func(s1, s2)
            df_jarak.loc[s1["alamat"], s2["alamat"]] = jarak

    df_jarak = df_jarak.astype(float).round(3)

    print(f"\nMatrix Jarak {nama_file.replace('_', ' ')} (dalam kilometer):")
    print(tabulate(df_jarak, headers="keys", tablefmt="pretty", showindex=True))

    #buat validasi
    output_path = os.path.join(output_dir, f"{nama_file}.xlsx")
    df_jarak.to_excel(output_path)
    print(f"\nDisimpan ke: {output_path}")
    
    if gambar:
        plt.figure(figsize=(10, 6))
        sns.heatmap(df_jarak, annot=True,cmap="coolwarm", fmt=".3f", cbar_kws={'label': 'Jarak (km)'})
        plt.title(f"Matrix Jarak {nama_file.replace('_', ' ')}")
        plt.xlabel("Staisun Meteorologi"),
        plt.ylabel("Stasiun Polutan")
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()

    return df_jarak

#=============================================================#
#====================RUNNING PREPROCESSING====================#
#=============================================================#
df_meteo_proc = preprocess_dict(df_meteorologi)
df_polu_proc  = preprocess_dict(df_polutan)

StasiunMeteorologi = get_stations_from_dfs(df_meteo_proc)
StasiunPolutan     = get_stations_from_dfs(df_polu_proc)

output_dir = r"D:\Skripsi\Program\Script\Dataset\Validasi try\5.Matriks Jarak"

matriks = matriks(StasiunMeteorologi,StasiunPolutan,calculate,output_dir,"Matriks", gambar = True)

#melakukan parsing tanggal 
def parsedate(series):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s1 = pd.to_datetime(series, dayfirst=False, errors="coerce")
        s2 = pd.to_datetime(series, dayfirst=True, errors="coerce")
        if s1.notna().sum() >= s2.notna().sum():
            return s1
        else:
            return s2
        
        
def gabung(df_jarak, stations1, stations2, df_meteo, df_polu, output_dir, join_type="inner"):
    print("\nList Stasiun Polutan dan Meteorologi Terdekat:")
    os.makedirs(output_dir, exist_ok=True)

    for s2 in stations2:
        alamat2 = s2["alamat"]
        if alamat2 not in df_jarak.columns:
            print(f"{alamat2} tidak ditemukan dalam matriks jarak")
            continue

        nearest_row = df_jarak[alamat2].astype(float).idxmin()
        min_dist = df_jarak.loc[nearest_row, alamat2]

        closest = next((s1 for s1 in stations1 if s1["alamat"] == nearest_row), None)
        if closest is None:
            print(f"Stasiun {nearest_row} tidak ditemukan dalam daftar meteorologi")
            continue

        print(f"{alamat2} → {nearest_row} ({min_dist:.2f} km)")

        df2 = df_polu[s2["df_name"]].copy()
        df1 = df_meteo[closest["df_name"]].copy()
        
        if "stasiun" in df1.columns:
            df1 = df1.drop(columns=["stasiun"])

        # Normalisasi nama kolom tanggal
        def normalize_tanggal(df_):
            for cand in ["tanggal", "Tanggal", "TANGGAL", "tanggal_waktu", "waktu"]:
                if cand in df_.columns:
                    df_ = df_.rename(columns={cand: "Tanggal"})
                    break
            return df_

        df2 = normalize_tanggal(df2)
        df1 = normalize_tanggal(df1)

        df2["Tanggal"] = parsedate(df2["Tanggal"]).dt.date
        df1["Tanggal"] = parsedate(df1["Tanggal"]).dt.date

        merged = pd.merge(df2, df1, on="Tanggal", how=join_type, suffixes=("_Polu", "_Meteo"))

        out_dir_merge = r"D:\Skripsi\Program\Script\Dataset\Validasi new\6.Merging Dataset"
        os.makedirs(out_dir_merge, exist_ok=True)
        out_path = os.path.join(out_dir_merge, f"{s2['df_name']}_vs_{closest['df_name']}.xlsx")
        merged.to_excel(out_path, index=False)
        print(f"✔ Disimpan ke: {out_path}")

    print("\nSemua stasiun selesai digabungkan.")
    
    
output_dir = r"D:\Skripsi\Program\Script\Dataset\Validasi try\6.Merging Dataset"

gabung(matriks, StasiunMeteorologi, StasiunPolutan, df_meteo_proc, df_polu_proc,
       output_dir)
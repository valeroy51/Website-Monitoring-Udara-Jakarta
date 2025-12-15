from API.Utils.Program_MSSA import run_mssa_pipeline
from django.conf import settings
import os, glob

def run_mssa_for_all():
    BASE = settings.BASE_DIR
    
    MERGE_DIR = os.path.join(BASE, "Dataset", "Preprocess_2", "Merged")
    NORM_DIR  = os.path.join(BASE, "Dataset", "Preprocess_2", "MinMax")
    OUT_ROOT  = os.path.join(BASE, "Dataset", "MSSA")

    os.makedirs(OUT_ROOT, exist_ok=True)

    hasil = []
    merged_files = glob.glob(os.path.join(MERGE_DIR, "*.xlsx"))

    for path in merged_files:
        nama = os.path.splitext(os.path.basename(path))[0]
        if "_vs_" not in nama:
            continue

        pol, met = nama.split("_vs_")
        norm_pol = os.path.join(NORM_DIR, f"{pol}_MinMax.xlsx")
        norm_met = os.path.join(NORM_DIR, f"{met}_MinMax.xlsx")

        out_dir = os.path.join(OUT_ROOT, nama)
        os.makedirs(out_dir, exist_ok=True)

        h = run_mssa_pipeline(
            DATA_PATH=path,
            NORM_POL_PATH=norm_pol,
            NORM_MET_PATH=norm_met,
            OUT_DIR=out_dir,
            energy_thr=0.97,
            l_min=40,
            l_max=100,
            n_jobs_inner=-1
        )
        hasil.append({
            "pair": nama,
            "result": h
        })
        
        if hasil:
            import pandas as pd
            df_summary = pd.DataFrame([h["result"] for h in hasil])
            summary_path = os.path.join(OUT_ROOT, "Master_Summary.xlsx")
            df_summary.to_excel(summary_path, index=False)
            print(f"[MSSA] Master summary tersimpan di: {summary_path}")

        print(f"[MSSA] Selesai: {nama}")

    return hasil

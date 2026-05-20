# README

## Overview

1. Problem framming
2. Planned analisys.
3. How is Justice being assessed?


## Data Organization & Cleaning Process

This section describes the steps taken to load, organize, and consolidate multiple CSV data sources into a single unified dataframe (`upl`) for analysis.

---
### 0. Getting data

The source CSV files were obtained from the Encuesta Multipropósito, conducted jointly by DANE (Departamento Administrativo Nacional de Estadística) and the Secretaría Distrital de Planeación of Bogotá D.C. The survey is published as a large Excel workbook containing a wide range of socioeconomic and demographic variables at the UPL (Unidad de Planeamiento Local) level. From this workbook, a selection of variables considered relevant for an accessibility to education analysis were identified and exported individually as CSV files, each prefixed with em to indicate their origin from the Encuesta Multipropósito.

### 1. Loading CSV Files

All CSV files are loaded dynamically from a local folder and each of them is read into a dataframe.

**Example:** `em_ingreso_por_hogar.csv` → dataframe stored as `dfs["ingreso_por_hogar"]`

---

### 2. Merging into the `upl` Dataframe

A selection of columns from each source dataframe is merged into the main `upl` geodataframe using `CODIGO_UPL` as the join key (left join).

Only the relevant columns are brought in from each source. When multiple dataframes share a column name (e.g., `PROMEDIO`), columns are automatically renamed to `{df_name}_{column_name}` in lowercase to avoid conflicts.

#### Resulting Column Names

| Source Dataframe                    | Original Column    | Renamed To                                        |
|-------------------------------------|--------------------|---------------------------------------------------|
| `ingreso_por_hogar`                 | `PROMEDIO`         | `ingreso_por_hogar_promedio`                      |
| `promedio_edad`                     | `PROMEDIO`         | `promedio_edad_promedio`                          |
| `promedio_personas_hogar`           | `PROMEDIO`         | `promedio_personas_hogar_promedio`                |
| `minutos_al_estudio`                | `PROMEDIO`         | `minutos_al_estudio_promedio`                     |
| `minutos_al_trabajo`                | `PROMEDIO`         | `minutos_al_trabajo_promedio`                     |
| `satisfaccion_con_barrio_comunidad` | `PROMEDIO`         | `satisfaccion_con_barrio_comunidad_promedio`      |
| `satisfaccion_con_ingresos`         | `PROMEDIO`         | `satisfaccion_con_ingresos_promedio`              |
| `satisfaccion_con_la_vida`          | `PROMEDIO`         | `satisfaccion_con_la_vida_promedio`               |
| `personas_segun_sexo`               | `TOTAL_HOMBRE`     | `personas_segun_sexo_total_hombre`                |
| `personas_segun_sexo`               | `TOTAL_MUJER`      | `personas_segun_sexo_total_mujer`                 |
| `personas_segun_sexo`               | `TOTAL_INTERSEXUAL`| `personas_segun_sexo_total_intersexual`           |

---

### 3. Join Strategy

- **Type:** Left join — all rows from `upl` are preserved.
- **Key:** `CODIGO_UPL` — present in all source dataframes, not duplicated in the output.
- **Result:** A single enriched `upl` dataframe with one row per UPL unit and all relevant indicators as columns.

---

### Notes

- All merged column names are lowercased to ensure consistency.
- Source files must include a `CODIGO_UPL` column to be mergeable.

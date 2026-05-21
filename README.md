# README

## Overview

1. Problem framming

Access to higher education in Bogotá is not spatially equitable. Higher education institutions are concentrated in the central and north areas of the city, resulting in an unequal distribution of educational opportunities across the territory. This spatial inequality is reinforced by the socioeconomic conditions of the population, with areas with lower income tending to be further from educational offerings. This analysis seeks to highlight this dual dimension of spatial injustice: the physical and the socioeconomic.

1. Planned analisys

**Phase 1 - Physical Proximity:** Build a Simple Spatial Weights Matrix to measure connectivity between UPLs and HEIs.

**Phase 2 - Socioeconomic Capacity:** Incorporate average household income as an explanatory variable and see how this spatial inequality is reinforced by the socioeconomic conditions of the population.

3. How is Justice being assessed?
This analysis seeks to highlight this dual dimension of spatial injustice involving the physical and the socioeconomic factors.


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

A selection of columns from each source dataframe is merged into the main `upl` geodataframe using `CODIGO_UPL` as the join key (left join). Initially, several columns have been added even if now are not used (available to do future analysis)

When multiple dataframes share a column name (e.g., `PROMEDIO`), columns are automatically renamed to `{df_name}_{column_name}` in lowercase to avoid conflicts.

#### Resulting Column Names

| Source Dataframe                    | Original Column    | Renamed To                                        |
|-------------------------------------|--------------------|---------------------------------------------------|
| `ingreso_por_hogar`                    |`PROMEDIO`       | `ingreso_por_hogar_promedio  `                    |
| `promedio_edad`                        |`PROMEDIO`       | `promedio_edad_promedio`                          |
| `promedio_personas_hogar`              |`PROMEDIO`       | `promedio_personas_hogar_promedio`               |
| `minutos_al_estudio`                     | `PROMEDIO`         | `minutos_al_estudio_promedio`                     |
| `minutos_al_trabajo`                     | `PROMEDIO`         | `minutos_al_trabajo_promedio`                     |
| `personas_segun_sexo`                    | `PORCENTAJE_HOMBRE`     | `personas_segun_sexo_porcentaje_hombre`                |
| `personas_segun_sexo`                    | `PORCENTAJE_MUJER`      | `personas_segun_sexo_porcentaje_mujer`                 |
| `personas_segun_sexo`                    | `PORCENTAJE_INTERSEXUAL`| `personas_segun_sexo_porcentaje_intersexual`           |
| `personas_segun_si_actualmente_estudian` | `PORCENTAJE_SI` | `personas_segun_si_actualmente_estudian_porcentaje_si`           |
| `personas_segun_si_actualmente_estudian` | `PORCENTAJE_NO` | `personas_segun_si_actualmente_estudian_porcentaje_no`           |
| `personas_segun_si_saben_leer_y_escribir` | `PORCENTAJE_SI` | `personas_segun_si_saben_leer_y_escribir_porcentaje_si`           |
| `personas_segun_si_saben_leer_y_escribir` | `PORCENTAJE_NO` | `personas_segun_si_saben_leer_y_escribir_porcentaje_no`          |
| `nivel_educativo` | `PORCENTAJE_TECNICO` | `nivel_educativo_porcentaje_tecnico` |
| `nivel_educativo` | `PORCENTAJE_TECNOLOGO` | `nivel_educativo_porcentaje_tecnologo` |
| `nivel_educativo` | `PORCENTAJE_UNIVERSITARIO_INCOMPLETO` | n`ivel_educativo_porcentaje_universitario_incompleto` |
| `nivel_educativo` | `PORCENTAJE_UNIVERSITARIO_COMPLETO` | `nivel_educativo_porcentaje_universitario_completo` |

---

### 3. Join Strategy

- **Type:** Left join — all rows from `upl` are preserved.
- **Key:** `CODIGO_UPL` — present in all source dataframes, not duplicated in the output.
- **Result:** A single enriched `upl` dataframe with one row per UPL unit and all relevant indicators as columns.

---

### Notes

- All merged column names are lowercased to ensure consistency.
- Source files must include a `CODIGO_UPL` column to be mergeable.

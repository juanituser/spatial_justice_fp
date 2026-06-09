# Accessibility to higher education level

## Overview

### 1. Problem framming

Access to higher education in Bogotá is not spatially equitable. Higher Education Institutions (HEIs) are concentrated in the central and northern areas of the city, resulting in an unequal distribution of educational opportunities across the territory. This spatial inequality is further reinforced by the socioeconomic conditions of the population: Districts with lower income tend to be located further from educational offerings, and subjective factors such as life satisfaction and perception of the neighborhood may compound the difficulty of accessing higher education.

This analysis proposes that physical distance alone is insufficient to measure accessibility. A district may be 2km away from a HEI, but that distance is effectively greater when mediated by low income, dissatisfaction with life, or a weak sense of belonging to the community. The goal is to build a composite accessibility indicator that reflects both the spatial and the human dimensions of this inequality.

### 2. Planned Analysis

- **Phase 1 — Physical Proximity:** Calculate the number of HEIs within each district and the distance to the nearest HEI as a baseline physical accessibility variable. This represents the raw, unadjusted measure of spatial access.

- **Phase 2 — Socioeconomic Weighting:** Adjust the physical accessibility measure by incorporating average household income as a penalization factor. District with lower income will have their effective accessibility reduced, reflecting the real economic barriers that condition access to higher education beyond mere physical distance.

- **Phase 3 — Subjective Perception Weighting:** Further adjust the accessibility indicator by incorporating three satisfaction variables — satisfaction with neighborhood/community, satisfaction with income, and satisfaction with life in general. These variables capture how people's subjective experience of their environment may amplify the difficulty of accessing higher education, even when physical distance is moderate.

- **Phase 4 — Spatial Autocorrelation:** Build a Spatial Weights Matrix (Rook and Queen contiguity) and apply Moran's I to test whether districts with low composite accessibility cluster spatially. This clustering would constitute the core evidence of spatial injustice in the distribution of higher education access across Bogotá.

### 3. How is Justice being assessed?

Justice is assessed from a **distributive** perspective: are educational resources (HEIs) equitably distributed across the territory? And from a **social** perspective: do populations with lower socioeconomic capacity and lower life satisfaction face compounded barriers to accessing higher education?

The composite accessibility indicator built in this analysis allows for identifying which UPLs face the greatest structural disadvantage — not only because they are physically distant from HEIs, but because that distance is amplified by economic and subjective factors.

## Data sources

- Socioeconomic and demographic variables: [Secretaría Distrital de Planeación](https://sdp.gov.co/gestion-estudios-estrategicos/informacion-estadisticas/encuesta-multiproposito)
- Boundaries: [Mapas Bogotá](https://mapas.bogota.gov.co/#)
- Education Institutions: [Ministerio de Educacion Nacional ](https://www.mineducacion.gov.co/portal/)

## Data loading and preprocessing

### 0. Raw data

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
| `edad`                        |`PROMEDIO`       | `edad_promedio`                          |
|`personas_hogar` | `PROMEDIO`|`personas_hogar_promedio`|
|`satisfaccion_con_barrio_comunidad` | `PROMEDIO`|`satisfaccion_con_barrio_comunidad_promedio`|
|`satisfaccion_con_ingresos` | `PROMEDIO`|`satisfaccion_con_ingresos_promedio`|
|`satisfaccion_con_la_vida` | `PROMEDIO`|`satisfaccion_con_la_vida_promedio`|
|`nivel_educativo` | `PORCENTAJE_TECNICO`|`nivel_educativo_porcentaje_tecnico`|
|`nivel_educativo` | `PORCENTAJE_TECNOLOGO`|`nivel_educativo_porcentaje_tecnologo`|
|`nivel_educativo` | `PORCENTAJE_UNIVERSITARIO_COMPLETO`|`nivel_educativo_porcentaje_universitario_completo`|

---
### 3. Join Strategy

- **Type:** Left join — all rows from `upl` are preserved.
- **Key:** `CODIGO_UPL` — present in all source dataframes, not duplicated in the output.
- **Result:** A single enriched `upl` dataframe with one row per UPL unit and all relevant indicators as columns.

### 4. Superior Education Index

To measure the proportion of the population that has completed any form of higher education, a composite index was built by summing the percentages of people who finished each of the following levels:

- Technical (*Técnico*)
- Technological (*Tecnólogo*)
- University degree (*Universitario completo*)

These categories are mutually exclusive — a person appears in only one of them — so summing them yields the total percentage of people in each UPL who have achieved any higher education level. This index is the primary variable used in the spatial analysis to assess educational access across the city.

---

### Notes

- All merged column names are lowercased to ensure consistency.
- All source files included a `codigo_upl` column to be mergeable.


## Licencia
This project is under [MIT](./LICENCE.md).

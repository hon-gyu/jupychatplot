Chat with DataFrame inside Jupyter notebooks

### About
- Embedded in Jupyter notebooks
- Chat with pandas `DataFrame` or any data structure supporting the DataFrame Interchange Protocol (containing a `__dataframe__` attribute), including polars and pyarrow
- Create truly scientific visualizations using `altair`, `plotly`, and `matplotlib`
- Automatically perform Exploratory Data Analysis (EDA)

### Features
- drop-in replacement for `df.info()`, `df.describe()`

### Pipeline
DataFrame <-> Formal Representation of Visualization (FRV) <-> Visualization Code (`altair`, `plotly`, `matplotlib`) <-> Plot

With each chat interaction, the FRV is dynamically updated, increasingly incorporating context from the previous conversation history.

### TODO
- n_column, n_row
- about <-> data
- facts / insights <-> viz_code
  - relationship (2d and 3d)
  - distribution
  - outliers, anomalies and their explanations
- gen reports
  - about (summarized ver.)
  - list[tuple[str, str]]: [(facts / insights, viz_code)]
- critical questions
- suggested explorations
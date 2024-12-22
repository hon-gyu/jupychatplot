Chat with DataFrame inside Jupyter notebooks

### About
- Embedded in Jupyter notebooks
- Chat with pandas `DataFrame` or any data structure supporting the DataFrame Interchange Protocol (containing a `__dataframe__` attribute), including polars and pyarrow
- Create scientific and beautiful visualizations using `altair`, `plotly`, and `matplotlib`
- Automatically perform Exploratory Data Analysis (EDA)

### Pipeline
DataFrame <-> Formal Representation of Visualization (FRV) <-> Visualization Code (`altair`, `plotly`, `matplotlib`) <-> Plot

With each chat interaction, the FRV is dynamically updated, increasingly incorporating context from the previous conversation history.

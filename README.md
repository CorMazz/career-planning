# Wealth Calculator

## Exporting as HTML

`jupyter nbconvert --to html analysis.ipynb --TagRemovePreprocessor.remove_input_tags='{"hide_input"}'`

The tag preprocessor competely removes the input of cells with the "hide_input" tag. It was being a major PITA to try to figure out how to properly just add toggleable cells,
so I went with this as good enough.
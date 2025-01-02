# Sample Bonsai code

## Markdown
using the markdown `workflow` codeblock:
``````markdown
```workflow
../workflows/CentroidModel.bonsai
```
``````
using the `workflow` directive:
```markdown
:::{workflow}
../workflows/CentroidModel.bonsai
:::
```
or optionally providing alt-text:
``````markdown
```workflow
:alt: PredictCentroids
../workflows/CentroidModel.bonsai
```

or

:::{workflow}
:alt: PredictCentroids
../workflows/CentroidModel.bonsai
:::
``````

will render as
```workflow
:alt: PredictCentroids
../workflows/CentroidModel.bonsai
```
## RST
using the `workflow` directive:
```rst
.. workflow::
    ../workflows/CentroidModel.bonsai
```
or optionally providing alt-text:
```rst
.. workflow::
    :alt: PredictCentroids
    
    ../workflows/CentroidModel.bonsai
```
will render as
```{eval-rst}
.. workflow::
    :alt: PredictCentroids

    ../workflows/CentroidModel.bonsai
```

# Sample Bonsai code

## Markdown
using the markdown `workflow` codeblock:
``````markdown
```workflow ../workflows/CentroidModel.bonsai
```
``````
using the `workflow` directive:
```markdown
:::{workflow} ../workflows/CentroidModel.bonsai
:::
```
or optionally providing alt-text:
``````markdown
:::{workflow} ../workflows/CentroidModel.bonsai
    :alt: PredictCentroids
:::

```workflow ../workflows/CentroidModel.bonsai
    :alt: PredictCentroids
```
``````

will render as
```workflow ../workflows/CentroidModel.bonsai
```

## RST
using the `workflow` directive:
```rst
.. workflow:: ../workflows/CentroidModel.bonsai
```
or
```rst
.. workflow:: 
    ../workflows/CentroidModel.bonsai
```
or optionally providing alt-text:
```rst
.. workflow:: ../workflows/CentroidModel.bonsai
    :alt: PredictCentroids
```
will render as
```{eval-rst}
.. workflow:: ../workflows/CentroidModel.bonsai
```

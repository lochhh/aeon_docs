# Sample Bonsai code

## Markdown
```markdown
:::{workflow} ../workflows/CentroidModel.bonsai
:::

or optionally providing alt-text

:::{workflow} ../workflows/CentroidModel.bonsai
    :alt: PredictCentroids
:::
```
will render as

:::{workflow} ../workflows/CentroidModel.bonsai
:::

## RST
```rst
.. workflow:: ../workflows/CentroidModel.bonsai

or

.. workflow:: 
    ../workflows/CentroidModel.bonsai

or optionally providing alt-text

.. workflow:: ../workflows/CentroidModel.bonsai
    :alt: PredictCentroids
```
will render as
```{eval-rst}
.. workflow:: ../workflows/CentroidModel.bonsai
```

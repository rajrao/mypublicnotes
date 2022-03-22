Use **Explain** before the query to get the plan.

To view the query plan visually, you can use Graphviz (Dot) to generate an image. To do this, you need to output the plan in GraphViz dot format and this done by using Explain (Format Graphviz).

```
explain (FORMAT GRAPHVIZ)
select .....
from ....
```

Save the output a text file. The output is in DOT format, so you can save it as a ".dot" file. You need to copy everything after the "query plan" line.

```
Query Plan <<< !!SKIP THIS LINE!!
digraph logical_plan {
subgraph cluster_graphviz_plan {
...
...
...
}
```

Here is a sample command to convert the "dot" file to an image.

```
dot -Tpng c:\temp\explainPlan.dot -o c:\temp\explainPlanImage.png
```
More info about command line options in: https://graphviz.org/pdf/dotguide.pdf (page 24).


Notes:
https://docs.aws.amazon.com/athena/latest/ug/athena-explain-statement.html
https://www.youtube.com/watch?v=GcS02yTNwC0&t=1222s

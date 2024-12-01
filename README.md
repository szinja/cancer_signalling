# BMA Cancer Signalling Network Analysis

The model used for the analysis can be found at [CancerSgnalling.JSON](https://biomodelanalyzer.org/preloaded/CancerSignalling.json).

## This project has four python scripts
- ```script.py```:
> This script extracts the list of nodes in the network, and knockouts each node by setting the ```RangeFrom, RangeTo and Formula to 0```. The modified model is saved as ```KO_variableID.json``` under a different input folder.
> The importance of doing this is to later run the ```-engine VMCAI -prove``` command to check the stability of the network after each node is knocked out. We ultimately want to see which node is of significance to the network's stability, and which ones aren't. 

- ```script2.py```:
> Here we run the ```BioCheckConsole.exe``` file on the KO files directory one at a time, and store the results in an ```outputs``` directory. Each output file is named based on the node that was knocked out.
> For example:
> ```output_2.json``` corresponds to the network's state when node 2 is knocked out.

- ```script3.py```:
> Each output file has the following structure:
 - > ```Status```: ```Stabilizing``` indicates that the network does indeed reach a stable state after the knockout of the targeted node. 
 - > ```Error```: ```""``` shows us that there are no errors during execution.
 - > ```Ticks```: This is a list of time stamps towards stable converging of the network. A tick has ```Time``` of snapshot, and list of all```Variables```.
>
> For example: ``` { "Status": "Stabilizing", "Error": "", "Ticks": [ { "Time": 36, "Variables": [ {"Id": 2, "Lo": 0, "Hi": 0}, {"Id": 3, "Lo": 0, "Hi": 1}, ... ] }, ... ] }```
> With this particular ```CancerSignalling``` model, the network is stable after every knockout. This means that the network **converges** and the model has reached a stable state where the removal of certain nodes does not significantly alter it's overall behavior.


- ```script4.py```:
> The summary of the node states across all output files is saved as ```variable_changes_summary1.csv```, found under the output directory. This file makes it easier to see differences across knockouts and analyze dependencies between nodes.
> This table sorts the nodes numerically so it is clear which node has the most impact on the functionality of the network.
> We see that the network stabilizes regardless of which node is knocked out, evident from the ```Status: Stabilizing``` of all output files.
> The table stores the ```(Lo, Hi)``` values which remain the same across all knockouts.
> The **_critical node_** whose knockout causes major changes in the network's behavior is **<ins>Node 2</ins>**. The ```output_2.json``` file reveals distinct stabilization states for node 2. 


For any further questions, please feel free to drop me a message.
  

# random-graph-generator
## Abstract
The work being developed is based around the idea of creating a Generative Adversarial Network (GAN) for translating computerized images of 2-D graphs to tactile graphics. Tactile graphics are the standard format used by the Braille Authority of North America for conveying non-textual information to people who are blind or visually impaired. While this may include tactile representations of pictures, maps, graphs, diagrams, and other images, however, in the context of this project it will only represent 2-D graphs. Graphs of varying types will need to be generated, including but not limited to area graphs, bar charts, box plots, bubble plots, contour plots, error bar plots, histograms, KDE plots, line graphs, scatter plots, and violin plots. As having a reliable and robust set of training data is the fundamental step in any data science problem, **this project is concerned with generating an endless amount of fully randomized training data in the form of 2-D graphs**. These graphs will be plotted using random data generated through a multitude of ways and stylized with various libraries and themes. Once generated, the graphs will be fed into a GAN for translation in a future project alongside a graduate student of the same supervisor.

</br>

## Setup
The `setup/setup.sh` script can be used to automatically setup the project environment. However, if a manual installation is preferred, the instructions below provide a step-by-step breakdown of the entire process. Once completed, the notebook will be ready to run.

**Note:** The setup instructions below assume both [Anaconda](https://www.anaconda.com/products/individual) and [Jupyter](https://jupyter.org/install) are installed, and accessible through the command line. If they are not already installed, please do so. Additionally, both sets of setup instructions assume you are in the projects root dir.

</br> 

<details open>
<summary><b>Automated (Unix / MacOS)</b></summary>
    
1. *Execute the `setup/setup.sh` script*
    ```
    sh setup/setup.sh
    ```
1. *Select created kernel*

    As seen in the following image, switch the kernel to
    ```
    random-graph-generator-kernel
    ```
</details>

</br> 

<details>
<summary><b>Manual (Windows / Unix / MacOS)</b></summary>

1. *Create the conda environment using the `environment.yml` file included in the repository*
    ```
    conda env create -n random-graph-generator -f setup/environment.yml
    ```
1. *Activate the Anaconda environment you just created*
    ```
    conda activate random-graph-generator
    ```
1.  *Install an iPython kernel in the new environment*
    ```
    ipython kernel install --user --name=random-graph-generator-kernel 
    ```
1. *Deactivate the Anaconda environment*
    ```
    conda deactivate
    ```
1. *Start Jupyter (and open the generation notebook)*
    ```
    jupyter notebook random_graph_generator.ipynb
    ````
1. *Select created kernel*

    As seen in the following image, switch the kernel to
    ```
    random-graph-generator-kernel
    ```
</details>

</br>
</br>

## Research
All information regarding research and the techniques used for data generation can be found within Chapter 3 of the report.
This includes topics such as Midpoint Displacement, regression models, and distribution sampling amonst others.

</br>

## Output
Examples of generated output can be seen in the report Appendix under the Generation Output section.

</br>

## Libraries
- Python 3
- Jupyter
- scikit-learn
- NumPy
- pandas
- Altair
- Bokeh
- plotnine
- Matplotlib
- SciPy
- Anaconda

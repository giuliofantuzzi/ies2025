# Towards Smarter Player Scouting: Learning Football Player Embeddings with Variational Autoencoders (VAEs)

## About
This repository contains all the code necessary to replicate the experiments from the paper: <u>***Towards Smarter Player Scouting: Learning Football Player Embeddings with Variational Autoencoders (VAEs)***</u>, by [Giulio Fantuzzi](https://www.linkedin.com/in/giuliofantuzzi/),[Leonardo Egidi](https://leoegidi.github.io) and [Nicola Torelli](https://scholar.google.it/citations?user=l5fIs0wAAAAJ&hl=it), accepted at *[IES 2025](https://ies2025.sis-statistica.it) – Statistical Methods for Evaluation and Quality, the 12th Scientific Meeting of the Statistics for the Evaluation and Quality of Services Group of the Italian Statistical Society ([SVQS](https://www.svqs.it) - [SIS](https://www.sis-statistica.it))*.

The paper is available both in this repository (check [here](paper/ies2025_player-embeddings-vae.pdf)) and in the Book of the Conference, accessible [here](https://drive.google.com/file/d/1ok0qtSR0FbAjfU5w_icom5Z64L8gBNUL/view)

## Getting Started
To get started, first clone the repository (you may also want to fork it):

```bash
git clone https://github.com/giuliofantuzzi/ies2025.git
```

I recommend creating a virtual environment to avoid conflicts with your system's Python packages:

```bash
python -m virtualenv path/to/env
source path/to/env/bin/activate
pip install --upgrade pip
```

Once activated the environment, install the required dependencies specified in `pyproject.toml`:

```bash
cd ies2025/
pip install .
```

## Contents & Usage

This repository is organized as follows:

- [`data/`](data/)- contains the datasets used for training and evaluation, along with a [**data card**](data/README.md) detailing sources, preprocessing steps, and variable descriptions.
- [`models/`](models/) - contains the python implementation of the VAE model and the VAE loss.
- [`scraping/`](scraping/)- contains the code used to retrieve the data from web.
- [`data_processing.ipynb`](data_processing.ipynb)- a Jupyter notebook detailing all the data preprocessing steps.
- [`training.py`](training.py) - a python script to train the VAE model. To train the model with the paper configuration, run:
    ```bash
    python training.py --DataPath path/to/data --CheckpointsPath path/to/weights.pt
    ```
    Notice that different configurations can be specified directly from command line. To see all the available options, run:
    ```bash
    python training.py --help
    ```
- [`checkpoints/`](checkpoints/)- contains the weights of the trained model (stored as `vae.pth` file).
- [`experiments.ipynb`](experiments.ipynb): a python notebook to reproduce the experimental results from Section 4 of the paper.

# Difforge

Difforge is a diffusion model designed to generate structures in Minecraft. It integrates a diffusion process with custom data formats, a block vectorizer, and a web scraper to collect and process Minecraft structures. The project aims to generate realistic and creative structures using AI-driven techniques.

Difforge is a project for a class at Cal Poly SLO (CSC 570 - AI in Games - Rodrigo Canaan)

Project Team Members: David Hernandez, Gannon Gonsiorowski, Mitashi Parikh and Xiuyuan Qiu

This repo holds code for different models we tried throughout the quarter. Many of these models failed to generate interesting buildings, but we still include the code in this repo. Because many of the models were fundamentally different and relied on completely different libraries, we have included requirements.txt files in the different dirs of this repo. 

## Results
Results are provided in the ```mcvis/``` directory. Since diffusion can be computationally intensive, we have a [video version of our demo](https://www.youtube.com/watch?v=tiw2H88Os1Q).

## Usage
See individual directories and submodules for usages. See ```TODO``` section below for more information.

## TODO:
- Convert this repo into a streamlined Minecraft PCGML repo. Ideally, this codebase would be more modular. There would be one python file that could be called to train/evaluate a number of models. There would be a singular requirements.txt file that contains only the necessary packages to run our code.
- Add functionality to the MC Vectorizer submodule in datatype/. Ideally, this package could translate between Litematic, Schematic, GrabCraft Blueprints, Render Objects, and a string based format for transformers (see [MarioGPT's](https://github.com/shyamsn97/mario-gpt/tree/main) level encoding scheme).
- Continue training diffusion models to generate structures.
 
## Project Structure

The repository is organized as follows:

```
├── difforge
│   ├── datatype         # Custom data formats and block vectorization logic
│   ├── diffusion        # Contains the diffusion model for voxel-based generation
│   ├── mcvis           # Visualizations for models
│   ├── models          # Trained models and checkpoints
│   ├── scraper         # Web scraper for gathering Minecraft structure data
│   ├── utils           # Helper functions and utilities
│   ├── .gitignore       # Files to be ignored by Git
│   ├── .gitmodules       # Submodules included in this repo
│   ├── README.md        # Project documentation
```

## Development Standards

### Git Workflow
- Follow the Git feature-branch workflow:
  1. Create a new branch for each feature or fix (`git checkout -b feature-name`)
  2. Commit changes with clear messages (`git commit -m "Add feature description"`)
  3. Push to the remote repository (`git push origin feature-name`)
  4. Open a pull request for review before merging
- Keep the `main` branch stable and functional
- Use meaningful commit messages. Commit messages should start with a present-tense verb (add, update, remove/rm, fix, etc.)
- Regularly pull from `main` to keep branches up to date

### Dependencies and Environments
- Use `pip` for managing dependencies. Install requirements with:
  ```sh
  pip install -r requirements.txt
  ```
- A `conda` environment is recommended for development. Create it with:
  ```sh
  conda env create -f backup_env.yml
  conda activate difforge
  ```
- When adding new dependencies:
  - Update `requirements.txt` (`pip freeze > requirements.txt`)
  - Update `environment.yml` accordingly

### .gitignore Etiquette
Ensure `.gitignore` includes:
- Virtual environments (`venv/`, `.env/`)
- Python cache files (`__pycache__/`, `*.pyc`, `*.pyo`)
- Large files and datasets (`data/`, `*.csv`, `*.json` unless necessary)
- Model checkpoints (`models/`, `*.pt`, `*.h5`)
- Logs and temporary files (`logs/`, `*.log`, `*.tmp`)

## Contributing Guide

We welcome contributions! To get started:

1. **Fork the Repository** – Click the "Fork" button on GitHub.
2. **Clone Your Fork** –
   ```sh
   git clone https://github.com/your-username/difforge.git
   cd difforge
   ```
3. **Set Up the Environment** –
   ```sh
   conda env create -f backup_env.yml
   conda activate difforge
   pip install -r requirements.txt
   ```
4. **Create a Branch** –
   ```sh
   git checkout -b feature-name
   ```
5. **Make Changes & Commit** – Ensure commits are atomic and descriptive.
6. **Push to GitHub** –
   ```sh
   git push origin feature-name
   ```
7. **Open a Pull Request** – Submit changes for review.

### Code Style & Testing
- Follow PEP8 for Python code style
- Write unit tests where applicable (`tests/` directory)
- Run tests before submitting PRs:
  ```sh
  pytest tests/
  ```

---


# 📦 Data Versioning with DVC (Hands-on Experiment)
## Project Overview
This repository demonstrates how to use **DVC (Data Version Control)** along with **Git** to version large data files while keeping the Git repository lightweight and reproducible.
Instead of storing data files directly in Git, DVC tracks them using **small metadata (`.dvc`) files** that contain a **hash of the data**. Git tracks the code and these metadata files, while DVC stores the actual data in a **separate remote location** (local storage in this experiment).
This setup allows:
- Clean Git history
- Multiple data versions with the same filename
- Easy rollback and reproducibility of experiments

## Experiment Summary
Two versions of the same dataset (`customer.csv`) are created using different preprocessing logic:
- **Version 1**:
    - Removes textual columns
    - Drops `Avg. Session Length`
    - Keeps rows where `Length of Membership > 3`
- **Version 2**:
    - Removes textual columns
    - Drops `Time on Website`
    - Keeps rows where `Length of Membership > 1`
Each version is tracked using DVC and linked to a specific Git commit.

## Tech Stack
- Python
- Git
- DVC
- Pandas

## Reproducing This Project
`git clone <repo_url> dvc pull`
After running these commands, the repository will be restored with the **correct version of the dataset** corresponding to the current Git commit.

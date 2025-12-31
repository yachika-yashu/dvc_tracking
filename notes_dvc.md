# Data Versioning with DVC – Step-by-Step 
DVC maintains a **separate data repository**, which can be either **local or cloud-based**, specifically to track large data files. Instead of storing the actual data file (like `data.csv`) in Git, DVC tracks it using a **small metadata file**. This metadata file contains important information such as a **hash of the data**, which uniquely represents the exact version of that data. Because this metadata file is very small, it is safely tracked by **Git along with Python code and other source files**. Git is responsible for versioning the code and DVC metadata, while **DVC handles the actual data files**. When we run `git pull`, Git pulls the latest code and DVC metadata files. After that, when we run `dvc pull`, DVC reads the metadata file, checks the data version using the stored hash, and then pulls the **correct version of the data file** from the DVC remote storage. In this way, Git and DVC work together to ensure that the **code, metadata, and data are always in sync** and reproducible in the future.
## Step 1 – Explain the Problem Statement
### What I am doing
I am creating **two different versions of the same dataset** using different preprocessing logic.
### Why I am doing this
DVC makes sense only when:
- Data changes
- File name stays the same
- We want to reproduce older experiments
### Experiments
**Version 1**
- Remove all textual columns
- Drop column `Avg. Session Length`
- Keep rows where `Length of Membership > 3`
**Version 2**
- Remove all textual columns
- Drop column `Time on Website`
- Keep rows where `Length of Membership > 1`
Later, I will **switch between these two versions** using Git + DVC.
## Step 2 – Create Project Directory Structure
```bash
cd dvc_tracking
subl .
```
```bash
mkdir src
mkdir data
```
### Why this step exists
- `src/` → code lives here (tracked by Git)
- `data/` → data lives here (tracked by DVC)
Keeping them separate avoids confusion.
## Step 3 – Initialize Git and DVC
```bash
git init
```
```bash
pip install dvc
dvc init
```
### Why both are required
- Git alone cannot handle large data
- DVC cannot replace Git
They must be initialized **together** so they cooperate.
### What changes
- `.git/` → Git internal tracking
- `.dvc/` → DVC internal tracking
- `.dvcignore` → files DVC should ignore
## Step 4 – Understand DVC Files
After `dvc init`:
- `.dvc/` contains:
    - `config` → DVC remote info
    - `.gitignore` → prevents Git from tracking DVC internals
- `.dvcignore` → prevents DVC from tracking unwanted files
This is DVC’s **control center**.
## Step 5 – Create GitHub Repository
### Why
Remote Git repository is needed to:
- Share code
- Store `.dvc` metadata
- Reproduce experiments later
## Step 6 – Add Git Remote
```bash
git remote add origin https://github.com/yachika-yashu/dvc_tracking.git
```
### Why
This connects **local Git → GitHub**.

## Step 7 – Add DVC Remote (Local Storage)
### Why this is necessary
DVC does **not store actual data in Git**.  
It needs a **separate location** to store data files.
Find temp directory:
```bash
echo %temp%
```
Add DVC remote:
```bash
dvc remote add -d myremote C:\Users\yachi\AppData\Local\Temp\dvc_track
```
### What changes
`.dvc/config` is updated:
```ini
[core]
    remote = myremote
['remote "myremote"']
    url = C:\Users\yachi\AppData\Local\Temp\dvc_track
```
Now DVC knows **where data will be pushed and pulled from**.

## Step 8 – First Git Commit (DVC Setup)
```bash
git status
git add .
git commit -m "Initial commit with dvc config files"
```
### Why this commit is important
This locks:
- DVC configuration
- Remote information
Anyone cloning this repo will have **the same DVC setup**.
## Step 9 – Write and Run Python Code (Version 1)
`src/data_ingestion.py`
```python
import pandas as pd
import os
df = pd.read_csv(
    'https://raw.githubusercontent.com/araj2/customer-database/master/Ecommerce%20Customers.csv'
)
df = df.iloc[:, 3:]
df = df[df['Length of Membership'] > 3]
df.drop(columns=['Avg. Session Length'], inplace=True)
df.to_csv(os.path.join('data', 'customer.csv'), index=False)
```
Run:
```bash
python src/data_ingestion.py
```
### What this produces
- `data/customer.csv`
- 364 rows
- This is **data version 1**
At this point:
- Git sees a CSV
- DVC has not tracked it yet
## Step 10 – DVC Add (Most Important Step)
```bash
dvc add data/customer.csv
```
### Why this step exists
This tells DVC:
> “This file should be versioned by you, not Git.”
### What happens internally
1. DVC computes a **hash** of the file
2. File is stored in **DVC cache (staging area)**
3. `data/.gitignore` is updated → Git ignores CSV
4. `customer.csv.dvc` file is created
The `.dvc` file is the **only thing Git tracks for data**.
## Step 11 – Git Add Code and DVC Metadata
```bash
git status
git add .
```
### Why
We commit:
- Python code
- `.dvc` metadata file  
    Not the CSV itself.
## Step 12 – Git Commit (Version 1)
```bash
git commit -m "version 1"
```
### Meaning of this commit
“This code depends on **this exact data version**.”

## Step 13 – Push Data to DVC Remote
```bash
dvc push
```
### Why
This uploads the actual CSV to the DVC remote storage.

## Step 14 – Push Code to GitHub (Experiment 1)
```bash
git push origin master
```
### Observation
GitHub **does not contain the CSV**, only `.dvc` files.

## Step 15 – Start Experiment 2 (Change Code)
Modify `data_ingestion.py`:
```python
df = df[df['Length of Membership'] > 1]
df.drop(columns=['Time on Website'], inplace=True)
```
Run:
```bash
python src/data_ingestion.py
```
### Result
- 496 rows
- Same filename
- Different data → **new version**
## Step 16 – Check Status
```bash
git status
dvc status
```
Shows:
- Data changed
- Metadata outdated
## Step 17 – DVC Add (Version 2)
```bash
dvc add data/customer.csv
```
### Meaning
DVC creates a **new hash**, representing version 2.

## Step 18 – Git Add Updated Files
```bash
git add .
```
Modified:
- `customer.csv.dvc`
- `data_ingestion.py`
## Step 19 – Git Commit (Version 2)
```bash
git commit -m "version 2"
```

## Step 20 – Push Everything
```bash
dvc push
git push origin master
```

## Rolling Back to Any Version
```bash
git log --oneline
git checkout <commit_hash>
dvc checkout
```
### Why both commands
- Git restores **code + metadata**
- DVC restores **matching data**

## Cloning This Repo Later
```bash
git clone <repo_url>
dvc pull
```
Equivalent to:
- `dvc fetch`
- `dvc checkout`
## What Happens When You Clone This Repo?
When you run `git clone`, Git downloads:
- Source code
- DVC configuration
- `.dvc` metadata files (which act as pointers to data)
The **actual data file is not downloaded** because Git never tracked it.  
Running `dvc pull` completes the setup by restoring the data.
Internally, `dvc pull` is equivalent to running:
- **`dvc fetch`** → downloads the required data from the DVC remote into the local DVC cache
- **`dvc checkout`** → places the correct version of the data into the working directory (`data/customer.csv`) based on the current Git commit
This two-step process ensures that **code, metadata, and data are always in sync**, making the experiment fully reproducible.

# 🌍 Earthquake Prediction Using Machine Learning & Deep Learning

![License](https://img.shields.io/github/license/your-github-id/earthquake-prediction)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Framework](https://img.shields.io/badge/Built%20With-FastAPI|TensorFlow|ScikitLearn-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-green)

> Predict earthquake **magnitude** and **severity** using ML/DL to support disaster preparedness and early warning systems.  
> Real-time interactive web app hosted on [Hugging Face App Here 🤗](https://luffyking-earthquake-predictor.hf.space/?__theme=system).

---

## 📚 Table of Contents

- [🌟 Project Overview](#-project-overview)
- [👥 Team Members](#-team-members)
- [📊 Data Sources](#-data-sources)
- [⚙️ Methodology](#-methodology)
- [📈 Key Results](#-key-results)
- [🛠️ Built With](#-built-with)
- [🚀 How to Use](#-how-to-use)
- [🌐 Hugging Face App](#hugging-face-app)
- [🤝 Contributing](#-contributing)
- [🔮 Future Work](#-future-work)
- [📄 License](#-license)
- [✉️ Contact Us](#-contact-us)
- [🙏 Acknowledgments](#-acknowledgments)
- [📖 Citation](#-citation)

---

## 🌟 Project Overview

This project leverages **Machine Learning (ML)** and **Deep Learning (DL)** to:

- 🔍 Predict earthquake **magnitudes** (e.g., 6.5 Richter)
- ⚠️ Classify severity levels: *mild*, *moderate*, *severe*
- 🌐 Visualize temporal & spatial earthquake patterns
- 🧐 Explore time-based sequences using **LSTM** and **Neural Networks**
- 🚀 Provide a **real-time Hugging Face app** for user interaction

🎯 **Objective**: Empower communities with predictive tools for early warning & seismic research.

---

## 👥 Team Members


| Name    | GitHub                                                  | Email    |
|---------|---------------------------------------------------------|----------|
| SIBANSHA MISHRA   | [[GitHubID](https://github.com/SIBANSHAMISHRA)1]([https://github.com/GitHubID1](https://github.com/SIBANSHAMISHRA))               | sibanshamishra73@gmail.com   |
| DEEPAM JYOTI MOHANTY   | [[GitHubID2](https://github.com/PHONEIX-06)]([https://github.com/GitHubID2](https://github.com/PHONEIX-06))               | deepamjyoti12345@gmail.com   |
| SATYAKAM ACHARYA   | [[GitHubID3](https://github.com/Satyakamcoder)]([https://github.com/GitHubID3](https://github.com/Satyakamcoder))               | acharyasatyakam03@gmail.com   |
| SAMBIT PRUTHWIRAJ MOHANTY   | [[GitHubID4](https://github.com/SambitPruthwiraj)]](https://github.com/SambitPruthwiraj)               | sambitpruthwiraj@gmail.com   |
| ARBIND MISHRA   | [[GitHubID5](https://github.com/Arbind4678)]([https://github.com/GitHubID5](https://github.com/Arbind4678))               | arbindmishra4678@gmail.com   |
| SAMIR PARIDA   | [[GitHubID6](https://github.com/samirparida-119)]([https://github.com/GitHubID6](https://github.com/samirparida-119))               | Paridasamir71@gmail.com   |

---

## 📊 Data Sources

| Dataset                    | Description                | Rows   | Key Columns                                      | Source |
|----------------------------|----------------------------|--------|--------------------------------------------------|--------|
| `earthquake_1995-2023.csv` | Historical seismic records | ~1,575 | `magnitude`, `date_time`, `depth`, `lat`, `lon`  | USGS   |
| `earthquake_3000_plus.csv` | 2025 earthquake records    | ~3,000 | `time`, `year`, `month`, `mag`, `depth`, `severity` | USGS   |

📌 *Earthquake clustering & heatmaps visualized via Plotly.*

---

## ⚙️ Methodology

### 🔧 Data Preprocessing
- Removed null/missing entries
- Extracted `year`, `month`, and `timedelta`
- Applied clustering for regional grouping

### 🤖 Model Development

#### Magnitude Prediction
- `RandomForestRegressor`
- `Dense Neural Networks`
- `LSTM` for time-based patterns

#### Severity Classification
- `RandomForestClassifier`
- `LSTM` for sequence classification

### 📊 Model Evaluation
- Metrics: **MAE**, **RMSE**, **R²**, **Accuracy**
- Charts: Line plots, confusion matrices, feature importance

### 🌐 Deployment
- API: Built with **FastAPI**
- Hosted: **Hugging Face Spaces**
- DB: **Firebase** for real-time storage
- Models saved via `joblib` & `HDF5`

---

## 📈 Key Results

| Model                       | Task                 | MAE  | RMSE | R² / Accuracy |
|-----------------------------|----------------------|------|------|---------------|
| `RandomForestRegressor`     | Magnitude Prediction | 0.32 | 0.54 | 0.87          |
| `Dense Neural Network`      | Magnitude Prediction | 0.28 | 0.48 | 0.89          |
| `LSTM`                      | Magnitude Prediction | 0.25 | 0.45 | 0.91          |
| `RandomForestClassifier`    | Severity Classification | –    | –    | 87.6%         |
| `LSTM`                      | Severity Classification | –    | –    | 90.3%         |

🖼️ *Add your graphs, model curves, and confusion matrices here.*

---

## 🛠️ Built With

- 💻 Python 3.8+
- 🤖 Scikit-learn, TensorFlow, Keras
- 📊 Pandas, NumPy, Seaborn, Plotly, Matplotlib
- 🚀 FastAPI
- 🔥 Firebase (Realtime DB)
- 🤗 Hugging Face Spaces

---

## 🚀 How to Use

```bash
# 1. Clone the repo
git clone https://github.com/your-github-id/earthquake-prediction.git
cd earthquake-prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the notebook
jupyter notebook Earthquake_prediction.ipynb
```

---

## 🌐 Hugging Face App

- 🌐 **Online Demo:** Try our model on [[[Hugging Face Spaces](https://luffyking-earthquake-predictor.hf.space/?__theme=system)]] for an interactive web demo.
- ⚙️ **No Installation Required:** Simply click the link above to access the demo; no setup needed.
<!-- 📸 Screenshot: Add an illustrative screenshot of the Hugging Face App interface here. -->

---

## 🤝 Contributing

- 🤝 **Contributions Welcome:** We encourage contributions from the community! Please feel free to submit issues or pull requests.
- ✨ **Pull Requests:** For major changes, please open an issue to discuss your idea before submitting a pull request.
- 🛠️ **Development Setup:** To get started, clone the repo and install dependencies:
    ```bash
    git clone https://github.com/your-github-id/earthquake-prediction.git
    cd earthquake-prediction
    pip install -r requirements.txt
    ```
- 📚 **Guidelines:** See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community guidelines.

---

## 🔮 Future Work

- 🔭 **New Features:** Add advanced analytics and an interactive visualization dashboard.
- 🌐 **Multilingual Support:** Extend support for more languages and diverse datasets.
- ⚡ **Optimization:** Improve model performance and reduce latency for real-time applications.

---

## 📄 License

📄 This project is licensed under the [MIT License](LICENSE).

---

## ✉️ Contact Us

- 📫 **Email:** [sibanshamishra73@gmail.com](mailto:your.email@example.com)
- 💬 **GitHub Issues:** Use the [Issues Page](https://github.com/SIBANSHAMISHRA/EARTHQUAKE-PREDICTION-SYSTEM/issues) to ask questions.
- 👤 **Maintainer:** [[SIBANSHAMISHRA](https://github.com/SIBANSHAMISHRA)]([[https://github.com/your-github-id](https://github.com/SIBANSHAMISHRA)])

---

## 🙏 Acknowledgments

- 🙏 **USGS Earthquake Hazards Program**
- 🛠️ **Hugging Face**, **Firebase**, **Scikit-learn**, **TensorFlow**, **Keras**
- 📊 **Plotly**, **FastAPI**, **Seaborn**
- 🎓 Inspired by open-source contributors and the data science community.

---

## 📖 Citation

```bibtex
@misc{YourTeam2025,
  title        = {Earthquake Prediction Using Machine Learning and Deep Learning},
  author       = {TITAN},
  year         = {2025},
  howpublished = [{(https://github.com/SIBANSHAMISHRA/EARTHQUAKE-PREDICTION-SYSTEM)}],
}
```

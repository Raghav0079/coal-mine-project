# Coal Mine Project 🏭

A comprehensive data science project for analyzing coal mine operations data through exploratory data analysis and machine learning models.

## 📁 Project Structure

```
coal-mine-project/
├── README.md                 # Project documentation
├── dataset/                  # Data storage
│   ├── batch1.csv           # Dataset batch 1
│   ├── batch2.csv           # Dataset batch 2
│   ├── batch3.csv           # Dataset batch 3
│   ├── batch4.csv           # Dataset batch 4
│   ├── batch5.csv           # Dataset batch 5
│   ├── batch6.csv           # Dataset batch 6
│   ├── batch7.csv           # Dataset batch 7
│   ├── batch8.csv           # Dataset batch 8
│   ├── batch9.csv           # Dataset batch 9
│   ├── batch10.csv          # Dataset batch 10
│   └── convert_to_csv.py    # Data conversion utility
└── training/                 # Training and analysis notebooks
    ├── eda.ipynb            # Exploratory Data Analysis
    ├── training.ipynb       # Model training notebook 1
    ├── training2.ipynb      # Model training notebook 2
    └── training3.ipynb      # Model training notebook 3
```

## 🎯 Project Overview

This project analyzes coal mine operational data across multiple batches to extract insights and build predictive models. The analysis includes:

- **Exploratory Data Analysis (EDA)**: Understanding data distributions, patterns, and relationships
- **Data Processing**: Combining multiple data batches and preprocessing
- **Machine Learning**: Building and training predictive models
- **Visualization**: Creating interactive plots and dashboards

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Jupyter Notebook or JupyterLab
- Required Python libraries (see Installation)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Raghav0079/coal-mine-project.git
cd coal-mine-project
```

2. Install required dependencies:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy plotly jupyter
```

### Running the Analysis

1. **Exploratory Data Analysis**:
```bash
jupyter notebook training/eda.ipynb
```

2. **Model Training**:
```bash
jupyter notebook training/training.ipynb
```

## 📊 Dataset

The project uses coal mine operational data split across 10 batch files (batch1.csv to batch10.csv). The data is automatically combined during the analysis process.

### Data Loading

The EDA notebook automatically:
- Discovers all batch CSV files
- Loads and combines them into a single dataset
- Tracks the source batch for each record
- Reports combined dataset statistics

## 🔧 Features

- **Automated Batch Processing**: Combines multiple data batches seamlessly
- **Statistical Analysis**: Comprehensive statistical summaries and tests
- **Data Visualization**: Interactive plots using Plotly and Seaborn
- **Dimensionality Reduction**: PCA and t-SNE analysis
- **Machine Learning**: Multiple training approaches and model iterations

## 📈 Analysis Components

### 1. Exploratory Data Analysis (eda.ipynb)
- Data loading and combination
- Statistical summaries
- Distribution analysis
- Correlation analysis
- Feature engineering
- Visualization dashboards

### 2. Model Training (training.ipynb, training2.ipynb, training3.ipynb)
- Multiple modeling approaches
- Feature selection
- Model evaluation
- Performance comparison
- Hyperparameter tuning

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib & Seaborn**: Static visualizations
- **Plotly**: Interactive visualizations
- **Scikit-learn**: Machine learning algorithms
- **Jupyter**: Interactive development environment

## 📝 License

This project is available for educational and research purposes.

## 👤 Author

**Raghav0079**

- GitHub: [@Raghav0079](https://github.com/Raghav0079)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## ⭐ Show your support

Give a ⭐️ if this project helped you!

---

*Last updated: January 2026*

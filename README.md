# Coal Mine Project 🏭

A comprehensive data science project for analyzing coal mine operations data through exploratory data analysis and machine learning models.

## 📁 Project Structure

```
coal-mine-project/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── app.py                   # Main application
├── config.py                # Configuration settings
├── convert_to_csv.py        # Data conversion utility
├── dataset/                 # Data storage
│   ├── batch1.csv          # Dataset batches
│   └── ...                 # (batch2.csv to batch10.csv)
├── training/                # Training and analysis notebooks
│   ├── eda.ipynb           # Exploratory Data Analysis
│   ├── training.ipynb      # Model training notebooks
│   └── ...                 # Additional training notebooks
├── model results/           # Model outputs and results
└── assets/                  # Static assets
```

## 🎯 Project Overview

This project analyzes coal mine operational data across multiple batches to extract insights and build predictive models. The analysis includes:

- **Exploratory Data Analysis (EDA)**: Understanding data distributions, patterns, and relationships
- **Data Processing**: Combining multiple data batches and preprocessing
- **Machine Learning**: Building and training predictive models
- **Interactive Dashboard**: Web-based visualization using Dash/Plotly

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Raghav0079/coal-mine-project.git
cd coal-mine-project
```

2. **Create and activate a virtual environment:**

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

3. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Project

1. **Start the web application:**
```bash
python app.py
```

2. **Run Jupyter notebooks for analysis:**
```bash
jupyter notebook training/
```

3. **Access the dashboard:**
   - Open your browser and navigate to `http://localhost:8050`

## 📊 Dataset

The project uses coal mine operational data split across 10 batch files (batch1.csv to batch10.csv). The data is automatically processed and combined during analysis.

## 🔧 Features

- **Interactive Dashboard**: Real-time data visualization using Dash
- **Automated Batch Processing**: Combines multiple data batches seamlessly  
- **Statistical Analysis**: Comprehensive statistical summaries and tests
- **Machine Learning Models**: Predictive analytics and model evaluation
- **Responsive Design**: Bootstrap-styled web interface

## 📈 Technologies Used

- **Python**: Core programming language
- **Dash**: Interactive web applications
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Scikit-learn**: Machine learning algorithms
- **Gunicorn**: WSGI HTTP Server (for deployment)

## 🗂️ Key Dependencies

```
dash==2.16.1
plotly==5.17.0
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
dash-bootstrap-components==1.5.0
gunicorn==21.2.0
```

## 🚀 Deployment

The application is ready for deployment with Gunicorn:

```bash
gunicorn app:server
```

## 📝 Virtual Environment Management

This project uses a virtual environment to manage dependencies:

- **Virtual environment directory**: `.venv/` (excluded from Git)
- **Dependencies**: Listed in `requirements.txt`
- **Activation**: Use the commands above based on your OS

**Note**: The `.venv` directory is automatically excluded from version control via `.gitignore`

## 👤 Author

**Raghav0079**
- GitHub: [@Raghav0079](https://github.com/Raghav0079)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⭐ Show your support

Give a ⭐️ if this project helped you!

---

*Last updated: January 2026*

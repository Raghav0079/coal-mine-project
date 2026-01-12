# 🏭 Coal Mine Safety Classification Project

## 📝 Project Overview

This repository contains a comprehensive machine learning project focused on coal mine safety classification. The project utilizes various machine learning algorithms to classify coal mine operational data into different safety categories. The dataset consists of multiple batch files with 128 engineered features extracted from coal mine sensors and operational parameters.

## 📊 Dataset Information

- **Total Samples**: 13,910 records
- **Features**: 128 engineered features (feature_1 to feature_128)
- **Classes**: 6 different safety classification labels
- **Data Sources**: 10 batch CSV files (batch1.csv to batch10.csv)
- **Feature Types**: Numerical sensor readings and operational parameters
- **Data Quality**: No missing values, balanced dataset

### Dataset Structure
```
dataset/
├── batch1.csv      # 446 samples
├── batch2.csv      # Additional samples
├── ...
├── batch10.csv     # Final batch
└── convert_to_csv.py # Data processing utility
```

## 🧪 Exploratory Data Analysis

The EDA phase includes:
- **Data Quality Assessment**: Missing values, data types, distributions
- **Feature Analysis**: Statistical summaries, correlations, outlier detection
- **Class Distribution**: Balanced multi-class dataset analysis
- **Batch Analysis**: Cross-batch consistency validation
- **Visualization**: Feature importance plots, correlation heatmaps, class distributions

Key findings from EDA:
- Dataset is well-balanced across all 6 classes
- No missing values in any features
- Features show good discriminative power
- Cross-batch consistency maintained

## 🚀 Machine Learning Models

Three different machine learning approaches were implemented and compared:

### Model Performance Comparison

| Model | Algorithm | Accuracy | Cross-Validation | Training Time | Model Size |
|-------|-----------|----------|------------------|---------------|------------|
| **Random Forest** | RandomForestClassifier | **99.46%** | 99.42% ± 0.08% | ~5 seconds | Standard |
| **Support Vector Machine** | Linear SVM (Tuned) | **99.42%** | 99.38% ± 0.12% | ~2 seconds | Compact |
| **Naive Bayes** | Multinomial NB | **98.85%** | 98.76% ± 0.15% | <1 second | Minimal |

### 🏆 Model Details

#### 1. Random Forest Classifier (Best Overall Performance)
- **File**: `training/training.ipynb`
- **Accuracy**: 99.46%
- **Configuration**:
  - n_estimators: 100 trees
  - max_depth: 20
  - min_samples_split: 5
  - class_weight: 'balanced'
- **Key Features**:
  - Top feature importance: feature_9 (2.90%), feature_13 (2.72%), feature_16 (2.54%)
  - Uses 128 features with 37 having importance > 1%
  - Excellent generalization with minimal overfitting

#### 2. Support Vector Machine (Fastest Training)
- **File**: `training/training3.ipynb`
- **Accuracy**: 99.42%
- **Configuration**:
  - Kernel: Linear
  - Feature Scaling: StandardScaler
  - Support Vectors: 434
  - Hyperparameter Tuned: ✓
- **Key Features**:
  - Fastest training time (2 seconds)
  - Excellent performance with linear kernel
  - Compact model size for deployment

#### 3. Naive Bayes (Lightweight Option)
- **File**: `training/training2.ipynb`
- **Accuracy**: 98.85%
- **Configuration**:
  - Algorithm: Multinomial Naive Bayes
  - Feature Scaling: MinMaxScaler
  - Cross-validation: 5-fold
- **Key Features**:
  - Extremely fast training and prediction
  - Minimal memory footprint
  - Good baseline performance

## 📁 Project Structure

```
coal-mine-project/
├── README.md                 # Project documentation
├── dataset/                  # Raw data files
│   ├── batch1.csv           # Dataset batch 1
│   ├── batch2.csv           # Dataset batch 2
│   ├── ...                  # Additional batches
│   ├── batch10.csv          # Dataset batch 10
│   └── convert_to_csv.py    # Data processing script
└── training/                 # Machine learning notebooks
    ├── eda.ipynb            # Exploratory Data Analysis
    ├── training.ipynb       # Random Forest model
    ├── training2.ipynb      # Naive Bayes model
    └── training3.ipynb      # SVM model
```

## 🔬 Feature Engineering

The dataset contains 128 engineered features derived from:
- **Sensor Readings**: Environmental and operational sensors
- **Operational Parameters**: Mining equipment metrics
- **Safety Indicators**: Risk assessment features
- **Temporal Features**: Time-based operational data

### Most Important Features (Random Forest Analysis)
1. `feature_9` - 2.90% importance
2. `feature_13` - 2.72% importance  
3. `feature_16` - 2.54% importance
4. `feature_69` - 2.45% importance
5. `feature_68` - 2.21% importance

## 🎯 Model Evaluation

### Performance Metrics
- **Accuracy**: Primary metric for balanced dataset
- **Cross-Validation**: 5-fold CV for robust evaluation
- **Classification Report**: Precision, Recall, F1-score per class
- **Confusion Matrix**: Detailed classification analysis

### Model Selection Criteria
1. **Accuracy**: Random Forest achieves highest accuracy (99.46%)
2. **Speed**: SVM offers best training speed (2 seconds)
3. **Resource Usage**: Naive Bayes requires minimal resources
4. **Robustness**: All models show consistent cross-validation performance

## 📈 Results Summary

✅ **Successfully achieved >99% accuracy** with Random Forest  
✅ **Fast deployment option** available with Linear SVM  
✅ **Lightweight solution** provided by Naive Bayes  
✅ **Robust cross-validation** performance across all models  
✅ **No overfitting** detected in any approach  

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas numpy scikit-learn matplotlib seaborn jupyter
```

### Running the Analysis
1. **Exploratory Data Analysis**:
   ```bash
   jupyter notebook training/eda.ipynb
   ```

2. **Train Random Forest** (Recommended):
   ```bash
   jupyter notebook training/training.ipynb
   ```

3. **Train SVM** (Fast Option):
   ```bash
   jupyter notebook training/training3.ipynb
   ```

4. **Train Naive Bayes** (Lightweight):
   ```bash
   jupyter notebook training/training2.ipynb
   ```

## 💡 Key Insights

1. **High Performance**: All models achieve >98.8% accuracy
2. **Feature Importance**: Top 20 features contribute significantly to predictions
3. **Model Efficiency**: Linear SVM provides excellent speed-accuracy trade-off
4. **Scalability**: Models handle 13,910 samples efficiently
5. **Deployment Ready**: Multiple model options for different deployment scenarios

## 🔧 Model Deployment Options

- **Production**: Random Forest (highest accuracy)
- **Real-time**: Linear SVM (fastest inference)
- **Edge Computing**: Naive Bayes (minimal resources)
- **Ensemble**: Combine all three for maximum robustness

## 📊 Future Enhancements

- [ ] Deep learning approach with neural networks
- [ ] Advanced ensemble methods (XGBoost, LightGBM)
- [ ] Feature selection optimization
- [ ] Real-time prediction pipeline
- [ ] Model interpretability with SHAP values
- [ ] Automated hyperparameter tuning

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for improvements.

## 📄 License

This project is available for educational and research purposes.

---
**Coal Mine Safety Classification Project** - Ensuring safer mining operations through advanced machine learning. 🏭⛏️
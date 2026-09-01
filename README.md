# EduPro: Course Demand & Revenue Forecasting

A predictive analytics platform for online course planning, pricing, and instructor onboarding. This Streamlit-based application helps education platforms forecast course enrollment and revenue using machine learning models.

## Features

- **Prediction Dashboard**: Predict enrollment and revenue for new courses based on course attributes
- **Revenue Forecast Visualizations**: Analyze revenue trends by category, price, and other metrics
- **Feature Importance Explorer**: Understand which course features most impact enrollment and revenue
- **Category-Level Comparison**: Compare performance metrics across course categories

## Project Structure

```
edupro-analytics/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── data/
│   ├── course_data.xls            # Course data (CSV format)
│   ├── category_revenue.xls       # Revenue by category (CSV format)
│   └── EduPro Online Platform.xlsx # Original source data
├── models/
│   ├── model_enrollment.pkl       # Pre-trained enrollment prediction model
│   └── model_revenue.pkl          # Pre-trained revenue prediction model
└── notebooks/
    └── analysis.ipynb             # Data analysis and model training notebook
```

## Installation

### Prerequisites
- Python 3.14+
- pip or conda

### Setup

1. Clone the repository:
```bash
git clone https://github.com/anjana-2006/edupro-analytics.git
cd edupro-analytics
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Features Explained

#### 1. Prediction Dashboard
- Select course category, type, price, duration, and other attributes
- Get real-time predictions for:
  - **Enrollment Count**: Expected number of student enrollments
  - **Course Revenue**: Expected revenue from the course

#### 2. Revenue Forecast Visualizations
- View total revenue by course category
- Analyze relationship between course price and revenue
- Identify high-performing categories

#### 3. Feature Importance Explorer
- Understand which features drive enrollment predictions
- Identify key factors affecting revenue

#### 4. Category-Level Comparison
- Compare metrics across different course categories
- Filter and analyze category-specific trends

## Data

The application uses three primary data sources:

- **Courses**: Course metadata (name, category, type, price, duration, rating, level)
- **Teachers**: Instructor information (experience, rating, expertise)
- **Transactions**: Transaction/enrollment records (amount, timing, course-teacher pairs)

Aggregated metrics include:
- Course enrollment counts
- Revenue per course
- Teacher ratings and experience (averaged by course)
- Expertise match scores

## Models

### Model Enrollment (Random Forest)
- **Purpose**: Predicts the number of students who will enroll in a course
- **Input Features**: Course attributes, teacher metrics, category/type dummies, price bands
- **Note**: Low explanatory power (R² ≈ 0) - enrollment is influenced by factors not captured in these attributes

### Model Revenue (Random Forest)
- **Purpose**: Predicts log-transformed course revenue
- **Input Features**: Same as enrollment model
- **Key Drivers**: Course price and course type are the primary revenue predictors

## Requirements

Key dependencies:
- `streamlit>=1.28` - Web application framework
- `pandas>=2.1.0` - Data manipulation
- `numpy>=1.26.0` - Numerical computing
- `scikit-learn>=1.3.0` - Machine learning
- `matplotlib>=3.8.0` - Visualizations
- `joblib>=1.3.0` - Model serialization
- `openpyxl>=3.1.0` - Excel file support

## Development

### Regenerating Models

To retrain the models, run the Jupyter notebook:

```bash
jupyter notebook notebooks/analysis.ipynb
```

The notebook:
1. Loads and explores the source data
2. Engineers features and creates aggregations
3. Trains enrollment and revenue models
4. Saves trained models to `models/` directory

## Deployment

The application is configured for deployment on **Streamlit Cloud**:

1. Push changes to GitHub
2. Connect your repository to Streamlit Cloud
3. The app auto-deploys on each push to the `main` branch

## Notes

- Course enrollment predictions have limited explanatory power, suggesting that enrollment drivers exist beyond course/instructor attributes
- Revenue predictions are strongly influenced by course price and type
- The analysis uses cross-validation (5-fold) to evaluate model performance
- Price bands and duration buckets are engineered features used to improve model robustness

## License

MIT License

## Author

Anjana Reddy (anjana-2006)

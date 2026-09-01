import streamlit as st
import pandas as pd
import joblib

model_enrollment = joblib.load("models/model_enrollment.pkl")
model_revenue = joblib.load("models/model_revenue.pkl")
course_data = pd.read_excel("data/course_data.xls")
category_revenue = pd.read_excel("data/category_revenue.xls")

st.set_page_config(page_title="EduPro Demand & Revenue Forecasting", layout="wide")
st.title("EduPro: Course Demand & Revenue Forecasting")
st.caption("Predictive intelligence for course planning, pricing, and instructor onboarding.")

tab1, tab2, tab3, tab4 = st.tabs([
    "Prediction Dashboard",
    "Revenue Forecast Visualizations",
    "Feature Importance Explorer",
    "Category-Level Comparison"
])

with tab1:
    st.header("Predict Enrollment & Revenue for a New Course")
    st.write("Adjust the course details below to see predicted demand and revenue.")

    category = st.selectbox("Course Category", course_data['CourseCategory'].unique())
    course_type = st.selectbox("Course Type", course_data['CourseType'].unique())

    col1, col2 = st.columns(2)
    with col1:
        if course_type == 'Free':
            price = 0.0
            st.number_input("Course Price (₹)", value=0.0, disabled=True)
            st.caption("Price locked to ₹0 for Free courses.")
        else:
            price = st.number_input("Course Price (₹)", min_value=0.0, max_value=500.0, value=100.0)
        duration = st.number_input("Course Duration (hours)", min_value=1.0, max_value=60.0, value=20.0)
        level = st.selectbox("Course Level", course_data['CourseLevel'].unique())
    with col2:
        rating = st.slider("Expected Course Rating", 0.0, 5.0, 4.0)
        teacher_experience = st.slider("Instructor Years of Experience", 0, 30, 5)
        teacher_rating = st.slider("Instructor Rating", 0.0, 5.0, 4.0)

    if st.button("Predict", type="primary"):
        X_columns = model_enrollment.feature_names_in_
        row = pd.DataFrame(0, index=[0], columns=X_columns)

        if 'CoursePrice' in row.columns: row['CoursePrice'] = price
        if 'CourseDuration' in row.columns: row['CourseDuration'] = duration
        if 'CourseRating' in row.columns: row['CourseRating'] = rating
        if 'AvgTeacherExperience' in row.columns: row['AvgTeacherExperience'] = teacher_experience
        if 'AvgTeacherRating' in row.columns: row['AvgTeacherRating'] = teacher_rating

        if 'NumUniqueTeachers' in row.columns:
            row['NumUniqueTeachers'] = course_data['NumUniqueTeachers'].mean()
        if 'ExpertiseMatchScore' in row.columns:
            row['ExpertiseMatchScore'] = course_data['ExpertiseMatchScore'].mean()

        level_map = {'Beginner': 0, 'Intermediate': 1, 'Advanced': 2}
        if 'CourseLevelEncoded' in row.columns:
            row['CourseLevelEncoded'] = level_map.get(level, 0)

        def set_dummy(prefix, value):
            col_name = f"{prefix}_{value}"
            if col_name in row.columns:
                row[col_name] = 1

        set_dummy('CourseCategory', category)
        set_dummy('CourseType', course_type)

        def price_band(p):
            if p == 0: return 'Free'
            elif p <= 250: return 'Low'
            elif p <= 400: return 'Medium'
            else: return 'High'
        set_dummy('PriceBand', price_band(price))

        pred_enrollment = model_enrollment.predict(row)[0]
        pred_log_revenue = model_revenue.predict(row)[0]
        pred_revenue = (2.71828 ** pred_log_revenue) - 1

        st.subheader("Predictions")
        c1, c2 = st.columns(2)
        c1.metric("Predicted Enrollment Count", f"{pred_enrollment:.0f}")
        c2.metric("Predicted Course Revenue", f"₹{pred_revenue:,.2f}")

        st.caption(
            "Note: Enrollment predictions have low explanatory power (cross-validated R² ≈ 0), "
            "meaning enrollment is not well explained by course/instructor attributes alone. "
            "Revenue predictions are strongly driven by Course Price and Course Type."
        )

with tab2:
    st.header("Revenue Forecast Visualizations")

    st.subheader("Total Revenue by Category")
    rev_by_cat = course_data.groupby('CourseCategory')['CourseRevenue'].sum().sort_values()
    st.bar_chart(rev_by_cat)

    st.subheader("Course Price vs Course Revenue")
    st.scatter_chart(course_data, x='CoursePrice', y='CourseRevenue')

    st.subheader("Revenue Distribution Across Courses")
    st.bar_chart(course_data.sort_values('CourseRevenue', ascending=False).set_index('CourseName')['CourseRevenue'].head(15))

with tab3:
    st.header("Feature Importance Explorer")

    model_choice = st.radio("Select target to explore:", ["Enrollment Count", "Course Revenue"])

    if model_choice == "Enrollment Count":
        importances = pd.Series(
            model_enrollment.feature_importances_,
            index=model_enrollment.feature_names_in_
        ).sort_values(ascending=False).head(10)
    else:
        importances = pd.Series(
            model_revenue.feature_importances_,
            index=model_revenue.feature_names_in_
        ).sort_values(ascending=False).head(10)

    st.bar_chart(importances)
    st.caption(f"Top 10 features influencing {model_choice} predictions (Random Forest).")

with tab4:
    st.header("Category-Level Demand Comparison")

    st.subheader("Total Revenue by Category")
    st.dataframe(category_revenue.sort_values('CategoryRevenue', ascending=False), use_container_width=True)

    st.subheader("Average Enrollment by Category")
    avg_enrollment_by_cat = course_data.groupby('CourseCategory')['EnrollmentCount'].mean().sort_values(ascending=False)
    st.bar_chart(avg_enrollment_by_cat)

    st.subheader("Average Course Rating by Category")
    avg_rating_by_cat = course_data.groupby('CourseCategory')['CourseRating'].mean().sort_values(ascending=False)
    st.bar_chart(avg_rating_by_cat)
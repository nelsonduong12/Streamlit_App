import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

web_apps = st.sidebar.selectbox("Select Web Apps", ("Exploratory Data Analysis",))

df = None

if web_apps == "Exploratory Data Analysis":
    uploaded_file = st.sidebar.file_uploader("Choose a file")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        show_df = st.checkbox("Show Data Frame", key="disabled")

        if show_df:
            st.write(df)

        num_rows = df.shape[0]
        num_columns = df.shape[1]
        num_categorical = len(df.select_dtypes(include=['object']).columns)
        num_numerical = len(df.select_dtypes(include=['int64', 'float64']).columns)
        num_date = len(df.select_dtypes(include=['int64']).columns)

        # Data File Statistics

        st.subheader("Dataset Statistic")
        st.write("Number of rows:", num_rows)
        st.write("Number of columns:", num_columns)
        st.write("Number of categorical variables:", num_categorical)
        st.write("Number of numerical variables:", num_numerical)
        st.write("Number of date variables:", num_date)

        selected_column = st.sidebar.selectbox("Select a Column", df.columns)

        column_type = st.sidebar.selectbox('Select Data Type', ("Numerical", "Categorical", "Date"))

        if column_type == "Numerical":
            numerical_column = st.sidebar.selectbox('Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)

            # 5 number summary
            boxplot_title = st.text_input('Set Title', 'Box Plot')
            boxplot_ytitle = st.text_input('Set y-axis Title', numerical_column)
            boxplot_whisker_linestyle = st.selectbox('Set Whisker Line Style', ['-', '--', '-.', ':'])

            fig, ax = plt.subplots()
            sns.boxplot(data=df, x=numerical_column, y=numerical_column, color='#ff7f0e', flierprops={'marker': 'o', 'markerfacecolor': '#ff7f0e', 'markeredgecolor': '#ff7f0e'})
            ax.set_title(boxplot_title)
            ax.set_xlabel(numerical_column)
            ax.set_ylabel(boxplot_ytitle)


            # histogram

            hist_title = st.text_input('Set Title', 'Histogram')
            hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

            fig, ax = plt.subplots()
            ax.hist(df[numerical_column], bins=25, edgecolor="black", color="#69b3a2")
            ax.set_title(hist_title)
            ax.set_xlabel(hist_xtitle)
            ax.set_ylabel('Count')

            st.pyplot(fig)
            filename = "plot.png"
            fig.savefig(filename, dpi=300)

             # Display download button
            with open("plot.png", "rb") as file:
              btn = st.download_button(
                  label="Download image",
                  data=file,
                  file_name="flower.png",
                  mime="image/png"
              )
            
        elif column_type == "Categorical":
          categorical_column = st.sidebar.selectbox('Select a Column', df.select_dtypes(include=['object']).columns)


          category_count = df[categorical_column].value_counts()
          category_proportions = df[categorical_column].value_counts(normalize=True)

          bar_title = st.text_input('Set Title', 'Bar Plot')
          bar_xtitle = st.text_input('Set x-axis Title', categorical_column)

          st.write("Category Counts:")
          st.write(category_count)

          st.write("Category Proportions:")
          st.write(category_proportions)

          fig, ax = plt.subplots()
          sns.countplot(data=df, x=categorical_column, color = "#69b3a2")
          ax.set_title(f"Bar Plot: {categorical_column}")
          ax.set_xlabel(categorical_column)
          ax.set_ylabel("Count")

          st.pyplot(fig)
          filename = "barplot.png"
          fig.savefig(filename, dpi=300)

          # Display the download button
          with open("plot.png", "rb") as file:
            btn = st.download_button(
                label="Download image",
                data=file,
                file_name="flower.png",
                mime="image/png"
            )


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# st.toast("This application was developed by [Favour Taiwo] for educational purposes.")

# Streamlit application for levelling computation and visualization
st.markdown('<h1 style="text-align:center;"> Levelling Computation 📈 👷</h1>', unsafe_allow_html=True)
st.subheader("Data Analysis and Visualization")

with st.popover("User Guide"):
    st.write("### Instructions" \
    "\n" \
        "1. Upload a CSV file containing levelling data." \
            "\n" \
                "2. Select the appropriate columns for BackSight, InterSight, ForeSight, Instrument Height, and Reduced Level." \
                    "\n" \
                        "3. The application will compute the levelling data and display it in a table." \
                            "\n" \
                                "4. A graph of Reduced Level vs Observation Index will be generated for visualization."  )


csv_path= st.file_uploader("upload csv", type="csv")
if csv_path is not None:
    df= pd.read_csv(csv_path)
    cols = [None] + df.columns.tolist() 


def calculate_levels(df, backSight_str, interSight_str, foreSight_str, HI_str, RL_str):
    hi_list = []

    for index, row in df.iterrows():
        backsight = row.get(backSight_str)
        intSight = row.get(interSight_str)
        foresight = row.get(foreSight_str)

        if pd.notna(backsight):
            if pd.isna(foresight):
                heightIns = row.get(RL_str, 0) + backsight
                df.at[index, HI_str] = heightIns
                hi_list.append(heightIns)
            else:
                reducedLevel = hi_list[-1] - foresight
                df.at[index, RL_str] = reducedLevel

                heightIns = reducedLevel + backsight
                df.at[index, HI_str] = heightIns
                hi_list.append(heightIns)

        elif pd.notna(intSight):
            reducedLevel = hi_list[-1] - intSight
            df.at[index, RL_str] = reducedLevel

        else:
            reducedLevel = hi_list[-1] - foresight
            df.at[index, RL_str] = reducedLevel

    return df



st.header("Data Preview")
if csv_path is not None:
    st.dataframe(df.head(7))

    st.header("Column Selection")
    col1, col2, col3, col4, col5 = st.columns(5)
    backsight_col = col1.selectbox("BackSight Coln", cols)
    interSight_col = col2.selectbox("InterSight Coln", cols)
    foreSight_col = col3.selectbox("ForeSight Coln", cols)
    heightIns_col = col4.selectbox("InstrumentHeight Coln", cols)
    reducedLevel_col = col5.selectbox("ReducedLevel Coln", cols)

    if backsight_col and interSight_col and foreSight_col and heightIns_col and reducedLevel_col:
        st.header("Levelling Calculation")
        try:
            comp_df = calculate_levels(df, backsight_col, interSight_col, foreSight_col, heightIns_col, reducedLevel_col)
            st.dataframe(comp_df)
            
            st.download_button(label="Download Computed Data", data=comp_df.to_csv(index=False),
                               file_name="computed_levelling_data.csv", mime="text/csv")

            st.header("Data Visualization")
            st.subheader("Select Column for X-Axis")
            x_axis_col = st.selectbox("X-Axis Column", cols)
            fig, ax = plt.subplots()
            ax.plot(df[x_axis_col] if x_axis_col else df.index, df[reducedLevel_col], marker='o', label='Reduced Level')
            ax.set_xlabel(x_axis_col if x_axis_col else 'Observation Index')
            ax.set_ylabel('Reduced Level')
            ax.set_title('Reduced Level vs ' + (x_axis_col if x_axis_col else 'Observation Index'))
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    st.warning("Please upload a CSV file to proceed.")


# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("Made with ❤️ by [Favour Taiwo](https://github.com/favtai), with special thanks to developers of " \
"✨[Streamlit](https://streamlit.io/), [pandas](https://pandas.pydata.org/docs/) and [matplotlib](https://matplotlib.org/stable/api/pyplot_summary.html)✨")
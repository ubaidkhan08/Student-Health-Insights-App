import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import csv
import ast
from openai import OpenAI

# Access the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Function to fetch student data from CSV
def fetch_student_data(student_id):
    csv_file = "data.csv"  # Path to your CSV file
    data = pd.read_csv(csv_file)
    student_data = data[data['Student ID'].astype(str) == student_id]
    return student_data

def dicto(output_string):
    start_index = output_string.find("{'")
    end_index = output_string.rfind("'}") + 2
    dict_string = output_string[start_index:end_index]
    dict_string = dict_string.replace("\n", "").replace("Output: ", "")
    output2_dict = ast.literal_eval(dict_string)
    return output2_dict

# Function to display student data
def display_student_data(student_data):
    st.subheader("Student Details")
    st.write(student_data)

def beautify(data):
    df = pd.DataFrame(list(data.items()), columns=['Metric', 'Value'])

    st.title('Calculated Health Metrics')
    st.table(df)

    st.subheader('Categorical Metrics')
    categorical_data = df[df['Metric'].isin(['Fat Percentage', 'Viscral Fat Index', 'Weight Control', 'Obesity Rating'])]
    st.bar_chart(categorical_data.set_index('Metric'))    

# Function to generate insights
def generate_insights():
    prompt = "I want you to take the following inputs: 'Name', 'Student ID', 'Gender', 'Age', 'Height (cm)', 'Weight (kg)', 'Bone Mass (kg)', 'Fat Percentage (%)', 'Protein Amount (kg)', 'Moisture (%)'. And generate the below insights for this person (Use predictive analysis): BMI, BMR, Bone Mass, Fat Percentage, Viscral Fat Index, Muscle Mass, Protein Amount, Moisture, Weight Control, Obesity Rating. Return them in a python-dictionary format. Use the exact same words as I have used above as keys, and put YOUR output as their respective values. Sample output: Output: {'BMI': 26.1, 'BMR': 1859.5, 'Bone Mass': 3, 'Fat Percentage': '20%', 'Viscral Fat Index': 'Healthy', 'Muscle Mass': 52, 'Protein Amount': 10, 'Moisture': '60%', 'Weight Control': 'Healthy', 'Obesity Rating': 'Healthy'}. RETURN NOTHING ELSE BUT THE ABOVE OUTPUT! Real Input: Name = Aman Mishra, Student ID = 999, Gender = Male, Age = 16, Height (cm) = 170, Weight (kg) = 65, Bone Mass (kg) = 2.5, Fat Percentage (%) = 15, Protein Amount (kg) = 4.5, Moisture (%) = 35. RETURN NOTHING ELSE BUT INSIGHTS ON THE ABOVE OUTPUT!"
    
    client = OpenAI(api_key=openai_api_key)

    response = client.completions.create(
      model="gpt-3.5-turbo-instruct",
      prompt=prompt,
      temperature=1,
      max_tokens=1000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0)

    # Extracting insights from OpenAI response
    insights = dicto(response.choices[0].text)
    return insights


# Main function for Streamlit web app
def main():
    st.title("Student Health Insights")
    st.sidebar.title("Enter Student Information")

    # Sidebar inputs
    name = st.sidebar.text_input("Name of the Student:")
    student_id = st.sidebar.text_input("Student ID:")

    # Check if the student exists in the dataset
    if st.sidebar.button("Check Data and Give Insights"):
        student_data = fetch_student_data(student_id)
        if not student_data.empty:
            st.sidebar.success("Student found!")
            st.write(student_data)
            data = generate_insights()
            beautify(data)
   
        else:
            st.sidebar.error("Student not found. Please enter valid information.")

if __name__ == "__main__":
    main()

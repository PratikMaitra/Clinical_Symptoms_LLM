import openai
import pandas as pd
import os
import time

def query_gpt4o_severity(note, symptom, api_key, max_retries=3, timeout=60):
    """Queries OpenAI's GPT-4o model to rate the severity of a symptom."""
    if pd.isna(symptom) or symptom.strip() == "None":
        return "No Symptoms"

    prompt = f""" You are to roleplay as a physician or a nurse. You will be provided a clinical note or a medical transcription 
along with a list of symptom categories identified in the note. Your task would be to rate the severity of the 
symptom category in the clinical note. 

The clinical note is:
"{note}" 

The symptom category is: {symptom}

Only output the severity of the symptom category in the format Symptom:Rating with the rating as a number on 
a scale of 0 to 4, with 0 being no presence and 3 being most severe. Rating 4 is not assesable. If there are multiple symptoms like 
sym1, sym2, use the format sym1:rating1 , sym2:rating2."""

    client = openai.OpenAI(api_key=api_key)

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a highly experienced physician or nurse with expertise in symptom assessment and clinical severity ratings."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            time.sleep(2)  
    
    return "Error"

def process_severity(input_file, output_folder, output_file, api_key, batch_size=20):
    """Processes the notes file in batches, queries severity, and saves progress."""
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        alternative_files = [f for f in os.listdir() if f.endswith('.xlsx')]
        print("Available Excel files:", alternative_files)
        return

    df = pd.read_excel(input_file)

    if not {'Note', 'LLM_labels', 'MRN', 'GS_labels'}.issubset(df.columns):
        raise ValueError("Input file must contain 'Note', 'LLM_labels', 'MRN', and 'GS_labels' columns.")

    os.makedirs(output_folder, exist_ok=True)

    
    final_output_path = os.path.join(output_folder, output_file)
    processed_mrns = set()

    if os.path.exists(final_output_path):
        existing_df = pd.read_excel(final_output_path)
        processed_mrns = set(existing_df['MRN'])

    results = []
    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i+batch_size].copy()

        
        batch_df = batch_df[~batch_df['MRN'].isin(processed_mrns)]
        if batch_df.empty:
            continue

        batch_df['Severity'] = batch_df.apply(lambda row: query_gpt4o_severity(row['Note'], row['LLM_labels'], api_key), axis=1)

        batch_file = os.path.join(output_folder, f"batch_severity_{i//batch_size + 1}.xlsx")
        batch_df.to_excel(batch_file, index=False)
        results.append(batch_df)

        print(f"Saved batch {i//batch_size + 1} to {batch_file}")

    
    if results:
        final_df = pd.concat(results, ignore_index=True)
        final_df.to_excel(final_output_path, index=False)
        print(f"Final severity file saved as: {final_output_path}")

#### PLEASE MODIFY THIS SECTION BASED ON YOUR FILES ##############3


input_file = "YOUR INPUT FILE"
output_folder = "YOUR OUTPUT FOLDER"
output_file = "YOUR OUTPUT FILE"
api_key = os.environ.get("OPENAI_API_KEY", "YOUR API KEY")

process_severity(input_file, output_folder, output_file, api_key)

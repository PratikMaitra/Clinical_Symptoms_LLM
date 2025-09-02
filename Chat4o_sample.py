import openai
import pandas as pd
import os

def query_gpt4o(note, api_key):
    """Queries OpenAI's GPT-4o model to extract symptom categories."""
    prompt = f"""
    You are to roleplay as a physician or a nurse. You will be provided a clinical note or a medical transcription. Your task would be to detect the symptom categories in the clinical note. There are ten symptom categories and they are Anxiety/Anger, CNS, Cardiopulmonary symptoms, Depression, Fatigue, GI symptoms, Myelosupressed, Pain, Skin Changes, Sleep disturbance. The clinical note is:
    "{note}"
    Only output the relevant symptom categories you find in the clinical note as a single line with multiple symptom categories separated by commas.
    """
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are a highly experienced physician or nurse with expertise in clinical documentation and symptom assessment. Your role is to extract relevant symptom categories from medical notes."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def process_notes(input_file, output_folder, output_file, api_key, batch_size=20):
    """Processes the notes file in batches and queries GPT-4o for symptom detection."""
    df = pd.read_excel(input_file)
    
    
    if not {'Note', 'MRN', 'GS_labels'}.issubset(df.columns):
        raise ValueError("Input file must contain 'Note', 'MRN', and 'GS_labels' columns.")
    
    
    os.makedirs(output_folder, exist_ok=True)
    
    
    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i+batch_size].copy()
        batch_df['LLM_labels'] = batch_df['Note'].apply(lambda note: query_gpt4o(note, api_key))
        batch_file = os.path.join(output_folder, f"batch_{i//batch_size + 1}.xlsx")
        batch_df.to_excel(batch_file, index=False)
        print(f"Saved batch {i//batch_size + 1} to {batch_file}")
    
    
    df['LLM_labels'] = df['Note'].apply(lambda note: query_gpt4o(note, api_key))
    final_output_path = os.path.join(output_folder, output_file)
    df.to_excel(final_output_path, index=False)
    print(f"Final processed file saved as: {final_output_path}")


############### PLEASE CHANGE THIS SECTION BASED ON YOUR FILES ###################


input_file = "YOUR INPUT FILE"
output_folder = "YOUR OUTPUT FOLDER"
output_file = "YOUR OUTPUT FILE"
api_key = os.environ.get("OPENAI_API_KEY", "YOUR OPEN ROUTER OR ANOTHER API KEY")

process_notes(input_file, output_folder, output_file, api_key)

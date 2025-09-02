# Clinical_Symptoms_LLM

GitHub repository for LLM-based symptom severity annotation of clinical notes.

---

## Experiment and Models

We tested the performance of **four LLM models**:  
- **Llama-3.1-405B Instruct**  
- **GPT-4o**  
- **Claude 3.5 Sonnet**  
- **DeepSeek-R1 Chat**

The evaluation was conducted on **30 clinical notes**.  
Each model was evaluated on:  
- its ability to **detect symptoms**, and  
- its ability to **determine the severity of symptoms**.

We ran two experimental settings:  
1. **Symptom detection**  
2. **Symptom severity detection**

The 30 clinical notes had been annotated by a human expert for both **symptom presence** and **symptom severity**.  
Symptom-level categories (0–4) were defined based on prior literature in symptom detection.

Among the tested models, the **Llama 3.1-405B Instruct** model was assessed to have the best performance.  
We subsequently applied this model to **240 clinical notes** for large-scale evaluation.

The experiments with multiple models were conducted around **Feb–March**.

---

## Prompts Used

### Symptom Detection

```text
You are to roleplay as a physician or a nurse. You will be provided a clinical note or a medical transcription. 
Your task would be to detect the symptom categories in the clinical note. 

There are ten symptom categories and they are Anxiety/Anger, CNS, Cardiopulmonary symptoms, Depression, Fatigue, 
GI symptoms, Myelosupressed, Pain, Skin Changes, Sleep disturbance. 

The clinical note is:
"{note}"

Only output the relevant symptom categories you find in the clinical note as a single line with multiple 
symptom categories separated by commas.
```

### Symptom Severity Categorization

```text
You are to roleplay as a physician or a nurse. You will be provided a clinical note or a medical transcription 
along with a list of symptom categories identified in the note. Your task would be to rate the severity of the 
symptom category in the clinical note. 

The clinical note is:
"{note}" 

The symptom category is: {symptom}

Only output the severity of the symptom category in the format Symptom:Rating with the rating as a number on 
a scale of 0 to 4, with 0 absent, 1 being mild, 2 being moderate and 3 being most severe. Rating 4 is not assesable. If there are multiple symptoms like 
sym1, sym2, use the format sym1:rating1 , sym2:rating2.
```

---

## Repository Contents

- **Sample scripts** for running the experiments (requires input file and API key)  
- **Evaluation files** are provided under the `evaluation/` sub-folder  

---

## Citation

*Leveraging Generative Artificial Intelligence for Symptom Recognition: Extracting Symptom Presence and Severity in Patients with Acute Myeloid Leukemia Using Large Language Models*

- Sena Chae, PhD, RN<sup>1</sup>  
- Pratik Maitra, MS<sup>2</sup>  
- Alaa Albashayreh, PhD, RN<sup>1</sup>  

<sup>1</sup> University of Iowa, College of Nursing, Iowa City, IA, USA  
<sup>2</sup> Iowa State University, Department of Computer Science, Ames, IA, USA  



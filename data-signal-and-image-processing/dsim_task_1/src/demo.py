import pandas as pd
import gradio as gr
import os
import joblib
import preprocessing as pp
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = os.getenv("BASE_DIR")
MODEL_PATH = os.path.join(BASE_DIR, os.getenv("MODEL_FILE"))
DATA_DIR = os.path.join(BASE_DIR, os.getenv("DATA_FOLDER"))
CLASS_PATH = os.path.join(BASE_DIR, os.getenv("CLASS_FILE"))
SCALER_PATH = os.path.join(BASE_DIR, os.getenv("SCALER_FILE"))

            
def predict(file):
    try:
        model = pp.load_mod(MODEL_PATH)
        df = pd.read_csv(file.name, sep=";", header=None)
        
        file_name = os.path.basename(file.name)
        
        scaler = joblib.load(SCALER_PATH)
        descriptor = pp.extract_descriptor(df, scaler)
        prediction = model.predict(descriptor)[0]
        prediction_label = pp.dict_pred(prediction)
        
        plot = pp.plot_eeg(file)

        
        file_number = int(''.join(filter(str.isdigit, file_name)))
        classes_df = pd.read_csv(CLASS_PATH)
        true_label = classes_df.iloc[file_number - 1,0]#['class']
        
        return f"Predicted class: **{prediction_label}**  \nGround truth: **{true_label}**", plot

    except Exception as e:
        return f"Error during computation: {str(e)}"


    

def run_gradio():
    with gr.Blocks() as demo:
        gr.Markdown("# EEG classification")
        gr.Markdown("Upload a CSV file containing an EEG tracing in order to obtain the class prediction")
        
        with gr.Row():
            with gr.Column(scale=1):
                input_file = gr.File(label="Select a CSV file")
                prediction_output = gr.Markdown(label="Result of prediction")
            
            with gr.Column(scale=3):
                plot_output = gr.Plot(label="EEG Signal")
        
        input_file.change(
            fn=predict,
            inputs=input_file,
            outputs=[prediction_output, plot_output]
        )
    
    demo.launch()

if __name__ == "__main__":
    run_gradio()


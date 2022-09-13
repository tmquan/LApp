import os 
import lightning as L
import gradio as gr
import pandas as pd

from lightning_app.utilities.state import AppState
from lightning.app.components.serve import ServeGradio
from lightning.app.frontend import StreamlitFrontend
# from streamlit_option_menu import option_menu

def _streamlit_home(state: AppState):
    import streamlit as st
    _style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(_style, unsafe_allow_html=True)
    st.write("Not Implemented")

class LitStreamlitHome(L.LightningFlow):
    def configure_layout(self):
        return StreamlitFrontend(render_fn=_streamlit_home)

class QuestionAnsweringServeGradio(ServeGradio):
    # Example
    questions = []
    json_file = "questions.json"
    questions_list = pd.read_json(json_file)

    inputs = []
    inputs.append(gr.inputs.Textbox(lines=10, label=f"Context", placeholder="Type a sentence or paragraph here."))
    for k in range(len(questions_list)):
        inputs.append(gr.inputs.Textbox(lines=2, label=f"Question {k+1}", placeholder="Ask a question based on the context."))
    
    outputs = []
    for k in range(len(questions_list)):
        outputs.append(gr.outputs.Textbox(label=f"Answer {k+1}"))
        outputs.append(gr.outputs.Label(label=f"Score"))
    
    examples = []
    context = ["Harry James Potter (DOB: 31 July, 1980) was a half-blood wizard, and one of the most famous wizards of modern times. He was the only child and son of James and Lily Potter, both members of the original Order of the Phoenix. Harry's birth was overshadowed by a prophecy, naming either himself or Neville Longbottom as the one with the power to vanquish Lord Voldemort. After half of the prophecy was reported to Voldemort, courtesy of Severus Snape, Harry was chosen as the target due to his many similarities with the Dark Lord. This caused the Potter family to go into hiding. Voldemort made his first vain attempt to circumvent the prophecy when Harry was a year and three months old. During this attempt he murdered Harry's parents as they tried to protect him, but this unsuccessful attempt to kill Harry led to Voldemort's first downfall. This downfall marked the end of the First Wizarding War, and to Harry henceforth being known as the \"Boy Who Lived\"."]
    for item in questions_list['qas']:
        context.append(item["question"])
    examples = list([context])
    # examples = [
    #     [
    #         "Harry James Potter (DOB: 31 July, 1980) was a half-blood wizard, and one of the most famous wizards of modern times. He was the only child and son of James and Lily Potter, both members of the original Order of the Phoenix. Harry's birth was overshadowed by a prophecy, naming either himself or Neville Longbottom as the one with the power to vanquish Lord Voldemort. After half of the prophecy was reported to Voldemort, courtesy of Severus Snape, Harry was chosen as the target due to his many similarities with the Dark Lord. This caused the Potter family to go into hiding. Voldemort made his first vain attempt to circumvent the prophecy when Harry was a year and three months old. During this attempt he murdered Harry's parents as they tried to protect him, but this unsuccessful attempt to kill Harry led to Voldemort's first downfall. This downfall marked the end of the First Wizarding War, and to Harry henceforth being known as the \"Boy Who Lived\".", 
    #         "Patient First Name", 
    #         "Patient Last Name", 
    #         "Date of Birth", 
    #         "Sex", 
    #         "Smoking History", 
    #         "Diabetes", 
    #         "Is the patient receiving dialysis?", 
    #         "Patient Weight", 
    #         "Patient Height", 
    #         "Is the patient previously or currently using oral steroids for any reason?", 
    #         "Is the patient currently taking opioid medication to control his/her pain?", 
    #         "Baseline Numeric Rating Scale", 
    #     ],
    # ]

    def __init__(self, cloud_compute, *args, **kwargs):
        super().__init__(*args, cloud_compute=cloud_compute, **kwargs)
        self.ready = False  # required

    def build_model(self):
        pass

    def predict(self, context, question):
        print(question)
        return context

class ImageSegmentationServeGradio(ServeGradio):
    inputs = gr.inputs.Image(type="pil", label="Image")  # required
    outputs = gr.outputs.Image(type="pil")  # required
    examples = [os.path.join(str("./images"), f) for f in os.listdir("./images")]

    def __init__(self, cloud_compute, *args, **kwargs):
        super().__init__(*args, cloud_compute=cloud_compute, **kwargs)
        self.ready = False  # required

    def predict(self, img):
        return img

    def build_model(self):
        pass

class LitRootFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.home = LitStreamlitHome()
        self.qas = QuestionAnsweringServeGradio(L.CloudCompute("cpu"), parallel=True)
        self.ims = ImageSegmentationServeGradio(L.CloudCompute("cpu"), parallel=True)

    def configure_layout(self):
        tabs = []
        tabs.append({"name": "Home", "content": self.home})
        tabs.append({"name": "Question Answering", "content": self.qas})
        tabs.append({"name": "Image Segmentation", "content": self.ims})
        return tabs

    def run(self):
        self.home.run()
        self.ims.run()
        self.qas.run()
    
app = L.LightningApp(LitRootFlow())
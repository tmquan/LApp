import lightning as L
import streamlit as st
from lightning.app.frontend import StreamlitFrontend


def _streamlit_app(lightning_app_state):
    st.write("Not Implemented")
    # style = """
    #     <style>
    #     # MainMenu {visibility: hidden;}
    #     footer {visibility: hidden;}
    #     .stApp { bottom: 105px; }
    #     img.MuiBox-root {
    #         display: none;
    #     }
    #     </style>
    # """
    # st.markdown(style, unsafe_allow_html=True)

class LitStreamlit(L.LightningFlow):
    def configure_layout(self):
        return StreamlitFrontend(render_fn=_streamlit_app)

class LitMultiTabFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.lit_streamlit = LitStreamlit()

    def configure_layout(self):
        tabs = []
        tabs.append({"name": "Home", "content": self.lit_streamlit})
        tabs.append({"name": "Documentation", "content": self.lit_streamlit})
        tabs.append({"name": "Orchestration", "content": self.lit_streamlit})
        tabs.append({"name": "Demonstration", "content": self.lit_streamlit})
        tabs.append({"name": "Visualization", "content": self.lit_streamlit})
        return tabs

    def run(self):
        pass
    
app = L.LightningApp(LitMultiTabFlow())
import lightning as L
import streamlit as st
from lightning.app.frontend import StreamlitFrontend
from streamlit_option_menu import option_menu

def _streamlit_home(lightning_app_state):
    st.write("Not Implemented")

class LitStreamlitHome(L.LightningFlow):
    def configure_layout(self):
        return StreamlitFrontend(render_fn=_streamlit_home)

def _streamlit_demo(lightning_app_state):
    _style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(_style, unsafe_allow_html=True)
    # TODO
    with st.sidebar:
        page = option_menu(menu_title="Menu",
                            menu_icon="house-door",
                            options=[
                                "General Information",
                                "Semantic Segmentation",
                                "Proposal Segmentation",
                            ],
                            icons=[
                                None, 
                                None, 
                                None
                            ],
                            default_index=0
                        )
        
class LitStreamlitDemo(L.LightningFlow):
    def configure_layout(self):
        return StreamlitFrontend(render_fn=_streamlit_demo)

class LitRootFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.home = LitStreamlitHome()
        self.demo = LitStreamlitDemo()

    def configure_layout(self):
        tabs = []
        tabs.append({"name": "Home", "content": self.home})
        # tabs.append({"name": "Documentation", "content": self.lit_streamlit})
        # tabs.append({"name": "Orchestration", "content": self.lit_streamlit})
        tabs.append({"name": "Demonstration", "content": self.demo})
        # tabs.append({"name": "Uncategorized", "content": self.lit_streamlit})
        # tabs.append({"name": "Visualization", "content": self.lit_streamlit})
        return tabs

    def run(self):
        pass
    
app = L.LightningApp(LitRootFlow())
import os 
import lightning as L
import gradio as gr

from lightning.app.frontend import StreamlitFrontend
from lightning_app.utilities.state import AppState
from streamlit_option_menu import option_menu
from lightning.app.components.serve import ServeGradio

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

class Image2ImageServeGradio(ServeGradio):
    inputs = gr.inputs.Image(type="pil", label="Select an input image")  # required
    outputs = gr.outputs.Image(type="pil")  # required
    # examples = ["./images/comic_lr.png"]  # required
    examples = [os.path.join(str("./images"), f) for f in os.listdir("./images")]

    def __init__(self, cloud_compute, *args, **kwargs):
        super().__init__(*args, cloud_compute=cloud_compute, **kwargs)
        self.ready = False  # required

    def predict(self, img):
        return img
        # DEVICE = torch.device("cpu")

        # # resize image
        # height, width = img.size
        # print("Original size:", height, width)
        # max_size = max(height, width)
        # if max_size > 100:
        #     ratio = 100 / max_size
        #     new_size = (round(ratio * height), round(ratio * width))
        #     img = img.resize(new_size)

        # new_height, new_width = img.size
        # print("Resized size:", new_height, new_width)

        # # convert image to tensor
        # opencv_image = np.array(img)
        # opencv_image = opencv_image[:, :, ::-1].copy()
        # lr_image = opencv_image.astype(np.float32) / 255.0
        # lr_image = cv2.cvtColor(lr_image, cv2.COLOR_BGR2RGB)
        # lr_tensor = imgproc.image2tensor(lr_image, False, False).unsqueeze_(0)
        # lr_tensor = lr_tensor.to(device=DEVICE)

        # # get upscaled image
        # with torch.no_grad():
        #     sr_tensor = self.model(lr_tensor)
        # transform = T.ToPILImage()

        # # Remove batch dimension
        # sr_tensor.squeeze_(0)
        # return transform(sr_tensor)

    def build_model(self):
        pass
        # WEIGHTS_PATH = "./weights/SRGAN_x4-ImageNet-c71a4860.pth.tar"
        # DEVICE = torch.device("cpu")

        # # Initialize the model
        # model = Generator()
        # model = model.to(memory_format=torch.channels_last, device=DEVICE)
        # print("Build SRGAN model successfully.")

        # # Load the SRGAN model weights
        # checkpoint = torch.load(WEIGHTS_PATH)
        # model.load_state_dict(checkpoint["state_dict"])
        # print(f"Load SRGAN model weights `{WEIGHTS_PATH}` successfully.")
        # model.eval()

        # return model

class LitRootFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.home = LitStreamlitHome()
        # self.demo = LitStreamlitDemo()
        # self.demo = ImageServeGradio(L.CloudCompute("cpu"))
        self.xray = Image2ImageServeGradio(L.CloudCompute("cpu"))

    def configure_layout(self):
        tabs = []
        tabs.append({"name": "Home", "content": self.home})
        tabs.append({"name": "XRay", "content": self.xray})
        return tabs

    def run(self):
        self.home.run()
        self.xray.run()
    
app = L.LightningApp(LitRootFlow())
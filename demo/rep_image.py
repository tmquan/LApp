import warnings
warnings.simplefilter("ignore")
import logging
import os

from functools import partial
from subprocess import Popen
from lightning.app.storage import Path
from lightning.app.components.serve import ServeGradio
import gradio as gr

import torch
import torchvision.transforms as T

logger = logging.getLogger(__name__)

class ImageServeGradio(ServeGradio):
    inputs = gr.inputs.Image(type="pil", shape=(28, 28))
    outputs = gr.outputs.Label(num_top_classes=10)

    def __init__(self, cloud_compute, *args, **kwargs):
        super().__init__(*args, cloud_compute=cloud_compute, **kwargs)
        self.examples = None
        self.best_model_path = None
        self._transform = None
        self._labels = {idx: str(idx) for idx in range(10)}

    def run(self):
        ######### [DEMO PURPOSE] #########
        # Download some examples so it works locally and in the cloud (issue with gradio on loading the images.)
        # download_data("https://pl-flash-data.s3.amazonaws.com/assets_lightning/images.tar.gz", "./")
        self.examples = [os.path.join(str("./images"), f) for f in os.listdir("./images")]
        ######### [DEMO PURPOSE] #########

        self._transform = T.Compose([T.Resize((28, 28)), T.ToTensor()])
        super().run()

    def predict(self, img):
        # 1. Receive an image and transform it into a tensor
        img = self._transform(img)[0]
        img = img.unsqueeze(0).unsqueeze(0)

        # # 2. Apply the model on the image and convert the logits into probabilities
        # prediction = torch.exp(self.model(img))

        # # 3. Return the data in the `gr.outputs.Label` format
        # return {self._labels[i]: prediction[0][i].item() for i in range(10)}
        return img 

    def build_model(self):
        pass
        # # 1. Load the best model. As torchscripted by the first component, using torch.load works out of the box.
        # model = torch.load(self.best_model_path)

        # # 2. Prepare the model for predictions.
        # for p in model.parameters():
        #     p.requires_grad = False
        # model.eval()

        # # 3. Return the model.
        # return model


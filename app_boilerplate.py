import lightning as L

class LitApp(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        pass

app = L.LightningApp(LitApp())
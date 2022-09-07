import lightning as L

class LitRootFlow(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        pass
    
app = L.LightningApp(LitRootFlow())
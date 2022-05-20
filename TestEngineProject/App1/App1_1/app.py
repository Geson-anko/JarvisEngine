from JarvisEngine.apps import BaseApp

class App1_1(BaseApp):
    
    def Init(self) -> None:
        super().Init()
        self.logger.info("Init1_1")        
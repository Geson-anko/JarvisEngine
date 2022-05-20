from JarvisEngine.apps import BaseApp

class App1(BaseApp):
    
    def Init(self) -> None:
        self.logger.info("Init1")
        return super().Init()
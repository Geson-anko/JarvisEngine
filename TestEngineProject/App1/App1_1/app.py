from JarvisEngine.apps import BaseApp

class App1_1(BaseApp):
    
    def Init(self) -> None:
        super().Init()
        self.logger.info("Init1_1")        

    def RegisterProcessSharedValues(self, sync_manager) -> None:
        super().RegisterProcessSharedValues(sync_manager)
        self.addProcessSharedValue("str_value", "apple")
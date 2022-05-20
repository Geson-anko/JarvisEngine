from JarvisEngine.apps import BaseApp

class App1_2(BaseApp):
    
    def Init(self):
        self.logger.info("Init1_2")

    def RegisterProcessSharedValues(self, sync_manager) -> None:
        super().RegisterProcessSharedValues(sync_manager)
        self.addProcessSharedValue("float_value",0.0)

    def RegisterThreadSharedValues(self) -> None:
        super().RegisterThreadSharedValues()
        self.addThreadSharedValue("list_obj", [1,2,3])
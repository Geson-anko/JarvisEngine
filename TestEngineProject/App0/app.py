from JarvisEngine.apps import BaseApp

class App0(BaseApp):
    
    def Init(self) -> None:
        self.logger.info("Init0")

    def RegisterProcessSharedValues(self, sync_manager) -> None:
        super().RegisterProcessSharedValues(sync_manager)
        self.addProcessSharedValue("bool_value",True)

    def RegisterThreadSharedValues(self) -> None:
        super().RegisterThreadSharedValues()
        self.addThreadSharedValue("set_obj", {"number"})

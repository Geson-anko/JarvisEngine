from JarvisEngine.apps import BaseApp

class App1(BaseApp):
    
    def Init(self) -> None:
        self.logger.info("Init1")
        return super().Init()

    def RegisterProcessSharedValues(self, sync_manager) -> None:
        super().RegisterProcessSharedValues(sync_manager)

        self.addProcessSharedValue("int_value",100)

    def RegisterThreadSharedValues(self) -> None:
        super().RegisterThreadSharedValues()
        self.addThreadSharedValue("range_obj",range(10))
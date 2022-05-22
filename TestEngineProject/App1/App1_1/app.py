from JarvisEngine.apps import BaseApp

class App1_1(BaseApp):
    
    def Init(self) -> None:
        super().Init()
        self.logger.info("Init1_1")        

    def RegisterProcessSharedValues(self, sync_manager) -> None:
        super().RegisterProcessSharedValues(sync_manager)
        self.addProcessSharedValue("str_value", "apple")

    def RegisterThreadSharedValues(self) -> None:
        super().RegisterThreadSharedValues()
        self.addThreadSharedValue("tuple_obj",(True,False))

    def Awake(self) -> None:
        self.logger.info("Awake")
        assert self.process_shared_values == None
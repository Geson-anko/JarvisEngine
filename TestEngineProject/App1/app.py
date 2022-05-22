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

    def Awake(self) -> None:
        self.logger.info("Awake")
        assert self.process_shared_values == None

    def Start(self) -> None:
        self.logger.info("Start")
        assert self.getProcessSharedValue("MAIN.App0.bool_value") == True
        assert self.getProcessSharedValue("MAIN.App1.int_value") == 100
        assert self.getProcessSharedValue("MAIN.App1.App1_1.str_value") == "apple"
        assert self.getProcessSharedValue("MAIN.App1.App1_2.float_value") == 0.0
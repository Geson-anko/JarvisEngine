from JarvisEngine.apps import BaseApp
import multiprocessing as mp
class App0(BaseApp):
    
    def Init(self) -> None:
        self.logger.info("Init0")

    def RegisterProcessSharedValues(self, sync_manager) -> None:
        super().RegisterProcessSharedValues(sync_manager)
        self.addProcessSharedValue("bool_value",True)
        self.addProcessSharedValue("shared_int",mp.Value("i",0))

    def RegisterThreadSharedValues(self) -> None:
        super().RegisterThreadSharedValues()
        self.addThreadSharedValue("set_obj", {"number"})

    def Awake(self) -> None:
        self.logger.info("Awake")
        assert self.process_shared_values == None

    def Start(self) -> None:
        self.logger.info("Start")
        assert self.getProcessSharedValue("MAIN.App0.bool_value") == True
        assert self.getProcessSharedValue("MAIN.App1.int_value") == 100
        assert self.getProcessSharedValue("MAIN.App1.App1_1.str_value") == "apple"
        assert self.getProcessSharedValue("MAIN.App1.App1_2.float_value") == 0.0

        assert self.getProcessSharedValue("MAIN.App0.shared_int").value == 0
        assert self.getProcessSharedValue("MAIN.App1.shared_float").value == -10.0
        assert self.getProcessSharedValue("MAIN.App1.App1_1.shared_bool").value == True
        assert self.getProcessSharedValue("MAIN.App1.App1_2.shared_str").value == b"abc"
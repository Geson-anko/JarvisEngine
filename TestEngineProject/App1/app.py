from JarvisEngine.apps import BaseApp
import multiprocessing as mp

class App1(BaseApp):
    
    def Init(self) -> None:
        self.logger.info("Init1")
        return super().Init()

    def RegisterProcessSharedValues(self, sync_manager) -> None:
        super().RegisterProcessSharedValues(sync_manager)

        self.addProcessSharedValue("int_value",100)
        self.addProcessSharedValue("shared_float",mp.Value("f",-10.0))

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
        
        assert self.getProcessSharedValue("MAIN.App0.shared_int").value == 0
        assert self.getProcessSharedValue("MAIN.App1.shared_float").value == -10.0
        assert self.getProcessSharedValue("MAIN.App1.App1_1.shared_bool").value == True
        assert self.getProcessSharedValue("MAIN.App1.App1_2.shared_str").value == b"abc"

        assert self.getThreadSharedValue("MAIN.App0.set_obj") is None
        assert self.getThreadSharedValue("MAIN.App1.range_obj") == range(10)
        assert self.getThreadSharedValue("MAIN.App1.App1_1.tuple_obj") == (True, False)
        assert self.getThreadSharedValue("MAIN.App1.App1_2.list_obj") is None
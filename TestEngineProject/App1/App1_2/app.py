from JarvisEngine.apps import BaseApp
import multiprocessing as mp
import ctypes

class App1_2(BaseApp):
    
    def Init(self):
        self.logger.info("Init1_2")

    def RegisterProcessSharedValues(self, sync_manager) -> None:
        super().RegisterProcessSharedValues(sync_manager)
        self.addProcessSharedValue("float_value",0.0)
        self.addProcessSharedValue("shared_str", mp.Array(ctypes.c_char, b"abc"))

    def RegisterThreadSharedValues(self) -> None:
        super().RegisterThreadSharedValues()
        self.addThreadSharedValue("list_obj", [1,2,3])

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
        assert self.getThreadSharedValue("MAIN.App1.range_obj") is None
        assert self.getThreadSharedValue("MAIN.App1.App1_1.tuple_obj") is None
        assert self.getThreadSharedValue("MAIN.App1.App1_2.list_obj") == [1,2,3]
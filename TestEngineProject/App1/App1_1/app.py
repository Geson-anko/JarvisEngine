import ctypes
import multiprocessing as mp

from JarvisEngine.apps import BaseApp


class App1_1(BaseApp):
    def Init(self) -> None:
        super().Init()
        self.logger.info("Init1_1")

    def RegisterProcessSharedValues(self, sync_manager) -> None:
        super().RegisterProcessSharedValues(sync_manager)
        self.addProcessSharedValue("str_value", "apple")
        self.addProcessSharedValue("shared_bool", mp.Value(ctypes.c_bool, True))

    def RegisterThreadSharedValues(self) -> None:
        super().RegisterThreadSharedValues()
        self.addThreadSharedValue("tuple_obj", (True, False))

    def Awake(self) -> None:
        self.logger.info("Awake")
        assert self.process_shared_values is None

    def Start(self) -> None:
        self.logger.info("Start")
        assert self.getProcessSharedValue("Launcher.App0.bool_value") is True
        assert self.getProcessSharedValue("Launcher.App1.int_value") == 100
        assert self.getProcessSharedValue("Launcher.App1.App1_1.str_value") == "apple"
        assert self.getProcessSharedValue("Launcher.App1.App1_2.float_value") == 0.0

        assert self.getProcessSharedValue("Launcher.App0.shared_int").value == 0
        assert self.getProcessSharedValue("Launcher.App1.shared_float").value == -10.0
        assert self.getProcessSharedValue("Launcher.App1.App1_1.shared_bool").value is True
        assert self.getProcessSharedValue("Launcher.App1.App1_2.shared_str").value == b"abc"

        assert self.getThreadSharedValue("Launcher.App0.set_obj") is None
        assert self.getThreadSharedValue("Launcher.App1.range_obj") == range(10)
        assert self.getThreadSharedValue("Launcher.App1.App1_1.tuple_obj") == (True, False)
        assert self.getThreadSharedValue("Launcher.App1.App1_2.list_obj") is None

    frame_rate = 10

    def Update(self, delta_time: float) -> None:
        self.logger.info("Update")

    def End(self) -> None:
        self.logger.info("End")

    def Terminate(self) -> None:
        self.logger.info("Terminate.")

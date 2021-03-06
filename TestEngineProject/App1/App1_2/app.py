import ctypes
import multiprocessing as mp

from JarvisEngine.apps import BaseApp


class App1_2(BaseApp):
    def Init(self):
        self.logger.info("Init1_2")

    def RegisterProcessSharedValues(self, sync_manager) -> None:
        super().RegisterProcessSharedValues(sync_manager)
        self.addProcessSharedValue("float_value", 0.0)
        self.addProcessSharedValue("shared_str", mp.Array(ctypes.c_char, b"abc"))

    def RegisterThreadSharedValues(self) -> None:
        super().RegisterThreadSharedValues()
        self.addThreadSharedValue("list_obj", [1, 2, 3])

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
        assert self.getThreadSharedValue("Launcher.App1.range_obj") is None
        assert self.getThreadSharedValue("Launcher.App1.App1_1.tuple_obj") is None
        assert self.getThreadSharedValue("Launcher.App1.App1_2.list_obj") == [1, 2, 3]

    frame_rate = -1.0
    log_num = 5
    logged_num = 0

    def Update(self, delta_time: float) -> None:
        if self.logged_num < self.log_num:
            self.logger.info("Update")
            self.logged_num += 1
        return super().Update(delta_time)

    def End(self) -> None:
        self.logger.info("End")

    def Terminate(self) -> None:
        self.logger.info("Terminate.")

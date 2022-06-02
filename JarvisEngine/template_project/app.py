from JarvisEngine.apps import BaseApp

class App(BaseApp):

    def Start(self):
        self.logger.info("Started!")

    frame_rate = 10.0
    def Update(self, delta_time: float) -> None:
        self.logger.info(f"Updating in {delta_time:.2f} secs.")

from threading import Thread


class BackgroundWorker:

    @staticmethod
    def run(
        target,
        *args
    ):

        thread = Thread(
            target=target,
            args=args
        )

        thread.daemon = True

        thread.start()

        return thread